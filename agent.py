from datetime import datetime

from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from audio import transcribe_audio
from database import init_db, save_idea, read_ideas, save_message, read_messages
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

tools = [
    {
        "type": "function",
        "function": {
            "name": "save_idea",
            "description": "Guarda una idea en la base de datos. Úsala cuando el usuario quiera registrar una idea.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {"type": "string", "description": "El texto de la idea"},
                    "category": {
                        "type": "string",
                        "description": "Categoría de la idea: 'tech', 'negocio', 'personal', 'general'",
                        "enum": ["tech", "negocio", "personal", "general", "gimnasio", "data science"]
                    }
                },
                "required": ["text"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_ideas",
            "description": "Lee las ideas guardadas. Puede filtrar por categoría o mostrar todas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Filtrar por categoría. Si no se especifica, devuelve todas.",
                        "enum": ["tech", "negocio", "personal", "general", "gimnasio", "data science"]
                    }
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "transcribe_audio",
            "description": "Transcribe un archivo de audio a texto. Úsala cuando el usuario pase una nota de voz.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_route": {
                        "type": "string",
                        "description": "Ruta al archivo de audio (.mp3, .wav, .m4a)"
                    }
                },
                "required": ["file_route"]
            }
        }
    }
]

available_tools = {
    "save_idea": save_idea,
    "read_ideas": read_ideas,
    "transcribe_audio": transcribe_audio
}

def execute_agent(message):
    old_messages = read_messages("default")

    print("\nHistorial de mensajes anteriores:", old_messages)

    messages = [
        {
            "role": "system",
            "content": """Eres un asistente personal que ayuda a capturar y organizar ideas.
            Cuando el usuario mencione un archivo de audio, primero transcríbelo,
            luego extrae la idea principal y guárdala en la categoría más apropiada.
            Siempre confirma lo que hiciste de forma breve."""
        },
        *old_messages,
    ]

    save_message("default", "user", datetime.now(), message)

    while True:
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=messages,
            tools=tools,
        )

        message = response.choices[0].message

        if message.tool_calls:
            messages.append(message)

            save_message("default", "assistant", datetime.now(), message.content, tool_calls=message.tool_calls)

            for tool_call in message.tool_calls:
                name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                print(f"  [tool: {name} → {arguments}]")

                result = available_tools[name](**arguments)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

                save_message("default", "tool", datetime.now(), result, tool_call_id=tool_call.id)
        else:
            print(f"\nAgente: {message.content}\n")
            save_message("default", "assistant", datetime.now(), message.content)
            break

if __name__ == "__main__":
    init_db()

    execute_agent('Mi nombre es Adrian')
    execute_agent('¿Cual es mi nombre?')
    
    print(read_messages("default"))