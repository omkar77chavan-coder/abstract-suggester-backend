from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Dummy abstracts for suggestion
abstracts = [
    "A study on AI-based gesture recognition for assistive communication.",
    "Exploration of emotion-driven feedback in real-time web interfaces.",
    "Webcam-based attention tracking for intelligent content delivery.",
    "Personalized content suggestions using facial micro-expressions.",
    "Building adaptive UI based on eye-gaze patterns and stress detection."
]

@app.route('/')
def home():
    return "Abstract Suggester Backend is Running"

@app.route('/suggest', methods=['GET'])
def suggest_abstract():
    try:
        return jsonify({"suggestion": random.choice(abstracts)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)