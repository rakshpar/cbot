import sys
sys.path.append(r'C:\Users\rakeparm\Desktop\generative ai\documentation-helper-1-start-here')
import os
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import Pinecone
import pinecone
from const import INDEX_NAME

pinecone.init(api_key="72c1a122-fef4-4ef0-9b8a-93dd24d49a47",environment="us-west4-gcp-free")

def run_llm(query:str)-> any:
    embeddings = OpenAIEmbeddings()
    doc_search = Pinecone.from_existing_index(index_name=INDEX_NAME,embedding=embeddings)
    chat = ChatOpenAI(verbose=True,temperature=0)
    qa = RetrievalQA.from_chain_type(llm=chat,chain_type="stuff",retriever = doc_search.as_retriever(),return_source_documents=True)
    return qa({'query':query})

if __name__ == "__main__":
    res = run_llm("What is langchain ?")
    print(res)

