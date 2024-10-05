import gradio as gr
import requests
import json
import webbrowser
from threading import Timer

# Ollama API Endpunkt (ggf. anpassen)
OLAMA_API_URL = "http://localhost:11434/api/generate"

# Verfügbare Ollama-Modelle, kann man ändern/erweitern
MODELS = ["llama3.2:3b-instruct-q8_0", "llama3.1:latest", "llama3.2:3b", "deepseek-coder-v2:16b"]

def generate_text(prompt, model):
    """Generates text using the specified Ollama model and prompt."""

    headers = {"Content-Type": "application/json"}  # Set content type for JSON
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False  
    }

    try:
        response = requests.post(OLAMA_API_URL, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for bad status codes

        response_data = response.json()
        return response_data.get("response", "No response received") 

    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

# Create the Gradio interface
iface = gr.Interface(
    fn=generate_text,
    inputs=[
        gr.Textbox(lines=4, placeholder="Geben Sie hier Ihre Eingabe ein..."),
        gr.Dropdown(choices=MODELS, label="Modell auswählen")
    ],
    outputs="text",
    title="Ollama AI Interface",
    description="Generiere Text mit Ollama AI Modelle"
)

# Funktion um den Browser zu öffnen
def open_browser():
    webbrowser.open_new("http://127.0.0.1:7860")

# Start der Gradio-Anwendung
if __name__ == "__main__":
    Timer(1, open_browser).start()  
    iface.launch(share=True)