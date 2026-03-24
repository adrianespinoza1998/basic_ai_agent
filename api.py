import os

from flask import Flask, request, jsonify
from agent import execute_agent, init_db
from dotenv import load_dotenv

app = Flask(__name__)
init_db()

load_dotenv()

base_url = "/api"

@app.route(f"{base_url}/agent", methods=["POST"])
def agent():
    data = request.json
    message = data.get("message")

    print(f"Mensaje recibido: {message}")

    if not message:
        return jsonify({"error": "No se proporcionó un mensaje"}), 400

    response = execute_agent(message)

    print(f"Respuesta del agente: {response}")

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(port = int(os.getenv('APP_PORT')), debug=True)