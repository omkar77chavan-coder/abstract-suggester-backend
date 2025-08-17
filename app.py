from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# ============================================================
# FULL DATASET (UG + PG)
# - UG: solid but shorter paragraphs
# - PG: super long & technical paragraphs
# - 6 streams × 3 variants each
# ============================================================
VARIANTS = {
    "UG": {
        "AI": [
            {
                "abstract": "This undergraduate project in Artificial Intelligence explores foundational approaches to intelligent problem solving through search, knowledge representation, and introductory supervised learning. Students implement breadth-first and A* search to understand optimality and complexity trade-offs, and build small rule-based agents that encode domain knowledge in transparent ways. The work includes a compact classification pipeline using decision trees over curated datasets, highlighting feature selection and simple error analysis. Emphasis is placed on readable implementations and reflective reports that connect algorithm behavior to real outcomes.",
                "conclusion": "Results show that core AI techniques can be effectively learned via compact, well-scaffolded projects, building clear intuition for state spaces, heuristics, and data-driven generalization that prepares students for deeper AI study."
            },
            {
                "abstract": "Undergraduate AI learning is most effective when theory is paired with hands-on prototyping. This study focuses on rule-based reasoning for simple diagnostics, finite-state agents for game dynamics, and a small convolution-free image classifier to demystify the pipeline from raw data to predictions. Students compare confusion matrices across baseline and tuned models to see where assumptions break. Ethical framing is introduced early by analyzing failure modes and dataset bias using short, structured reflection templates.",
                "conclusion": "The project concludes that transparent baselines and structured evaluation cultivate healthy skepticism and technical confidence, ensuring learners grasp both the capabilities and limits of early AI systems."
            },
            {
                "abstract": "This AI project emphasizes classical planning and lightweight learning methods. Students encode problems in a planning formalism, evaluate heuristic quality, and contrast that with data-driven classification on tabular datasets. They also explore simple knowledge graphs to appreciate how structure guides inference. The iterative process—formulate, implement, assess—helps learners understand why AI decomposes problems into search, representation, and learning components.",
                "conclusion": "Findings support the value of mixed classical and statistical perspectives at the undergraduate level, giving students a durable conceptual map for advanced AI topics."
            }
        ],
        "ML": [
            {
                "abstract": "This undergraduate Machine Learning project introduces supervised learning with linear and logistic regression, decision trees, and k-nearest neighbors. Students run controlled experiments with training/validation splits, apply basic normalization, and track accuracy, precision, recall, and F1 scores. Small ablation studies reveal the impact of noisy features and class imbalance, while error inspection clarifies when simple models are sufficient versus when they underfit.",
                "conclusion": "The work demonstrates that carefully scoped datasets and transparent metrics help beginners internalize the ML workflow and recognize the trade-offs between simplicity and performance."
            },
            {
                "abstract": "Hands-on ML practice is built around reproducible pipelines. This study guides students through data cleaning, feature engineering with one-hot encoding, and baseline models, followed by incremental tuning. Learners practice k-fold cross-validation and maintain experiment logs to prevent cherry-picking. A final comparison across models highlights the tension between interpretability and accuracy in early-stage projects.",
                "conclusion": "The project concludes that disciplined evaluation and small, explainable models offer the best learning ROI for undergraduates entering ML."
            },
            {
                "abstract": "The focus of this ML project is approachable unsupervised learning. Students implement k-means and hierarchical clustering, discuss initialization sensitivity, and visualize clusters to understand separability limits. A lightweight PCA step illustrates variance capture and dimensionality reduction in practice. Short reflections clarify how unsupervised structure can inform supervised tasks downstream.",
                "conclusion": "Results indicate that even minimal unsupervised tooling adds value to student intuition, making later supervised modeling more principled and data-aware."
            }
        ],
        "CSE": [
            {
                "abstract": "This undergraduate Computer Science project blends data structures with algorithmic analysis. Students implement lists, stacks, queues, and hash maps, profiling operations to link asymptotic complexity with real timings. They then apply these structures to a toy search engine that indexes short documents, emphasizing modular design, unit tests, and readable interfaces. Code reviews reinforce naming, documentation, and clean separation of concerns.",
                "conclusion": "Outcomes confirm that disciplined structure-first development improves correctness and performance, forming a foundation for robust software engineering practices."
            },
            {
                "abstract": "Students explore the pillars of computing by building a microservice that exposes CRUD operations, connects to a lightweight database, and logs requests for debugging and observability. They compare iterative versus recursive solutions in hot paths and measure impact on stack depth, readability, and latency. A final reflection connects theoretical complexity to practical system behavior.",
                "conclusion": "The course project shows that seeing algorithms in the context of I/O, persistence, and concurrency helps undergraduates transition from toy problems to real systems."
            },
            {
                "abstract": "This project centers on algorithmic problem solving with emphasis on sorting, searching, and graph traversal. Students analyze constant factors in addition to big-O to appreciate engineering trade-offs. A small benchmarking harness encourages hypothesis-driven optimization, while a style guide ensures the code remains maintainable as complexity grows.",
                "conclusion": "Findings suggest that methodical measurement and clean code habits are as crucial as asymptotic reasoning in day-to-day software development."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "This undergraduate cybersecurity project introduces confidentiality, integrity, and availability through labs in hashing, salted password storage, and basic symmetric encryption. Students practice threat modeling for a small web app, then validate mitigations with controlled injection and XSS tests in a sandbox. Checklists and incident reports teach structured thinking during triage.",
                "conclusion": "Early, realistic exercises create durable security hygiene and foster a prevention mindset that students carry into larger software efforts."
            },
            {
                "abstract": "Students perform guided penetration testing on intentionally vulnerable services, documenting each step from reconnaissance to reporting. They compare rate-limited versus unprotected endpoints and evaluate basic WAF rules. The exercise underscores lawful, ethical boundaries and emphasizes reproducible scripts rather than ad-hoc clicking.",
                "conclusion": "Results highlight that process discipline and documentation are as important as tooling in cultivating responsible security practice."
            },
            {
                "abstract": "Network security fundamentals are taught via packet inspection and simple IDS rules. Learners label traffic captures, create signatures for obvious anomalies, and discuss false positives. They also review secure defaults for TLS and cookie handling in a tiny demo site to connect protocol theory with application behavior.",
                "conclusion": "Students gain actionable intuition for defense-in-depth and the value of secure-by-default configurations."
            }
        ],
        "Data Science": [
            {
                "abstract": "This undergraduate data science project walks through the full lifecycle: data acquisition, cleaning, EDA, modeling, and communication. Students use descriptive statistics and visualizations to reveal distributions and outliers, then fit baseline regression or classification models. A short dashboard communicates results to non-technical audiences with careful caveats.",
                "conclusion": "The project confirms that storytelling and transparency are integral to responsible, beginner-friendly data science."
            },
            {
                "abstract": "Predictive modeling is explored with attention to leakage, target imbalance, and proper splits. Students implement cross-validation and compare ROC-AUC to accuracy for skewed classes. Simple calibration reveals over-confident probability outputs and motivates post-processing steps.",
                "conclusion": "Findings show that basic guarding against leakage and imbalance has an outsized effect on trustworthy predictions."
            },
            {
                "abstract": "Students practice unsupervised discovery using clustering on mixed data, followed by PCA for dimensionality reduction. Visual summaries help communicate structure to stakeholders, and short write-ups explain when unsupervised insights are actionable.",
                "conclusion": "The work demonstrates that even minimal unsupervised methods can enrich downstream supervised learning and analysis planning."
            }
        ],
        "Electronics": [
            {
                "abstract": "This undergraduate electronics project develops a low-cost environmental monitor using a microcontroller, temperature and air-quality sensors, and a basic LCD. Students design and simulate simple analog front-ends, then validate measurements against references. Emphasis is placed on noise considerations, debouncing, and power budgeting for battery operation.",
                "conclusion": "The prototype shows how disciplined measurement and iteration translate theory into practical, reliable circuits."
            },
            {
                "abstract": "Learners build a traffic signal controller with timers, counters, and finite-state logic, then migrate to a microcontroller version with interrupt handling. They compare propagation delay and flexibility across the two designs and document edge cases like pedestrian overrides.",
                "conclusion": "Results emphasize that understanding both discrete logic and firmware yields better architectural choices for embedded systems."
            },
            {
                "abstract": "A wearable heart-rate monitor is prototyped with an optical sensor, analog amplification, and digital filtering. Students characterize sensor placement, motion artifacts, and sampling strategies while validating readings against a commercial device.",
                "conclusion": "The project underscores the value of signal conditioning and empirical testing in bio-instrumentation."
            }
        ]
    },
    "PG": {
        "AI": [
            {
                "abstract": "This postgraduate study investigates deep reinforcement learning for embodied control with emphasis on sample efficiency, stability, and safe deployment. We implement proximal policy optimization with generalized advantage estimation and curriculum schedules that gradually increase environment difficulty. To mitigate distributional shift, we employ domain randomization and off-policy auxiliary replay. We analyze variance reduction via baseline design, examine catastrophic forgetting in non-stationary tasks, and incorporate constrained optimization to satisfy safety invariants. Ablations quantify sensitivity to reward shaping, entropy regularization, and clipping thresholds across continuous control benchmarks, while wall-clock profiling explains throughput scaling under mixed precision.",
                "conclusion": "Findings indicate that careful interaction between algorithmic choices and environment design is decisive for stability and generalization, and that principled safety constraints can be integrated without prohibitive performance loss in modern actor-critic pipelines."
            },
            {
                "abstract": "We explore interpretable neural modeling by combining attention mechanisms with prototype-based layers to yield faithful, human-auditable rationales. A distillation framework transfers knowledge from high-capacity transformers to sparse concept bottlenecks, preserving task performance while exposing semantically meaningful factors. We formalize faithfulness via counterfactual consistency and report robustness under spurious-correlation stress tests. Case studies in clinical triage and contract analysis demonstrate that explanations enable more precise error triage and governance alignment. Hardware-aware pruning and quantization keep latency within strict SLAs for regulated domains.",
                "conclusion": "The results show that interpretability need not be an afterthought: with targeted architectural inductive biases and evaluation criteria, transparency can coexist with accuracy, robustness, and deployment efficiency in high-stakes AI."
            },
            {
                "abstract": "This work studies multimodal foundation models for video-text reasoning under low-resource adaptation. We investigate parameter-efficient fine-tuning (LoRA, adapters) and retrieval-augmented prompting with structured memory. A temporal alignment module integrates tubelet tokenization with cross-attention that respects motion dynamics. We benchmark zero-shot and few-shot generalization, quantify compute-accuracy trade-offs, and analyze failure cases including temporal hallucination and object identity drift. A deployment section details vector indexing, streaming inference, and content safety filters for production workflows.",
                "conclusion": "Our evaluation suggests that judicious parameter-efficient strategies and temporal priors achieve strong transfer while keeping adaptation affordable, enabling practical multimodal reasoning in resource-constrained settings."
            }
        ],
        "ML": [
            {
                "abstract": "This postgraduate ML research examines optimization landscapes of over-parameterized networks with emphasis on implicit bias and generalization. We analyze training dynamics under adaptive methods versus SGD with momentum, derive conditions where flat minima correlate with out-of-distribution robustness, and propose a Hessian-aware schedule that balances curvature exploration with stability. Experiments on vision and tabular benchmarks include sharpness-aware minimization, label smoothing interactions, and mixup regularization. We report calibration metrics, reliability diagrams, and selective prediction curves, linking geometry to actionable deployment guarantees.",
                "conclusion": "Empirical and theoretical evidence converges on a practical recipe: curvature-sensitive training with modest regularizers yields models that are measurably more reliable under plausible distribution shifts without sacrificing in-distribution accuracy."
            },
            {
                "abstract": "We present a federated learning framework with differential privacy and secure aggregation designed for heterogeneous client populations. Our method adapts aggregation weights via server-side meta-learning, accounts for non-IID drift, and schedules clients with fairness constraints. We quantify privacy-utility trade-offs across ε budgets, evaluate stragglers and partial participation, and demonstrate throughput improvements using sparse updates with error feedback. A resource section details communication compression and on-device quantization for realistic mobile deployments.",
                "conclusion": "Results indicate that privacy-preserving FL can achieve competitive accuracy when heterogeneity is modeled explicitly and communication is engineered holistically, enabling production-grade learning on sensitive, distributed data."
            },
            {
                "abstract": "This study evaluates graph neural networks with structure-inductive priors for scientific discovery. We integrate equivariant message passing with physics-informed losses and compare spectral and spatial formulations across molecular property prediction and materials design tasks. Uncertainty is quantified via deep ensembles and evidential regression. Active-learning loops propose candidates subject to domain constraints and cost bounds, while ablations isolate the contribution of symmetry encoding and positional encodings. Practical notes cover batching strategies and mixed precision for large graphs.",
                "conclusion": "Encoding scientific symmetries directly into ML architectures delivers sample efficiency and robustness, accelerating closed-loop discovery when paired with principled uncertainty estimation and cost-aware acquisition."
            }
        ],
        "CSE": [
            {
                "abstract": "We design and verify a high-concurrency storage engine that combines log-structured merges with hybrid page caching and epoch-based reclamation. Formal specifications in TLA+ capture crash-consistency invariants; model checking reveals corner cases in compaction and write-ahead logging. We implement optimistic concurrency control with adaptive backoff and show tail-latency reductions under mixed OLTP/OLAP workloads. A profiling study attributes wins to cache residency heuristics and vectorized operators, while chaos testing validates failure handling under process and disk faults.",
                "conclusion": "The work demonstrates that rigorous specification, targeted concurrency control, and careful cache policy co-design yield tangible reliability and latency benefits for modern data systems."
            },
            {
                "abstract": "This project presents a compiler toolchain with SSA-based IR, polyhedral scheduling for loop nests, and auto-tuning of memory layouts targeting GPUs. We integrate alias analysis with cost models to guide fusion/fission and use region-based allocation to reduce allocator churn. End-to-end benchmarks show speedups on dense linear algebra and stencil kernels; code size remains manageable via profile-guided specialization. A validation suite ensures numerical stability and deterministic builds.",
                "conclusion": "Our results confirm that principled IR design plus auto-tuning closes a large fraction of the gap to hand-tuned kernels while keeping builds reproducible and maintainable."
            },
            {
                "abstract": "We prototype a self-healing microservice architecture that blends circuit breakers, quorum reads/writes, and autoscaling driven by SLO-aware controllers. Formal latency SLOs steer scaling and queue shaping; distributed tracing pinpoints propagation delays. We quantify brownout strategies for overload mitigation and evaluate progressive delivery with canary analysis and automatic rollback. Security baselines include mTLS, short-lived certs, and policy-as-code for zero-trust segments.",
                "conclusion": "The study shows that reliability emerges from layered resilience patterns coupled with measurable SLOs and automated guardrails rather than ad-hoc patches."
            }
        ],
        "Cybersecurity": [
            {
                "abstract": "We investigate post-quantum cryptography deployment in hybrid TLS with lattice-based KEMs and signatures. Compatibility tests cover handshake sizes, CPU costs, and fallback strategies; we analyze downgrade resistance and side-channel considerations on commodity hardware. Formal reasoning validates key reuse safety and certificate chains. Operational guidance addresses monitoring, alerting on cipher changes, and staged rollout to high-latency geos.",
                "conclusion": "Hybrid PQC in TLS is deployable today with careful parameter choices and rollout hygiene, offering forward secrecy against quantum adversaries while preserving ecosystem interoperability."
            },
            {
                "abstract": "This research develops anomaly-aware intrusion detection using representation learning with contrastive pretraining on raw network flows. The system integrates active learning with analyst feedback loops and uses cost-sensitive loss to triage high-impact alerts. We evaluate on mixed enterprise traffic, quantify evasion robustness, and present an interpretable casebook that maps latent clusters to analyst-friendly labels.",
                "conclusion": "Anomaly detection augmented by human-in-the-loop feedback increases precision at fixed recall and accelerates incident response through interpretable, continuously improving models."
            },
            {
                "abstract": "We study socio-technical risks by modeling phishing susceptibility with behavioral signals and contextual policy enforcement. A randomized field trial compares training modalities, just-in-time prompts, and simulated campaigns. Results indicate durable gains when training is paired with friction-light policy nudges. Governance guidance covers metrics, red-teaming protocols, and privacy-respecting telemetry.",
                "conclusion": "Human-centric controls, when integrated with technical defenses, materially reduce successful phishing while maintaining employee trust and productivity."
            }
        ],
        "Data Science": [
            {
                "abstract": "This postgraduate data science work addresses causal inference at scale. We combine doubly robust learners with orthogonalization and evaluate identifiability under measured confounding with sensitivity analyses. Heterogeneous treatment effects are estimated via causal forests and meta-learners; we validate with synthetic controls and staggered adoption designs. Reproducibility is enforced through lineage tracking and declarative pipelines; governance includes PII minimization and audit trails.",
                "conclusion": "Our findings show that with disciplined identification strategies and reproducible pipelines, large-scale causal claims can be both credible and operationally tractable for policy and product decisions."
            },
            {
                "abstract": "We present streaming analytics with approximate query processing and probabilistic sketches for cardinality, heavy hitters, and quantiles. A windowed feature store supports near-real-time models with drift detection and automatic retraining gates. We quantify latency/accuracy trade-offs, discuss watermarking and exactly-once guarantees, and integrate cost-aware autoscaling to meet strict SLAs.",
                "conclusion": "The system demonstrates that principled approximation paired with tight MLOps yields timely, cost-efficient insights without sacrificing reliability in production streams."
            },
            {
                "abstract": "This research integrates interpretable Bayesian modeling with multimodal data—text, images, and graphs—via amortized variational inference. We provide calibrated uncertainty estimates and propagate them to decision layers with utility-sensitive thresholds. A human-in-the-loop UI supports counterfactual exploration and model debugging; audits document dataset shifts and fairness diagnostics.",
                "conclusion": "Results indicate that uncertainty-aware, interpretable DS workflows improve trust and decision quality, especially where costs of error are asymmetric and evolving."
            }
        ],
        "Electronics": [
            {
                "abstract": "We develop a low-power, near-sensor ML accelerator using quantized operators and event-driven processing. A co-designed toolflow maps tiny CNNs onto a tiled architecture with scratchpad memories and DMA engines. Post-layout results in 28nm show energy/inf trade-offs versus microcontroller baselines. Robustness to voltage scaling and temperature drift is validated; firmware exposes primitives for adaptive quality modes.",
                "conclusion": "Tight HW/SW co-design delivers meaningful ML throughput under severe power budgets, enabling always-on perception in embedded and IoT form factors."
            },
            {
                "abstract": "This project implements a mixed-signal front-end for biomedical sensing with chopper-stabilized amplifiers, programmable gain, and SAR ADC readout. We characterize 1/f noise, input-referred offset, and CMRR over physiological ranges. A digital backend performs artifact suppression with adaptive filters and on-chip compression. Safety considerations include isolation, fault detection, and watchdog resets.",
                "conclusion": "Measured performance validates that careful analog design plus modest DSP yields clinical-grade signals while meeting power and safety constraints."
            },
            {
                "abstract": "We prototype a cyber-physical platform with time-sensitive networking, synchronized motor control loops, and formal latency budgeting. The stack spans real-time OS scheduling, sensor fusion on heterogeneous cores, and secure boot with measured attestation. Fault-injection tests evaluate resilience; EMI and thermal characterization inform enclosure and layout.",
                "conclusion": "The study shows that disciplined timing, security roots of trust, and cross-layer validation are indispensable to dependable CPS deployments."
            }
        ]
    }
}

