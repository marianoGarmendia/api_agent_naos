from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from naos.main import react_graph
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Instanciar FastAPI
app = FastAPI()
print("FastAPI inicializado")
print("FastAPI inicializado")
print("server.py")
print(sys.path)
# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir solicitudes desde cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para la validación del mensaje
class MessageRequest(BaseModel):
    message: str

class AgentRequest(BaseModel):
    message: str
    threadId: str

# Endpoint para manejar mensajes simples
@app.post("/api/message")
async def handle_message(request: MessageRequest):
    message = request.message
    print(f"Mensaje recibido: {message}")
    return {"status": "success", "received_message": message}

# Endpoint para manejar mensajes del agente
@app.post("/api/agent")
async def handle_agent(request: AgentRequest):
    message = request.message
    threadId = request.threadId

    config = {
        "configurable": {"thread_id": threadId},
    }

    # Invocar react_graph
    try:
        response = react_graph.invoke({"messages": [HumanMessage(content=message)]}, config)
        return {"message": response["messages"][-1].content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando el agente: {str(e)}")

# Punto de entrada principal
if __name__ == "__main__":
    import uvicorn

    # Obtener el puerto desde la variable de entorno
    port = int(os.getenv("PORT", 8080))

    # Servir la aplicación usando Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)
