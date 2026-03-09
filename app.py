from flask import Flask, request, Response, render_template
import ollama
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    def generate():

        stream = ollama.chat(
            model="llama3.2",
            messages=[{"role":"user","content":user_message}],
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            yield f"data:{content}\n\n"

    return Response(generate(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True)