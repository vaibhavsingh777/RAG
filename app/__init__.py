import os

class QAPipeline:
    def __init__(self):
        # Other setup...
        index_path = "data/faiss_index"

        if os.path.exists(index_path):
            # Load the index only if it exists
            self.db = FAISS.load_local(index_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            # Build the index if it's not there
            loader = TextLoader("data/docs.txt")  # or whatever your doc path is
            documents = loader.load()
            texts = [doc.page_content for doc in documents]
            self.db = FAISS.from_texts(texts, self.embeddings)
            self.db.save_local(index_path)
