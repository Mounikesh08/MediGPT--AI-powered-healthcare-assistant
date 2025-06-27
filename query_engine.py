import os
from langchain_community.vectorstores import Chroma
from langchain_aws import BedrockEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import Bedrock
from dotenv import load_dotenv

load_dotenv()

def query_engine():
    print("📥 Loading vectorstore...")
    vectordb = Chroma(persist_directory="rag/vectorstore", embedding_function=BedrockEmbeddings())

    print("🤖 Setting up LLM and Retrieval QA chain...")
    llm = Bedrock(model_id=os.getenv("BEDROCK_MODEL_ID"))

    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectordb.as_retriever(),
        return_source_documents=True
    )

    while True:
        query = input("\nEnter your healthcare query (or 'exit' to quit): ")
        if query.lower() == 'exit':
            break

        print("\n⏳ Retrieving answer...")
        result = qa(query)

        print("\n💡 Answer:\n", result['result'])
        print("\n📚 Source documents:")
        for doc in result['source_documents']:
            print(f"- {doc.metadata.get('source', 'Unknown source')}")

if __name__ == "__main__":
    query_engine()
