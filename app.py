from flask import Flask, request, jsonify
from flask_cors import CORS   # ✅ Added CORS
import random

app = Flask(__name__)
CORS(app)   # ✅ Enable CORS for all routes

# Track last used abstract to avoid repetition
last_used = {
    "UG": {s: None for s in ["AI","ML","CSE","Cybersecurity","Data Science","Electronics"]},
    "PG": {s: None for s in ["AI","ML","CSE","Cybersecurity","Data Science","Electronics"]}
}

# ----------- DATASET -----------
DATA = {
    "UG": {
        "AI": [
            {
                "abstract": "Artificial Intelligence introduces students to the basics of intelligent systems, covering problem solving, knowledge representation, and introductory machine learning. Through hands-on examples, learners explore how AI enables computers to perform tasks like classification and recommendation.",
                "conclusion": "AI empowers students to understand how machines mimic decision-making. Foundational exposure builds readiness for deeper exploration."
            },
            {
                "abstract": "This project introduces core AI concepts such as search algorithms, simple neural networks, and rule-based systems. Students gain experience in how machines can analyze environments and act with purpose.",
                "conclusion": "Students discover that AI combines logic and data. These basics build confidence for advanced research."
            },
            {
                "abstract": "Artificial Intelligence brings together computing, data, and logic to create systems that learn. This project highlights introductory supervised learning models, simple agents, and ethical considerations of AI in society.",
                "conclusion": "Students recognize AI’s real-world relevance while learning the importance of responsible development."
            }
        ],
        "ML": [
            {
                "abstract": "Machine Learning at the undergraduate level emphasizes supervised and unsupervised approaches. Students explore regression, clustering, and basic classification through datasets that reveal patterns in everyday problems.",
                "conclusion": "ML demonstrates how data patterns can guide predictions. Beginners grasp both power and limitations."
            },
            {
                "abstract": "This project introduces students to the steps of training, validating, and testing simple models. Practical exercises include predicting grades and grouping survey responses.",
                "conclusion": "Hands-on tasks demystify ML. Learners see how algorithms translate data into insights."
            },
            {
                "abstract": "Undergraduates study the principles of learning from examples. Through decision trees and k-means, they build an intuition of how algorithms identify relationships in datasets.",
                "conclusion": "ML builds analytical thinking and sparks curiosity about deeper AI techniques."
            }
        ],
        "CSE": [
            {
                "abstract": "Computer Science introduces learners to programming, algorithms, and data structures. This project focuses on recursion, sorting, and searching as tools for efficient problem solving.",
                "conclusion": "Students develop algorithmic thinking that forms the backbone of computing."
            },
            {
                "abstract": "Through small coding projects, undergraduates experience how computational logic can solve real-world tasks, from managing records to building small games.",
                "conclusion": "Learners gain early confidence. Practice equips them for complex software design."
            },
            {
                "abstract": "This project highlights abstraction, logic, and modular design in computing. Learners are guided to connect theory with applications in day-to-day computing systems.",
                "conclusion": "Students recognize how fundamental CS concepts power modern technologies."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "Cybersecurity introduces undergraduates to protecting systems from threats. This project covers basics of encryption, authentication, and password safety.",
                "conclusion": "Students learn the importance of security hygiene. Simple practices reduce real risks."
            },
            {
                "abstract": "Learners are introduced to common attack types such as phishing and malware, alongside basic countermeasures. Labs simulate simple exploits and defenses.",
                "conclusion": "By practicing security, students appreciate the balance of risk and protection."
            },
            {
                "abstract": "This project explains core cybersecurity principles: confidentiality, integrity, and availability. It shows how these apply to securing personal devices and networks.",
                "conclusion": "Learners build awareness of digital safety, an essential modern skill."
            }
        ],
        "Data Science": [
            {
                "abstract": "Data Science integrates statistics, programming, and domain knowledge to extract insights from large datasets. This study explores foundational tools such as data cleaning, visualization, and predictive models.",
                "conclusion": "Students understand how messy data becomes actionable. Foundations prepare them for advanced analytics."
            },
            {
                "abstract": "With increasing digital information, Data Science plays a key role in transforming data into knowledge. This work focuses on introductory Python techniques for distribution and correlation analysis.",
                "conclusion": "Learners see how simple tools enable impactful decision-making."
            },
            {
                "abstract": "This project introduces students to the data lifecycle: collection, preprocessing, visualization, and simple interpretation. Challenges like bias and missing values are discussed.",
                "conclusion": "Awareness of pitfalls prepares students for responsible analysis."
            }
        ],
        "Electronics": [
            {
                "abstract": "Electronics teaches circuit basics, semiconductors, and measurements. Learners build hands-on projects to connect theory with devices around them.",
                "conclusion": "Simple circuits demonstrate how theory powers technology."
            },
            {
                "abstract": "Students explore resistors, capacitors, and transistors. Projects highlight their role in daily technologies like computers and phones.",
                "conclusion": "Hands-on work helps learners appreciate the building blocks of electronics."
            },
            {
                "abstract": "The study covers signals, circuit analysis, and prototyping. Learners practice building, debugging, and testing designs.",
                "conclusion": "Practical skills bridge theory and application."
            }
        ]
    },

    # PG dataset same as before (omitted here for brevity, keep your version) …
    "PG": {  # Keep your original PG dataset unchanged
        # ... (AI, ML, CSE, Cybersecurity, Data Science, Electronics)
    }
}

# ----------- SIMPLER FALLBACK for Off-Center Gaze -----------
SIMPLE_DATA = {
    "abstract": "A quick overview of the chosen field is provided with simple explanations.",
    "conclusion": "This short conclusion summarizes the key idea in a straightforward way."
}

# ----------- HELPER -----------
def choose_variant(level, stream):
    """Pick random variant without consecutive repeat"""
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
    stream = data.get("stream")
    level = data.get("academicLevel", "UG")
    gaze = data.get("gazeStatus", "none")

    if level not in DATA:
        level = "UG"
    if stream not in DATA[level]:
        return jsonify({"error": "Invalid stream"}), 400

    if gaze == "centered":
        choice = choose_variant(level, stream)
    elif gaze == "off-center":  # left/right head movement
        choice = SIMPLE_DATA
    else:
        choice = choose_variant(level, stream)

    return jsonify(choice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
