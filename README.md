<p align="center">
  <img src="https://raw.githubusercontent.com/PsymoNiko/ChatOnPayment/main/docs/logo.png" alt="ChatOnPayment Logo" width="120"/>
</p>

<h1 align="center">ChatOnPayment 💬</h1>
<p align="center">
  <em>Rust‑powered microservices platform for real‑time chat & TON blockchain payments</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=github&color=gold" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=github&color=blue" alt="GitHub Forks">
  <img src="https://img.shields.io/github/license/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=apache" alt="License">
  <img src="https://img.shields.io/badge/microservices-architecture-dodgerblue?style=for-the-badge&logo=serverless" alt="Microservices">
  <img src="https://img.shields.io/badge/TON-blockchain-0098ea?style=for-the-badge&logo=ton&logoColor=white" alt="TON Blockchain">
</p>

---

## 🏗️ The Vision: A Self‑Hostable Platform, Not Just an App

**ChatOnPayment** is designed as a production‑grade **platform** – a blueprint for a horizontally scalable, observable, and secure microservices ecosystem. The final goal is a **one‑command deployable** system that provides real‑time chat and payment rails as a service.

---

## 🛠️ Tech Stack (by Category)

### 🦀 Languages & Frameworks

<p>
  <img src="https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rust">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/Node.js-339933?style=for-the-badge&logo=nodedotjs&logoColor=white" alt="Node.js">
</p>

### 🗄️ Databases & Storage

<p>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL">
  <img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis">
  <img src="https://img.shields.io/badge/MinIO-FF6C37?style=for-the-badge&logo=minio&logoColor=white" alt="MinIO">
  <img src="https://img.shields.io/badge/Rustfs_(planned)-000000?style=for-the-badge&logo=rust&logoColor=white" alt="Rustfs planned">
</p>

### 🔄 Message Queue & Event Streaming

<p>
  <img src="https://img.shields.io/badge/Kafka-231F20?style=for-the-badge&logo=apachekafka&logoColor=white" alt="Kafka">
  <img src="https://img.shields.io/badge/Zookeeper-231F20?style=for-the-badge&logo=apachezookeeper&logoColor=white" alt="Zookeeper">
</p>

### 🔭 Observability (Tracing, Metrics, Logs)

<p>
  <img src="https://img.shields.io/badge/Jaeger-66cfe6?style=for-the-badge&logo=jaeger&logoColor=black" alt="Jaeger">
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=grafana&logoColor=white" alt="Grafana">
  <img src="https://img.shields.io/badge/Sentry-362D59?style=for-the-badge&logo=sentry&logoColor=white" alt="Sentry">
  <img src="https://img.shields.io/badge/Elasticsearch-005571?style=for-the-badge&logo=elasticsearch&logoColor=white" alt="Elasticsearch">
  <img src="https://img.shields.io/badge/Kibana-005571?style=for-the-badge&logo=kibana&logoColor=white" alt="Kibana">
  <img src="https://img.shields.io/badge/Logstash-005571?style=for-the-badge&logo=logstash&logoColor=white" alt="Logstash">
</p>

### 🔐 Authentication & Security

<p>
  <img src="https://img.shields.io/badge/Keycloak-0078D7?style=for-the-badge&logo=keycloak&logoColor=white" alt="Keycloak">
  <img src="https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white" alt="JWT">
  <img src="https://img.shields.io/badge/OAuth-Google/GitHub-4285F4?style=for-the-badge&logo=oauth&logoColor=white" alt="OAuth">
</p>

### 🐳 Container & Orchestration

<p>
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/Docker_Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Compose">
  <img src="https://img.shields.io/badge/Kubernetes_(planned)-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes planned">
  <img src="https://img.shields.io/badge/NGINX-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="NGINX">
</p>

---

## ✨ Core Engineering Pillars

* **🦀 True Microservices in Rust** – Performance‑critical services (Accounts, Core) are written in Rust for maximum throughput and memory safety.
* **⚡️ Hybrid Object Storage** – Currently uses **MinIO** (S3‑compatible); planned migration to **Rustfs** (Rust‑native, up to 2.3x faster for small objects) for high‑performance media storage.
* **🔭 Deep Observability** – Jaeger (tracing), Prometheus (metrics), Grafana (visualisation), Sentry (error tracking), ELK (logs).
* **⚖️ Event‑Driven Architecture** – Apache Kafka for asynchronous communication between services, with Zookeeper for coordination.
* **🔐 Enterprise Authentication** – **Keycloak** as identity provider, supporting JWT, OAuth 2.0, and social logins (Google, GitHub).
* **🧩 Data Separation** – Two PostgreSQL instances: one for application data, one for logs. Redis for caching and session clustering.

---

## 🗺 Platform Architecture & Evolution Roadmap

