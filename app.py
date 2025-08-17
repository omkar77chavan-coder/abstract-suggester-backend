from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------- VARIANTS DATASET ----------------
VARIANTS = {
    "UG": {
        "AI": {
            "centered": {
                "abstract": "This undergraduate-level Artificial Intelligence project explores foundational algorithms, supervised and unsupervised methods, and the ethical implications of AI adoption. By providing a detailed account of early-stage neural architectures, optimization strategies, and real-world case applications, it aims to introduce students to AI both as a technical and social discipline.",
                "conclusion": "AI at the undergraduate level empowers learners with a baseline understanding of intelligent systems while highlighting the importance of ethical awareness and practical application."
            },
            "partial": {
                "abstract": "A partial undergraduate AI abstract highlights fundamental exploration of algorithms and data-driven methods, but omits extended depth due to incomplete input.",
                "conclusion": "Conclusion remains succinct and provisional given the partial data provided."
            },
            "off-center": {
                "abstract": "An abbreviated undergraduate AI abstract captures only a subset of approaches and methods.",
                "conclusion": "Conclusion is shortened due to off-center gaze detection, offering only limited insight."
            }
        },
        "ML": {
            "centered": {
                "abstract": "Undergraduate research in Machine Learning emphasizes core concepts of supervised models, basic neural architectures, and model evaluation metrics. It introduces learners to hands-on experimentation with datasets, highlighting generalization, overfitting, and interpretability challenges.",
                "conclusion": "The work underlines ML’s potential in cultivating foundational skills and bridging theory with practice."
            },
            "partial": {
                "abstract": "A partially detected undergraduate ML abstract focuses on introductory algorithms but remains incomplete.",
                "conclusion": "Conclusion is brief due to limited details provided during face tracking."
            },
            "off-center": {
                "abstract": "Undergraduate ML work summarized in a limited manner due to off-center detection.",
                "conclusion": "Conclusion compressed as a result of unstable gaze capture."
            }
        },
    },
    "PG": {
        "AI": {
            "centered": {
                "abstract": "Postgraduate Artificial Intelligence research expands into advanced deep learning architectures, optimization strategies, and domain-specific AI applications. This includes transformer-based systems, reinforcement learning for adaptive environments, and cross-disciplinary uses in healthcare, finance, and engineering. The abstract explores interpretability frameworks, ethical governance models, and large-scale computational considerations, all presented with a research-driven rigor that reflects postgraduate depth.",
                "conclusion": "Postgraduate AI research validates the transformative potential of intelligent systems by advancing both technical depth and interdisciplinary applicability."
            },
            "partial": {
                "abstract": "Partial facial detection led to an abbreviated postgraduate AI abstract. It outlines the problem framing, the primary approach, and a narrow slice of results, omitting secondary analyses and extensive ablations.",
                "conclusion": "A compact conclusion notes preliminary significance and limitations; full detail requires stable gaze or manual confirmation."
            },
            "off-center": {
                "abstract": "An off-center postgraduate AI abstract was captured with limited context, reducing narrative detail.",
                "conclusion": "Conclusion notes that output is constrained due to unstable gaze, urging a fuller review."
            }
        },
        "ML": {
            "centered": {
                "abstract": "Graduate-level Machine Learning work covers reinforcement learning, generative adversarial networks, and distributed model training at scale. The abstract highlights emerging themes such as multimodal learning, fairness, and resource-efficient optimization, situating ML as a frontier of scientific and industrial research. Technical exploration extends into statistical underpinnings and computational complexities.",
                "conclusion": "The study concludes with ML’s promise for scalable, explainable, and societally transformative applications."
            },
            "partial": {
                "abstract": "A partial postgraduate ML abstract captures only essential framing and primary methods but excludes detailed evaluation.",
                "conclusion": "Conclusion remains preliminary; comprehensive significance awaits complete detection."
            },
            "off-center": {
                "abstract": "Due to unstable detection, postgraduate ML abstract output is summarized briefly without extended discussion.",
                "conclusion": "Conclusion condensed because of incomplete visual confirmation."
            }
        },
    }
}

# ---------------- ROUTE ----------------
@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json()
        level = data.get("academicLevel", "")
        stream = data.get("stream", "")
        abstract_input = data.get("abstractInput", "")
        gaze = data.get("gazeStatus", "manual")

        # ✅ Validation
        if level not in VARIANTS:
            return jsonify({"error": "Invalid academic level"}), 400
        if stream not in VARIANTS[level]:
            return jsonify({"error": "Invalid stream"}), 400
        if not abstract_input or len(abstract_input.split()) < 15:
            return jsonify({"error": "Abstract must be at least 15 words"}), 400

        # ✅ Always return something from dataset
        selected_stream = VARIANTS[level][stream]

        if gaze in ["centered", "partial", "off-center"]:
            choice = selected_stream[gaze]
        else:
            # manual fallback = full abstract
            choice = selected_stream["centered"]

        return jsonify(choice)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
