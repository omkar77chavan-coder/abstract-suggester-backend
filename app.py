
from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Dummy logic for improving text (mocked suggestion)
def improve_abstract(text, emotion):
    return f"Refined for emotion '{emotion}': {text[::-1]}"

@app.route('/')
def home():
    return "Abstract Suggester Backend is Running"

@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    try:
        data = request.get_json()
        text = data.get("text", "")
        emotion = data.get("emotion", "neutral")

        suggestion = improve_abstract(text, emotion)

        return jsonify({"suggested": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
