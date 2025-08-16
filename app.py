from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Allow requests from anywhere (change "*" to your Odoo domain if needed)
CORS(app, resources={r"/*": {"origins": "*"}})

# Hardcoded UG and PG variations
variations = {
    "UG": {
        "AI": ("AI enables automation and problem-solving capabilities that enhance efficiency across industries...",
               "In conclusion, AI enables automation and problem-solving capabilities that enhance efficiency across industries... This emphasizes the significance of AI in modern applications."),
        "Data Science": ("Data Science involves extracting knowledge and insights from structured and unstructured data...",
                         "In conclusion, Data Science enables evidence-based decision-making and innovation across domains.")
        # Add all remaining UG streams...
    },
    "PG": {
        "AI": ("Advanced AI systems leverage deep learning and reinforcement learning to solve complex problems...",
               "In conclusion, advanced AI techniques expand possibilities in automation, decision-making, and predictive analytics."),
        "Data Science": ("Techniques such as Bayesian modeling and feature engineering enhance predictive accuracy in large datasets...",
                         "In conclusion, Techniques such as Bayesian modeling and feature engineering enhance predictive accuracy in large datasets... This emphasizes the significance of Data Science in modern applications.")
        # Add all remaining PG streams...
    }
}

@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json(force=True) or {}
        name = data.get("name", "")
        age = data.get("age", "")
        gender = data.get("gender", "")
        stream = data.get("stream", "")
        academic_level = data.get("academicLevel", "")
        gaze_status = data.get("gazeStatus", "")
        abstract_text = data.get("abstract", "")

        if not (name and age and gender and stream and academic_level and abstract_text):
            return jsonify({"error": "missing_fields"}), 400

        stream_variations = variations.get(academic_level.upper(), {})
        if stream in stream_variations:
            abstract, conclusion = stream_variations[stream]
        else:
            abstract = f"Default abstract for {stream} at {academic_level} level."
            conclusion = f"Default conclusion for {stream} at {academic_level} level."

        return jsonify({"abstract": abstract, "conclusion": conclusion}), 200
    except Exception as e:
        return jsonify({"error": "server_error", "detail": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
