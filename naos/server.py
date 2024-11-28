from flask import Flask, request, jsonify
from langchain_core.messages import HumanMessage
import os
from flask_cors import CORS

from naos.main import react_graph


app = Flask(__name__)
CORS(app,origins="https://uiagentnaos-production.up.railway.app")

@app.route('/api/message', methods=['POST'])
def handle_message():
    # Verificar si el cuerpo de la solicitud tiene un JSON válido
    if not request.is_json:
        return jsonify({"error": "La petición debe tener un cuerpo JSON"}), 400
    
    # Obtener el JSON enviado
    data = request.get_json()
    
    # Verificar que el JSON contiene el campo 'message'
    if 'message' not in data:
        return jsonify({"error": "Falta el campo 'message' en el JSON"}), 400
    
    # Extraer el mensaje
    message = data['message']
    
    # Procesar el mensaje (puedes agregar tu lógica aquí)
    print(f"Mensaje recibido: {message}")
    
    # Responder con un mensaje de éxito
    return jsonify({"status": "success", "received_message": message}), 200

@app.route('/api/agent', methods=['POST'])
def handle_agent():
    data = request.get_json()

    if 'message' not in data:
        return jsonify({"error": "Falta el campo 'message' en el JSON"}), 400
    
    message = data['message']
    id = data['threadId']
   
    # Definir el thread_id threadId = "1234"
    threadId = id
    config = {
        "configurable": {"thread_id": threadId},
   
    }
    response = react_graph.invoke({"messages": [HumanMessage(content=message)]},config)
    return jsonify({"message":response["messages"][-1].content}), 200
    # Verificar si el cuerpo de la solicitud tiene un JSON válido
    


if __name__ == "__main__":
    from waitress import serve
    import os

    # Obtener el puerto de Railway (Railway establece la variable de entorno PORT)
    port = int(os.getenv("PORT", 8080))
    
    # Servir la aplicación usando Waitress
    serve(app, host="0.0.0.0", port=port)
