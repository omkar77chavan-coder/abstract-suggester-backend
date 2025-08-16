from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Track last used abstract to avoid repetition
last_used = {
    "UG": {s: None for s in ["AI", "ML", "CSE", "Cybersecurity", "Data Science", "Electronics"]},
    "PG": {s: None for s in ["AI", "ML", "CSE", "Cybersecurity", "Data Science", "Electronics"]}
}

# ----------- DATASET -----------
DATA = {
    "UG": {
        "AI": [
            {"abstract": "Artificial Intelligence introduces students to the basics of intelligent systems, covering problem solving, knowledge representation, and introductory machine learning. Through hands-on examples, learners explore how AI enables computers to perform tasks like classification and recommendation.",
             "conclusion": "AI empowers students to understand how machines mimic decision-making. Foundational exposure builds readiness for deeper exploration."},
            {"abstract": "This project introduces core AI concepts such as search algorithms, simple neural networks, and rule-based systems. Students gain experience in how machines can analyze environments and act with purpose.",
             "conclusion": "Students discover that AI combines logic and data. These basics build confidence for advanced research."},
            {"abstract": "Artificial Intelligence brings together computing, data, and logic to create systems that learn. This project highlights introductory supervised learning models, simple agents, and ethical considerations of AI in society.",
             "conclusion": "Students recognize AI’s real-world relevance while learning the importance of responsible development."}
        ],
        "ML": [
            {"abstract": "Machine Learning at the undergraduate level emphasizes supervised and unsupervised approaches. Students explore regression, clustering, and basic classification through datasets that reveal patterns in everyday problems.",
             "conclusion": "ML demonstrates how data patterns can guide predictions. Beginners grasp both power and limitations."},
            {"abstract": "This project introduces students to the steps of training, validating, and testing simple models. Practical exercises include predicting grades and grouping survey responses.",
             "conclusion": "Hands-on tasks demystify ML. Learners see how algorithms translate data into insights."},
            {"abstract": "Undergraduates study the principles of learning from examples. Through decision trees and k-means, they build an intuition of how algorithms identify relationships in datasets.",
             "conclusion": "ML builds analytical thinking and sparks curiosity about deeper AI techniques."}
        ],
        # ... (CSE, Cybersecurity, Data Science, Electronics same as before)
    },
    "PG": {
        "AI": [
            {"abstract": "Postgraduate research in Artificial Intelligence examines advanced learning paradigms such as deep neural architectures, reinforcement learning, and probabilistic reasoning. This work explores not only algorithmic improvements but also interpretability, trust, and fairness in AI deployment. By bridging symbolic and sub-symbolic approaches, the research highlights how hybrid models address real-world complexity across domains such as healthcare, finance, and autonomous systems.",
             "conclusion": "AI at the postgraduate level advances both theoretical frameworks and ethical safeguards, ensuring systems remain powerful, transparent, and accountable."},
            {"abstract": "This project investigates frontier AI techniques including generative modeling, transfer learning, and human-AI collaboration. Emphasis is placed on scaling algorithms for large datasets while reducing computational costs through model compression and distributed optimization. Applications extend to drug discovery, language technologies, and personalized recommendations, with careful consideration of ethical risks like algorithmic bias.",
             "conclusion": "Postgraduate AI work balances innovation with responsibility, positioning AI as both a scientific frontier and a societal force."},
            {"abstract": "Research at this level critically examines the limits of AI generalization and robustness. Experimental studies assess adversarial resilience, domain adaptation, and the integration of symbolic reasoning for explainable systems. Insights from cognitive science inspire architectures that learn more human-like representations while maintaining mathematical rigor and computational feasibility.",
             "conclusion": "Such inquiry defines AI as a discipline that is simultaneously technical, scientific, and profoundly human-centered."}
        ],
        # ... (ML, CSE, Cybersecurity, Data Science, Electronics same as before)
    }
}

# ----------- SIMPLE & PARTIAL FALLBACKS -----------
SIMPLE_DATA = {
    "abstract": "A quick overview of the chosen field is provided with simple explanations.",
    "conclusion": "This short conclusion summarizes the key idea in a straightforward way."
}

PARTIAL_DATA = {
    "AI": {"abstract": "An incomplete attempt at explaining AI concepts.", "conclusion": "The conclusion trails off, missing clarity."},
    "ML": {"abstract": "Partial notes on machine learning with missing pieces.", "conclusion": "The conclusion remains unfinished."},
    "CSE": {"abstract": "Computer Science fundamentals described in fragments.", "conclusion": "The explanation cuts short midway."},
    "Cybersecurity": {"abstract": "Security principles outlined, but incomplete.", "conclusion": "The conclusion is abruptly halted."},
    "Data Science": {"abstract": "Data Science concepts started but not fully expressed.", "conclusion": "The conclusion is left open-ended."},
    "Electronics": {"abstract": "Only partial details of circuits and signals provided.", "conclusion": "Conclusion was cut before completion."}
}

# ----------- HELPERS -----------
def normalize_stream(stream):
    if not stream:
        return None
    s = stream.strip().lower()
    mapping = {
        "ai": "AI", "artificial intelligence": "AI",
        "ml": "ML", "machine learning": "ML",
        "cse": "CSE", "computer science": "CSE", "cs": "CSE",
        "cybersecurity": "Cybersecurity", "cyber": "Cybersecurity",
        "data science": "Data Science", "ds": "Data Science",
        "electronics": "Electronics", "ece": "Electronics"
    }
    return mapping.get(s, None)

def choose_variant(level, stream):
    options = DATA[level][stream]
    prev = last_used[level][stream]
    choices = [i for i in range(len(options)) if i != prev]
    idx = random.choice(choices)
    last_used[level][stream] = idx
    return options[idx]

# ----------- ROUTE -----------
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    stream_raw = data.get("stream")
    level = data.get("academicLevel", "UG")
    gaze = data.get("gazeStatus", "none")

    stream = normalize_stream(stream_raw)
    if level not in DATA:
        level = "UG"
    if not stream or stream not in DATA[level]:
        return jsonify({"error": "Invalid stream"}), 400

    if gaze == "centered":
        choice = choose_variant(level, stream)
    elif gaze == "off-center":
        choice = SIMPLE_DATA
    elif gaze == "partial":
        choice = PARTIAL_DATA.get(stream, SIMPLE_DATA)
    else:
        choice = choose_variant(level, stream)

    return jsonify(choice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
