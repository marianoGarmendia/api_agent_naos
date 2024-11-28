from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv


from app.naos.utils.load import doc_load, text_splitters, connect_to_astra_vstore, add_docs_astra_and_get_retriever

load_dotenv()


ruta_pdf_guia_naos = os.path.join(os.path.dirname(__file__), "data", "guia_y_beneficios_naos_productos.pdf")
ruta_pdf_faq_naos = os.path.join(os.path.dirname(__file__), "data", "faq_naos.pdf")


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")



embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    api_key=OPENAI_API_KEY
    # openai_api_key=OPENAI_API_KEY,
)

llm = ChatOpenAI(model="gpt-4o")

def rag_load(load):
    if load is False:    
        docs =  doc_load(ruta_pdf_guia_naos)
        text_splitter = text_splitters(docs, "guia")

        docs_faq =  doc_load(ruta_pdf_faq_naos)
        text_splitter_faq =  text_splitters(docs_faq, "guia")

        naos_guia_vector_db = connect_to_astra_vstore(embeddings, "naos_guia_beneficios")
        faq_naos_vectordb = connect_to_astra_vstore(embeddings, "faq_naos")

        retriever_guia =  add_docs_astra_and_get_retriever(naos_guia_vector_db, text_splitter)
        retriever_faq = add_docs_astra_and_get_retriever(faq_naos_vectordb, text_splitter_faq)

        return retriever_guia, retriever_faq
    else:
        naos_guia_vector_db =  connect_to_astra_vstore(embeddings, "naos_guia_beneficios")
        faq_naos_vectordb =  connect_to_astra_vstore(embeddings, "faq_naos")

        retriever_guia =  naos_guia_vector_db.as_retriever(search_kwargs={"k":5})
        retriever_faq =  faq_naos_vectordb.as_retriever(search_kwargs={"k":5})

        return retriever_guia, retriever_faq




# async def rag_load(load):
#     if load is False:
#     # Carga de documentos en paralelo
#         docs, docs_faq = await asyncio.gather(
#             doc_load(ruta_pdf_guia_naos),
#             doc_load(ruta_pdf_faq_naos),
#         )
        
#         # División de textos en paralelo
#         text_splitter, text_splitter_faq = await asyncio.gather(
#             text_splitters(docs, "guia"),
#             text_splitters(docs_faq, "faq"),
#         )
        
#         # Conexión a la base de datos
#         naos_guia_vector_db, faq_naos_vectordb = await asyncio.gather(
#             connect_to_astra_vstore(embeddings, "naos_guia_beneficios"),
#             connect_to_astra_vstore(embeddings, "faq_naos"),
#         )
        
#         # Agregar documentos y recuperar información
#         retriever_guia, retriever_faq = await asyncio.gather(
#             add_docs_astra_and_get_retriever(naos_guia_vector_db, text_splitter),
#             add_docs_astra_and_get_retriever(faq_naos_vectordb, text_splitter_faq),
#         )

#         return retriever_guia, retriever_faq
#     else:
#         naos_guia_vector_db, faq_naos_vectordb = await asyncio.gather(
#             connect_to_astra_vstore(embeddings, "naos_guia_beneficios"),
#             connect_to_astra_vstore(embeddings, "faq_naos"),
#         )
        
#         # Agregar documentos y recuperar información
#         retriever_guia, retriever_faq = await asyncio.gather(
#             add_docs_astra_and_get_retriever(naos_guia_vector_db, text_splitter),
#             add_docs_astra_and_get_retriever(faq_naos_vectordb, text_splitter_faq),
#         )
#         return retriever_guia, retriever_faq


