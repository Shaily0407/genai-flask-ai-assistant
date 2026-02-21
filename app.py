from flask import Flask, render_template, request, jsonify, session
from model import generate_response

app = Flask(__name__)

# 🔥 SECRET KEY MUST BE HERE
app.secret_key = "supersecretkey"


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    user_message = data.get("message")
    model_name = data.get("model")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Initialize session chat history
    if "chat_history" not in session:
        session["chat_history"] = []

    chat_history = session["chat_history"]

    try:
        response = generate_response(user_message, model_name, chat_history)

        # Save updated history back to session
        session["chat_history"] = response["updated_history"]

        return jsonify(response["data"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/clear", methods=["POST"])
def clear_chat():
    session.pop("chat_history", None)
    return jsonify({"message": "Chat cleared"})


if __name__ == "__main__":
    app.run(debug=True)