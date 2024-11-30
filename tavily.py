
# import os
# from rag import rag_product_load
# TAVILY_API_KEY = os.environ["TAVILY_API_KEY"]
# rag_product_load()

# from langchain_community.tools import TavilySearchResults
# tavilyTool = TavilySearchResults(
#     name="Naos_Kingdom_Proteinas",
#     max_results=5,
#     include_answer=True,
#     include_raw_content=True,
#     include_images=True,
#     search_depth="advanced",
#     include_domains = ["https://naoskingdom.com/collections/proteinas", "https://naoskingdom.com/collections/proteinas",
#     "https://naoskingdom.com/collections/bcaa",
#                         "https://naoskingdom.com/collections/creatina",
#                         "https://naoskingdom.com/collections/quemador-de-grasa", 
#                         "https://naoskingdom.com/collections/pre-entreno",
#                         "https://naoskingdom.com/collections/vitaminas",
#                         "https://naoskingdom.com/products/white-lion-proteina-whey",
#                         "https://naoskingdom.com/products/blue-rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/lioness-proteina-whey",
#                         "https://naoskingdom.com/products/diet-rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/lion-proteina-whey",
#                         "https://naoskingdom.com/products/rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/blue-tiger-collagen-whey-protein",
#                         "https://naoskingdom.com/products/white-bulldog-bcaa",
#                         "https://naoskingdom.com/products/bulldog-bcaa",
#                         "https://naoskingdom.com/products/white-bull-creatina",
#                         "https://naoskingdom.com/products/white-fox-quemador-de-grasa",
#                         "https://naoskingdom.com/products/ram-quemador-de-grasa",
#                         "https://naoskingdom.com/products/fox-quemador-de-grasa",
#                         "https://naoskingdom.com/products/white-cheetah-pre-entreno",
#                         "https://naoskingdom.com/products/gazelle-pre-entreno",
#                         "https://naoskingdom.com/products/gold-deer-youth",
#                         "https://naoskingdom.com/products/indigo-deer-sleep",
#                         "https://naoskingdom.com/products/blue-deer-recovery",
#                         "https://naoskingdom.com/products/green-deer-vitality",
#                         "https://naoskingdom.com/products/white-deer-growth",
#                         "https://naoskingdom.com/products/red-deer-immunity",
#                         ],
#     description="""
#         Utiliza esta herramienta para buscar informacion sobre los suplementos de Naos Kingdom.
#         precio, beneficios, ingredientes, marca y más detalles, como asi tambien cantidades, sabores, promociones etc.
#         Si te preguntan por un producto en especifico, ingresa a la url especifica y busca la información solicitada.
#         url de ejemplo "https://naoskingdom.com/products/producto",
#     """,
   
#     # include_raw_content=True,
#     # exclude_domains = []
# )


# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o")



# tools=[tavilyTool]

# llm_with_tools = llm.bind_tools(tools)


# # ## WEBBASELOADER - Otra modalidad de carga y consulta de la web
# # - Tambien se puede utilizar un cargador de la web para convertirlo en embbedings que podamos consultar

# from langgraph.graph import MessagesState
# from langchain_core.messages import HumanMessage, SystemMessage

# # System message
# sys_msg = SystemMessage(content="""
# Eres un experto vendedor de la empresa Naos kingdom, debes representarlos y hablar sobre sus productos en tono positivo. refiriendote a uds como los mejores del mercado. ("nosotros", "nuestro", etc)
# siempre que respondes hablas en primera persona del plural
                        
# Uso obligatorio de la herramienta:

