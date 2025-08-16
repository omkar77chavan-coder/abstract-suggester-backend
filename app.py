ffrom flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Track last used index to prevent repetition
last_used = {"UG": {}, "PG": {}}

# Data: 5 streams × 2 levels (UG/PG) × 3 variations each (abstract + conclusion)
abstracts_data = {
    "UG": {
        "AI": [
            {
                "abstract": "Artificial Intelligence is transforming industries by automating simple decision-making and assisting human tasks with long descriptive approaches suitable for beginner-level understanding...",
                "conclusion": "In conclusion, Artificial Intelligence offers foundational opportunities for students to learn, experiment, and explore its potential in shaping the future."
            },
            {
                "abstract": "At the undergraduate level, AI is introduced as a broad concept covering algorithms, data handling, and rule-based systems with practical examples that make learning engaging...",
                "conclusion": "In conclusion, undergraduate study of AI provides learners with a strong yet simple platform to explore problem-solving methods with technology."
            },
            {
                "abstract": "AI in early studies emphasizes concepts like supervised learning, search algorithms, and knowledge representation, explained in accessible terms with straightforward examples...",
                "conclusion": "In conclusion, by starting simple, undergraduates can develop confidence in AI and gradually move toward advanced applications."
            }
        ],
        "Data Science": [
            {
                "abstract": "Data Science for undergraduates focuses on basic data cleaning, visualization, and interpreting patterns in large datasets through simple and understandable techniques...",
                "conclusion": "In conclusion, undergraduate Data Science makes students aware of how raw data can be converted into meaningful stories and insights."
            },
            {
                "abstract": "Students at UG level explore descriptive statistics, spreadsheets, and beginner-friendly tools that allow them to experiment with simple data-driven questions...",
                "conclusion": "In conclusion, the undergraduate journey in Data Science emphasizes clarity, simplicity, and developing curiosity about working with data."
            },
            {
                "abstract": "Through introductory projects, undergraduates learn how to organize data, perform simple analysis, and visualize trends in ways that build strong foundational skills...",
                "conclusion": "In conclusion, the UG path in Data Science equips learners with practical exposure to understanding information step by step."
            }
        ],
        "ML": [
            {
                "abstract": "Machine Learning at the undergraduate level introduces classification, regression, and clustering through long but accessible explanations with hands-on projects...",
                "conclusion": "In conclusion, undergraduates benefit by learning how machines can gradually improve from data in simple scenarios."
            },
            {
                "abstract": "Students begin with small datasets and easy-to-understand models such as decision trees and linear regression, taught with descriptive detail...",
                "conclusion": "In conclusion, UG-level ML serves as a foundation for future exploration into more complex predictive systems."
            },
            {
                "abstract": "Undergraduate ML learning emphasizes experimentation with simple algorithms, real-life case studies, and a narrative style that fosters easy understanding...",
                "conclusion": "In conclusion, UG learners gain a practical sense of how machines can identify patterns and make predictions."
            }
        ],
        "CSE": [
            {
                "abstract": "Computer Science and Engineering undergraduates explore algorithms, programming basics, and computing systems through long explanatory modules and introductory projects...",
                "conclusion": "In conclusion, UG-level CSE prepares learners for solving problems by combining theory and practice in accessible ways."
            },
            {
                "abstract": "At the undergraduate stage, CSE introduces structured programming, problem decomposition, and networking concepts with simple illustrative examples...",
                "conclusion": "In conclusion, UG CSE builds the foundation for designing and understanding computer-based solutions."
            },
            {
                "abstract": "UG learners are guided through database systems, operating systems, and software engineering principles in approachable, descriptive terms...",
                "conclusion": "In conclusion, UG CSE establishes fundamental knowledge of how computing frameworks work in daily life."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "Cybersecurity for undergraduates emphasizes password safety, encryption basics, and recognizing simple cyber threats explained in a clear narrative...",
                "conclusion": "In conclusion, undergraduate Cybersecurity highlights awareness and prevention as the first steps toward digital safety."
            },
            {
                "abstract": "Students learn how to protect information, understand access control, and build habits of secure browsing in descriptive and easy lessons...",
                "conclusion": "In conclusion, UG Cybersecurity introduces basic strategies to protect both individuals and organizations from attacks."
            },
            {
                "abstract": "With practical examples, UG-level Cybersecurity emphasizes threats like phishing, malware, and highlights tools for maintaining system integrity...",
                "conclusion": "In conclusion, undergraduate Cybersecurity fosters awareness and practical approaches to ensuring safe use of technology."
            }
        ]
    },
    "PG": {
        "AI": [
            {
                "abstract": "Postgraduate-level Artificial Intelligence integrates deep learning, reinforcement learning, and explainable AI with emphasis on technical accuracy and domain-specific use cases...",
                "conclusion": "In conclusion, PG-level AI highlights advanced methods that balance performance, interpretability, and innovation in research applications."
            },
            {
                "abstract": "AI research at PG level involves neural architectures, multimodal systems, and optimization strategies aimed at solving complex domain-specific problems...",
                "conclusion": "In conclusion, PG-level AI establishes a rigorous platform for advancing machine capabilities in specialized fields."
            },
            {
                "abstract": "Postgraduate learners in AI explore state-of-the-art generative models, symbolic reasoning, and hybrid systems with practical implementations...",
                "conclusion": "In conclusion, advanced AI studies emphasize creating scalable, efficient, and human-centered intelligent systems."
            }
        ],
        "Data Science": [
            {
                "abstract": "PG Data Science integrates advanced statistical learning, Bayesian methods, and large-scale computing pipelines for highly accurate predictions...",
                "conclusion": "In conclusion, postgraduate Data Science is about precision, scalability, and domain-adapted analytical techniques."
            },
            {
                "abstract": "Students explore distributed systems, ETL pipelines, and predictive analytics tailored for real-world, high-volume datasets...",
                "conclusion": "In conclusion, PG-level Data Science fosters mastery of techniques that scale with big data challenges."
            },
            {
                "abstract": "PG studies emphasize model generalization, optimization of features, and integration of contextual domain knowledge into analysis...",
                "conclusion": "In conclusion, postgraduate Data Science demonstrates the strategic value of analytics across industries."
            }
        ],
        "ML": [
            {
                "abstract": "Postgraduate Machine Learning explores ensemble techniques, meta-learning, and hyperparameter optimization with a focus on model interpretability...",
                "conclusion": "In conclusion, PG ML emphasizes balancing accuracy, efficiency, and transparency in predictive models."
            },
            {
                "abstract": "Students at PG level focus on transfer learning, federated learning, and deep reinforcement learning frameworks...",
                "conclusion": "In conclusion, PG Machine Learning highlights advanced solutions designed for complex and sensitive domains."
            },
            {
                "abstract": "Research emphasizes fairness, explainability, and scalability of ML models across specialized industries...",
                "conclusion": "In conclusion, postgraduate ML enables researchers to craft adaptive solutions suited for evolving challenges."
            }
        ],
        "CSE": [
            {
                "abstract": "PG Computer Science and Engineering investigates blockchain systems, edge computing, and compiler optimizations for advanced efficiency...",
                "conclusion": "In conclusion, PG-level CSE fosters contributions to distributed systems, quantum-safe algorithms, and performance-driven software."
            },
            {
                "abstract": "Research includes parallel architectures, algorithmic complexity, and hardware-software co-design for specialized tasks...",
                "conclusion": "In conclusion, PG CSE demonstrates mastery of designing advanced computing frameworks for research and industry."
            },
            {
                "abstract": "Postgraduate learners explore secure distributed environments, optimization strategies, and performance-driven architectures...",
                "conclusion": "In conclusion, PG CSE emphasizes tackling challenges of scalability, speed, and system reliability."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "PG Cybersecurity emphasizes post-quantum cryptography, anomaly detection, and zero-trust systems to secure high-stakes data...",
                "conclusion": "In conclusion, PG Cybersecurity integrates proactive strategies that address evolving global cyber risks."
            },
            {
                "abstract": "Research includes blockchain-based identity management, advanced cryptographic methods, and intelligent intrusion detection...",
                "conclusion": "In conclusion, postgraduate Cybersecurity cultivates deep expertise in protecting systems against emerging threats."
            },
            {
                "abstract": "PG-level Cybersecurity combines automation frameworks, intelligence aggregation, and privacy-preserving techniques...",
                "conclusion": "In conclusion, postgraduate Cybersecurity ensures holistic and adaptive strategies for securing critical infrastructures."
            }
        ]
    }
}


@app.route('/suggest', methods=['POST'])
def suggest():
    data = request.json
    stream = data.get("stream")
    academic_level = data.get("academicLevel")
    gaze_status = data.get("gazeStatus", "unstable")

    if not stream or not academic_level:
        return jsonify({"error": "Missing required fields"}), 400

    # Validate level and stream
    if academic_level not in abstracts_data or stream not in abstracts_data[academic_level]:
        return jsonify({"error": "Invalid academic level or stream"}), 400

    variations = abstracts_data[academic_level][stream]

    # If gaze unstable → no response
    if gaze_status == "unstable":
        return jsonify({"error": "Unstable gaze detected. Please stabilize your view."}), 400

    # If off-center → pick variation 0 (simpler)
    if gaze_status == "off-center":
        selected = variations[0]
    else:
        # Avoid repeating last index
        prev_index = last_used[academic_level].get(stream, -1)
        idx_choices = [i for i in range(len(variations)) if i != prev_index]
        idx = random.choice(idx_choices)
        selected = variations[idx]
        last_used[academic_level][stream] = idx

    return jsonify({
        "abstract": selected["abstract"],
        "conclusion": selected["conclusion"]
    })


if __name__ == '__main__':
    app.run(debug=True)
