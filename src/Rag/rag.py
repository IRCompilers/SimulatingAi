import os
import string

import dill
import pandas as pd
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.Rag.rag_config import RagConfig


class RAG:
    def __init__(self, data: pd.DataFrame = None, config: RagConfig = None):

        self.config = config

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
            self.embedding_model = SentenceTransformer("thenlper/gte-large")
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

    def query_medications_for_patients(self, symptoms: list[str]) -> list[str]:

        if self.config.use_llm:
            query = " , ".join(symptoms)

            amount = len(symptoms)
            top_k_results = self._query_vector(query, amount)
            llm_answer = self._query_llm(query, top_k_results)
            return self._strip_llm_answer(llm_answer, amount)
        else:
            top_k_results = [self._query_vector(symptom, 1) for symptom in symptoms]
            return [df['name'].iloc[0] for df in top_k_results]

    @staticmethod
    def _query_llm(query: str, top_docs: pd.DataFrame):
        context = ""

        names = top_docs["name"].tolist()
        ids = top_docs["id"].tolist()
        descriptions = top_docs["description"].tolist()

        for i in range(len(names)):
            context += f"Name:{names[i]},  Id: {ids[i]}, Description: {descriptions[i]}\n"

        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system",
                 "content": f"{context}. Model should recommend a medication for each of the symptoms: {query}"},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
        )

        return completion

    def _query_vector(self, query: str, top_k: int = 5) -> pd.DataFrame:
        query_embedding = self._get_embedding(query)

        # Compute the cosine similarity between the query and all embeddings in the dataframe
        similarities = cosine_similarity([query_embedding], self.data['embedding'].tolist())[0]

        df = self.data.copy()
        df.drop(columns=['embedding'], inplace=True)
        df['similarity'] = similarities

        return df.sort_values(by='similarity', ascending=False).head(top_k)

    def _attach_embedding(self, data: pd.DataFrame):
        data["embedding"] = data["description"].apply(lambda x: self._get_embedding(x))
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

    def _strip_llm_answer(self, completion: ChatCompletion, amount: int):
        message_content = completion.choices[0].message.content

        output = []

        for word in message_content.split():
            word = word.translate(str.maketrans('', '', string.punctuation)).strip("*")

            if word in self.data['name'].tolist():
                output.append(word)

                if len(output) == amount:
                    break

        while len(output) < amount:
            output.append(None)

        return output


if __name__ == '__main__':
    os.environ["TOKENIZERS_PARALLELISM"] = "true"

    # data = pd.read_csv('medications.csv')
    rag_config = RagConfig(use_persistence=True, use_llm=False)
    rag = RAG(config=rag_config)
    result = rag.query_medications_for_patients(['flu', 'fever'])
    print(result)
