from flask import Flask, request, jsonify
from flask_cors import CORS   # <-- Add this
import random

app = Flask(__name__)
CORS(app)  # <-- Enable CORS for all routes

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

    "PG": {
        "AI": [
            {
                "abstract": "Artificial Intelligence at the postgraduate level involves advanced exploration of deep learning architectures, reinforcement learning systems, and natural language understanding. This research focuses on developing scalable multi-agent environments where adaptive policies emerge through collaboration and competition. Students investigate how transformers, generative adversarial networks, and neuro-symbolic systems converge to solve complex perception and reasoning tasks. Special emphasis is placed on ethical implications, including fairness, interpretability, and algorithmic accountability. Experiments draw from healthcare diagnostics, autonomous robotics, and intelligent tutoring systems, combining real-time data with decision-making frameworks. By integrating distributed computing pipelines and advanced optimization techniques, the study highlights both opportunities and challenges in achieving robust, generalizable intelligence.",
                "conclusion": "Postgraduate AI research reveals how deep architectures and ethical rigor together define the pathway toward trustworthy intelligence."
            },
            {
                "abstract": "This postgraduate AI project examines hybrid learning systems that blend symbolic reasoning with neural computation to overcome the limitations of black-box models. Advanced study involves creating explainable decision pipelines for high-stakes environments like finance, climate modeling, and precision medicine. The methodology integrates reinforcement learning with Bayesian optimization to design policies that balance efficiency with safety. Cloud-based distributed training frameworks are implemented to scale learning across petabyte-level datasets, while ensuring model reproducibility and energy efficiency. A multi-disciplinary approach ensures alignment with cognitive science and human-computer interaction, highlighting how AI can augment rather than replace human judgment.",
                "conclusion": "By uniting symbolic and statistical paradigms, AI research offers interpretability without sacrificing performance."
            },
            {
                "abstract": "Graduate-level AI research explores generalization beyond narrow problem-solving. This study focuses on self-supervised learning, lifelong adaptation, and transferability of knowledge across domains. Experiments include training multimodal systems capable of integrating vision, speech, and structured data for holistic reasoning. Advanced theoretical frameworks are presented for analyzing convergence, uncertainty, and robustness against adversarial inputs. Applied contributions extend to smart cities, disaster response, and multilingual education technologies. Beyond technical scope, the work emphasizes the sociotechnical impact of AI, ensuring inclusion, transparency, and accountability in design. Postgraduate learners not only advance AI’s frontier but also define the ethical compass for future innovation.",
                "conclusion": "Postgraduate AI demands balancing technical depth with societal responsibility. Outcomes reinforce AI’s dual role as innovation driver and ethical challenge."
            }
        ],
        "ML": [
            {
                "abstract": "Postgraduate research in Machine Learning extends beyond introductory models to advanced approaches such as ensemble learning, probabilistic inference, and reinforcement strategies. This study investigates scalable architectures capable of handling massive datasets, with focus on deep neural networks, attention mechanisms, and online learning. Experiments apply these models to areas including genomics, speech synthesis, and environmental forecasting, highlighting trade-offs between accuracy and computational complexity. Robustness under noisy and adversarial data is evaluated, alongside interpretability frameworks like SHAP and counterfactual reasoning. Learners also study responsible AI, ensuring that algorithmic decisions align with fairness and societal expectations.",
                "conclusion": "Graduate ML work demonstrates how scalable algorithms balance prediction power with responsibility in deployment."
            },
            {
                "abstract": "This ML project explores continual learning and meta-learning, enabling models to rapidly adapt to novel tasks with minimal supervision. Leveraging gradient-based optimization and probabilistic programming, the study develops frameworks that mimic human-like generalization. Applications include adaptive healthcare, real-time fraud detection, and low-resource language translation. Methodological contributions examine stability-plasticity trade-offs, catastrophic forgetting, and curriculum design for incremental tasks. The project further emphasizes deployment challenges, focusing on energy-efficient model compression, federated learning for privacy, and edge inference pipelines for resource-constrained environments.",
                "conclusion": "Graduate ML research proves adaptability is as crucial as accuracy. Solutions pave the way for intelligent, flexible systems."
            },
            {
                "abstract": "This research investigates theoretical foundations of learning theory, focusing on generalization bounds, complexity measures, and optimization dynamics in deep architectures. Experimental work benchmarks gradient descent variants, evolutionary algorithms, and quantum-assisted optimization for large-scale ML tasks. Applications extend to drug discovery, predictive maintenance, and financial forecasting. The project incorporates cross-disciplinary perspectives, showing how insights from neuroscience and physics inspire new learning paradigms. Ethical reflections include how algorithmic bias propagates through models trained on biased data, and what interventions can mitigate harm. The emphasis is on shaping ML into a science grounded in both rigor and societal impact.",
                "conclusion": "Theoretical and applied rigor in ML defines postgraduate research. Outcomes highlight ML as both a science of patterns and a tool for change."
            }
        ],
        "CSE": [
            {
                "abstract": "Graduate Computer Science research addresses scalability, reliability, and security of computational systems. This project examines distributed consensus, blockchain resilience, and parallel architectures for processing massive graph-structured data. Advanced algorithms for NP-hard optimization are developed using heuristics and approximation strategies. Verification frameworks validate correctness of safety-critical software, while energy-efficient design principles are applied to heterogeneous architectures. Applications span aerospace navigation, large-scale search, and quantum-inspired computation. The project integrates theory and engineering, showing how rigorous design translates into real-world systems.",
                "conclusion": "Graduate CS research proves algorithmic rigor and system design together shape computing’s future."
            },
            {
                "abstract": "This postgraduate CS project investigates next-generation computing paradigms, focusing on quantum algorithms, high-performance computing, and AI-driven compiler design. Quantum-classical hybrids are benchmarked against traditional supercomputers for cryptography and optimization. Advances in operating systems enhance concurrency and memory management for massively parallel tasks. Cross-disciplinary collaborations ensure breakthroughs in computational biology and materials science. A strong emphasis is placed on bridging theoretical exploration with industry deployment, ensuring CS innovations are impactful and sustainable.",
                "conclusion": "CS research highlights emerging frontiers in quantum and HPC, shaping scientific and industrial discovery."
            },
            {
                "abstract": "This project explores formal methods, type theory, and model checking for concurrent and distributed systems. It benchmarks proof assistants like Coq and Isabelle on real vulnerabilities. Practical studies involve building secure compilers and resilient edge-computing frameworks for robotics and medical systems. By combining mathematical rigor with robust engineering, postgraduate learners demonstrate how correctness, security, and efficiency can coexist. The work reflects both theoretical sophistication and applied urgency.",
                "conclusion": "Formal methods ensure correctness at scale. Graduate CS proves why rigorous foundations are critical in safety-critical systems."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "Postgraduate Cybersecurity research investigates advanced cryptographic frameworks, threat intelligence, and intrusion detection powered by AI. This project develops homomorphic encryption schemes for secure data sharing, along with zero-trust architectures for enterprise networks. Simulations model sophisticated attacks including APTs and insider threats, while countermeasures are tested across distributed cloud environments. Learners also explore the socio-legal aspects of cyber defense, analyzing how regulation and policy intersect with technical enforcement. Practical contributions include prototypes for secure IoT deployments and forensic investigation pipelines.",
                "conclusion": "Graduate cybersecurity blends technical depth with policy insights. Resilient systems emerge at the intersection of law and code."
            },
            {
                "abstract": "This study focuses on privacy-preserving machine learning and federated analytics in hostile environments. Secure aggregation, differential privacy, and adversarial robustness are examined in the context of healthcare and finance. The research designs algorithms that safeguard confidentiality while enabling collaborative modeling across organizations. Extensive experiments test resilience under model poisoning and data exfiltration attempts. Ethical considerations address surveillance, human rights, and the geopolitics of cyber conflict, situating cybersecurity in a global context.",
                "conclusion": "Cybersecurity ensures that innovation remains aligned with privacy and rights. Graduate work expands both defense and ethics."
            },
            {
                "abstract": "This project examines hardware security, side-channel attack mitigation, and trusted execution environments. Postgraduate learners design countermeasures against cache timing attacks and electromagnetic leakage, validating them with FPGA prototypes. Integration of blockchain-based identity verification strengthens trust in decentralized ecosystems. Applications extend to secure medical devices, automotive electronics, and defense systems. The combination of low-level protection with system-wide architectures reflects the holistic scope of postgraduate cybersecurity.",
                "conclusion": "Hardware-rooted defenses complement software safeguards. Graduate cybersecurity strengthens the full digital ecosystem."
            }
        ],
        "Data Science": [
            {
                "abstract": "Postgraduate Data Science research expands into high-dimensional modeling, distributed computing, and interpretability. This work orchestrates Spark pipelines with deep neural networks to process terabytes of multi-modal data. Case studies span climate forecasting, medical imaging, and financial risk. Methods include ensemble uncertainty quantification, federated learning, and ethical auditing for bias. The project balances mathematical rigor with real-world deployment, ensuring scalable and responsible analytics.",
                "conclusion": "Graduate Data Science proves how scalable models become impactful only with ethical oversight."
            },
            {
                "abstract": "This project investigates probabilistic inference, Bayesian learning, and reinforcement strategies for uncertainty-aware prediction. Applications include personalized medicine, adaptive supply chains, and disaster response. Experiments test transferability across domains, ensuring generalizable models. Privacy-preserving computation, fairness audits, and cross-institutional collaboration through federated learning highlight the project’s applied importance. Theoretical and applied insights reinforce postgraduate training as both scientific and societal contribution.",
                "conclusion": "By quantifying uncertainty, postgraduate Data Science ensures both robustness and trustworthiness."
            },
            {
                "abstract": "This research emphasizes self-supervised learning, domain adaptation, and multi-modal reasoning in Data Science. Experiments combine textual, numerical, and image data to design models that generalize across tasks. Visualization, interpretability, and explainability are central, making outcomes actionable for policy and business. Applications include energy forecasting, public health, and global trade. The project reflects Data Science’s position as both technical practice and strategic tool for informed decision-making.",
                "conclusion": "Data Science at PG level defines how knowledge guides action. Graduate inquiry ensures evidence-driven change."
            }
        ],
        "Electronics": [
            {
                "abstract": "Postgraduate Electronics research emphasizes advanced VLSI, low-power architectures, and embedded system integration. Projects simulate transistor scaling, FinFET architectures, and reliability under stress. Mixed-signal SoC design for IoT is explored, with embedded encryption to ensure hardware security. Reliability modeling includes thermal and aging effects. Applications extend to next-generation computing hardware, secure devices, and sustainable electronics.",
                "conclusion": "Graduate Electronics balances miniaturization with reliability, ensuring progress in hardware design."
            },
            {
                "abstract": "This research investigates wireless communication, RF systems, and high-frequency circuits for 5G and beyond. Antenna arrays, spectrum-sharing algorithms, and adaptive modulation techniques are prototyped with FPGA systems. Error correction and interference management are tested for resilience in crowded channels. Applications impact both telecom infrastructure and consumer devices.",
                "conclusion": "Electronics PG research drives connectivity advances. Learners show how circuits sustain global communication."
            },
            {
                "abstract": "Graduate Electronics explores renewable energy integration and neuromorphic hardware. Projects design power electronics with SiC/GaN devices for efficiency, and neuromorphic circuits for edge AI. Battery management and grid stabilization strategies are validated with simulations and prototypes. The dual emphasis on sustainability and intelligence defines modern electronic innovation.",
                "conclusion": "Electronics research at PG level ensures technology is both green and intelligent."
            }
        ]
    }
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

    choice = choose_variant(level, stream) if gaze=="centered" else choose_variant("UG", stream)
    return jsonify(choice)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
