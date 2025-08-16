from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Track last output used to avoid consecutive repeats
last_used = {}

# Variations dictionary
variations = {
    "UG": {
        "AI": [
            "Artificial Intelligence is reshaping everyday life with smarter decision-making systems...",
            "AI enables automation and problem-solving capabilities that enhance efficiency across industries...",
            "The field of AI combines algorithms and data to simulate human-like reasoning..."
        ],
        "Data Science": [
            "Data Science transforms raw data into meaningful insights through statistical methods...",
            "Data-driven decision making is becoming the backbone of competitive industries...",
            "Data Science integrates machine learning and analytics to forecast and optimize outcomes..."
        ],
        "ML": [
            "Machine Learning enables systems to learn from experience without explicit programming...",
            "ML algorithms are driving personalization, automation, and predictive analytics worldwide...",
            "With vast data, ML models improve decision-making accuracy and adaptability..."
        ],
        "CSE": [
            "Computer Science Engineering focuses on computational systems, programming, and problem-solving...",
            "CSE combines hardware knowledge with software expertise to create innovative solutions...",
            "Engineering in computing drives advancements in AI, networks, and system architecture..."
        ],
        "Cybersecurity": [
            "Cybersecurity safeguards digital systems from threats and vulnerabilities...",
            "With growing online activity, robust security frameworks are essential for safety...",
            "The field of cybersecurity ensures confidentiality, integrity, and availability of information..."
        ]
    },
    "PG": {
        "AI": [
            "Artificial Intelligence encompasses deep neural networks, probabilistic reasoning, and advanced cognitive architectures...",
            "The AI domain integrates reinforcement learning, knowledge representation, and explainable models for scalable solutions...",
            "Cutting-edge AI research leverages transfer learning and generative models for domain adaptation..."
        ],
        "Data Science": [
            "Advanced Data Science applies complex statistical models and big data frameworks to uncover hidden patterns...",
            "The discipline utilizes distributed computing, advanced visualization, and inferential statistics for robust insights...",
            "Techniques such as Bayesian modeling and feature engineering enhance predictive accuracy in large datasets..."
        ],
        "ML": [
            "Postgraduate-level ML incorporates hyperparameter tuning, ensemble methods, and deep learning architectures...",
            "Advanced ML applications involve unsupervised representation learning and semi-supervised algorithms...",
            "Optimization techniques, including gradient boosting and meta-learning, drive modern ML advancements..."
        ],
        "CSE": [
            "CSE at postgraduate level involves algorithm complexity analysis, distributed systems, and advanced compiler design...",
            "Research in CSE spans high-performance computing, quantum algorithms, and large-scale system integration...",
            "Advanced CSE integrates fault-tolerant systems, scalable databases, and microservices architecture..."
        ],
        "Cybersecurity": [
            "Postgraduate cybersecurity delves into cryptographic protocol design, penetration testing, and threat intelligence...",
            "The field emphasizes zero-trust architecture, blockchain-based security, and incident forensics...",
            "Advanced cyber defense strategies involve AI-driven anomaly detection and adaptive risk management..."
        ]
    }
}

# Simple responses for off-center gaze
simple_variations = {
    "AI": "AI helps machines make decisions and learn from data.",
    "Data Science": "Data Science helps understand data and make better choices.",
    "ML": "Machine Learning teaches computers to learn from examples.",
    "CSE": "Computer Science is about computers and how they work.",
    "Cybersecurity": "Cybersecurity keeps digital information safe."
}

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.json
    stream = data.get("stream")
    academic_level = data.get("academicLevel", "UG")
    gaze_status = data.get("gazeStatus", "centered")  # centered, off-center

    if not stream or not academic_level:
        return jsonify({"error": "Missing required fields"}), 400

    # Off-center gaze → simple output
    if gaze_status == "off-center":
        abstract = simple_variations.get(stream, "This field is important.")
        conclusion = f"In conclusion, {abstract.lower()}"
        return jsonify({"abstract": abstract, "conclusion": conclusion})

    # Centered gaze → pick from variations list (no repeat)
    options = variations[academic_level][stream]
    prev_choice = last_used.get((stream, academic_level, gaze_status))
    choices = [o for o in options if o != prev_choice]

    if not choices:
        choices = options  # if all used, reset

    abstract = random.choice(choices)
    last_used[(stream, academic_level, gaze_status)] = abstract

    conclusion = f"In conclusion, {abstract} This emphasizes the significance of {stream} in modern applications."

    return jsonify({"abstract": abstract, "conclusion": conclusion})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
