
import os
import sys
# Agregado para langgraph studio
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from langchain_openai import ChatOpenAI
from langchain_community.tools import TavilySearchResults
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import START, StateGraph
from langgraph.prebuilt import tools_condition
from langgraph.prebuilt import ToolNode
from rag import rag_load

from toolShopify import get_shopify_order_status , get_shopify_order_status_by_num_seguimiento
from dotenv import load_dotenv


load_dotenv()
# from IPython.display import Image, display


#--------------------------------------------------------------------------------------------------------------------------------------

TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]

retriever_guia, retriever_faq , retriever_products = rag_load(load=True)

from langchain.tools.retriever import create_retriever_tool
retriever_tool_guia = create_retriever_tool(
    retriever=retriever_guia,
    name="obtener_informacion_de_naos",
    description="Usar para obtener información de guía y beneficios de los productos de naos kingdom , como tomarlos, como cobinarlos, para que utilizarlos, recomendaciones.",	
    
)

retriever_tool_faq = create_retriever_tool(
    retriever=retriever_faq,
    name="obtener_informacion_de_naos_faq",
    description="Usar para obtener informacion sobre las preguntas frecuentes sobre informacion relacionada a como, cuando, que, donde, por que y para que de los productos de naos, además tambien sobre consultas sobre tu pedido, problemas con el envio, devoluciones, ",
)

retriever_tool_products = create_retriever_tool(
    retriever=retriever_products,
    name="obtener_informacion_de_productos_naos",
    description="Usar para obtener informacion de los productos naos kingdom como ingredientes, url, sabores, presentaciones",
    
)


tavilyTool = TavilySearchResults(
    name="Naos_Kingdom_Productos",
    max_results=5,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    search_depth="advanced",
    include_domains = ["https://naoskingdom.com/collections/proteinas", "https://naoskingdom.com/collections/proteinas",
    "https://naoskingdom.com/collections/bcaa",
                        "https://naoskingdom.com/collections/creatina",
                        "https://naoskingdom.com/collections/quemador-de-grasa", 
                        "https://naoskingdom.com/collections/pre-entreno",
                        "https://naoskingdom.com/collections/vitaminas",
                        "https://naoskingdom.com/products/white-lion-proteina-whey",
                        "https://naoskingdom.com/products/blue-rhino-proteina-vegana",
                        "https://naoskingdom.com/products/lioness-proteina-whey",
                        "https://naoskingdom.com/products/diet-rhino-proteina-vegana",
                        "https://naoskingdom.com/products/lion-proteina-whey",
                        "https://naoskingdom.com/products/rhino-proteina-vegana",
                        "https://naoskingdom.com/products/blue-tiger-collagen-whey-protein",
                        "https://naoskingdom.com/products/white-bulldog-bcaa",
                        "https://naoskingdom.com/products/bulldog-bcaa",
                        "https://naoskingdom.com/products/white-bull-creatina",
                        "https://naoskingdom.com/products/white-fox-quemador-de-grasa",
                        "https://naoskingdom.com/products/ram-quemador-de-grasa",
                        "https://naoskingdom.com/products/fox-quemador-de-grasa",
                        "https://naoskingdom.com/products/white-cheetah-pre-entreno",
                        "https://naoskingdom.com/products/gazelle-pre-entreno",
                        "https://naoskingdom.com/products/gold-deer-youth",
                        "https://naoskingdom.com/products/indigo-deer-sleep",
                        "https://naoskingdom.com/products/blue-deer-recovery",
                        "https://naoskingdom.com/products/green-deer-vitality",
                        "https://naoskingdom.com/products/white-deer-growth",
                        "https://naoskingdom.com/products/red-deer-immunity",
                        ],
    description="""
        Utiliza esta herramienta para buscar informacion sobre precios de los suplementos de Naos Kingdom.
        ",
    """,
   
    # include_raw_content=True,
    # exclude_domains = []
)


