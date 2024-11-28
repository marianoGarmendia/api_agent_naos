import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# from langchain.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain_astradb import AstraDBVectorStore




def doc_load(file_path:str):
    file_path_src = file_path #Ruta al archivo PDF
    loader = PyPDFLoader(file_path_src)

    docs = loader.load()

    return docs 

def text_splitters(docs, pdf):
    if pdf == "guia": 
        text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1500,
        chunk_overlap=300,
        length_function=len
        )

        docs_splitter = text_splitter.split_documents(docs)
        return docs_splitter

    if pdf == "faq":
        text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
        )

        docs_splitter = text_splitter.split_documents(docs)
        return docs_splitter
        
def connect_to_astra_vstore(embeddings, collection_name):
    ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    desired_namespace = os.getenv("ASTRA_DB_KEYSPACE")

#     openai_vectorize_options = CollectionVectorServiceOptions(
#     provider="openai",
#     model_name="text-embedding-3-small",
#     authentication={
#         "providerKey": OPENAI_API_KEY,
#     },
# )
    
    if desired_namespace:
        ASTRA_DB_KEYSPACE = desired_namespace
    else:
        ASTRA_DB_KEYSPACE = None
    
    vstore_astra = AstraDBVectorStore(
        embedding=embeddings,
        collection_name=collection_name,
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

      
    return vstore_astra

def add_docs_astra_and_get_retriever(vstore_astra , documents):
    # vstore_astra.delete_collection()
    vstore_astra.add_documents(documents=documents)
    retriever_astra = vstore_astra.as_retriever(search_kwargs={"k":5})
    return retriever_astra