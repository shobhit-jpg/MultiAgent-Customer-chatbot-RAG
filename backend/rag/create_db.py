from backend.rag.vectorstore import VectorStore

class CreateDb:

    def build_vectorstore(self):

        vectorstore = VectorStore()

        if vectorstore.db._collection.count() == 0:
            print("Creating vector database...")
            pdfs = [
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\FAQ.pdf",
                    "category": "faq"
                },
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\pricing.pdf",
                    "category": "billing"
                },
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\products.pdf",
                    "category": "products"
                },
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\refund_policy.pdf",
                    "category": "refund_policy"
                },
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\shipping.pdf",
                    "category": "shipping"
                },
                {
                    "path": r"C:\Labmentix\Customer_care- chatbot\knowledge_base\warranty.pdf",
                    "category": "warranty"
                }  
            ]

            for pdf in pdfs:
                vectorstore.ingest_pdf(
                pdf_path=pdf["path"],
                category=pdf["category"]
            )
        else :
            print("Existing vector database found.")
        
        return vectorstore
