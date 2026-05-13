# AI-Powered Content Moderation API

A high-performance FastAPI service that uses Deep Learning to moderate text in real-time. 

## 🚀 The Architecture
- **FastAPI:** Asynchronous API framework for high-throughput.
- **Detoxify (AI):** Open-source Transformer model for toxic comment classification.
- **Redis:** Used for two critical patterns:
  - **Caching:** Reduces AI inference latency by 98% for repeated text.
  - **Rate Limiting:** Protects the AI engine from compute-exhaustion attacks.
- **PostgreSQL:** Permanent storage for moderation logs using SQLAlchemy 2.0 (Async).
- **Docker Compose:** Fully containerized environment with optimized build layers.

                ┌──────────────┐
                │   Client     │
                │ (Frontend /  │
                │  API User)   │
                └──────┬───────┘
                       │ HTTP Request
                       ▼
            ┌────────────────────┐
            │   FastAPI Server   │
            │  (Business Logic)  │
            └──────┬─────┬──────┘
                   │     │
     Cache Check   │     │ Rate Limit Check
                   ▼     ▼
            ┌──────────┐  ┌──────────┐
            │  Redis   │  │  Redis   │
            │ Cache    │  │ Rate Lim │
            └──────────┘  └──────────┘
                   │
                   ▼
        ┌────────────────────┐
        │ AI Inference Layer │
        │   (Detoxify NLP)   │
        └────────┬───────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ PostgreSQL DB      │
        │ (Audit Logging)    │
        └────────────────────┘


## 🛠️ Engineering Highlights 
- **Layer Optimization:** Split Docker requirements into "Heavy AI" and "Light API" layers to optimize build times and bandwidth.
- **Model Persistence:** Used Docker Named Volumes to persist 400MB+ AI weights, avoiding redundant downloads.
- **Graceful Startup:** Implemented a Python-based health check script to ensure the API only starts once Postgres is ready.
- **Test-Driven:** Includes a full suite using `pytest` and `aiosqlite` for in-memory DB simulation.

### 📉 Docker Image Size Optimization (5GB down to 1.63GB)
- **Problem:** Initial builds pulled the full, heavyweight PyTorch GPU library (`torch`), inflating the Docker image size to over 5GB and disk usage to over 8GB. This is highly inefficient for CPU-bound cloud deployments.
- **Solution:** Configured the `pip` installation layer to explicitly pull the specialized CPU-only wheel using the PyTorch extra index URL:
  ```bash
  pip install torch --extra-index-url https://download.pytorch.org/whl/cpu
  ```
- **Impact:** 
  - Reduced the final API container footprint (`content_moderation_api-api:latest`) from **5GB to 1.63GB**.
  - Slashed active base layers down to **336MB**, dramatically accelerating deployment and CI/CD pipeline speeds.
  - Decreased local disk space usage from **~8GB down to 1.6GB**
