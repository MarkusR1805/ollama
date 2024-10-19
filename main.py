import gradio as gr
import requests
import json
import subprocess
import torch

# Überprüfen, ob MPS verfügbar ist
if torch.backends.mps.is_available():
    device = torch.device("mps")
    print("MPS wird verwendet\n")
elif torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA wird verwendet\n")
else:
    device = torch.device('cpu')
    print("CPU wird verwendet\n")

def get_ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            # Verarbeiten der Ausgabe
            lines = result.stdout.strip().split('\n')
            model_list = [line.split()[0] for line in lines if line]
            return model_list
        else:
            print(f"Error: {result.stderr}")
            return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {str(e)}")
        return []

def generate_code(prompt, model):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt
    }
    try:
        response = requests.post(url, json=data, stream=True)

        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    data = json.loads(decoded_line)
                    if 'response' in data:
                        full_response += data['response']
                    if data.get('done', False):
                        break
            return full_response
        else:
            return f"Error: {response.status_code}, {response.text}"
    except Exception as e:
        return f"Ein Fehler ist aufgetreten: {str(e)}"

# Liste der verfügbaren Modelle dynamisch laden
model_list = get_ollama_models()

iface = gr.Interface(
    fn=generate_code,
    inputs=[
        gr.Textbox(lines=2, placeholder="Deine Frage/Anforderung hier...", label="Prompt"),
        gr.Dropdown(choices=model_list, value=model_list[0] if model_list else "", label="Modell auswählen")
    ],
    outputs="text",
    title="Wähle Dein LLM-Modell und nutze sie offline!",
    description="Gib einen Prompt ein und wähle ein Modell:"
)

if __name__ == "__main__":
    iface.launch(server_port=8080, share=True, inbrowser=True)