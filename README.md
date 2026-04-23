
<p align="center">
  <img src="https://raw.githubusercontent.com/PsymoNiko/ChatOnPayment/main/docs/logo.png" alt="ChatOnPayment Logo" width="120"/>
</p>

<h1 align="center">ChatOnPayment 💬</h1>
<p align="center">
  <em>A platform-scale microservices ecosystem for real-time communication & blockchain payments on the TON network.</em>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=github&color=gold" alt="GitHub Stars">
  <img src="https://img.shields.io/github/forks/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=github&color=blue" alt="GitHub Forks">
  <img src="https://img.shields.io/github/license/PsymoNiko/ChatOnPayment?style=for-the-badge&logo=apache" alt="License">
  <img src="https://img.shields.io/badge/microservices-architecture-dodgerblue?style=for-the-badge&logo=serverless" alt="Microservices">
    <img src="https://img.shields.io/badge/TON-blockchain-0098ea?style=for-the-badge&logo=ton&logoColor=white" alt="TON Blockchain">
</p>

<p align="center">
    <img src="https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white" alt="Go">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
    <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
    <br>
    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=for-the-badge&logo=kubernetes&logoColor=white" alt="Kubernetes">
    <img src="https://img.shields.io/badge/Nginx-009639?style=for-the-badge&logo=nginx&logoColor=white" alt="NGINX">
    <img src="https://img.shields.io/badge/Jaeger-66cfe6?style=for-the-badge&logo=jaeger&logoColor=black" alt="Jaeger">
    <img src="https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=prometheus&logoColor=white" alt="Prometheus">
    <img src="https://img.shields.io/badge/MinIO-FF6C37?style=for-the-badge&logo=minio&logoColor=white" alt="MinIO">
</p>

## 🏗️ The Vision: A Self-Hostable Platform, Not Just an App

**ChatOnPayment** is designed from the ground up as a production-grade platform. My goal is to demonstrate how to build a horizontally scalable, observable, and secure system. This project acts as a blueprint for a microservices ecosystem, where each component is a purposeful building block for a larger platform.

The final vision is a **one-command deployable platform** that provides real-time chat and payment rails as a service.

## ✨ Core Engineering Pillars

*   **🏛️ True Microservices Architecture**: Business capabilities are decoupled into independent services.
*   **⚡️ High-Performance Object Storage**: Powered by MinIO, with a planned evaluation of RustFS—to benchmark against MinIO for potential performance gains in specific workloads, especially for media-heavy chat features.
*   **🔭 Deep Observability**: Full integration with Jaeger for distributed tracing and Prometheus for metrics.
*   **⚖️ Intelligent Load Balancing**: NGINX serves as the gateway and reverse proxy.
*   **🔐 Security by Design**: Every service is designed with authentication and secure communication in mind.

## 🗺 Platform Architecture & Evolution Roadmap

The current implementation is **Phase 2** of the roadmap. Each new phase will introduce production-grade patterns.

| Phase | Focus & Deliverables | Key Tools & Patterns |
| :--- | :--- | :--- |
| **Phase 1 ✅** | **MVP Launch** | Basic messaging, TON wallet integration, single-instance deployment. |
| **Phase 2 ✅** *(Current)* | **Containerization & Orchestration Readiness** | Full Docker Compose setup with microservices (Accounts, Chat, Payment, Core). Integrated **Jaeger** for tracing, **Prometheus** for metrics, **MinIO** for object storage, and **NGINX** for routing. |
| **Phase 3 ⚙️** *(In Progress)* | **Production Hardening** | Move to **Kubernetes** (EKS) with Helm charts. Implement **GitOps** (ArgoCD) and **service mesh** (Istio) for advanced traffic management and security. |
| **Phase 4 📈** | **Data & Storage at Scale** | Migrate from MinIO to a **RustFS cluster** for high-performance media storage. Implement **PostgreSQL** with master-slave replication for chat history and **Redis** for session clustering and caching. |
| **Phase 5 🔮** | **The Self-Hostable Platform** | Develop a CLI tool (`ctpctl`) for single-command deployments to any cloud. Package the entire platform as a self-hostable appliance. |

## 🛠️ Deep Dive: Current Tech Stack (Phase 2)

The platform is built as a set of focused, single-responsibility services.

| Service | Language/Framework | Responsibility |
| :--- | :--- | :--- |
| **Accounts Service** | Go | User authentication, authorization, and profile management. |
| **Chat Service** | Python (FastAPI) + WebSockets | Real-time messaging logic, room management, and delivery. |
| **Payment Service** | TypeScript (Node.js) | TON blockchain interactions, wallet connections, and transaction finality. |
| **Core Service** | Go | The system orchestrator. Handles service discovery and inter-service communication. |
| **NGINX** | - | Reverse proxy, SSL termination, and load balancer. |
| **Jaeger** | - | End-to-end distributed tracing to visualize request flows across services. |
| **Prometheus** | - | Metrics collection, storage, and alerting for the entire stack. |
| **MinIO** | - | S3-compatible object storage for chat attachments, media, and transaction receipts. |

> **💡 A Note on MinIO and RustFS**: MinIO is currently used for its robust S3 compatibility and battle-tested nature. However, I'm investigating **RustFS** for future phases. Built in Rust, RustFS offers impressive performance benchmarks (e.g., `2.3x faster than MinIO for 4KB objects`), and its modern architecture aligns with the performance goals of this platform[reference:0].

## 🚀 Getting Started (You'll be live in minutes)

1.  **Clone & Enter the Repository**:
    ```bash
    git clone https://github.com/PsymoNiko/ChatOnPayment.git
    cd ChatOnPayment
    ```

2.  **Configure Environment**:
    ```bash
    cp .env.sample .env
    # Edit .env with your configuration
    ```

3.  **Build & Launch the Ecosystem**:
    ```bash
    docker-compose up --build
    ```
    This single command builds and starts all 8 services.

4.  **Access the Platform**:
    *   **Chat Interface**: `http://localhost`
    *   **Jaeger Tracing UI**: `http://localhost:16686`
    *   **Prometheus Metrics**: `http://localhost:9090`

5.  **Stopping the Ecosystem**:
    ```bash
    docker-compose down
    ```

## 👩‍💻 For Platform Engineers & Contributors

This project is structured as a monorepo for easy development:

```text
ChatOnPayment/
├── services/
│   ├── accounts-service/   (Go)
│   ├── chat-service/       (Python/FastAPI)
│   ├── payment-service/    (TypeScript/Node.js)
│   └── core-service/       (Go)
├── infrastructure/
│   ├── docker-compose.yml  # Current orchestration
│   └── k8s/                (Coming soon: K8s manifests)
└── docs/                   # Architecture diagrams & RFCs
```

I am actively looking for contributions, especially in these areas:

· Kubernetes & GitOps: Help transition the Docker Compose setup to a production-grade K8s cluster.
· Blockchain Integrations: Extend the payment service to support other chains.
· Performance Benchmarking: Help develop load tests (e.g., with k6) to validate system behavior under pressure.

📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

<p align="center">
  Built with ☕ by <a href="https://github.com/PsymoNiko">Ali Mohammadnia</a>
  <br>
  <em>Platform Engineer • Infrastructure Architect • Open Source Contributor</em>
</p>
