import os
from langchain_aws import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

def ingest_pdf_incremental(file_path: str):
    print("📥 Starting incremental PDF ingestion...")

    # Step 1: Load PDF
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    print(f"📄 Loaded {len(docs)} document(s) from {file_path}")

    # Step 2: Split documents
    splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks")

    # Step 3: Embed using Bedrock
    embeddings = BedrockEmbeddings()

    print("🔁 Testing Bedrock Embedding...")
    try:
        emb = embeddings.embed_query("Test from Bedrock")
        print(f"✅ Got embedding of length {len(emb)}")
    except Exception as e:
        print(f"❌ Failed to get embedding: {e}")
        return

    # Step 4: Load existing Chroma vectorstore or create new
    persist_directory = "rag/vectorstore"
    os.makedirs(persist_directory, exist_ok=True)

    if os.listdir(persist_directory):
        print("🔄 Loading existing vectorstore for incremental update...")
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )
    else:
        print("🆕 Creating new vectorstore...")
        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

    # Step 5: Add new document chunks to vectorstore
    vectordb.add_documents(chunks)
    vectordb.persist()
    print("✅ Incremental ingestion complete and saved to vectorstore.")

if __name__ == "__main__":
    pdf_path = "uploads/sample report1.pdf"
    if os.path.exists(pdf_path):
        ingest_pdf_incremental(pdf_path)
    else:
        print(f"❌ File not found: {pdf_path}")
