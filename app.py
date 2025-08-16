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
                "abstract": "Postgraduate research in Artificial Intelligence focuses on advanced paradigms such as deep reinforcement learning, generative adversarial networks, and neurosymbolic AI. The emphasis lies not only on creating scalable algorithms but also on ensuring explainability, interpretability, and fairness. Research extends into integrating AI across domains such as healthcare for diagnostic systems, finance for fraud detection, and autonomous robotics for adaptive control. These studies highlight how AI systems can generalize across environments and minimize biases, ensuring trust in deployment.",
                "conclusion": "AI at the postgraduate level is not only about achieving higher accuracy but also about embedding transparency and responsibility into algorithmic decisions."
            },
            {
                "abstract": "This work explores frontier AI techniques such as transfer learning, self-supervised representation learning, and federated AI. The research emphasizes building models that can adapt with minimal labeled data, handle distributed environments, and ensure privacy in data-sensitive applications. The integration of symbolic reasoning with deep architectures enhances explainability while maintaining scalability across billion-parameter models. The practical applications span drug discovery, natural language understanding, and AI-driven creative systems.",
                "conclusion": "The research situates AI as a scientific and social force that balances innovation with ethical accountability."
            },
            {
                "abstract": "Research at this level interrogates the robustness and resilience of AI models under adversarial conditions. The project investigates adversarial defense, domain adaptation, and meta-learning frameworks. A deeper inquiry into human-inspired learning mechanisms, such as attention modulation and episodic memory, provides architectures that bridge cognitive psychology and computational systems. Ethical discourse highlights the challenges of bias, surveillance, and decision accountability in high-stakes domains like law enforcement and defense.",
                "conclusion": "Postgraduate AI defines a pathway where advanced technical rigor meets human-centered responsibility."
            }
        ],
        "ML": [
            {
                "abstract": "Machine Learning research at the postgraduate level deeply investigates optimization landscapes, convergence theory, and fairness-aware generalization bounds. The studies include federated learning for privacy-preserving collaboration, quantum-assisted ML for next-generation computation, and continual learning to overcome catastrophic forgetting. Applications are framed in the contexts of predictive healthcare, climate change modeling, and large-scale industrial automation. The balance between mathematical rigor and engineering scalability defines the trajectory of ML at this level.",
                "conclusion": "ML research transcends prediction, offering scalable and ethical solutions to global challenges."
            },
            {
                "abstract": "This work examines state-of-the-art deep architectures such as transformers and graph neural networks, evaluating their expressive power and efficiency. Research analyzes optimization methods, parameter-efficient fine-tuning, and reproducibility benchmarks. Special emphasis is given to low-resource adaptation, where ML extends access to underrepresented communities and smaller organizations. Practical domains include natural language processing, computational biology, and financial risk management.",
                "conclusion": "Research outcomes in ML highlight a discipline that evolves with responsibility, inclusivity, and technical depth."
            },
            {
                "abstract": "Postgraduate research emphasizes lifelong learning and adaptive systems capable of reusing prior knowledge. Theoretical work integrates reinforcement learning, meta-learning, and biologically inspired algorithms to produce agents that mimic human adaptability. Interdisciplinary collaborations with neuroscience provide frameworks for algorithms that balance stability and plasticity. Applications extend to robotics, multi-agent collaboration, and human-in-the-loop AI systems.",
                "conclusion": "Such research pushes ML toward creating agents that learn continuously, responsibly, and reliably."
            }
        ],
        "CSE": [
            {
                "abstract": "Postgraduate-level computer science research explores scalability, distributed computing, and formal verification. Emphasis lies on secure multiparty computation, cloud-native architectures, and concurrency management across heterogeneous devices. The studies highlight the tension between computational complexity and practical deployment, investigating cryptographic protocols, adaptive compilers, and systems that ensure both performance and security. Applications include large-scale social platforms, financial systems, and cloud-edge hybrid infrastructures.",
                "conclusion": "CSE research builds innovations that underpin robust, scalable, and globally distributed systems."
            },
            {
                "abstract": "This research focuses on the theoretical boundaries of computing, including computational complexity, approximation algorithms, and cryptographic primitives. The practical investigations tie these foundations into compiler design, formal verification frameworks, and secure hardware-software co-design. The project bridges pure theory and applied systems, ensuring that algorithmic advances remain practically deployable and verifiably correct.",
                "conclusion": "CSE emerges as a discipline that anticipates technical and social challenges simultaneously."
            },
            {
                "abstract": "The integration of ML with CSE domains leads to intelligent operating systems, adaptive compilers, and self-healing software architectures. Interdisciplinary collaborations extend computing to biology, creative arts, and social sciences. This research aims to expand computer science as both a fundamental discipline and an applied catalyst across multiple sectors.",
                "conclusion": "CSE evolves as a domain that blends technical rigor with societal utility."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "Advanced cybersecurity research investigates zero-trust architectures, privacy-preserving cryptographic frameworks such as homomorphic encryption, and quantum-safe protocols. Emphasis is placed on formal verification of security models and multiparty computation for collaborative but secure systems. Real-world use cases span healthcare data sharing, resilient blockchain infrastructure, and secure national communication networks.",
                "conclusion": "Cybersecurity research ensures that future societies rely on digital ecosystems that are private, resilient, and trustworthy."
            },
            {
                "abstract": "This project situates human factors at the core of cybersecurity research. Investigations highlight socio-technical vulnerabilities including insider threats, behavioral economics of phishing, and policy-driven compliance challenges. Technical studies integrate ML-based intrusion detection, anomaly monitoring, and adaptive countermeasures. The balance between user behavior and technical defenses becomes central to resilient security.",
                "conclusion": "Cybersecurity transcends technology, incorporating human and institutional dimensions for resilience."
            },
            {
                "abstract": "Research integrates large-scale simulations of cyberattacks, attack graph analysis, and system-level resilience testing. Ethical considerations address surveillance, privacy trade-offs, and the geopolitics of cyber conflict. Formal methods and AI-driven frameworks are leveraged to automate defenses while respecting ethical boundaries.",
                "conclusion": "Cybersecurity establishes a future where systems are mathematically assured and ethically governed."
            }
        ],
        "Data Science": [
            {
                "abstract": "Postgraduate Data Science emphasizes causal inference, interpretable modeling, and large-scale analytics across heterogeneous data. Research investigates bias correction, data reproducibility, and integration of multimodal data sources such as text, images, and social networks. Applications extend to policy modeling, healthcare decision-making, and knowledge discovery in sciences. The work combines computational power with statistical responsibility.",
                "conclusion": "Data Science at PG transforms data into evidence-based insights with accountability."
            },
            {
                "abstract": "This project explores streaming analytics, high-dimensional modeling, and scalable Bayesian inference. It integrates cloud-native architectures and real-time pipelines to produce timely intelligence for industries such as healthcare and transportation. Ethical concerns include fairness, interpretability, and transparency in real-time decision-making systems.",
                "conclusion": "The field evolves into a discipline of both technical sophistication and ethical vigilance."
            },
            {
                "abstract": "Research investigates human-data interaction, visual analytics, and integration of qualitative reasoning with quantitative modeling. By developing tools for explainability, accessibility, and interdisciplinary collaboration, data science becomes not only computational but also communicative, bridging sciences and humanities.",
                "conclusion": "Data Science emerges as the universal lens for inquiry, combining rigor and inclusivity."
            }
        ],
        "Electronics": [
            {
                "abstract": "Advanced electronics research explores quantum-scale devices, nanotechnology integration, and energy-harvesting systems. Investigations include photonic circuits, nanoscale transistors, and MEMS-based intelligent sensors. Sustainability becomes central, with biodegradable electronics and low-power embedded intelligence. Applications span autonomous vehicles, next-generation communication, and biomedical implants.",
                "conclusion": "Electronics research drives miniaturization and sustainability, redefining the boundaries of technology."
            },
            {
                "abstract": "This project investigates FPGA acceleration, VLSI design, and architectures for AI workloads. Emphasis is placed on chip-level co-design, efficient power management, and real-time performance optimization. Applications include 5G systems, biomedical circuits, and space-grade electronics.",
                "conclusion": "Such work develops tailored computing platforms where performance aligns with energy efficiency."
            },
            {
                "abstract": "Research integrates advanced signal processing, embedded intelligence, and cyber-physical systems. By uniting IoT, robotics, and AI, electronics becomes the bedrock of intelligent environments that adapt and interact seamlessly with humans.",
                "conclusion": "Electronics at the postgraduate level transforms from hardware to intelligent ecosystems."
            }
        ]
    }
}

