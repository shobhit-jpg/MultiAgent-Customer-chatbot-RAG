# backend/vectorstore/vectorstore.py
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from backend.rag.embeddings import SentenceTransformerEmbedding


class VectorStore:

    def __init__(self):

        self.embedding = SentenceTransformerEmbedding()

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        self.db = Chroma(
            collection_name="customer_support",
            embedding_function=self.embedding,
            persist_directory="backend/vectorstore/chroma_db"
        )

    def ingest_pdf(self, pdf_path: str, category: str):
        """
        Load a PDF, split it into chunks, attach metadata,
        and store the chunks in ChromaDB.

        Example:
            category = "billing"
        """

        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        chunks = self.splitter.split_documents(documents)

        for index, chunk in enumerate(chunks):

            metadata = {
                "source": Path(pdf_path).name,
                "chunk_id": index,
                "category": category            }

            chunk.metadata.update(metadata)

        self.db.add_documents(chunks)

        print(f"Indexed {len(chunks)} chunks from {Path(pdf_path).name}")

    def get_retriever(self, categories=None, k=3):

        search_kwargs = {"k": k}

        if categories:

            if isinstance(categories, str):
                categories = [categories]

            search_kwargs["filter"] = {
                "category": {
                    "$in": categories
                }
            }

        return self.db.as_retriever(search_kwargs=search_kwargs)