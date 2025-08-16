from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ------------ SAMPLE VARIANTS ------------
VARIANTS = {
    "UG": {
        "AI": {
            "abstract": "As an undergraduate AI project, this abstract explores core algorithms and foundational methods.",
            "conclusion": "The study concludes with insights suitable for undergraduate learning and experimentation."
        },
        "ML": {
            "abstract": "Undergraduate research in ML often emphasizes supervised techniques and basic model evaluation.",
            "conclusion": "The project highlights the role of ML in building core applied understanding."
        }
    },
    "PG": {
        "AI": {
            "abstract": "Postgraduate-level AI work focuses on deep learning, optimization, and domain-specific applications.",
            "conclusion": "The conclusion underlines AI’s transformative role at an advanced research level."
        },
        "ML": {
            "abstract": "Graduate-level ML research expands to reinforcement learning, generative models, and scalability.",
            "conclusion": "This study concludes with novel ML applications and directions for future exploration."
        }
    }
}

# ------------ ROUTE ------------
@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json()
        name = data.get("name", "")
        age = data.get("age", "")
        gender = data.get("gender", "")
        level = data.get("academicLevel", "")
        stream = data.get("stream", "")
        abstract_input = data.get("abstractInput", "")
        gaze = data.get("gazeStatus", "manual")

        # ✅ Validation
        if level not in ["UG", "PG"]:
            return jsonify({"error": "Invalid academic level"}), 400
        if not stream:
            return jsonify({"error": "Stream is required"}), 400
        if not abstract_input or len(abstract_input.split()) < 15:
            return jsonify({"error": "Abstract must be at least 15 words"}), 400

        # ✅ Gaze logic
        if gaze == "centered":
            choice = VARIANTS.get(level, {}).get(stream, {
                "abstract": f"{abstract_input}\n\nThis abstract was expanded and refined for clarity.",
                "conclusion": "Based on a stable gaze, the conclusion is precise and complete."
            })
        elif gaze == "off-center":
            choice = {
                "abstract": "A short abstract was detected, but details were incomplete.",
                "conclusion": "This conclusion is shortened due to off-center input."
            }
        elif gaze == "partial":
            choice = {
                "abstract": "A partially written abstract was received.",
                "conclusion": "This conclusion remains unfinished due to partial details."
            }
        else:
            choice = {
                "abstract": f"{abstract_input}\n\nThis is a generated abstract draft.",
                "conclusion": "Generated conclusion based on manual submission."
            }

        return jsonify(choice)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