# ----------- SIMPLE FALLBACKS -----------
SIMPLE_DATA_UG = {
    "abstract": "A short undergraduate-level overview of the chosen field is provided here, focusing only on essentials.",
    "conclusion": "This brief conclusion sums up the key takeaway."
}

SIMPLE_DATA_PG = {
    "abstract": "A compact postgraduate-level note is generated. It captures high-level technical aspects but omits depth due to partial input.",
    "conclusion": "The conclusion is shortened, reflecting partial observation of the research focus."
}

# ----------- HELPERS -----------
def normalize_stream(stream):
    if not stream:
        return None
    s = stream.strip().lower()
    mapping = {
        "ai": "AI",
        "artificial intelligence": "AI",
        "ml": "ML",
        "machine learning": "ML",
        "cse": "CSE",
        "computer science": "CSE",
        "cs": "CSE",
        "cybersecurity": "Cybersecurity",
        "cyber": "Cybersecurity",
        "data science": "Data Science",
        "ds": "Data Science",
        "electronics": "Electronics",
        "ece": "Electronics"
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
    elif gaze == "partial":
        choice = SIMPLE_DATA_PG if level == "PG" else SIMPLE_DATA_UG
    else:
        return jsonify({"abstract": "", "conclusion": ""})

    return jsonify(choice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
