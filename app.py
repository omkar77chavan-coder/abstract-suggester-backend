from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re

app = Flask(__name__)
# Allow everything (you can tighten to your domain later)
CORS(app, resources={r"/suggest": {"origins": "*"}})

MIN_WORDS = 15

# -----------------------
# FULL INLINE DATASET
# -----------------------
DATASET = {
    "UG": {
        "AI": [
            {
                "abstract": "This project introduces undergraduate students to artificial intelligence concepts with emphasis on search algorithms, knowledge representation, and reasoning under uncertainty. The abstract highlights applied problem-solving through hands-on experiments and simulations that demystify core AI behavior.",
                "conclusion": "Undergraduate exposure to AI cultivates curiosity and strong foundations, positioning students to pursue advanced ML, NLP, and robotics with confidence."
            },
            {
                "abstract": "An undergraduate exploration of AI emphasizes supervised and unsupervised learning. Through simplified models, students engage with classification, clustering, and reinforcement examples that make artificial intelligence tangible and ethically aware.",
                "conclusion": "Early AI education delivers technical fluency and a broader perspective on automation, data responsibility, and human-centered system design."
            },
            {
                "abstract": "This work introduces neural networks at an undergraduate level, covering perceptrons and basic backpropagation. Students experiment with small datasets to understand how feature signals propagate and how loss functions guide learning.",
                "conclusion": "Even basic neural exposure equips learners with analysis skills and the confidence to extend into deep architectures and real-world deployments."
            }
        ],
        "Data Science": [
            {
                "abstract": "This undergraduate project explores the full data pipeline—collection, cleaning, visualization, and simple modeling. Emphasis is placed on descriptive statistics, reproducibility, and communicating findings using clear plots and concise narratives.",
                "conclusion": "Foundational data science builds statistical literacy and research readiness, enabling informed decisions across academic and industry contexts."
            },
            {
                "abstract": "Students analyze open datasets using Python libraries such as Pandas and Matplotlib. Hands-on exercises translate concepts like distribution, correlation, and sampling into practice, reinforcing critical thinking with code.",
                "conclusion": "Guided practice reveals how structured analysis transforms raw data into evidence for policy, product design, and scientific inquiry."
            },
            {
                "abstract": "An introductory module demonstrates regression and basic classification for common undergraduate problems. Learners evaluate models with hold-out validation and interpret errors to improve data strategy.",
                "conclusion": "Early application bridges theory with messy real-world data, helping students reason about uncertainty and model limits."
            }
        ]
    },
    "PG": {
        "AI": [
            {
                "abstract": (
                    "This postgraduate research investigates hybrid artificial intelligence systems that integrate symbolic reasoning with deep learning architectures. "
                    "Multi-modal pipelines combine language, vision, and knowledge graphs to address explainability, generalization, and transfer learning. "
                    "The study advances interpretable attention mechanisms and causal probes, enabling diagnosis of model decisions in safety-critical domains. "
                    "Applications span clinical decision support, cognitive robotics, and large-scale retrieval, with rigorous ablation studies and uncertainty calibration."
                ),
                "conclusion": (
                    "We conclude that rigorous synthesis of algorithmic theory, systems engineering, and socio-technical evaluation is essential to postgraduate AI. "
                    "Such integration yields transparent, accountable, and robust intelligent systems ready for responsible real-world deployment."
                )
            },
            {
                "abstract": (
                    "Advanced inquiry centers on reinforcement learning with hierarchical policies, multi-agent coordination, and intrinsic motivation. "
                    "We formalize exploration–exploitation trade-offs under partial observability and evaluate stability via distributional critics. "
                    "Benchmarks include complex continuous-control suites and procedurally generated environments, supported by reproducible open-source tooling."
                ),
                "conclusion": (
                    "At scale, reinforcement learning becomes a study of autonomous decision dynamics, where representation, credit assignment, and safety interplay. "
                    "Graduates gain the capacity to extend the frontier of sample-efficient and trustworthy RL."
                )
            }
        ],
        "Data Science": [
            {
                "abstract": (
                    "This postgraduate work emphasizes large-scale data science with distributed optimization, Bayesian non-parametrics, and causal inference. "
                    "We integrate probabilistic modeling with modern deep learners to quantify uncertainty while preserving performance, demonstrating end-to-end pipelines for healthcare analytics, risk modeling, and language intelligence. "
                    "Robustness, fairness, and reproducibility are first-class objectives throughout."
                ),
                "conclusion": (
                    "By unifying probabilistic reasoning, domain expertise, and scalable compute, postgraduate data science delivers methods that reliably inform critical decisions in high-stakes settings."
                )
            },
            {
                "abstract": (
                    "We study multimodal fusion of structured tables, free-text, and images using representation learning, attention, and graph embeddings. "
                    "Comparative experiments on sentiment analysis and medical diagnostics highlight accuracy–interpretability trade-offs and characterize domain shift impacts."
                ),
                "conclusion": (
                    "Integrative modeling emerges as central for next-generation data science, particularly where transparency and robustness drive adoption."
                )
            }
        ]
    }
}

SHORT_RESPONSE = {
    "abstract": "A short abstract was detected, but details were incomplete.",
    "conclusion": "This conclusion is intentionally brief due to partial or insufficient input."
}

EMPTY_RESPONSE = {"abstract": "", "conclusion": ""}


def word_count(text: str) -> int:
    if not text:
        return 0
    tokens = re.findall(r"\b[\w'-]+\b", text)
    return len(tokens)


def choose_variant(level: str, stream: str, mode: str):
    """mode: 'centered' | 'partial' | 'none'"""
    try:
        if mode == "centered":
            return random.choice(DATASET[level][stream])
        if mode == "partial":
            return SHORT_RESPONSE
        return EMPTY_RESPONSE
    except KeyError:
        return EMPTY_RESPONSE


@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json(force=True, silent=True) or {}
    level = data.get("academicLevel", "").strip()
    stream = data.get("stream", "").strip()
    gaze = (data.get("gazeStatus") or "").strip().lower()
    abstract_text = (data.get("abstractText") or "").strip()

    # Soft logic: never return HTML/400 that breaks the UI
    wc = word_count(abstract_text)

    if gaze == "centered" and wc >= MIN_WORDS:
        mode = "centered"
    elif gaze in ("centered", "partial", "off-center", "offcentre", "offcenter") or wc < MIN_WORDS:
        mode = "partial"
    else:
        mode = "none"

    result = choose_variant(level or "UG", stream or "AI", mode)
    # Include a hint for the UI (optional)
    result.update({"words": wc, "mode": mode})
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
