import os
from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

open_ai_api_key = os.getenv("OPEN_AI_API_KEY")

client = OpenAI(api_key=open_ai_api_key)

# Tool function

def save_idea(idea):
    with open("ideas.txt", "a") as file:
        file.write(idea + "\n")
    return "Idea guardada: '{idea}'"

def read_ideas():
    if not os.path.exists("ideas.txt"):
        return "No hay ideas guardadas."
    
    with open("ideas.txt", "r") as file:
        ideas = file.read().strip()
    
    return f"Ideas guardadas:\n{ideas}"

tool_list = {
    "save_idea": save_idea,
    "read_ideas": read_ideas
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "save_idea",
            "description": "Guarda una idea en un archivo de texto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "idea": {
                        "type": "string",
                        "description": "El texto de la idea a guardar"
                    }
                },
                "required": ["idea"]
            }
        } 
    },
    {
        "type": "function",
        "function": {
            "name": "read_ideas",
            "description": "Lee todas las ideas guardadas desde el archivo de texto.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

def execute_agent(message):
    messages = [
        {"role": "system", "content": "Eres un asistente de inteligencia artificial que ayuda a capturar y gestionar ideas."},
        {"role": "user", "content": message}
    ]

    finished = False

    while not finished:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message
        messages.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                if tool_name in tool_list:
                    result = tool_list[tool_name](**tool_args)
                else:
                    result = f"Herramienta desconocida: {tool_name}"

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })
        else:
            print("Agente: ", message.content)
            finished = True
        

# Example usage
""" execute_agent("Guarda esta idea: 'Crear una aplicación de lista de tareas'")
execute_agent("¿Cuáles son mis ideas guardadas?") """