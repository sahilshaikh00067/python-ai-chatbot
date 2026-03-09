from flask import Flask, request, Response, render_template
import ollama
import os

app = Flask(__name__)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Chat API
@app.route("/chat", methods=["POST"])
def chat():

    user_message = request.json["message"]

    def generate():

        stream = ollama.chat(
            model="llama3.2",
            messages=[{"role": "user", "content": user_message}],
            stream=True
        )

        for chunk in stream:
            if "message" in chunk:
                content = chunk["message"]["content"]
                yield f"data:{content}\n\n"

    return Response(generate(), mimetype="text/event-stream")


# Run server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