| Phase | Focus & Deliverables | Key Tools & Patterns |
| :--- | :--- | :--- |
| **Phase 1 ✅** | MVP Launch | Basic messaging, TON wallet, single‑instance. |
| **Phase 2 ✅** *(Current)* | **Containerisation & Observability** | Docker Compose with Rust/Python/TS services, Jaeger, Prometheus, MinIO, Kafka, ELK, Sentry, and NGINX. |
| **Phase 3 ⚙️** *(In Progress)* | **Production Hardening** | Kubernetes (EKS) + Helm, GitOps (ArgoCD), service mesh (Istio). |
| **Phase 4 📈** | **Storage Migration** | Replace MinIO with **Rustfs cluster**; implement PostgreSQL master‑slave + Redis cluster. |
| **Phase 5 🔮** | **Self‑Service Platform** | One‑command deployment CLI (`ctpctl`); fully self‑hostable appliance. |

---

## 🛠️ Deep Dive: Current Tech Stack (Phase 2)

| Service | Language/Framework | Responsibility |
| :--- | :--- | :--- |
| **Accounts Service** | **Rust** (Actix‑web) | Auth, JWT, OAuth (Google/GitHub via Keycloak), user profiles. |
| **Chat Service** | Python (FastAPI) + WebSockets | Real‑time messaging, room management. |
| **Payment Service** | TypeScript (Node.js) | TON blockchain interactions. |
| **Core Service** | **Rust** (Tokio) | Service discovery, orchestrator. |
| **NGINX** | - | Reverse proxy, SSL termination, load balancer. |
| **Keycloak** | - | Identity provider (JWT + OAuth). |
| **Jaeger** | - | Distributed tracing. |
| **Prometheus + Grafana** | - | Metrics collection & dashboards. |
| **Sentry** | - | Error tracking. |
| **ELK** (Elasticsearch, Logstash, Kibana) | - | Centralised logging (chat logs stored in separate PostgreSQL + ELK). |
| **Kafka + Zookeeper** | - | Event‑driven communication. |
| **MinIO** | - | S3‑compatible object storage (attachments, media). |
| **PostgreSQL ×2** | - | Main database + logs database. |
| **Redis** | - | Session cache, pub/sub. |

> **📌 Storage Evolution**  
> Currently `MinIO` handles all object storage. In Phase 4, we will migrate to **Rustfs** – a Rust‑native, high‑performance object store designed for low‑latency media serving. Benchmarks show Rustfs outperforms MinIO by 2.3x for 4KB objects, making it ideal for chat attachments and transaction receipts.

> **🔐 Authentication**  
> `Keycloak` provides JWT tokens and integrates with Google & GitHub OAuth. All services validate tokens via a shared public key.

---

## 🚀 Getting Started (You'll be live in minutes)

1. **Clone & Enter the Repository**
   ```bash
   git clone https://github.com/PsymoNiko/ChatOnPayment.git
   cd ChatOnPayment
   ```

2. **Configure Environment**
   ```bash
   cp .env.sample .env
   # Edit .env with your TON testnet keys, OAuth credentials, etc.
   ```

3. **Launch the Entire Ecosystem**
   ```bash
   docker-compose up --build
   ```
   This starts all 15+ services (Rust, Python, Node, databases, message queue, observability stack).

4. **Access the Platform**
   - Chat UI: `http://localhost:8080`
   - Jaeger Tracing: `http://localhost:16686`
   - Prometheus: `http://localhost:9090`
   - Grafana: `http://localhost:3000` (admin/admin)
   - Kibana: `http://localhost:5601`
   - Sentry: `http://localhost:9900`
   - Keycloak Admin: `http://localhost:8080/auth` (admin/admin)

---

## 👩‍💻 For Platform Engineers & Contributors

Repository structure (monorepo):

```text
ChatOnPayment/
├── services/
│   ├── accounts-service/   (Rust)
│   ├── chat-service/       (Python/FastAPI)
│   ├── payment-service/    (TypeScript/Node)
│   └── core-service/       (Rust)
├── infrastructure/
│   ├── docker-compose.yml  # Current orchestration
│   └── k8s/                (Coming soon)
├── config/
│   ├── keycloak/           # Realm export
│   └── prometheus/         # Prometheus config
└── docs/                   # Architecture diagrams
```

We welcome contributions in:
- **Rust microservices** (performance optimisations, new features)
- **Kubernetes manifests** (moving away from Docker Compose)
- **Rustfs integration** (storage layer migration)
- **Load testing** (k6 / Locust scripts)

---

## 📄 License

MIT © [Ali Mohammadnia](https://github.com/PsymoNiko)

---

<p align="center">
  Built with 🦀 & ☕ by <a href="https://github.com/PsymoNiko">Ali Mohammadnia</a><br>
  <em>Platform Engineer • Infrastructure Architect • Open Source Contributor</em>
</p>