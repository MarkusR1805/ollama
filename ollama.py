import gradio as gr
import requests
import json
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

# Liste der verfügbaren Modelle
model_list = ["llama3.2:3b", "deepseek-coder-v2:16b"]

iface = gr.Interface(
    fn=generate_code,
    inputs=[
        gr.Textbox(lines=2, placeholder="Deine Frage/Anforderung hier...", label="Prompt"),
        gr.Dropdown(choices=model_list, value="llama3.2:3b", label="Modell auswählen")
    ],
    outputs="text",
    title="Arbeiten mit LLM-Modellen",
    description="Gib einen Prompt ein und wähle ein Modell:"
)

if __name__ == "__main__":
    iface.launch(server_port=8080, share=True, inbrowser=True)
