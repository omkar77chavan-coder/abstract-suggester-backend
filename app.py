from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Sample abstracts and conclusions for each stream
STREAM_ABSTRACTS = {
    'ai': """Artificial Intelligence (AI) is a transformative field that integrates computational intelligence to mimic human cognitive processes. This abstract explores the application of AI in solving complex real-world problems, emphasizing areas like machine learning, natural language processing, and robotics. We discuss how AI enhances automation, decision-making, and data analysis across diverse sectors such as healthcare, finance, and education. Key innovations in neural networks and deep learning architectures are reviewed, including convolutional and recurrent models. The paper also considers ethical concerns and future challenges. Overall, the exploration aims to provide a comprehensive overview of the role AI plays in reshaping technological landscapes.""",

    'data science': """Data Science is the interdisciplinary field that extracts actionable insights from vast datasets. This abstract highlights core methods such as data mining, visualization, and predictive analytics. Tools like Python, R, and SQL are explored in conjunction with frameworks like TensorFlow and Hadoop. The focus is on real-world case studies across industries including retail, healthcare, and marketing. Emphasis is placed on preprocessing techniques, model validation, and communication of results. Ethical considerations regarding privacy and algorithmic bias are addressed. This overview aims to capture the essence of data-driven decision-making and the value of structured, unstructured, and streaming data in modern enterprises.""",

    'ml': """Machine Learning (ML) is a dynamic subset of AI that enables systems to learn patterns from data and improve over time without explicit programming. This abstract dives into supervised, unsupervised, and reinforcement learning techniques. It evaluates common algorithms such as decision trees, SVMs, k-means, and Q-learning. We assess model accuracy, overfitting, and performance tuning methods. Special attention is given to cross-validation, confusion matrices, and ROC curves. Applications in image classification, recommendation systems, and fraud detection are discussed. This study underscores the power of ML in automating insights and building intelligent, adaptive applications.""",

    'cse': """Computer Science and Engineering (CSE) combines foundational principles of computation with practical software and hardware engineering. This abstract introduces topics ranging from algorithm design and data structures to system programming, operating systems, and database management. The paper explores recent advancements in cloud computing, distributed systems, and cybersecurity. We delve into coding paradigms like object-oriented and functional programming and highlight the significance of scalable software development. CSE serves as the backbone of modern IT solutions and digital infrastructures, empowering innovations in smart technologies and automation.""",

    'cybersecurity': """Cybersecurity is the practice of protecting systems, networks, and programs from digital threats. This abstract examines strategies for mitigating cyberattacks, including firewalls, encryption, ethical hacking, and penetration testing. The growing importance of secure coding, user authentication, and vulnerability assessment is discussed. Topics also include network security protocols, incident response plans, and regulatory compliance (e.g., GDPR, HIPAA). Real-world case studies demonstrate evolving threats like ransomware, phishing, and DDoS attacks. The field's dynamic nature demands constant vigilance and innovation to ensure digital trust in an increasingly connected world."""
}

STREAM_CONCLUSIONS = {
    'ai': """In conclusion, Artificial Intelligence continues to redefine how we interact with machines and interpret data. Its role in automating decisions and solving complex problems cannot be overstated. As the field matures, ethical governance and explainability will be crucial. Future advancements will demand interdisciplinary collaboration to unlock AI’s full potential across all domains.""",

    'data science': """In conclusion, Data Science serves as a bridge between raw information and strategic decision-making. The ability to extract value from large datasets empowers businesses and researchers alike. As technologies evolve, data scientists must navigate challenges around bias, transparency, and real-time analysis to build meaningful solutions.""",

    'ml': """In conclusion, Machine Learning is a catalyst for intelligent automation and insight generation. Its applicability across fields makes it a key component of modern systems. Continued progress in algorithm efficiency, interpretability, and ethical implementation will shape the future of ML-driven innovation.""",

    'cse': """In conclusion, Computer Science and Engineering lies at the heart of technological evolution. From code to cloud, CSE professionals play a pivotal role in shaping secure, scalable, and innovative digital ecosystems. As boundaries blur between disciplines, CSE will continue enabling breakthroughs in AI, IoT, and human-computer interaction.""",

    'cybersecurity': """In conclusion, cybersecurity is a cornerstone of digital resilience in the modern age. With threats evolving daily, the emphasis on proactive defense, policy compliance, and awareness is more critical than ever. Building a secure cyberspace requires collaboration, innovation, and unwavering commitment to protecting digital integrity."""
}


@app.route('/')
def home():
    return "✅ Abstract Generator Backend is Live"


@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    try:
        data = request.get_json()
        stream = data.get("stream", "").lower()
        text = data.get("text", "")

        print(f"[LOG] Received request for stream: {stream} | Text length: {len(text)}")

        abstract = STREAM_ABSTRACTS.get(stream)
        conclusion = STREAM_CONCLUSIONS.get(stream)

        if not abstract or not conclusion:
            return jsonify({"error": "Stream not supported or missing"}), 400

        return jsonify({
            "abstract": abstract,
            "conclusion": conclusion
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)



