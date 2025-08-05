from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # ✅ This enables cross-origin requests (solves CORS issue)

# Sample abstracts categorized by emotion (you can expand this)
suggestions_by_emotion = {
    "neutral": [
        "Exploration of emotion-driven feedback in real-time web interfaces.",
        "Webcam-based attention tracking for intelligent content delivery."
    ],
    "happy": [
        "Leveraging cheerful states to drive engaging abstract suggestions.",
        "Using joy to enhance creativity in content generation."
    ],
    "sad": [
        "Designing reflective UI for emotionally sensitive interactions.",
        "Using empathy-based AI models to generate content."
    ],
    "angry": [
        "Building adaptive feedback systems for high-stress environments.",
        "Channeling intensity to improve abstract phrasing."
    ],
    "surprised": [
        "Incorporating spontaneous user reactions in adaptive UI.",
        "Analyzing real-time facial responses for smart suggestions."
    ]
}

@app.route('/')
def home():
    return "✅ Abstract Suggester Backend is Running"

@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    try:
        data = request.get_json()
        text = data.get('text', '')
        emotion = data.get('emotion', 'neutral').lower()

        # Choose from emotion-based list or fallback
        if emotion in suggestions_by_emotion:
            suggestion = random.choice(suggestions_by_emotion[emotion])
        else:
            suggestion = random.choice(sum(suggestions_by_emotion.values(), []))  # Flatten all lists

        return jsonify({"suggested": suggestion})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    ...
    return jsonify({...})

@app.route('/stream_suggest', methods=['POST'])
def stream_suggest():
    return suggest_abstract()
if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)



