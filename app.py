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

# ----------- DATASET (UG + PG, long abstracts) -----------
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
    "PG": {
        "AI": [
            {
                "abstract": "Postgraduate research in Artificial Intelligence examines advanced learning paradigms such as deep neural architectures, reinforcement learning, and probabilistic reasoning. This work explores not only algorithmic improvements but also interpretability, trust, and fairness in AI deployment. By bridging symbolic and sub-symbolic approaches, the research highlights how hybrid models address real-world complexity across domains such as healthcare, finance, and autonomous systems.",
                "conclusion": "AI at the postgraduate level advances both theoretical frameworks and ethical safeguards, ensuring systems remain powerful, transparent, and accountable."
            },
            {
                "abstract": "This project investigates frontier AI techniques including generative modeling, transfer learning, and human-AI collaboration. Emphasis is placed on scaling algorithms for large datasets while reducing computational costs through model compression and distributed optimization. Applications extend to drug discovery, language technologies, and personalized recommendations, with careful consideration of ethical risks like algorithmic bias.",
                "conclusion": "Postgraduate AI work balances innovation with responsibility, positioning AI as both a scientific frontier and a societal force."
            },
            {
                "abstract": "Research at this level critically examines the limits of AI generalization and robustness. Experimental studies assess adversarial resilience, domain adaptation, and the integration of symbolic reasoning for explainable systems. Insights from cognitive science inspire architectures that learn more human-like representations while maintaining mathematical rigor and computational feasibility.",
                "conclusion": "Such inquiry defines AI as a discipline that is simultaneously technical, scientific, and profoundly human-centered."
            }
        ],
        "ML": [
            {
                "abstract": "Machine Learning research at the postgraduate stage investigates optimization theory, non-convex landscapes, and generalization bounds in deep models. Work also emphasizes quantum-assisted ML, federated learning for privacy, and fairness-aware optimization. Applications span predictive healthcare, climate modeling, and industrial automation. By merging mathematics with experimentation, students develop novel frameworks that advance the scalability and reliability of ML systems.",
                "conclusion": "ML research at this level extends beyond prediction—it shapes ethical, scalable solutions with global impact."
            },
            {
                "abstract": "This project analyzes state-of-the-art models, from transformers to graph neural networks, exploring how structural priors enhance representation learning. Postgraduates evaluate theoretical underpinnings of expressivity while implementing benchmarks for reproducibility and fairness. The work draws from optimization, probability theory, and software systems to achieve a balance of rigor and real-world relevance.",
                "conclusion": "Research outcomes highlight ML as an evolving discipline where abstraction meets application, and models gain social responsibility."
            },
            {
                "abstract": "Advanced ML studies include robust evaluation metrics, the dynamics of continual learning, and lifelong adaptation of agents. By exploring catastrophic forgetting, transfer mechanisms, and emergent behaviors, the research underscores ML’s role in autonomous decision-making. Interdisciplinary collaborations with neuroscience provide fresh insights into biologically inspired algorithms.",
                "conclusion": "Such efforts push ML towards a future where algorithms adapt gracefully while remaining interpretable and reliable."
            }
        ],
        "CSE": [
            {
                "abstract": "Postgraduate computer science research addresses scalability, concurrency, and formal verification of complex software systems. Investigations include new paradigms in distributed computing, programming languages that emphasize safety and expressivity, and the intersection of theoretical computer science with modern hardware constraints. Case studies illustrate how algorithms scale in cloud environments, edge devices, and heterogeneous architectures.",
                "conclusion": "CSE research balances theory with implementation, producing innovations that underpin global-scale systems."
            },
            {
                "abstract": "This work focuses on the foundations and frontiers of computing, including computational complexity, cryptographic protocols, and advances in compiler design. Explorations cover how computational limits inform algorithmic choices and how verification frameworks strengthen security and correctness. The project also addresses ethical dimensions in computing, from energy efficiency to accessibility.",
                "conclusion": "The conclusion situates CSE as a discipline that not only solves technical problems but also anticipates societal challenges."
            },
            {
                "abstract": "Research at the postgraduate level integrates machine learning with classical computing systems, exploring adaptive operating systems, intelligent compilers, and self-healing software architectures. Interdisciplinary synergies expand computing’s scope into domains such as biology, social sciences, and creative industries.",
                "conclusion": "CSE emerges as both a core science and a catalyst for cross-disciplinary discovery."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "Advanced cybersecurity research examines zero-trust architectures, homomorphic encryption, and post-quantum cryptography. Projects investigate secure multiparty computation and formal proofs of resilience against adversarial models. Applications include privacy-preserving medical systems, secure blockchain protocols, and resilient national infrastructure.",
                "conclusion": "Postgraduate cybersecurity creates frameworks where security and usability coexist, ensuring trust in digital society."
            },
            {
                "abstract": "This work explores human factors in cybersecurity, studying socio-technical vulnerabilities alongside technical exploits. Researchers evaluate behavioral economics of phishing, insider threats, and the role of policy in shaping cyber resilience. Technical aspects include intrusion detection powered by ML and adaptive defense strategies.",
                "conclusion": "Cybersecurity research emphasizes that systems are only as strong as the people and processes that govern them."
            },
            {
                "abstract": "Research here integrates formal methods, AI-based detection, and large-scale simulations of cyberattacks. Ethical discussions cover surveillance, privacy trade-offs, and the geopolitics of cyber conflict. Theoretical advancements include attack graph analysis and resilient system architectures.",
                "conclusion": "Postgraduate cybersecurity balances mathematical assurance with ethical foresight to safeguard the digital future."
            }
        ],
        "Data Science": [
            {
                "abstract": "Postgraduate Data Science research emphasizes large-scale analytics, causal inference, and interpretable models. Projects include bias correction in social data, reproducibility of experiments, and the integration of heterogeneous sources such as text, images, and graphs. Statistical rigor combines with computational efficiency to create insights that drive policy and innovation.",
                "conclusion": "Data Science at the PG level produces not only predictions but also trustworthy evidence for decision-making."
            },
            {
                "abstract": "This project addresses streaming analytics, high-dimensional modeling, and scalable Bayesian inference. By combining cloud platforms with optimized algorithms, the research delivers actionable intelligence for industries ranging from healthcare to transportation. Emphasis is also placed on reproducibility and ethics in handling sensitive datasets.",
                "conclusion": "Postgraduate work ensures data-driven systems remain both impactful and socially responsible."
            },
            {
                "abstract": "Research investigates the future of data science in automation, explainability, and human-data interaction. Postgraduates explore interactive visualizations, mixed-method research, and integration of qualitative insights with quantitative models. The project situates data science as a bridge across disciplines, not just a computational practice.",
                "conclusion": "The field matures into a unifying lens for evidence-based inquiry across sciences and humanities."
            }
        ],
        "Electronics": [
            {
                "abstract": "Advanced electronics research examines nanotechnology, semiconductor scaling limits, and quantum device architectures. Projects evaluate integration of MEMS, photonics, and nanoscale transistors for next-generation computing and sensing. Research also investigates sustainable electronics through biodegradable materials and energy-harvesting devices.",
                "conclusion": "Electronics at this level advances toward both miniaturization and sustainability, reshaping the technological landscape."
            },
            {
                "abstract": "This project explores VLSI design, FPGA acceleration, and low-power system architectures. Postgraduates optimize chips for machine learning workloads, 5G communications, and biomedical applications. The work emphasizes co-design across hardware and software layers.",
                "conclusion": "Such research creates specialized platforms that align efficiency with innovation."
            },
            {
                "abstract": "Research covers advanced signal processing, embedded intelligence, and cyber-physical systems. By uniting electronics with AI, robotics, and IoT, the study demonstrates how hardware intelligence fuels autonomous and adaptive systems.",
                "conclusion": "Electronics emerges as both an enabler of digital futures and a testbed for interdisciplinary advances."
            }
        ]
    }
}

