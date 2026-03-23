# Basic AI Agent

Agente de IA conversacional construido con la API de OpenAI (GPT). Captura y organiza ideas por categoría, transcribe notas de voz, y recuerda el historial de conversación entre sesiones usando SQLite.

## Qué puede hacer

- **Guardar ideas** con categoría automática (`tech`, `negocio`, `personal`, `general`, `gimnasio`, `data science`)
- **Leer ideas guardadas**, filtrando por categoría o mostrando todas
- **Transcribir audio** — acepta archivos `.mp3`, `.wav`, `.m4a`, extrae la idea y la guarda
- **Recordar conversaciones anteriores** — el historial persiste en una base de datos local

## Requisitos

- Python 3.12+
- API key de OpenAI

## Instalación

**1. Clonar el repositorio**

```bash
git clone <url-del-repositorio>
cd basic_ai_agent
```

**2. Crear y activar el entorno virtual**

```bash
python -m venv venv
```

- Windows (PowerShell): `.\venv\Scripts\Activate.ps1`
- Windows (CMD): `venv\Scripts\activate.bat`
- Linux / macOS: `source venv/bin/activate`

**3. Instalar dependencias**

```bash
pip install -r requirements.txt
```

**4. Configurar la API key**

Crear un archivo `.env` en la raíz del proyecto:

```env
OPEN_AI_API_KEY=tu-api-key-de-openai
```

## Uso

Editar el bloque `__main__` en `agent.py` con los mensajes que quieras probar:

```python
if __name__ == "__main__":
    init_db()
    execute_agent("Tengo una idea para una app de finanzas personales")
    execute_agent("¿Qué ideas tengo guardadas de negocio?")
```

Luego ejecutar:

```bash
python agent.py
```

El agente imprime cada tool que invoca y su respuesta final:

```
[tool: save_idea → {'text': 'App de finanzas personales', 'category': 'negocio'}]

Agente: Guardé tu idea en la categoría 'negocio'.
```

## Estructura del proyecto

```
agent.py        # Loop principal del agente y definición de tools
database.py     # Persistencia en SQLite (ideas e historial)
audio.py        # Transcripción de audio con Whisper
requirements.txt
.env            # API key (no commitear)
ideas.db        # Generado automáticamente al correr init_db()
```

## Dependencias

| Paquete | Versión | Uso |
|---|---|---|
| `openai` | 2.28.0 | Cliente GPT + Whisper |
| `python-dotenv` | 1.2.2 | Variables de entorno |
| `pydantic` | 2.12.5 | Validación de datos |
