from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Elaborate content for each stream
stream_data = {
    "AI": {
        "abstract": "Artificial Intelligence (AI) has evolved into a transformative force across industries, redefining how machines emulate human cognition. This abstract discusses the integration of AI in modern systems, including its applications in natural language processing, computer vision, and autonomous decision-making. With the advent of deep learning and neural networks, AI has made significant strides in tasks previously considered exclusively human. From predictive analytics in healthcare to recommendation systems in e-commerce, AI is revolutionizing the digital ecosystem. This study aims to highlight the current trends, challenges, and opportunities in AI research while emphasizing ethical concerns and the need for explainable AI solutions.",
        "conclusion": "In conclusion, the field of Artificial Intelligence is entering a new era of innovation and accessibility. As AI systems become more capable and integrated into our daily lives, it is critical to prioritize ethical development, transparency, and inclusivity. Future advancements will depend on responsible research and collaboration across disciplines, ensuring that AI benefits humanity as a whole."
    },
    "Data Science": {
        "abstract": "Data Science merges statistics, computer science, and domain expertise to extract insights from vast datasets. This abstract delves into methodologies such as data preprocessing, feature engineering, and advanced analytics. It also examines the use of data science in real-world applications like fraud detection, customer segmentation, and public health forecasting. With the rise of big data technologies and cloud computing, data science is more accessible and scalable than ever. The paper explores frameworks such as Hadoop and Spark and their impact on distributed data processing.",
        "conclusion": "In summary, Data Science empowers organizations to make data-driven decisions with confidence. The discipline continues to evolve rapidly, pushing boundaries in predictive modeling and AI-driven automation. Its interdisciplinary nature ensures its relevance across sectors, from finance to healthcare and beyond."
    },
    "ML": {
        "abstract": "Machine Learning (ML) is at the heart of artificial intelligence, enabling computers to learn from data without explicit programming. This abstract outlines core ML algorithms including supervised, unsupervised, and reinforcement learning. The applications range from spam filtering and image classification to complex game-playing agents. As datasets grow in size and complexity, the role of ML becomes increasingly crucial. This work reviews techniques for improving accuracy and generalization, including regularization and ensemble methods, while acknowledging the risks of overfitting and bias.",
        "conclusion": "To conclude, Machine Learning is revolutionizing technology through its ability to adapt and improve over time. Continued research is necessary to build models that are robust, interpretable, and fair. The synergy of ML with other domains like IoT and blockchain will shape the future of intelligent systems."
    },
    "CSE": {
        "abstract": "Computer Science Engineering (CSE) encompasses the design, analysis, and implementation of computer systems and software. This abstract covers foundational areas such as algorithms, data structures, operating systems, and computer networks. With the growing importance of cybersecurity and cloud computing, CSE plays a pivotal role in both academia and industry. The paper highlights innovations in compiler design, database management systems, and software engineering practices. Furthermore, it evaluates the role of CSE in shaping emerging technologies like quantum computing and blockchain.",
        "conclusion": "In conclusion, CSE continues to be a cornerstone of technological progress. As the field evolves, it is essential to equip students and professionals with both theoretical knowledge and practical skills. The future of CSE lies in interdisciplinary integration and continuous innovation."
    },
    "Cybersecurity": {
        "abstract": "Cybersecurity has become a critical concern in the digital age, where data breaches and cyberattacks are increasingly common. This abstract explores strategies for securing networks, systems, and data. Topics include encryption, intrusion detection systems, access control, and cybersecurity frameworks like NIST. It examines real-world incidents and the lessons learned from them, emphasizing proactive defense mechanisms and user awareness. The paper also addresses the growing threat of AI-powered attacks and the role of ethical hacking.",
        "conclusion": "To summarize, cybersecurity is not just a technical issue but a strategic priority for individuals, businesses, and governments. Building a resilient cyber defense requires continuous learning, vigilance, and adaptation to emerging threats. As technology advances, so must our strategies to protect digital assets."
    }
}

@app.route('/')
def home():
    return "✅ Smart Abstract Backend is Running!"

@app.route('/suggest', methods=['POST'])
def suggest_abstract():
    try:
        data = request.get_json()
        text = data.get('text', '')
        stream = data.get('stream', 'AI').strip()

        response = {
            "abstract": stream_data.get(stream, stream_data["AI"])["abstract"],
            "conclusion": stream_data.get(stream, stream_data["AI"])["conclusion"]
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

    app.run(debug=True)



