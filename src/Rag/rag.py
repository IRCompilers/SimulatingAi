import os
import string

import pandas as pd
from openai import OpenAI
from openai.types.chat import ChatCompletion
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class RAG:
    def __init__(self, data: pd.DataFrame = None, use_persistence: bool = True):

        if use_persistence:
            self.client = MongoClient('mongodb://localhost:27017/')
            self.db = self.client['RAG']
            self.collection = self.db['medications']

        self.embedding_model = SentenceTransformer("thenlper/gte-large")

        if data is None:
            if use_persistence:
                self.data = pd.DataFrame(list(self.collection.find()))
                self.data.drop(columns='_id', inplace=True)
            else:
                raise ValueError("Data cannot be None if use_persistence is False: data must be provided.")

        else:

            print("Data provided.")

            data = self._attach_embedding(data)

            if use_persistence:
                self._reset_domain(data)

            self.data = data

    def query_medications(self, symptoms: list[str], top_k: int = 5):
        query = " , ".join(symptoms)
        top_k_results = self._query_vector(query, top_k)
        llm_answer = self._query_llm(query, top_k_results)

        print("answer: ", llm_answer.choices[0].message.content)

        return self._strip_llm_answer(llm_answer, len(symptoms))

    def _query_llm(self, query: str, top_docs: pd.DataFrame):
        context = ""

        names = top_docs["name"].tolist()
        ids = top_docs["id"].tolist()
        descriptions = top_docs["description"].tolist()

        for i in range(len(names)):
            context += f"Name:{names[i]},  Id: {ids[i]}, Description: {descriptions[i]}\n"

        client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        print("query: ", query)

        completion = client.chat.completions.create(
            model="local-model",
            messages=[
                {"role": "system",
                 "content": f"{context}. Model should recommend a medication for each of the symptoms: {query}"},
                {"role": "user", "content": query}
            ],
            temperature=0.9,
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
    rag = RAG()
    result = rag.query_medications(['flu', 'fever'])
    print(result)
