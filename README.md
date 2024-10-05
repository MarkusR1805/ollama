<div align="center">
    <h1>LLM with Ollama</h1>
</div>
<div align="center">Download and start Ollama https://ollama.com</div>
<div align="center"><h3>You need the Python library “Gradio”</h3></div>

```
pip install gradio
```
or
```
pip install --upgrade gradio
```
<br>

![Picture3](https://image.civitai.com/xG1nkqKTMzGDvpLrqFT7WA/39f5fc9b-9999-469f-b6ca-01d2771f6ff1/original=true,quality=90/04102024-macbook-m2_00015_.jpeg)

### Select your models, the following models are listed in the code:
<h3>MODELS = [“llama3.2:3b-instruct-q8_0”, “llama3.1:latest”, “llama3.2:3b”, “deepseek-coder-v2:16b”]</h3>
You must edit this line 11 if you use other models!
To install these models you have to execute the following command in the terminal:

```
ollama pull llama3.2:3b-instruct-q8_0
```
```
ollama pull llama3.1:latest
```
```
ollama pull llama3.2:3b
```
```
ollama pull deepseek-coder-v2:16b
```
Use the terminal to go to the directory where you installed the repository.<br>
Start the program in the terminal with:
```
python ollama.py
```