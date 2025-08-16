from flask import Flask, request, jsonify
import random

app = Flask(__name__)

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
        ],
        "Computer Science": [
            {
                "abstract": "Graduate-level Computer Science research is defined by its pursuit of efficiency, security, and scalability in computational systems. This work investigates distributed consensus protocols, fault-tolerant architectures, and algorithmic complexity to address challenges in blockchain, cloud computing, and large-scale information retrieval. Parallel computing techniques are employed to reduce runtime complexity of NP-hard problems, while verification frameworks are applied to formally validate correctness of mission-critical software. Hardware-software co-design principles are explored to optimize computing pipelines, focusing on energy efficiency without compromising performance. Case studies include simulations of secure transaction platforms, large-scale graph processing, and optimization of compiler design for heterogeneous architectures.",
                "conclusion": "Results demonstrate how rigorous algorithms combined with system-level design yield scalable, secure platforms. Graduate research ensures computing remains both powerful and trustworthy."
            },
            {
                "abstract": "This postgraduate project extends the foundations of Computer Science into advanced areas such as quantum algorithms, high-performance computing, and AI-driven compilers. The research investigates how qubits and quantum gates may reduce asymptotic complexity for factoring and search problems, while hybrid quantum-classical systems are benchmarked against traditional HPC pipelines. Advanced operating system kernels are studied for memory and thread optimization in massively parallel workloads, while machine learning-based heuristics are integrated into compiler optimizations to automatically adjust execution flow. Cross-disciplinary focus ensures that theoretical contributions translate into engineering breakthroughs in domains such as cryptography, bioinformatics, and aerospace systems.",
                "conclusion": "Graduate exploration reveals computing frontiers in quantum and HPC. These innovations reshape secure systems and accelerate scientific discovery."
            },
            {
                "abstract": "The field of Computer Science at the graduate level emphasizes not only theoretical elegance but also rigorous application in industrially relevant contexts. This study investigates algorithmic verification techniques, type-theoretic foundations, and model checking for concurrent and distributed systems. It benchmarks state-of-the-art verification tools like Coq, Isabelle, and SPIN against real-world software vulnerabilities. Alongside verification, the work explores secure software engineering practices, compiler optimization strategies, and resilient architectures for edge computing. Case applications include security-critical aviation systems, medical devices, and autonomous robotics. Through this lens, the research establishes a framework that combines mathematical rigor with engineering robustness.",
                "conclusion": "Formal methods ensure software correctness at scale. Graduate work highlights the indispensable role of verification in mission-critical computing."
            }
        ],
        "Electronics": [
            {
                "abstract": "Electronics at the postgraduate level transcends foundational circuit analysis, focusing instead on advanced VLSI design, signal integrity, and embedded system integration for real-world applications. This project presents detailed simulations of CMOS scaling challenges, low-power circuit topologies, and novel transistor architectures, including FinFET and GAAFET technologies. Furthermore, it evaluates mixed-signal system-on-chip (SoC) designs for IoT applications, incorporating hardware-level encryption modules to ensure security. Reliability analysis is carried out through accelerated aging simulations, while thermal management strategies are modeled using finite-element analysis. This comprehensive work highlights both the opportunities and constraints in the next generation of semiconductor technologies.",
                "conclusion": "Graduate research demonstrates the delicate balance between scaling and reliability. Advances in VLSI design extend the possibilities of modern electronics."
            },
            {
                "abstract": "In this postgraduate study, Electronics research is extended toward wireless communication systems, RF circuit design, and high-frequency signal processing. Millimeter-wave antenna arrays are prototyped and evaluated using advanced EM simulation, targeting 5G and beyond. The research also investigates advanced error correction coding schemes, signal-to-noise optimization, and spectrum-sharing algorithms that ensure reliability in congested environments. Additionally, FPGA-based prototyping is used to demonstrate adaptive modulation techniques, highlighting real-time adaptability of embedded wireless systems. Findings contribute both to academic theory and practical deployments in communication infrastructure.",
                "conclusion": "Results prove how postgraduate-level electronics can bridge theory and wireless deployment. Insights enhance both connectivity and spectrum efficiency."
            },
            {
                "abstract": "Graduate-level Electronics emphasizes sustainable energy and next-generation embedded intelligence. This project explores power electronics for renewable energy integration, including advanced inverters, battery management systems, and grid stabilization strategies. Cutting-edge semiconductor devices such as SiC and GaN transistors are investigated for high-efficiency conversion. Additionally, neuromorphic circuit design is presented, enabling energy-efficient computation for edge AI devices. The work combines extensive simulation with experimental validation, showing how electronic design directly supports clean energy and intelligent embedded systems.",
                "conclusion": "Advanced devices and sustainable circuits redefine electronic design. Graduate work drives efficiency in both renewable energy and AI hardware."
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

    # Default to UG if missing
    if level not in DATA: level = "UG"
    if stream not in DATA[level]: return jsonify({"error": "Invalid stream"}), 400

    # Logic based on gaze
    if gaze == "centered":
        choice = choose_variant(level, stream)  # give exact level
    else:
        # off-center/unstable -> fallback to UG
        choice = choose_variant("UG", stream)

    return jsonify({
        "abstract": choice["abstract"],
        "conclusion": choice["conclusion"]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
