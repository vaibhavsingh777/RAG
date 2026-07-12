import os
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline as hf_pipeline
from langchain.schema import Document


class QAPipeline:
    def __init__(self):
        # Load local embedding model
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

        # Load or create FAISS index
        self.index_path = "data/faiss_index"
        if os.path.exists(self.index_path):
            print("Loading existing FAISS index...")
            self.db = FAISS.load_local(self.index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            print("Creating new FAISS index...")
            loader = TextLoader("data/my_docs.txt")
            documents = loader.load()
            texts = [doc.page_content for doc in documents]
            self.db = FAISS.from_texts(texts, self.embeddings)
            self.db.save_local(self.index_path)

        # Local QA model from Hugging Face
        self.qa_pipeline = hf_pipeline("question-answering", model="deepset/roberta-base-squad2")

    def get_answer(self, query: str) -> str:
        # Search similar chunks
        results = self.db.similarity_search(query, k=3)

        if not results:
            return "No relevant documents found."

        # Concatenate retrieved docs for context
        context = "\n".join([doc.page_content for doc in results])

        # Run local QA model
        answer = self.qa_pipeline({
            "question": query,
            "context": context
        })

        return answer.get("answer", "No answer found.")
