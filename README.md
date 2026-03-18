# Basic AI Agent

Agente de IA básico que utiliza la API de OpenAI para mantener conversaciones interactivas por consola.

## Requisitos

- Python 3.12+
- Una API key de OpenAI

## Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd basic_ai_agent
   ```

2. **Crear el entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - Linux / macOS:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar las dependencias**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configurar las variables de entorno**

   Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

   ```env
   OPEN_AI_API_KEY=tu-api-key-de-openai
   ```

## Ejecución

```bash
python main.py
```

Escribe tus mensajes en la consola y el agente responderá. Para salir, escribe `salir`, `exit` o `quit`.