# ----------- SIMPLE FALLBACK (off-center gaze) -----------
SIMPLE_DATA = {
    "abstract": "A quick overview of the chosen field is provided with simple explanations.",
    "conclusion": "This short conclusion summarizes the key idea in a straightforward way."
}

# ----------- PARTIAL GAZE DATA (one-liners per stream) -----------
PARTIAL_DATA = {
    "AI": [
        {"abstract": "AI explores machines that think a little like humans.", "conclusion": "AI opens paths to smarter systems."},
        {"abstract": "Artificial Intelligence studies decision-making in software.", "conclusion": "AI blends logic with data."}
    ],
    "ML": [
        {"abstract": "Machine Learning finds patterns in data with algorithms.", "conclusion": "ML enables predictive insights."},
        {"abstract": "ML trains computers to learn from examples.", "conclusion": "It grows smarter with more data."}
    ],
    "CSE": [
        {"abstract": "Computer Science builds foundations for modern computing.", "conclusion": "CSE powers digital innovation."},
        {"abstract": "CSE teaches coding, logic, and algorithms.", "conclusion": "It underpins all software systems."}
    ],
    "Cybersecurity": [
        {"abstract": "Cybersecurity keeps systems safe from threats.", "conclusion": "It ensures digital trust."},
        {"abstract": "Cybersecurity guards data and privacy.", "conclusion": "Strong security prevents attacks."}
    ],
    "Data Science": [
        {"abstract": "Data Science extracts knowledge from raw information.", "conclusion": "It drives evidence-based actions."},
        {"abstract": "Data Science makes sense of large datasets.", "conclusion": "It turns data into insights."}
    ],
    "Electronics": [
        {"abstract": "Electronics studies circuits and devices.", "conclusion": "It enables all digital hardware."},
        {"abstract": "Electronics powers everyday machines.", "conclusion": "It links theory with technology."}
    ]
}

last_used_partial = {s: None for s in PARTIAL_DATA.keys()}

# ----------- HELPERS -----------
def normalize_stream(stream):
    if not stream: return None
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

def choose_partial(stream):
    options = PARTIAL_DATA[stream]
    prev = last_used_partial[stream]
    choices = [i for i in range(len(options)) if i != prev]
    idx = random.choice(choices)
    last_used_partial[stream] = idx
    return options[idx]

# ----------- ROUTE -----------
@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    stream_raw = data.get("stream")
    level = data.get("academicLevel", "UG")
    gaze = data.get("gazeStatus", "none")

    stream = normalize_stream(stream_raw)
    if level not in DATA: level = "UG"
    if not stream or stream not in DATA[level]:
        return jsonify({"error": "Invalid stream"}), 400

    if gaze == "centered":
        choice = choose_variant(level, stream)
    elif gaze == "off-center":
        choice = SIMPLE_DATA
    elif gaze == "partial":
        choice = choose_partial(stream)
    else:
        choice = choose_variant(level, stream)

    return jsonify(choice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
