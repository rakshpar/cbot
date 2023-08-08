import os
from langchain.document_loaders import ReadTheDocsLoader
from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Pinecone
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from const import INDEX_NAME
import time
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff

pinecone.init(api_key="72c1a122-fef4-4ef0-9b8a-93dd24d49a47",environment="us-west4-gcp-free")

def ingest_doc()-> None:
    loader = PyPDFDirectoryLoader(r'C:\Users\rakeparm\Documents\langchain\into-to-vector-db\cbot')
    loader.encoding = "utf8"
    raw_documents = loader.load()    
    print(len(raw_documents))
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1500,chunk_overlap=100,separators=["\n"])
    documents = text_splitter.split_documents(documents=raw_documents)
    print(f"Splitted into {len(documents)} chunks")

    #for doc in documents:
    #    old_path = doc.metadata['source']
    #    new_path = old_path.replace("langchain-docs","https:/")
    #    doc.metadata.update({"source":new_path})

    print(f"going to insert {len(documents)} into pinecone")
    embeddings = OpenAIEmbeddings(chunk_size=1)
    batch_size = 1  # Define your preferred batch size
    index = pinecone.Index(INDEX_NAME)
    for i in range(377, len(documents), batch_size):
        chunk_batch = documents[i:i + batch_size]
        #vect = embeddings.embed_documents(chunk_batch)
        #index.upsert(vectors=vect)
        Pinecone.from_documents(documents=chunk_batch,embedding=embeddings,index_name= INDEX_NAME,batch_size=1)
        #time.sleep(120)
    #compleation_with_backoff(documents=documents,embeddings=embeddings)

    """ vector_store = Pinecone(index=INDEX_NAME, embeddings=embeddings)
    
    # Batch insert the chunks into the vector store
    batch_size = 50  # Define your preferred batch size
    for i in range(0, len(documents), batch_size):
        chunk_batch = documents[i:i + batch_size]
        vector_store.add_documents(chunk_batch)

    # Flush the vector store to ensure all documents are inserted
    vector_store.flush() """
    print("**** added to pinecode vectors****")



if __name__ == "__main__":
    ingest_doc()
