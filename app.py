from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Sample abstracts for testing
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

@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    try:
        data = request.get_json()
        text = data.get('text', '')
        emotion = data.get('emotion', '')
        suggestion = f"Refined for emotion '{emotion}': {text[::-1]}"
        return jsonify({"suggested": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)



