import os

import openai
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request, session
from flask_cors import CORS

from instructions.system_instructions import LLM_INSTRUCTIONS
from main import chatbot, init_chat

load_dotenv()
client = openai

app = Flask(__name__)
CORS(app)
app.secret_key = os.urandom(24)


@app.route("/")
def home():
    return {"Message": "Hello World"}


@app.route("/chat", methods=["POST"])
def chat():
    if "messages" not in session:
        session["messages"] = init_chat()
    data = request.get_json()
    user_message = data.get("message")
    session["messages"].append({"role": "user", "content": user_message})
    response = chatbot(messages=session["messages"])
    session["messages"] = response
    return render_template("messages.html", messages=session.get("messages"))
    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)
