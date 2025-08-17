from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ----------------- DATASET -----------------
# Streams handled: AI, ML, CSE, Cybersecurity, Data Science, Electronics
# For each stream and level (UG/PG) there are: centered (full), off-center (medium), partial (short)

VARIANTS = {
    "UG": {
        "ai": {
            "centered": {
                "abstract": (
                    "This undergraduate AI project investigates classic and modern learning algorithms to design a "
                    "small yet end-to-end intelligent system. The pipeline begins with problem framing and dataset "
                    "curation, followed by data cleaning, feature extraction, and baseline models (logistic regression, "
                    "decision trees, k-NN). We then introduce neural components—lightweight CNNs for images or MLPs for "
                    "tabular signals—optimized with mini-batch training, early stopping, and validation splits. "
                    "Performance is assessed using accuracy, precision–recall, and confusion matrices; error analysis "
                    "drives iteration on features, thresholds, and augmentation. The system is packaged with input "
                    "validation and simple monitoring hooks so students can observe model drift and latency. Limitations "
                    "include restricted data diversity and compute budgets; mitigations, such as stratified sampling and "
                    "cross-validation, are discussed to support reproducibility and responsible use."
                ),
                "conclusion": (
                    "Results show that careful preprocessing, clear evaluation, and small neural components can provide "
                    "strong baselines for undergraduate AI problems. Future work should explore richer augmentation, "
                    "explainability dashboards, and lightweight deployment on constrained devices."
                )
            },
            "off-center": {
                "abstract": (
                    "The study builds a compact AI pipeline combining basic classifiers with a small neural network. "
                    "Data preparation, validation splits, and error analysis guide iterations. Accuracy and precision–recall "
                    "demonstrate steady gains over baselines. Compute limits are acknowledged, with suggestions for "
                    "augmentation and cross-validation to improve robustness."
                ),
                "conclusion": (
                    "A blended classical–neural approach is practical for undergraduate AI tasks, with clear metrics and "
                    "iteration loops leading to dependable improvements."
                )
            },
            "partial": {
                "abstract": (
                    "We implement a concise AI workflow: clean data, train simple models, add a small neural net, and study "
                    "results via accuracy and precision–recall. Error review guides refinements and responsible use."
                ),
                "conclusion": (
                    "The project offers a clear baseline for AI experimentation and a path toward explainability and deployment."
                )
            }
        },
        "ml": {
            "centered": {
                "abstract": (
                    "This undergraduate ML project focuses on supervised learning with reproducible evaluation. After "
                    "profiling the dataset, we implement pipelines for normalization, feature selection, and categorical "
                    "encoding. Models include regularized linear regression, tree ensembles, and SVMs, tuned via grid "
                    "search over cross-validation folds. We analyze bias–variance trade-offs, inspect feature importances, "
                    "and compare ROC–AUC against a naive baseline. A lightweight experiment tracker captures parameters, "
                    "metrics, and artifacts, enabling transparent reporting. Error slices (rare classes or boundary cases) "
                    "reveal where calibration and thresholding help. We also document failure modes and assumptions so "
                    "future teams can extend the work responsibly."
                ),
                "conclusion": (
                    "The study demonstrates that disciplined preprocessing and cross-validated tuning produce reliable ML "
                    "predictors for undergraduate settings. Next steps include probabilistic calibration, interpretability "
                    "tools, and robust handling of class imbalance."
                )
            },
            "off-center": {
                "abstract": (
                    "We compare several supervised ML models under a common pipeline for preprocessing and cross-validation. "
                    "Regularization, feature selection, and thresholding improve generalization. ROC–AUC and error analysis "
                    "highlight strengths and gaps relative to a naive baseline."
                ),
                "conclusion": (
                    "A standardized pipeline yields dependable results, and tracking experiments simplifies reporting and iteration."
                )
            },
            "partial": {
                "abstract": (
                    "The project evaluates linear models, tree ensembles, and SVMs with cross-validation and feature engineering. "
                    "Metrics and error slices inform threshold selection and next steps."
                ),
                "conclusion": (
                    "Findings provide a solid foundation for improved calibration and interpretability in future work."
                )
            }
        },
        "cse": {
            "centered": {
                "abstract": (
                    "This undergraduate CSE project engineers a modular web application emphasizing clean architecture and "
                    "testability. The stack uses a RESTful backend, a typed API layer, and a responsive frontend. Core modules "
                    "implement authentication, rate limiting, input validation, and persistence with ORM migrations. We add "
                    "caching and pagination to reduce latency and memory footprint. CI pipelines run unit and integration tests, "
                    "linting, and container builds. Observability is provided through structured logging and metrics. We run "
                    "load tests to characterize throughput and tail latency across configurations, documenting bottlenecks and "
                    "optimizations such as query indexing and connection pooling."
                ),
                "conclusion": (
                    "Results confirm that layered design, automated testing, and simple observability yield a maintainable and "
                    "performant CSE system suitable for undergraduate delivery."
                )
            },
            "off-center": {
                "abstract": (
                    "We built a service-oriented web app with authentication, validation, and database migrations. Caching and "
                    "pagination improve responsiveness, while CI tests preserve quality. Load testing exposed hotspots addressed "
                    "via indexing and pooling."
                ),
                "conclusion": (
                    "A pragmatic architecture plus CI and profiling produced dependable performance for course-scale deployments."
                )
            },
            "partial": {
                "abstract": (
                    "A modular web service with secure endpoints, typed API contracts, and basic caching was implemented. "
                    "Tests and logs support maintainability."
                ),
                "conclusion": (
                    "The design provides a sound base for features, scaling, and further automation."
                )
            }
        },
        "cybersecurity": {
            "centered": {
                "abstract": (
                    "This undergraduate cybersecurity project designs a small enterprise network lab with defense-in-depth. "
                    "We configure segmented subnets, least-privilege access, MFA, and logging at the gateway and host levels. "
                    "A SIEM pipeline aggregates events for alerting; a honeypot captures attacker behavior. We run threat "
                    "simulations (phishing and lateral movement) and evaluate detection/response runbooks. Vulnerability scans "
                    "and patch metrics guide remediation priorities. Documentation includes asset inventory, risk register, and "
                    "backup/restore drills."
                ),
                "conclusion": (
                    "Layered controls and rehearsed incident handling significantly reduce risk in student environments. "
                    "Future work explores zero-trust segmentation and purple-team exercises."
                )
            },
            "off-center": {
                "abstract": (
                    "We implemented a segmented lab, MFA, logging, and a SIEM for alerts. Simulated attacks and vulnerability "
                    "scans informed remediation and playbooks."
                ),
                "conclusion": (
                    "Foundations for detection and response were established, with clear paths toward zero-trust enhancements."
                )
            },
            "partial": {
                "abstract": (
                    "A compact defense-in-depth lab was built with network segmentation, MFA, and centralized logging. "
                    "Basic runbooks support incidents."
                ),
                "conclusion": (
                    "The lab enables practical security practice and continuous improvement."
                )
            }
        },
        "data science": {
            "centered": {
                "abstract": (
                    "This undergraduate data-science project develops a structured analytics workflow from raw collection to "
                    "actionable insight. We perform data profiling, handle missingness, and standardize units. Feature crafting "
                    "uses domain rules and interaction terms; baselines are compared against regularized models. Evaluation "
                    "employs cross-validation and bootstrap intervals to quantify uncertainty. Visualization communicates trends, "
                    "anomalies, and fairness slices. A lightweight report template automates figures and tables for reproducible "
                    "summaries."
                ),
                "conclusion": (
                    "The workflow shows that transparent preprocessing, uncertainty estimates, and clear visuals make results "
                    "trustworthy and repeatable."
                )
            },
            "off-center": {
                "abstract": (
                    "We turn raw data into a clean analytical table, build baselines and regularized models, and report uncertainty "
                    "with cross-validation and bootstraps. Visualizations reveal trends and outliers."
                ),
                "conclusion": (
                    "A disciplined pipeline improves reliability and communication of data-science findings."
                )
            },
            "partial": {
                "abstract": (
                    "The project cleans data, engineers features, and evaluates models with simple uncertainty estimates. "
                    "Plots aid interpretation."
                ),
                "conclusion": (
                    "Deliverables emphasize reproducibility and clear reporting."
                )
            }
        },
        "electronics": {
            "centered": {
                "abstract": (
                    "This undergraduate electronics project designs a low-power embedded system for periodic sensing and wireless "
                    "telemetry. The PCB integrates a microcontroller, sensor front-end, power regulation, and BLE radio. Firmware "
                    "implements duty-cycled acquisition, buffering, CRC checks, and over-the-air configuration. We profile current "
                    "draw across modes and estimate battery life under different sampling schedules. EMC considerations, decoupling, "
                    "and enclosure constraints are documented. A desktop viewer verifies packet integrity and plots sensor streams."
                ),
                "conclusion": (
                    "Measurements confirm multi-day operation with stable telemetry. Next steps include energy harvesting and secure "
                    "pairing mechanisms."
                )
            },
            "off-center": {
                "abstract": (
                    "We built a battery-powered sensing node with BLE, focusing on power budgeting and reliable packets. Duty cycling "
                    "and buffering extend runtime. A viewer validates transmissions."
                ),
                "conclusion": (
                    "The platform is a solid basis for longer deployments and secure communication upgrades."
                )
            },
            "partial": {
                "abstract": (
                    "A compact embedded board samples sensors and transmits data over BLE with CRC checks and configurable duty cycles."
                ),
                "conclusion": (
                    "Results indicate practical runtimes and a clear route to hardening."
                )
            }
        }
    },
    "PG": {
        "ai": {
            "centered": {
                "abstract": (
                    "This postgraduate AI study develops an end-to-end learning system emphasizing principled optimization, "
                    "robustness, and reproducibility. The model family comprises residual CNN backbones with squeeze-and-excitation "
                    "blocks, optionally combined with transformer layers for long-range context. We compare cross-entropy, focal, and "
                    "label-smoothing losses; optimization uses AdamW with cosine schedules, gradient clipping, mixed precision, and "
                    "exponential moving averages. Regularization includes strong augmentation, stochastic depth, and dropout. "
                    "Evaluation is conducted across stratified folds with calibration curves, ECE, and cost-sensitive metrics. "
                    "Ablations isolate the contribution of data augmentation, architectural choices, and optimization strategies. "
                    "Robustness is studied under distribution shift via corruption benchmarks and test-time augmentation; fairness "
                    "slices quantify subgroup disparity. The system is containerized with deterministic seeds and versioned datasets; "
                    "weights, configs, and metrics are tracked in an experiment registry. Finally, an inference service exposes batched "
                    "prediction with CPU/GPU fallbacks and structured logging for drift monitoring."
                ),
                "conclusion": (
                    "Results show statistically significant gains in calibrated performance and shift robustness compared to strong "
                    "baselines. The ablation study clarifies that augmentation and schedule choice drive most of the improvement, "
                    "while architectural depth yields diminishing returns beyond compute budgets. The framework is suitable for "
                    "research extensions in self-supervision, active learning, or efficient adaptation."
                )
            },
            "off-center": {
                "abstract": (
                    "We evaluate residual CNN–transformer hybrids trained with AdamW, label smoothing, and strong augmentation. "
                    "Cross-validated metrics, calibration, and corruption tests quantify generalization and shift robustness. "
                    "Reproducible containers and an experiment registry ensure traceability."
                ),
                "conclusion": (
                    "The system achieves calibrated, robust accuracy and provides a clear platform for advanced research directions."
                )
            },
            "partial": {
                "abstract": (
                    "A modern AI pipeline combines residual networks, careful regularization, and tracked experiments. "
                    "Calibration and ablation clarify reliability and design trade-offs."
                ),
                "conclusion": (
                    "Outcomes indicate consistent improvements with reproducible training and principled evaluation."
                )
            }
        },
        "ml": {
            "centered": {
                "abstract": (
                    "This postgraduate ML research studies structured prediction under class imbalance and covariate shift. "
                    "The methodology integrates gradient-boosted trees, calibrated linear models, and tabular neural networks "
                    "with embedding layers for mixed data types. We investigate loss re-weighting, focal objectives, and "
                    "distribution-aware sampling. Model selection uses nested cross-validation; hyper-parameters are optimized "
                    "via Bayesian search with early stopping. Uncertainty estimation is obtained by ensembling and Monte-Carlo "
                    "dropout, while post-hoc calibration (isotonic and temperature scaling) improves decision thresholds for "
                    "cost-sensitive settings. To address shift, we evaluate covariate shift correction by importance weighting "
                    "and domain adversarial training. A comprehensive audit logs data lineage, feature drift statistics, and "
                    "privacy constraints."
                ),
                "conclusion": (
                    "The study achieves superior cost-aware performance with calibrated probabilities and competitive robustness "
                    "under moderate shift. The analysis suggests that principled sampling and calibration have the largest impact, "
                    "while complex adversarial objectives yield marginal gains for tabular data."
                )
            },
            "off-center": {
                "abstract": (
                    "We compare boosted trees, calibrated linear models, and tabular neural nets under imbalance and shift. "
                    "Bayesian optimization tunes hyper-parameters; ensembles and calibration deliver reliable probabilities. "
                    "Importance weighting and drift statistics quantify robustness."
                ),
                "conclusion": (
                    "Well-calibrated ensembles provide strong, cost-aware predictions and a pragmatic defense against moderate shift."
                )
            },
            "partial": {
                "abstract": (
                    "The project emphasizes calibrated prediction for imbalanced data using ensembles, Bayesian tuning, and "
                    "distribution-aware validation."
                ),
                "conclusion": (
                    "Findings highlight calibration and sampling as primary levers for dependable ML."
                )
            }
        },
        "cse": {
            "centered": {
                "abstract": (
                    "This postgraduate CSE system implements a cloud-native, observable microservice platform. The design adopts "
                    "DDD boundaries, gRPC for high-throughput internal calls, and REST for external clients. Services publish "
                    "structured events to a message bus with exactly-once semantics; an idempotent gateway deduplicates retries. "
                    "State is managed via transactional outbox, read models, and schema-migrated storage. CI/CD performs static "
                    "analysis, unit/integration/E2E tests, and canary deployments with automatic rollback. Distributed tracing, "
                    "RED metrics, and SLO-based alerts provide actionable telemetry. We evaluate latency and saturation under realistic "
                    "traffic mixes and chaos injections (pod evictions, network jitter), then optimize tail latency via connection "
                    "pooling, adaptive timeouts, and circuit breakers."
                ),
                "conclusion": (
                    "The platform maintains reliability under failure scenarios while controlling tail latency. The approach is "
                    "readily extensible to multi-region topologies and policy-driven autoscaling."
                )
            },
            "off-center": {
                "abstract": (
                    "We engineered gRPC microservices with an event bus, transactional outbox, and robust CI/CD. Tracing and RED "
                    "metrics support SLO alerts. Chaos tests and canaries validate reliability and constrain tail latency."
                ),
                "conclusion": (
                    "Results show resilient performance and a clear path to multi-region expansion."
                )
            },
            "partial": {
                "abstract": (
                    "A modular microservice stack uses gRPC, eventing, and strong observability with SLO alerts and automated rollbacks."
                ),
                "conclusion": (
                    "Tail-latency controls and testing practices yield dependable operations."
                )
            }
        },
        "cybersecurity": {
            "centered": {
                "abstract": (
                    "This postgraduate cybersecurity work operationalizes zero-trust principles in a small enterprise lab. "
                    "We implement identity-aware proxies, continuous device posture checks, and micro-segmentation enforced by "
                    "policy. Detection stacks combine EDR telemetry, DNS sinkholing, and behavioral analytics shipped to a SIEM "
                    "for correlation with threat intel. Purple-team exercises measure mean-time-to-detect and response across the "
                    "kill chain (initial access, persistence, lateral movement, exfiltration). Automated hardening baselines are "
                    "verified by compliance as code; vulnerability management is risk-based with exploit-prediction scoring. "
                    "Backups are encrypted and periodically restored to test RPO/RTO promises. Findings quantify trade-offs among "
                    "user friction, visibility, and containment."
                ),
                "conclusion": (
                    "Zero-trust enforcement materially reduces blast radius while analytics improve detection speed. The program "
                    "balances usability with security and provides concrete metrics for continuous improvement."
                )
            },
            "off-center": {
                "abstract": (
                    "We evaluate zero-trust controls with identity-aware access, segmentation, and EDR-driven detection. "
                    "Purple-team drills and compliance as code validate effectiveness and recovery objectives."
                ),
                "conclusion": (
                    "Measured improvements in detection and containment support phased rollout of zero-trust capabilities."
                )
            },
            "partial": {
                "abstract": (
                    "A lab demonstrates zero-trust access, segmentation, and SIEM correlation with practical response playbooks."
                ),
                "conclusion": (
                    "Metrics indicate reduced risk and faster investigation cycles."
                )
            }
        },
        "data science": {
            "centered": {
                "abstract": (
                    "This postgraduate data-science project develops a fully reproducible analytics stack with rigorous inference. "
                    "Data contracts enforce schema and lineage; transformations are versioned and tested. We integrate mixed-effects "
                    "models and Bayesian inference to quantify uncertainty and hierarchical variation. Counterfactual analysis and "
                    "uplift modeling estimate intervention impact, while double-robust estimators mitigate confounding. Missingness "
                    "mechanisms are probed (MCAR/MAR/MNAR), and sensitivity analyses communicate robustness. Reporting is automated "
                    "with parameter tables, credible intervals, and model diagnostics; plots emphasize uncertainty, priors, and "
                    "posterior predictive checks. All artifacts (code, data snapshots, and results) are archived for auditability."
                ),
                "conclusion": (
                    "The framework yields defensible, decision-ready insights with quantified uncertainty and transparent lineage. "
                    "It is suitable for regulated settings where traceability matters."
                )
            },
            "off-center": {
                "abstract": (
                    "We deliver a reproducible pipeline with tested transformations, hierarchical models, and Bayesian inference. "
                    "Counterfactuals and uplift quantify impact, while sensitivity analyses express robustness."
                ),
                "conclusion": (
                    "Decision-makers gain calibrated estimates and auditable analytics with clear uncertainty communication."
                )
            },
            "partial": {
                "abstract": (
                    "A versioned analytics workflow combines hierarchical modeling and Bayesian estimation with automated reports."
                ),
                "conclusion": (
                    "Outputs are reproducible, calibrated, and suitable for policy evaluation."
                )
            }
        },
        "electronics": {
            "centered": {
                "abstract": (
                    "This postgraduate electronics project designs a telemetry platform for long-life sensing at the edge. "
                    "A multilayer PCB hosts a low-leakage MCU, precision analog front-end, power-path manager, and sub-GHz radio. "
                    "Firmware provides RTOS scheduling, DMA pipelines, delta compression, secure boot, and OTA updates with A/B "
                    "partitions. We formally specify low-power states and verify transitions with current-probe traces; profiling "
                    "quantifies energy per sample across workloads. RF performance is characterized in shielded tests with swept "
                    "attenuation; forward-error correction and interleaving improve reliability in noisy channels. Security includes "
                    "attestation, key derivation from hardware unique IDs, and signed updates. A gateway service manages fleets and "
                    "collects metrics for anomaly detection."
                ),
                "conclusion": (
                    "Measurements confirm robust telemetry under harsh radio conditions with multi-month operation. The platform is "
                    "ready for field pilots with secure lifecycle management."
                )
            },
            "off-center": {
                "abstract": (
                    "We prototype a low-power sensing node with RTOS, secure boot, OTA, and sub-GHz radio. Energy profiling guides "
                    "duty-cycle policies; FEC and interleaving harden links. A gateway handles fleet metrics."
                ),
                "conclusion": (
                    "Results demonstrate reliable telemetry and a secure upgrade path for extended deployments."
                )
            },
            "partial": {
                "abstract": (
                    "An embedded platform integrates precision sensing, RTOS scheduling, and secure OTA updates over long-range radio."
                ),
                "conclusion": (
                    "Energy profiling indicates durable operation with maintainable firmware."
                )
            }
        }
    }
}

