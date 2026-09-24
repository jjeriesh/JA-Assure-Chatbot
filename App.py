from flask import Flask, render_template_string, request, jsonify
from agent import run_agent

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>JA Assure - AI Chatbot</title>

    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #111827;
            color: white;
        }

        .container {
            width: 700px;
            max-width: 90%;
            margin: 60px auto;
            background: #1f2937;
            border-radius: 15px;
            padding: 25px;
            box-shadow: 0 0 30px rgba(0,0,0,0.3);
        }

        h1 {
            text-align: center;
        }

        #chat {
            height: 400px;
            overflow-y: auto;
            background: #111827;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
        }

        .message {
            padding: 12px;
            margin: 10px 0;
            border-radius: 10px;
        }

        .user {
            background: #2563eb;
            text-align: right;
        }

        .bot {
            background: #374151;
        }

        .input-area {
            display: flex;
            gap: 10px;
        }

        input {
            flex: 1;
            padding: 14px;
            border-radius: 8px;
            border: none;
            outline: none;
            font-size: 16px;
        }

        button {
            padding: 14px 20px;
            background: #f97316;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
        }

        button:hover {
            background: #ea580c;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>🤖 JA Assure Chatbot</h1>

    <div id="chat"></div>

    <div class="input-area">

        <input
            type="text"
            id="message"
            placeholder="Ask anything..."
            onkeypress="handleEnter(event)"
        >

        <button onclick="sendMessage()">Send</button>

    </div>

</div>

<script>

function handleEnter(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}

function addMessage(message, type) {

    const chat = document.getElementById("chat");

    const div = document.createElement("div");

    div.className = "message " + type;

    div.innerText = message;

    chat.appendChild(div);

    chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {

    const input = document.getElementById("message");

    const message = input.value.trim();

    if (!message) {
        return;
    }

    addMessage(message, "user");

    input.value = "";

    addMessage("Thinking...", "bot");

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })

        });

        const data = await response.json();

        const chat = document.getElementById("chat");

        chat.removeChild(chat.lastChild);

        addMessage(data.response, "bot");

    } catch (error) {

        const chat = document.getElementById("chat");

        chat.removeChild(chat.lastChild);

        addMessage("Something went wrong. Please try again.", "bot");

    }
}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()

    user_message = data.get("message", "")

    if not user_message:
        return jsonify({
            "response": "Please enter a message."
        })

    response = run_agent(user_message)

    return jsonify({
        "response": response
    })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )
