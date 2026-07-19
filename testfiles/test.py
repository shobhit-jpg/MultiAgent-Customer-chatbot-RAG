from vectorstore import VectorStore

vectorstore= VectorStore()
pdfpath = "C:\Labmentix\Customer_care- chatbot\knowledge_base\TechMart_Electronics_Warranty_Policy.pdf"
vectorstore.ingest_pdf(pdf_path=pdfpath,category="warranty")


results = vectorstore.db.similarity_search(
    "How long is the laptop warranty?",
    k=3
)

for i, doc in enumerate(results, 1):
    print("=" * 70)
    print(f"Result {i}")
    print(doc.page_content)
    print(doc.metadata)