# ============================================================
# RESULT LOCKING: lock a response after first generation
# Key includes ALL user inputs so any change unlocks a new result
# ============================================================
LOCKED_RESULTS = {}

def _lock_key(payload: dict) -> str:
    # Include everything that user controls to truly “lock” until changed
    parts = [
        payload.get("name", "").strip(),
        str(payload.get("age", "")).strip(),
        payload.get("gender", "").strip(),
        payload.get("academicLevel", "").strip(),
        payload.get("stream", "").strip(),
        payload.get("abstractInput", "").strip()
    ]
    return "||".join(parts)


# ============================================================
# /suggest endpoint
# ============================================================
@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json(force=True)

        # Inputs
        level = (data.get("academicLevel") or "").strip()
        stream = (data.get("stream") or "").strip()
        abstract_input = (data.get("abstractInput") or "").strip()
        gaze = (data.get("gazeStatus") or "manual").strip()

        # Validation
        if level not in ("UG", "PG"):
            return jsonify({"error": "Invalid academic level"}), 400
        if stream not in VARIANTS[level]:
            return jsonify({"error": "Invalid stream"}), 400

        # Minimum words for the user's typed abstract
        word_count = len([w for w in abstract_input.split() if w.strip()])
        if word_count < 15:
            return jsonify({"error": "Abstract must be at least 15 words"}), 400

        # Locking key (all user inputs)
        key = _lock_key(data)
        if key in LOCKED_RESULTS:
            return jsonify(LOCKED_RESULTS[key])

        # Gaze-based selection
        if gaze == "centered":
            # Full, long variant rotated among 3 options
            choice = random.choice(VARIANTS[level][stream])

        elif gaze == "off-center":
            # Shorter variant; PG a bit longer & technical than UG
            if level == "PG":
                choice = {
                    "abstract": "A concise postgraduate summary is provided due to off-center gaze. Key technical points are distilled: core methodology, evaluation protocol, and principal findings—enough for a quick review while preserving rigor.",
                    "conclusion": "A brief, technically focused conclusion is returned acknowledging reduced engagement while retaining the essential implications and deployment takeaways."
                }
            else:
                choice = {
                    "abstract": "A brief undergraduate abstract is provided based on off-center gaze, summarizing method and outcome at a high level.",
                    "conclusion": "A short conclusion highlights the main learning and next steps."
                }

        elif gaze == "partial":
            # Incomplete style; PG still a bit richer than UG
            if level == "PG":
                choice = {
                    "abstract": "Partial facial detection led to an abbreviated postgraduate abstract. It outlines the problem framing, the primary approach, and a narrow slice of results, omitting secondary analyses and extensive ablations.",
                    "conclusion": "A compact conclusion notes preliminary significance and limitations; full detail requires stable gaze or manual confirmation."
                }
            else:
                choice = {
                    "abstract": "Only a partial undergraduate abstract could be generated due to incomplete face detection.",
                    "conclusion": "Conclusion remains succinct and provisional given partial input."
                }

        else:
            # Manual/button always works: expand user input into a clean draft
            choice = {
                "abstract": abstract_input + "\n\nThis draft has been structured for readability and can be refined based on feedback.",
                "conclusion": "A concise conclusion has been produced based on the provided abstract and context."
            }

        # Lock result until any input changes
        LOCKED_RESULTS[key] = choice
        return jsonify(choice)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # Local dev server; in Render, a WSGI server (gunicorn) will run this app
    app.run(host="0.0.0.0", port=5000)
