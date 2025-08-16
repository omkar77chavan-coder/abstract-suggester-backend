from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Variation storage tracker
last_used = {"UG": {}, "PG": {}}

# Abstracts data
abstracts_data = {
    "UG": {
        "AI": [
            "AI enables automation and problem-solving capabilities that enhance efficiency across industries...",
            "Artificial Intelligence empowers systems to learn from data, improving decision-making processes...",
            "AI supports innovative solutions that transform user experiences and streamline operations...",
            "With AI, machines can simulate human intelligence for tasks like vision, speech, and decision-making...",
            "AI bridges technology and creativity, enabling personalized and adaptive systems..."
        ],
        "Data Science": [
            "Data Science extracts meaningful patterns from large datasets to support informed decision-making...",
            "By combining statistics and computing, Data Science transforms raw data into valuable insights...",
            "Data Science leverages machine learning and analytics to drive innovation across domains...",
            "The role of Data Science is pivotal in predicting trends and optimizing processes...",
            "Data Science empowers businesses to unlock hidden opportunities within complex data..."
        ],
        "ML": [
            "Machine Learning enables systems to learn patterns from data without explicit programming...",
            "ML algorithms adapt to data changes, offering dynamic and accurate predictions...",
            "Through ML, automation reaches new heights in fields like healthcare and finance...",
            "ML applications span from recommendation engines to fraud detection systems...",
            "With ML, machines continuously improve performance over time..."
        ],
        "CSE": [
            "Computer Science and Engineering underpins the design and development of cutting-edge technologies...",
            "CSE integrates theory and practice to solve computational problems efficiently...",
            "From algorithms to architecture, CSE drives innovation in every tech domain...",
            "CSE enables the creation of secure, scalable, and high-performance systems...",
            "The discipline of CSE shapes the foundation of modern computing..."
        ],
        "Cybersecurity": [
            "Cybersecurity safeguards systems and data against evolving digital threats...",
            "The field focuses on preventing unauthorized access and ensuring data integrity...",
            "Cybersecurity combines technology and strategy to protect sensitive information...",
            "From encryption to monitoring, Cybersecurity defends against cyber risks...",
            "Cybersecurity awareness is vital to maintaining trust in digital interactions..."
        ]
    },
    "PG": {
        "AI": [
            "Advanced AI employs deep neural architectures and reinforcement learning to solve domain-specific challenges with precision...",
            "AI research integrates symbolic reasoning with machine learning for explainable and robust solutions...",
            "Generative AI models transform creative industries by producing original, high-quality content from minimal input...",
            "AI optimization techniques enhance scalability and efficiency in high-dimensional problem spaces...",
            "Cutting-edge AI integrates multimodal data processing for comprehensive situational awareness..."
        ],
        "Data Science": [
            "Techniques such as Bayesian modeling and feature engineering enhance predictive accuracy in large datasets...",
            "Data Science pipelines incorporate ETL, distributed computing, and statistical learning for robust analytics...",
            "Advanced clustering and dimensionality reduction techniques reveal hidden patterns in complex data...",
            "Big Data ecosystems integrate Spark, Hadoop, and cloud platforms for scalable analytics...",
            "Domain-specific Data Science models leverage contextual knowledge for superior insights..."
        ],
        "ML": [
            "State-of-the-art ML models utilize ensemble learning and meta-learning for superior generalization...",
            "ML research explores explainability to enhance trust in black-box predictive systems...",
            "Transfer learning accelerates model performance in low-data regimes across specialized domains...",
            "Federated learning frameworks ensure privacy-preserving collaborative model training...",
            "Hyperparameter optimization techniques refine ML models for peak accuracy..."
        ],
        "CSE": [
            "Advanced CSE encompasses parallel computing, algorithmic complexity, and hardware-software co-design...",
            "CSE research integrates blockchain architectures for secure distributed systems...",
            "Edge computing solutions in CSE minimize latency for real-time applications...",
            "Compiler optimization techniques enhance performance in domain-specific computing tasks...",
            "CSE methodologies drive advancements in quantum-safe cryptographic protocols..."
        ],
        "Cybersecurity": [
            "Advanced Cybersecurity integrates AI-driven anomaly detection with zero-trust architectures...",
            "Post-quantum cryptography research addresses future-proof secure communication...",
            "Threat intelligence platforms aggregate and analyze multi-source cyber threat data...",
            "Blockchain-based identity management enhances user privacy and security...",
            "Cybersecurity automation frameworks streamline vulnerability detection and remediation..."
        ]
    }
}

@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    stream = data.get("stream")
    academic_level = data.get("academicLevel")
    gaze_status = data.get("gazeStatus", "centered")

    if not stream or not academic_level:
        return jsonify({"error": "Missing required fields"}), 400

    variations = abstracts_data[academic_level][stream]

    # Gaze logic
    if gaze_status == "off-center":
        selected = variations[0]  # simpler/shorter version
    else:
        # Ensure no consecutive repetition
        prev_index = last_used[academic_level].get(stream, -1)
        idx_choices = [i for i in range(len(variations)) if i != prev_index]
        idx = random.choice(idx_choices)
        selected = variations[idx]
        last_used[academic_level][stream] = idx

    abstract = selected
    conclusion = f"In conclusion, {selected} This emphasizes the significance of {stream} in modern applications."

    return jsonify({
        "abstract": abstract,
        "conclusion": conclusion
    })

if __name__ == '__main__':
    app.run(debug=True)
