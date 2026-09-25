import os
from flask import Flask, render_template, request, jsonify
from agent import run_agent

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "JA Assure AI"
    })


@app.route("/chat", methods=["POST"])
def chat():

    try:
        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "Invalid JSON request"
            }), 400

        message = data.get("message", "").strip()

        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400

        response = run_agent(message)

        return jsonify({
            "response": str(response)
        })

    except Exception as error:

        print("Chat error:", error)

        return jsonify({
            "error": "Unable to process your request"
        }), 500


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "error": "Route not found"
    }), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
