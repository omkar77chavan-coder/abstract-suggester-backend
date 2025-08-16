from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # allow frontend requests

# Store last used index to avoid consecutive repeats
last_used = {"Data Science": None, "Computer Science": None, "Electronics": None}

# ----------- DATASET -----------
DATA = {
    "UG": {
        "Data Science": [
            {
                "abstract": "Data Science integrates statistics, programming, and domain knowledge to extract insights from large datasets. This study explores foundational tools such as data cleaning, visualization, and simple predictive models to help students grasp how raw information is converted into actionable results.",
                "conclusion": "Data Science empowers beginners to handle messy data. Even simple models can reveal impactful insights."
            },
            {
                "abstract": "With increasing digital information, Data Science plays a key role in transforming data into meaningful knowledge. This work explains introductory techniques in Python, focusing on understanding distributions, correlations, and building small predictive tasks.",
                "conclusion": "Early exploration shows how even simple tools can drive decision-making. This builds confidence for deeper studies."
            },
            {
                "abstract": "Data Science combines statistics and computation to solve real-world problems. This project covers data preprocessing, visualization, and model interpretation while highlighting challenges like missing values and bias.",
                "conclusion": "Students gain an understanding of the data lifecycle. These foundations prepare them for advanced analytics."
            }
        ],
        "Computer Science": [
            {
                "abstract": "Computer Science provides the backbone of computing technologies. This project introduces students to programming fundamentals, data structures, and problem-solving techniques through practical applications in sorting, searching, and recursion.",
                "conclusion": "Students build algorithmic thinking. These skills are crucial for further exploration of computing."
            },
            {
                "abstract": "With rapid digitalization, Computer Science is central to everyday applications. This project highlights basic programming, object-oriented concepts, and small software projects to build real-world relevance.",
                "conclusion": "Learners understand computing logic. Early practice builds both confidence and curiosity."
            },
            {
                "abstract": "Computer Science is the study of computational systems and algorithms. This project explains how abstraction, algorithms, and simple design techniques can create useful tools for society.",
                "conclusion": "Students learn to bridge theory and practice. This balance defines effective computing solutions."
            }
        ],
        "Electronics": [
            {
                "abstract": "Electronics is the foundation of modern devices. This project teaches circuit theory, semiconductors, and practical hands-on circuit building to help students connect theoretical knowledge with real applications.",
                "conclusion": "Foundational circuit skills empower students to innovate. Early practice builds practical understanding."
            },
            {
                "abstract": "Electronics introduces learners to resistors, capacitors, and transistors. This project focuses on simple circuit design and measurement, highlighting their role in daily technologies like phones and computers.",
                "conclusion": "Understanding components develops confidence. Even simple circuits demonstrate how technology comes alive."
            },
            {
                "abstract": "The study of Electronics equips students with skills to analyze signals and build functional circuits. This work emphasizes prototyping, debugging, and experimentation.",
                "conclusion": "Students learn by building and testing. Hands-on practice bridges the gap between theory and reality."
            }
        ]
    },
    "PG": {
        "Data Science": [
            {
                "abstract": "In the postgraduate domain, Data Science moves beyond introductory analytics into the rigorous application of advanced statistical learning and machine intelligence to solve complex, real-world challenges. This work investigates ensemble-based predictive frameworks that combine decision trees, gradient boosting, and deep neural architectures to improve both accuracy and robustness of models. Special attention is given to feature selection strategies, dimensionality reduction techniques such as PCA and t-SNE, and the integration of heterogeneous data sources including text, images, and structured tabular records. Additionally, fairness, interpretability, and bias mitigation are evaluated to ensure ethical deployment. By using diverse case studies in healthcare diagnostics and financial risk analysis, the research demonstrates how scalable, transparent, and generalizable models can drive innovation in high-stakes fields.",
                "conclusion": "Postgraduate exploration shows how ensemble approaches enhance prediction reliability. Ethical rigor ensures models remain impactful in sensitive applications."
            },
            {
                "abstract": "At the graduate level, Data Science research emphasizes the convergence of high-dimensional statistical modeling, distributed computing, and deep representation learning. This study explores how Spark, TensorFlow, and cloud-based pipelines are orchestrated to process terabytes of real-world data while maintaining low latency. Experimental results evaluate convolutional and transformer-based architectures for natural language and image-driven applications, comparing their strengths under diverse constraints such as noise, class imbalance, and missing data. The work also presents strategies for explainability, using SHAP and LIME to illuminate decision-making processes of otherwise opaque black-box systems. By balancing mathematical rigor with computational scalability, the project highlights pathways for developing models that are not only accurate but also interpretable, trustworthy, and deployable across industries.",
                "conclusion": "Graduate research validates that scalability and explainability are complementary. The results chart a path for deploying robust AI systems responsibly."
            },
            {
                "abstract": "Modern Data Science at the postgraduate stage demands integration of advanced optimization techniques, probabilistic inference, and domain adaptation to address pressing challenges across sectors. This research undertakes a comprehensive study of Bayesian modeling, ensemble uncertainty quantification, and reinforcement learning frameworks to address problems of prediction under uncertainty. Experiments span across domains such as personalized medicine, climate modeling, and financial forecasting, leveraging both structured and unstructured data. Special focus is placed on data ethics, privacy-preserving computation, and federated learning models that enable secure collaboration across institutions. Beyond technical contributions, the study articulates how postgraduate-level inquiry must balance methodological depth with practical deployment to achieve societal impact.",
                "conclusion": "By fusing optimization with probabilistic reasoning, research produces adaptable and secure models. Findings underline the dual need for performance and responsible innovation."
            }
        ]
    }
}

# ----------- HELPER -----------
def choose_variant(level, stream):
    """Pick a random variation without repeating last one."""
    options = DATA[level][stream]
    prev = last_used.get(stream)
    choices = [i for i in range(len(options)) if i != prev]
    idx = random.choice(choices)
    last_used[stream] = idx
    return options[idx]

# ----------- ROUTE -----------
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    stream = data.get("stream")
    level = data.get("academicLevel", "UG")
    gaze = data.get("gazeStatus", "none")

    if level not in DATA: level = "UG"
    if stream not in DATA[level]: return jsonify({"error": "Invalid stream"}), 400

    # Gaze logic
    if gaze == "centered":
        choice = choose_variant(level, stream)
    else:
        choice = choose_variant("UG", stream)

    return jsonify({
        "abstract": choice["abstract"],
        "conclusion": choice["conclusion"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

