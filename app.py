from flask import Flask, render_template, request
import json
import requests 
from langchain_community.llms import Ollama


# NOTE: ollama must be running for this to work, start the ollama app or run `ollama serve`
model = "llama2" 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

# ollama request 
def chat(messages):
    r = requests.post(
        "http://127.0.0.1:11434/api/chat",
        json={"model": model, "messages": messages, "stream": True},
    )
    r.raise_for_status()
    output = ""

    for line in r.iter_lines():
        body = json.loads(line)
        if "error" in body:
            raise Exception(body["error"])
        if body.get("done") is False:
            message = body.get("message", "")
            content = message.get("content", "")
            output += content
            # the response streams one token at a time, print that as we receive it
            print(content, end="", flush=True)

        if body.get("done", False):
            message["content"] = output
            return message
        
def chat_chain(messages):
    print(messages)
    llm = Ollama(model=model)
    res = llm.invoke(messages)
    print(res)
    return res

@app.route('/chat', methods=['POST'])
def chat_route():
    message = request.form.get('message')
    response = chat_chain(message)
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 