# -------------- Helpers --------------
def normalize_level(val: str):
    if not val: return None
    v = val.strip().lower()
    if v in ("ug","undergraduate"): return "UG"
    if v in ("pg","postgraduate"): return "PG"
    return None

def normalize_stream(val: str):
    if not val: return None
    v = val.strip().lower()
    # canonical keys we used in VARIANTS
    mapping = {
        "ai":"ai", "artificial intelligence":"ai",
        "ml":"ml", "machine learning":"ml",
        "cse":"cse", "computer science":"cse", "computer science and engineering":"cse",
        "cybersecurity":"cybersecurity", "cyber security":"cybersecurity",
        "data science":"data science", "datascience":"data science",
        "electronics":"electronics", "ece":"electronics"
    }
    return mapping.get(v)

# -------------- ROUTE --------------
@app.route("/suggest", methods=["POST"])
def suggest():
    try:
        data = request.get_json(force=True, silent=True) or {}

        level_raw = data.get("academicLevel", "")
        stream_raw = data.get("stream", "")
        abstract_input = (data.get("abstractInput") or "").strip()
        gaze = (data.get("gazeStatus") or "manual").strip().lower()

        level = normalize_level(level_raw)
        stream = normalize_stream(stream_raw)

        # Validation
        if not level or level not in VARIANTS:
            return jsonify({"error":"Invalid academic level"}), 400
        if not stream or stream not in VARIANTS[level]:
            return jsonify({"error":"Invalid stream"}), 400
        if len(abstract_input.split()) < 15:
            return jsonify({"error":"Abstract must be at least 15 words"}), 400

        # Always return something from dataset; choose by gaze when possible
        stream_pack = VARIANTS[level][stream]
        if gaze in ("centered","partial","off-center"):
            choice = stream_pack.get(gaze) or stream_pack["centered"]
        else:
            choice = stream_pack["centered"]

        return jsonify({
            "abstract": choice["abstract"],
            "conclusion": choice["conclusion"]
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render gives you PORT env var
    app.run(host="0.0.0.0", port=port)