llm = ChatOpenAI(model="gpt-4o")



tools=[tavilyTool, retriever_tool_guia, retriever_tool_faq, retriever_tool_products,get_shopify_order_status, get_shopify_order_status_by_num_seguimiento]

llm_with_tools = llm.bind_tools(tools)


# ## WEBBASELOADER - Otra modalidad de carga y consulta de la web
# - Tambien se puede utilizar un cargador de la web para convertirlo en embbedings que podamos consultar


# System message
sys_msg = SystemMessage(content="""
Rol = Eres un experto vendedor de la empresa Naos kingdom, debes representarlos y hablar sobre sus productos en tono positivo. refiriendote a uds como los mejores del mercado. ("nosotros", "nuestro", etc)
siempre que respondes hablas en primera persona del plural
                        
### SI TE PREGUNTAN SOBRE PRECIOS DE PRODUCTOS y STOCK  DEBES RESPONDER CON INFORMACION VERIDICA Y ACTUALIZADA CON LA HERRAMIENTA "naos_kingdom_productos" **
                        
### Si tienes mas de una llamada a herramienta en el mensaje, debes responder a cada una de ellas en el orden en que aparecen en el mensaje.Primero responde Una y luego responde la siguiente.                        

REGLAS:                       
- La herramienta Naos_Kingdom_Products debes usarla para obtener informacion relacionada a los precios y stock suplementos de Naos Kingdom.
- Si te preguntan por el precio de un producto en especifico, ingresa a la url especifica y busca la información solicitada.
- compone la url de busqueda con el nombre del producto que te consultan, por ejemplo: "https://naoskingdom.com/products/" + "nombre_del_producto",                        
- los enlaces web que estas consultando son: 
                        "https://naoskingdom.com/collections/proteinas"
                        "https://naoskingdom.com/collections/bcaa"
                        "https://naoskingdom.com/collections/creatina"
                        "https://naoskingdom.com/collections/quemador-de-grasa" 
                        "https://naoskingdom.com/collections/pre-entreno",
                        "https://naoskingdom.com/collections/vitaminas",
                        "https://naoskingdom.com/products/white-lion-proteina-whey",
                        "https://naoskingdom.com/products/blue-rhino-proteina-vegana",
                        "https://naoskingdom.com/products/lioness-proteina-whey",
                        "https://naoskingdom.com/products/diet-rhino-proteina-vegana",
                        "https://naoskingdom.com/products/lion-proteina-whey",
                        "https://naoskingdom.com/products/rhino-proteina-vegana",
                        "https://naoskingdom.com/products/blue-tiger-collagen-whey-protein",
                        "https://naoskingdom.com/products/white-bulldog-bcaa",
                        "https://naoskingdom.com/products/bulldog-bcaa",
                        "https://naoskingdom.com/products/white-bull-creatina",
                        "https://naoskingdom.com/products/white-fox-quemador-de-grasa",
                        "https://naoskingdom.com/products/ram-quemador-de-grasa",
                        "https://naoskingdom.com/products/fox-quemador-de-grasa",
                        "https://naoskingdom.com/products/white-cheetah-pre-entreno",
                        "https://naoskingdom.com/products/gazelle-pre-entreno",
                        "https://naoskingdom.com/products/gold-deer-youth",
                        "https://naoskingdom.com/products/indigo-deer-sleep",
                        "https://naoskingdom.com/products/blue-deer-recovery",
                        "https://naoskingdom.com/products/green-deer-vitality",
                        "https://naoskingdom.com/products/white-deer-growth",
                        "https://naoskingdom.com/products/red-deer-immunity".
- Para armar la url_de_la_imagen_del_producto extraela del elemento "img" de la pagina web de Naos Kingdom con "class"="product-item__primary-image" y pegala en la respuesta.


                                                
Usa la herramienta "naos_kingdom_productos" para obtener información sobre el precio los productos y presenta la respuesta en formato JSON dentro de un bloque de código usando la sintaxis de Markdown ```json. La respuesta debe tener las siguientes propiedades:

```json

{
  "nombre_del_producto":string, //nombre del producto consultado
  "precio_actual":string, // precio actual del producto
  "precio_anterior":string, // precio anterior del producto
  "url_al_producto": string, // url del producto ej: "https://naoskingdom.com/products/nombre_del_producto"
  "url_de_la_imagen_del_producto": string, // url de la imagen del producto 
  "tool_call_id": "naos_kingdom_productos",
  "sabores": []                    
}
            
```	
                       
------- Devuelve el JSON plano sin caracteres adicionales, necesito leer el JSON desde el código JavaScript. Elimina cualquier formato de texto '```json' que estés agregando. Mantén la estructura del JSON siempre en inglés y solo cambia los valores del JSON al idioma que identifiques en el sitio web. La respuesta debe ser el JSON y nada más"                        
Toda esta información debe ser extraída del contenido de la respuesta de la herramienta. Si no encuentras respuesta a alguna de esas propiedades, no la inventes y coloca null
                         
    
-----------------------                           
                        
### Si estas respondiendo sobre el estado de pedido de shopify, debes usar la herramienta "get_shopify_order_status" o "get_shopify_order_status_by_num_seguimiento" para obtener la información de la orden de pedido de shopify.

El formato de la respuesta sobre el estado del envío del pedido debe ser siguiendo solo este ejemplo: :
    'número de orden': '',
    'estado': '',
    'direccion': '',
    'fecha_de_envío': '',
    'nombre': '',
    'enviado por': '',
    'Observaciones del cliente': '',
    'Última persona con el pedido': ''

No dudes en preguntar si necesitas más información.
                        
### SI HACEN UNA PREGUNTA RELACIONADA AL USO, COMBINACIONES, RECOMENDACIONES, EFECTOS SECUNDARIOS, NUTRICION, COMO TOMARLOS, DEBES PRIMERO CONSULTAR EN LA HERRAMIENTA "obtener_informacion_de_naos_faq" Y LUEGO RESPONDER CON LA INFORMACION QUE ENCUENTRES.
SI NO ENCONTRASTE UNA RESPUESTA A LA PREGUNTA PUEDES CONSULTAR EN LA HERRAMIENTA "obtener_informacion_de_naos" PARA OBTENER INFORMACION DE LOS PRODUCTOS DE NAOS KINGDOM Y COMPLEMENTAR TU RESPUESTA.                       

                        """)




