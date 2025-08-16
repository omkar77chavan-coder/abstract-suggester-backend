from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# -----------------------
# FULL DATASET
# -----------------------
DATASET = {
    "UG": {
        "AI": [
            {
                "abstract": "This project introduces undergraduate students to artificial intelligence concepts with emphasis on search algorithms, knowledge representation, and reasoning under uncertainty. The abstract highlights applied problem-solving through hands-on experiments and simulations.",
                "conclusion": "The study concludes that undergraduate exposure to AI fosters curiosity and foundational understanding, preparing learners for deeper exploration."
            },
            {
                "abstract": "An undergraduate exploration of AI emphasizes supervised and unsupervised learning. Through simplified models, students engage with classification, clustering, and reinforcement examples that make AI tangible.",
                "conclusion": "Early AI education offers not just technical know-how but also broadens students’ perspective on automation and decision-making."
            },
            {
                "abstract": "The paper discusses neural networks at an undergraduate level, introducing students to perceptrons and basic backpropagation, enabling them to appreciate how machines learn.",
                "conclusion": "Even basic exposure equips students with analytical frameworks to pursue advanced AI applications."
            }
        ],
        "Data Science": [
            {
                "abstract": "This undergraduate project explores data collection, cleaning, and visualization. Emphasis is placed on descriptive statistics and reproducibility, empowering students to critically interpret datasets.",
                "conclusion": "The study concludes that foundational data science builds both statistical literacy and research readiness."
            },
            {
                "abstract": "Students analyze open datasets using Python libraries like Pandas and Matplotlib. The abstract demonstrates how hands-on exercises make concepts like correlation and distribution concrete.",
                "conclusion": "Through guided practice, students realize the value of structured analysis in decision-making."
            },
            {
                "abstract": "An introductory module on machine learning with regression and classification, tailored for undergraduates in data science.",
                "conclusion": "The conclusion affirms that early application bridges theory and real-world data challenges."
            }
        ]
    },
    "PG": {
        "AI": [
            {
                "abstract": (
                    "This postgraduate research delves into advanced artificial intelligence with emphasis on hybrid reasoning systems that integrate symbolic AI and deep neural architectures. "
                    "By leveraging multi-modal data, including natural language, vision, and structured knowledge graphs, the work demonstrates scalable solutions to problems of explainability, "
                    "generalization, and transfer learning. Special attention is paid to ethical considerations, including bias mitigation, responsible decision-making, and human-AI collaboration. "
                    "The research spans several application domains, such as automated medical diagnosis, cognitive robotics, and large-scale information retrieval."
                ),
                "conclusion": (
                    "The study concludes that postgraduate-level engagement with AI necessitates synthesis of algorithmic theory, system design, and socio-ethical analysis. "
                    "Such an integrative approach contributes not only to academic advancement but also to deployment of AI systems that are transparent, accountable, and beneficial to society."
                )
            },
            {
                "abstract": (
                    "Advanced postgraduate inquiry into artificial intelligence examines reinforcement learning with hierarchical policy optimization, multi-agent collaboration, and intrinsic motivation mechanisms. "
                    "The research situates RL within broader contexts of self-adaptive systems and emergent intelligence, highlighting both theoretical rigor and computational experimentation. "
                    "Simulation environments and benchmark datasets are used extensively to validate algorithmic improvements."
                ),
                "conclusion": (
                    "This work concludes that reinforcement learning at scale is not merely an optimization task but an investigation into the dynamics of autonomous decision-making. "
                    "Postgraduate students gain the ability to critically extend the frontier of AI capabilities."
                )
            }
        ],
        "Data Science": [
            {
                "abstract": (
                    "Postgraduate exploration of data science emphasizes large-scale distributed learning and integration of statistical inference with machine learning paradigms. "
                    "The work covers Bayesian non-parametrics, causal inference, and advanced optimization. Furthermore, attention is given to real-world applications across healthcare analytics, "
                    "financial risk modeling, and natural language processing. Emphasis is placed on reproducibility, ethical use of sensitive datasets, and methods for uncertainty quantification."
                ),
                "conclusion": (
                    "The research concludes that postgraduate training in data science cultivates deep methodological innovation. By unifying probabilistic reasoning, domain expertise, "
                    "and scalable algorithms, data scientists contribute tools that redefine both academic research and industrial practice."
                )
            },
            {
                "abstract": (
                    "The thesis investigates multimodal data fusion in postgraduate data science, integrating structured data, text, and imagery. "
                    "Techniques such as representation learning, attention mechanisms, and graph embeddings are compared across tasks like sentiment analysis and medical diagnostics. "
                    "The abstract underscores technical sophistication and applied breadth."
                ),
                "conclusion": (
                    "Conclusions point to the centrality of integrative modeling for next-generation data science, particularly where interpretability and robustness are paramount."
                )
            }
        ]
    }
}

# -----------------------
# HELPERS
# -----------------------
def choose_variant(level, stream, gaze):
    """Select abstract & conclusion based on academic level, stream, and gaze."""
    try:
        if gaze == "centered":
            return random.choice(DATASET[level][stream])
        elif gaze == "partial":
            return {
                "abstract": "A short abstract was detected, but details were incomplete.",
                "conclusion": "This conclusion is left unfinished due to partial input."
            }
        else:  # no gaze or off-center
            return {"abstract": "", "conclusion": ""}
    except KeyError:
        return {"abstract": "", "conclusion": ""}

# -----------------------
# ROUTE
# -----------------------
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    level = data.get("academicLevel")
    stream = data.get("stream")
    gaze = data.get("gazeStatus")

    if not level or not stream or not gaze:
        return jsonify({"error": "Missing fields"}), 400

    choice = choose_variant(level, stream, gaze)
    return jsonify(choice)

# -----------------------
# MAIN
# -----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
