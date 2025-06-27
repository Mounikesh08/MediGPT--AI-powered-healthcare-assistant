from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from langchain_community.vectorstores import Chroma
from langchain_aws import BedrockEmbeddings, BedrockLLM
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
import shutil
from rag.ingest import ingest_pdf_incremental  # your incremental ingestion function

load_dotenv()

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup vectorstore and QA chain
vectordb = Chroma(
    persist_directory="rag/vectorstore",
    embedding_function=BedrockEmbeddings()
)
llm = BedrockLLM(model_id=os.getenv("BEDROCK_MODEL_ID"))
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectordb.as_retriever(),
    return_source_documents=True
)

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_doc(req: QueryRequest):
    try:
        result = qa(req.question)
        answer = result["result"]
        sources = [doc.metadata.get("source", "Unknown") for doc in result["source_documents"]]
        return {"answer": answer, "sources": sources}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    # Ensure uploads directory exists
    os.makedirs("uploads", exist_ok=True)

    file_location = f"uploads/{file.filename}"

    # Save uploaded PDF
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print(f"Received file: {file.filename}")

    # Incrementally add new PDF to vectorstore
    ingest_pdf_incremental(file_location)

    return {"message": f"✅ '{file.filename}' uploaded and ingested successfully!"}
