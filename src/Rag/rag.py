import os
import string

import dill
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.Rag.rag_config import RagConfig

from dotenv import load_dotenv
import os

import google.generativeai as genai

example = [
    "{"
    "query: \"Given this context:Name:Muchiol,  Id: 13, Description: Cures osteoporosis. Side effects: dizziness, dry mouth. "
    "Name:Propol,  Id: 4, Description: Cures flu. Side effects: muscle pain, fever. "
    "Name:Kisuel,  Id: 12, Description: Cures arthritis. Side effects: muscle pain, fever. "
    "Name:Pepsiclox,  Id: 16, Description: Cures fever. Side effects: muscle pain, fever. "
    "Name:Glucose,  Id: 2, Description: Cures fever. Side effects: fatigue, dry mouth. "
    "Name:June,  Id: 8, Description: Cures asthma. Side effects: muscle pain, fever."
    "Name:Urinol,  Id: 15, Description: Cures diabetes. Side effects: drowsiness, dry eyes."
    "Name:Licuogex,  Id: 5, Description: Cures cough. Side effects: dizziness, dry mouth."
    "These are the input symptoms: osteoporosis and cough , diabetes and osteoporosis , fever , diabetes and fever\""
    "answer: \"Muchiol and Licuogex, Urinol and Muchiol, Pepsiclox, Urniol and Pepsiclox\"",
    "}"
]


class RAG:
    def __init__(self, data: pd.DataFrame = None, config: RagConfig = None):

        self.config = config

        genai.configure(api_key=config.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-pro')

        if not config:
            config = RagConfig(use_persistence=False, use_llm=False)

        if config.use_persistence:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.collection = self.client['RAG']['medications']

        # Embedding model
        if os.path.exists('embedding_model.pkl'):
            with open('embedding_model.pkl', 'rb') as f:
                self.embedding_model = dill.load(f)
        else:
            self.embedding_model = SentenceTransformer("thenlper/gte-small")
            with open('embedding_model.pkl', 'wb') as f:
                dill.dump(self.embedding_model, f)

        # Data loading
        if data is None:
            if config.use_persistence:
                self.data = pd.DataFrame(list(self.collection.find()))
                self.data.drop(columns='_id', inplace=True)
            else:
                raise ValueError("Data cannot be None if use_persistence is False: data must be provided.")
        else:
            data = self._attach_embedding(data)

            if config.use_persistence:
                self._reset_domain(data)

            self.data = data

    def query_medications_for_patients(self, symptoms: list[str]) -> list[list[str]]:

        if self.config.use_llm:
            query = " , ".join(symptoms)

            amount = len(symptoms)
            top_k_results = self._query_vector(query, amount * 2)
            llm_answer = self._query_llm(query, top_k_results)
            return self._strip_llm_answer(llm_answer, amount)
        else:
            top_k_results = [self._query_vector(symptom, 1) for symptom in symptoms]
            return [df['Name'].iloc[0] for df in top_k_results]

    def _query_llm(self, query: str, top_docs: pd.DataFrame) -> str:
        context = ""

        names = top_docs["Name"].tolist()
        # ids = top_docs["id"].tolist()
        descriptions = top_docs["Prescribed_For"].tolist()

        for i in range(len(names)):
            context += f"Name:{names[i]}, Description: {descriptions[i]}\n"

        query = (
            f"Given this example {example}. Given this context:{context} Return only the names of the medications that could best cure each of the following comma separated symptoms from"
            f" each patient. Return only comma separated names in the same order in which they appear in the input. These are the input symptoms: {query}")

        print("Query: ", query)

        response = self.model.generate_content(query)

        print("Response: ", response)

        return response.text

    def _query_vector(self, query: str, top_k: int = 5) -> pd.DataFrame:
        query_embedding = self._get_embedding(query)

        # Compute the cosine similarity between the query and all embeddings in the dataframe
        similarities = cosine_similarity([query_embedding], self.data['embedding'].tolist())[0]

        df = self.data.copy()
        df.drop(columns=['embedding'], inplace=True)
        df['similarity'] = similarities

        return df.sort_values(by='similarity', ascending=False).head(top_k)

    def _attach_embedding(self, data: pd.DataFrame):
        data["embedding"] = data["Prescribed_For"].apply(lambda x: self._get_embedding(x))
        return data

    def _reset_domain(self, data: pd.DataFrame):
        self.collection.delete_many({})

        return self.collection.insert_many(data.to_dict('records'))

    def _get_embedding(self, text: str) -> list[float]:
        if not text.strip():
            print("Attempted to get embedding for empty text.")
            return []

        embedding = self.embedding_model.encode(text)

        return embedding.tolist()

    def _strip_llm_answer(self, completion: str, amount: int) -> list[list[str]]:

        output = []

        for answer in completion.split(','):
            words = answer.split(" ")
            patient_output = []

            for word in words:
                if word.strip() in self.data['Name'].tolist():
                    patient_output.append(word.strip())

            output.append(patient_output)

            if len(output) == amount:
                break

        while len(output) < amount:
            output.append([])

        return output


if __name__ == '__main__':

    load_dotenv()
    os.environ["TOKENIZERS_PARALLELISM"] = "true"
    api_key = os.getenv('GOOGLE_API_KEY')

    data = pd.read_csv('..\..\data\Drugs.csv')
    rag_config = RagConfig(use_persistence=True, use_llm=False, gemini_api_key=api_key)
    rag = RAG(data = data, config=rag_config)
    result = rag.query_medications_for_patients(
        ['osteoporosis and cough', 'diabetes and osteoporosis', 'fever and cough and diabetes', 'diabetes and fever', 'arthritis'])
    print("Result: ", result)