# Node
def assistant(state: MessagesState):
       
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}




# Graph
builder = StateGraph(MessagesState)

# Define nodes: these do the work
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))



# Define edges: these determine how the control flow moves
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")


 

# builder.add_edge("evaluate", "assistant")
memory = MemorySaver()
react_graph = builder.compile(checkpointer=memory)

# Show
# display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))


# message = [HumanMessage(content="""El blue fox lo tienes?"""
# )]
# messages = react_graph.invoke({"messages": messages})


# threadId = "1234"
# config = {
#     "configurable": {"thread_id": threadId},
   
# }

# final_state = react_graph.invoke(
#     {"messages": [HumanMessage(content="Dime algunos precios de creatina")]},
#     config={"configurable": {"thread_id": threadId}},
# )
# final_state["messages"][-1].content




# print(final_state["messages"][-1].content)

# %% [markdown]
# BadRequestError: Error code: 400 - {'error': {'message': "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_26SuqYchIFxWazl58MvJ5RPM", 'type': 'invalid_request_error', 'param': 'messages.[11].role', 'code': None}}

# %%
# Start conversation
# for chunk in react_graph.stream({"messages": [HumanMessage(content="dime el precio de una proteina")]}, config, stream_mode="values"):
    # print(chunk)

# %%
# print(messages["messages"][-1].content)