# - Ésta herramienta debes usarla para obtener informacion relacionada a suplementos de Naos Kingdom.
# - los enlaces web que estas consultando son: 
#                         "https://naoskingdom.com/collections/proteinas"
#                         "https://naoskingdom.com/collections/bcaa"
#                         "https://naoskingdom.com/collections/creatina"
#                         "https://naoskingdom.com/collections/quemador-de-grasa" 
#                         "https://naoskingdom.com/collections/pre-entreno",
#                         "https://naoskingdom.com/collections/vitaminas",
#                         "https://naoskingdom.com/products/white-lion-proteina-whey",
#                         "https://naoskingdom.com/products/blue-rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/lioness-proteina-whey",
#                         "https://naoskingdom.com/products/diet-rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/lion-proteina-whey",
#                         "https://naoskingdom.com/products/rhino-proteina-vegana",
#                         "https://naoskingdom.com/products/blue-tiger-collagen-whey-protein",
#                         "https://naoskingdom.com/products/white-bulldog-bcaa",
#                         "https://naoskingdom.com/products/bulldog-bcaa",
#                         "https://naoskingdom.com/products/white-bull-creatina",
#                         "https://naoskingdom.com/products/white-fox-quemador-de-grasa",
#                         "https://naoskingdom.com/products/ram-quemador-de-grasa",
#                         "https://naoskingdom.com/products/fox-quemador-de-grasa",
#                         "https://naoskingdom.com/products/white-cheetah-pre-entreno",
#                         "https://naoskingdom.com/products/gazelle-pre-entreno",
#                         "https://naoskingdom.com/products/gold-deer-youth",
#                         "https://naoskingdom.com/products/indigo-deer-sleep",
#                         "https://naoskingdom.com/products/blue-deer-recovery",
#                         "https://naoskingdom.com/products/green-deer-vitality",
#                         "https://naoskingdom.com/products/white-deer-growth",
#                         "https://naoskingdom.com/products/red-deer-immunity"

# - son los únicos enlaces donde puedes usar para buscar información de:
# - Vas a recibir preguntas como:
                        
#                         Dime el precio de... 
#                         que beneficios tienen ...
#                         que precios tienen ...

#                         más preguntas relacionadas a los suplementos de Naos Kingdom.

                                                
# respuesta:
                        
#  **texto que creas necesario para responder la pregunta**
# **Si es más de un producto, puedes responder con una lista de productos**

#  Formato de respuesta del/los producto/s encontrado/s:                       
# Por favor, extrae la siguiente información del sitio web de Naos Kingdom que consultaste:

# (Extrae esta información si la encuentras, si no, no inventes datos)
# - Nombre del suplemento
# - Marca del suplemento
# - Precio del suplemento
# - Porciones por envase
# - sabores disponibles                                              

# Y representa estos datos como un elemento HTML moderno en el formato de un article, con estilos CSS embebidos. Asegúrate de que el diseño sea atractivo y responsivo.

# No dudes en preguntar si necesitas más información.


#                         """)

# # Node
# # def assistant(state: MessagesState):
# #    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}




# # from langgraph.checkpoint.memory import MemorySaver

# # from langgraph.graph import START, StateGraph
# # from langgraph.prebuilt import tools_condition
# # from langgraph.prebuilt import ToolNode
# # from IPython.display import Image, display

# # # Graph
# # builder = StateGraph(MessagesState)

# # # Define nodes: these do the work
# # builder.add_node("assistant", assistant)
# # builder.add_node("tools", ToolNode(tools))

# # # Define edges: these determine how the control flow moves
# # builder.add_edge(START, "assistant")
# # builder.add_conditional_edges(
# #     "assistant",
# #     # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
# #     # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
# #     tools_condition,
# # )
# # builder.add_edge("tools", "assistant")
# # memory = MemorySaver()
# # react_graph = builder.compile(checkpointer=memory)

# # # Show
# # # display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))


# # # message = [HumanMessage(content="""Cuales son las proteínas premium?"""
# # # )]
# # # messages = react_graph.invoke({"messages": messages})
# # threadId = "1234"
# # config = {
# #     "configurable": {"thread_id": threadId},
   
# # }

# # # react_graph.invoke(
# # #     {"messages": [HumanMessage(content="")]},
# # #     config={"configurable": {"thread_id": threadId}},
# # # )







# # print(final_state["messages"][-1].content)

# # %% [markdown]
# # BadRequestError: Error code: 400 - {'error': {'message': "An assistant message with 'tool_calls' must be followed by tool messages responding to each 'tool_call_id'. The following tool_call_ids did not have response messages: call_26SuqYchIFxWazl58MvJ5RPM", 'type': 'invalid_request_error', 'param': 'messages.[11].role', 'code': None}}

# # %%
# # # Start conversation
# # for chunk in react_graph.stream({"messages": [HumanMessage(content="dime el precio de una proteina")]}, config, stream_mode="values"):
# #     print(chunk)

# # %%
# # print(messages["messages"][-1].content)


