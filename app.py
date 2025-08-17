from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ------------ FULL VARIANTS DATASET ------------
VARIANTS = {
    "Undergraduate": {
        "AI": {
            "centered": {
                "abstract": (
                    "This undergraduate research in Artificial Intelligence introduces foundational algorithms "
                    "including search methods, supervised learning, and basic natural language models. It demonstrates "
                    "how AI can automate reasoning tasks such as classification, prediction, and decision-making. "
                    "Case studies include chatbot prototypes, simple computer vision applications, and recommender systems. "
                    "The methodology emphasizes simplicity, reproducibility, and ethical considerations, preparing learners "
                    "for advanced exploration while ensuring clarity of algorithmic processes."
                ),
                "conclusion": (
                    "The study concludes that undergraduate-level AI work builds strong conceptual foundations by "
                    "focusing on clear algorithmic implementations, small-scale experiments, and awareness of ethical impact."
                )
            },
            "partial": {
                "abstract": (
                    "An incomplete undergraduate AI project still provides valuable insights into supervised classification, "
                    "rule-based systems, or exploratory models. Even without full-scale experiments, it demonstrates an "
                    "understanding of AI’s core potential and applications in automating decision-making tasks."
                ),
                "conclusion": (
                    "The conclusion highlights the early progress, emphasizing the importance of completing pipelines and "
                    "evaluation stages to transform partial prototypes into mature AI projects."
                )
            },
            "off-center": {
                "abstract": (
                    "This abstract indicates an attempt at applying AI methods at the undergraduate level, "
                    "but omits deeper explanation of datasets or evaluation results."
                ),
                "conclusion": (
                    "The conclusion notes that further elaboration and testing are required for a complete study."
                )
            },
        },
        "ML": {
            "centered": {
                "abstract": (
                    "This undergraduate project explores machine learning principles through supervised and unsupervised "
                    "models, including regression, decision trees, and clustering. It emphasizes dataset preparation, "
                    "model training, and evaluation using accuracy, precision, and recall. Visualization and dimensionality "
                    "reduction techniques supplement the learning, ensuring a balanced understanding of both strengths and "
                    "limitations of ML techniques in small-scale experiments."
                ),
                "conclusion": (
                    "The project concludes that undergraduate-level ML provides an essential toolkit for handling structured "
                    "data problems, stressing evaluation and validation as cornerstones of responsible application."
                )
            },
            "partial": {
                "abstract": (
                    "Partial undergraduate ML work often involves experiments with regression or simple classifiers "
                    "without a complete evaluation cycle. While limited, these efforts highlight the iterative nature "
                    "of ML development and the importance of debugging and validation."
                ),
                "conclusion": (
                    "The conclusion acknowledges preliminary learning and points to the need for more systematic testing "
                    "to build robustness in ML projects."
                )
            },
            "off-center": {
                "abstract": (
                    "This abstract briefly notes the application of ML methods without detailing data preparation "
                    "or performance evaluation."
                ),
                "conclusion": (
                    "The conclusion is minimal, recommending elaboration on methodology and results."
                )
            },
        },
        "CSE": {
            "centered": {
                "abstract": (
                    "This undergraduate Computer Science and Engineering project covers the design and analysis of "
                    "software systems, programming paradigms, and database-driven applications. It highlights the "
                    "integration of algorithms, operating system concepts, and networking fundamentals into practical "
                    "implementations. The abstract emphasizes structured problem-solving, modular development, and "
                    "the role of testing frameworks in ensuring robust solutions."
                ),
                "conclusion": (
                    "The conclusion states that undergraduate CSE projects strengthen a student’s core programming and "
                    "system-building skills, laying the foundation for advanced software engineering practice."
                )
            },
            "partial": {
                "abstract": (
                    "A partial CSE project often demonstrates coding prototypes or incomplete system architectures. "
                    "It reflects developing skills in programming, modular design, or database integration."
                ),
                "conclusion": (
                    "The conclusion notes promising initial work while encouraging further development to achieve full functionality."
                )
            },
            "off-center": {
                "abstract": "This abstract notes a CSE theme without elaborating system architecture or testing.",
                "conclusion": "Conclusion remains brief; more comprehensive coverage of implementation is required."
            },
        },
        "Cybersecurity": {
            "centered": {
                "abstract": (
                    "This undergraduate cybersecurity project introduces core defense mechanisms such as encryption, "
                    "hashing, and secure authentication. It simulates common vulnerabilities like SQL injection and "
                    "demonstrates defensive coding practices. The abstract frames cybersecurity as both a technical "
                    "and ethical responsibility, highlighting the growing need for secure digital systems."
                ),
                "conclusion": (
                    "The conclusion reinforces that cybersecurity education equips learners with practical skills and "
                    "awareness to identify and mitigate vulnerabilities in real-world contexts."
                )
            },
            "partial": {
                "abstract": (
                    "A partial cybersecurity study often outlines cryptographic methods or system flaws but may not "
                    "fully integrate testing or defense validation."
                ),
                "conclusion": (
                    "The conclusion acknowledges early insights while stressing the importance of thorough evaluation "
                    "and adversarial testing."
                )
            },
            "off-center": {
                "abstract": "The abstract briefly identifies cybersecurity as the area of focus without deeper exploration.",
                "conclusion": "The conclusion is limited, suggesting further work in implementing robust safeguards."
            },
        },
        "Data Science": {
            "centered": {
                "abstract": (
                    "This undergraduate Data Science project examines structured and unstructured datasets using "
                    "statistical analysis and machine learning models. It demonstrates data wrangling, visualization, "
                    "and exploratory analysis as a foundation for predictive modeling. Case studies highlight insights "
                    "drawn from real-world datasets such as sales, healthcare, or social media."
                ),
                "conclusion": (
                    "The project concludes that data science provides undergraduates with a powerful lens for uncovering "
                    "patterns, encouraging responsible handling of datasets and reproducible reporting."
                )
            },
            "partial": {
                "abstract": (
                    "A partial data science submission may include dataset exploration and initial preprocessing steps "
                    "but lack comprehensive model evaluation."
                ),
                "conclusion": (
                    "The conclusion points to progress while noting that model deployment and validation remain necessary."
                )
            },
            "off-center": {
                "abstract": "The abstract identifies Data Science as the focus without detailed methodology.",
                "conclusion": "The conclusion stays minimal, emphasizing the need for structured pipelines."
            },
        },
        "Electronics": {
            "centered": {
                "abstract": (
                    "This undergraduate Electronics project focuses on the design and testing of analog and digital circuits. "
                    "It highlights practical experiments with microcontrollers, signal processing, and embedded systems. "
                    "The abstract emphasizes the translation of theoretical knowledge into hardware implementation, "
                    "covering prototyping, simulation, and testing phases."
                ),
                "conclusion": (
                    "The conclusion states that undergraduate Electronics projects bridge the gap between classroom "
                    "theory and hands-on circuit design, preparing students for industry-level challenges."
                )
            },
            "partial": {
                "abstract": (
                    "Partial electronics projects may demonstrate circuit schematics or preliminary breadboard models "
                    "without complete testing or debugging."
                ),
                "conclusion": (
                    "The conclusion highlights progress while pointing to the need for full prototyping and measurement."
                )
            },
            "off-center": {
                "abstract": "This abstract briefly indicates an electronics focus without covering experiments.",
                "conclusion": "Conclusion remains short; deeper analysis of results is necessary."
            },
        },
    },
    "Postgraduate": {
        "AI": {
            "centered": {
                "abstract": (
                    "This postgraduate Artificial Intelligence research investigates advanced deep learning architectures, "
                    "transformer models, and reinforcement learning. It focuses on large-scale multimodal datasets, "
                    "benchmarks against state-of-the-art systems, and addresses interpretability, scalability, and ethical AI. "
                    "The abstract details experimental rigor and the broader societal implications of deploying AI."
                ),
                "conclusion": (
                    "The conclusion emphasizes AI’s transformative role in healthcare, NLP, and robotics, while highlighting "
                    "scalability and fairness as critical research frontiers."
                )
            },
            "partial": {
                "abstract": (
                    "A partial postgraduate AI project outlines ambitious goals with deep models but lacks complete results. "
                    "It may describe dataset selection and high-level architectures without extensive benchmarks."
                ),
                "conclusion": (
                    "The conclusion highlights potential while pointing to the need for systematic ablations and comparative analysis."
                )
            },
            "off-center": {
                "abstract": "The abstract identifies AI as the research field without methodological depth.",
                "conclusion": "Conclusion is minimal; more detail is needed for publication-ready work."
            },
        },
        "ML": {
            "centered": {
                "abstract": (
                    "Postgraduate ML research explores reinforcement learning, GANs, transfer learning, and scalable models "
                    "for distributed systems. It integrates Bayesian methods, optimization, and interpretability techniques "
                    "to push the boundaries of applied and theoretical ML."
                ),
                "conclusion": (
                    "The study concludes with contributions to novel architectures and generalization, noting interpretability "
                    "and fairness as ongoing challenges."
                )
            },
            "partial": {
                "abstract": (
                    "A partial postgraduate ML study may describe reinforcement learning or generative approaches but "
                    "leave experimental analysis incomplete."
                ),
                "conclusion": (
                    "The conclusion records early advances and underscores the need for reproducible benchmarking."
                )
            },
            "off-center": {
                "abstract": "This abstract briefly mentions ML as the domain but omits methodology.",
                "conclusion": "The conclusion is compact, calling for depth and evaluation."
            },
        },
        "CSE": {
            "centered": {
                "abstract": (
                    "This postgraduate Computer Science research integrates distributed systems, cloud architectures, "
                    "and high-performance computing. It emphasizes algorithm optimization, database scalability, and "
                    "secure system design, validated with performance benchmarking across heterogeneous environments."
                ),
                "conclusion": (
                    "The conclusion underscores contributions to efficiency, scalability, and secure architecture design "
                    "with potential applications in enterprise and research computing."
                )
            },
            "partial": {
                "abstract": (
                    "Partial postgraduate CSE work often demonstrates prototypes of distributed or cloud systems without "
                    "extensive benchmarking."
                ),
                "conclusion": "The conclusion recommends thorough scalability testing for full validation."
            },
            "off-center": {
                "abstract": "This abstract identifies postgraduate CSE as the field but lacks system details.",
                "conclusion": "Conclusion is minimal, pointing to benchmarking needs."
            },
        },
        "Cybersecurity": {
            "centered": {
                "abstract": (
                    "This postgraduate cybersecurity research addresses advanced cryptographic protocols, intrusion detection "
                    "using ML, and resilience against zero-day vulnerabilities. It integrates penetration testing, secure "
                    "system design, and privacy-preserving computation, validated through large-scale simulations."
                ),
                "conclusion": (
                    "The conclusion emphasizes postgraduate cybersecurity’s critical role in safeguarding critical "
                    "infrastructure while contributing to trust in digital ecosystems."
                )
            },
            "partial": {
                "abstract": (
                    "Partial postgraduate cybersecurity work may outline advanced cryptographic algorithms or anomaly detection "
                    "without full deployment."
                ),
                "conclusion": "The conclusion recognizes potential but highlights the need for end-to-end testing."
            },
            "off-center": {
                "abstract": "The abstract notes cybersecurity as the domain without depth.",
                "conclusion": "The conclusion calls for elaboration in security validation."
            },
        },
        "Data Science": {
            "centered": {
                "abstract": (
                    "This postgraduate Data Science research integrates big data analytics, cloud computation, and advanced "
                    "predictive modeling techniques. It explores challenges of handling high-dimensional data, ethical "
                    "concerns in personal data analysis, and applications across finance, healthcare, and governance."
                ),
                "conclusion": (
                    "The conclusion highlights contributions to scalable pipelines, domain-specific insights, and reproducible science."
                )
            },
            "partial": {
                "abstract": "Partial postgraduate data science work outlines preprocessing and exploratory analysis without full models.",
                "conclusion": "The conclusion highlights need for end-to-end pipelines and benchmarking."
            },
            "off-center": {
                "abstract": "This abstract briefly notes data science but lacks methodology.",
                "conclusion": "Conclusion remains short, requiring detailed results."
            },
        },
        "Electronics": {
            "centered": {
                "abstract": (
                    "This postgraduate Electronics project explores advanced VLSI design, signal integrity in high-frequency circuits, "
                    "and embedded systems optimization. It employs simulation tools, FPGA prototyping, and extensive testing to "
                    "validate novel circuit architectures."
                ),
                "conclusion": (
                    "The conclusion states that postgraduate electronics research contributes to scalable and efficient hardware "
                    "design, addressing power and performance trade-offs."
                )
            },
            "partial": {
                "abstract": "Partial electronics work outlines novel design ideas without exhaustive prototyping.",
                "conclusion": "The conclusion notes early insights but urges full validation."
            },
            "off-center": {
                "abstract": "This abstract notes electronics as the theme without detail.",
                "conclusion": "Conclusion remains minimal; requires testing data."
            },
        },
    }
}

# ------------ ROUTE ------------
@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json()
        level = data.get("academicLevel", "")
        stream = data.get("stream", "")
        abstract_input = data.get("abstractInput", "")
        gaze = data.get("gazeStatus", "manual")

        # Validation
        if level not in VARIANTS:
            return jsonify({"error": "Invalid academic level"}), 400
        if stream not in VARIANTS[level]:
            return jsonify({"error": "Invalid stream"}), 400
        if not abstract_input or len(abstract_input.split()) < 15:
            return jsonify({"error": "Abstract must be at least 15 words"}), 400

        # Always fetch dataset for that stream
        selected_stream = VARIANTS[level][stream]

        # Gaze logic
        if gaze in ["centered", "partial", "off-center"]:
            choice = selected_stream[gaze]
        else:
            choice = selected_stream["centered"]  # fallback to full abstract

        return jsonify(choice)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
