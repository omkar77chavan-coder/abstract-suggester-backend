from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Store last used variation per stream+level to avoid repetition
last_used = {}

# Variation data
abstract_variations = {
    "UG": {
        "AI": [
            "Artificial Intelligence is transforming industries by automating decision-making, enhancing productivity, and enabling machines to perform human-like tasks.",
            "AI uses algorithms and data-driven approaches to simulate human intelligence, creating solutions that adapt and learn from new information.",
            "From virtual assistants to predictive analytics, AI is a growing field offering innovative tools for everyday applications."
        ],
        "Data Science": [
            "Data Science focuses on extracting valuable insights from large datasets using statistical methods and computational tools.",
            "By combining programming, math, and domain knowledge, data science helps organizations make data-driven decisions.",
            "Applications range from trend analysis to predictive modeling, transforming data into actionable strategies."
        ],
        "ML": [
            "Machine Learning allows systems to learn and improve from experience without explicit programming.",
            "By identifying patterns in data, ML enables automation in areas like speech recognition, recommendation systems, and fraud detection.",
            "ML bridges the gap between raw data and intelligent action, driving smarter decision-making."
        ],
        "CSE": [
            "Computer Science and Engineering integrates hardware, software, and computational theory to solve real-world problems.",
            "CSE equips learners with skills in coding, algorithms, and system design for diverse technology careers.",
            "From app development to AI, CSE is a versatile discipline with global opportunities."
        ],
        "Cybersecurity": [
            "Cybersecurity protects systems, networks, and data from digital attacks and unauthorized access.",
            "It involves preventive measures, detection systems, and response strategies to ensure data integrity and privacy.",
            "With rising cyber threats, cybersecurity skills are essential in all digital sectors."
        ]
    },
    "PG": {
        "AI": [
            "Artificial Intelligence encompasses deep learning architectures, reinforcement learning paradigms, and advanced NLP techniques driving autonomous decision-making in complex systems.",
            "Leveraging high-dimensional datasets, AI integrates symbolic reasoning with neural computation for robust, adaptive intelligence in dynamic environments.",
            "AI research at the postgraduate level emphasizes scalable architectures, ethical frameworks, and cross-domain deployment strategies."
        ],
        "Data Science": [
            "Postgraduate Data Science integrates advanced statistical inference, machine learning models, and big data frameworks for high-impact analytics.",
            "Leveraging distributed computing and feature engineering, it delivers predictive and prescriptive insights for strategic decision-making.",
            "Research-driven data science focuses on model interpretability, algorithmic fairness, and deployment optimization."
        ],
        "ML": [
            "Advanced Machine Learning explores ensemble techniques, deep neural architectures, and self-supervised paradigms for high-dimensional data processing.",
            "It includes optimization algorithms, regularization strategies, and transfer learning for efficient model generalization.",
            "Postgraduate ML applications include autonomous systems, biomedical informatics, and large-scale personalization engines."
        ],
        "CSE": [
            "Postgraduate CSE delves into distributed systems, advanced compiler design, and algorithmic complexity for high-performance computing.",
            "It integrates theoretical computing models with cutting-edge software engineering and AI systems.",
            "CSE at this level emphasizes scalable architectures, secure protocols, and innovation-driven problem solving."
        ],
        "Cybersecurity": [
            "Advanced Cybersecurity focuses on zero-trust architectures, cryptographic protocols, and AI-driven threat intelligence systems.",
            "It includes blockchain security, quantum-safe cryptography, and proactive vulnerability assessment frameworks.",
            "Postgraduate research addresses adaptive defense strategies against sophisticated and evolving cyber threats."
        ]
    }
}

conclusion_variations = {
    "UG": {
        "AI": [
            "AI offers immense potential for simplifying complex tasks, fostering innovation across industries.",
            "The continuous evolution of AI tools promises improved efficiency and accessibility.",
            "Students in AI can look forward to contributing to impactful and diverse projects."
        ],
        "Data Science": [
            "Data Science empowers decision-making with clarity and precision.",
            "Emerging tools in data analytics promise even more robust predictive capabilities.",
            "The field offers vast opportunities for research, industry, and entrepreneurship."
        ],
        "ML": [
            "Machine Learning is a key enabler of modern automation and personalization.",
            "It is a rapidly expanding field with applications in almost every domain.",
            "The future of ML is boundless, with innovation at its core."
        ],
        "CSE": [
            "CSE forms the foundation of many modern technological innovations.",
            "Graduates can explore careers from software development to AI research.",
            "The discipline remains vital to solving global digital challenges."
        ],
        "Cybersecurity": [
            "Cybersecurity is essential for protecting the digital backbone of society.",
            "With technology growth, security expertise will only become more critical.",
            "The field promises rewarding careers safeguarding vital data and infrastructure."
        ]
    },
    "PG": {
        "AI": [
            "AI at the postgraduate level demands a deep understanding of algorithms, scalability, and ethical AI deployment.",
            "Research opportunities in AI are vast, influencing policy, technology, and innovation.",
            "Graduates can lead the development of next-gen intelligent systems across domains."
        ],
        "Data Science": [
            "Postgraduate Data Science equips professionals to tackle large-scale, high-stakes analytical problems.",
            "Advanced analytics will shape industries by delivering deeper, actionable insights.",
            "Research-level work drives algorithmic innovation and business transformation."
        ],
        "ML": [
            "Postgraduate ML fosters innovation in adaptive systems and cross-domain AI applications.",
            "It enables breakthroughs in fields like precision medicine and autonomous technologies.",
            "Graduates are poised to contribute to cutting-edge AI research globally."
        ],
        "CSE": [
            "Advanced CSE prepares professionals for leadership roles in research and technology development.",
            "It builds the expertise to design secure, efficient, and scalable systems.",
            "The discipline remains critical to technological and societal progress."
        ],
        "Cybersecurity": [
            "Postgraduate cybersecurity develops leaders in proactive threat prevention and digital resilience.",
            "Graduates can shape global standards in data protection and cyber defense.",
            "It offers opportunities to pioneer advancements in secure technology infrastructures."
        ]
    }
}

def get_non_repeating_variation(level, stream, data_dict):
    global last_used
    options = data_dict[level][stream]
    last_index = last_used.get((level, stream), -1)
    
    available_indices = [i for i in range(len(options)) if i != last_index]
    chosen_index = random.choice(available_indices)
    
    last_used[(level, stream)] = chosen_index
    return options[chosen_index]

@app.route("/suggest", methods=["POST"])
def suggest():
    user_data = request.json
    stream = user_data.get("stream")
    level = user_data.get("academicLevel")
    gaze_status = user_data.get("gazeStatus", "centered")

    if not stream or not level:
        return jsonify({"error": "Missing required fields"}), 400

    # If gaze is off-center, force UG simple output
    if gaze_status != "centered":
        level = "UG"

    abstract = get_non_repeating_variation(level, stream, abstract_variations)
    conclusion = get_non_repeating_variation(level, stream, conclusion_variations)

    return jsonify({"abstract": abstract, "conclusion": conclusion})

if __name__ == "__main__":
    app.run(debug=True)
