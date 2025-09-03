# Fraud Detection Prototype (Full-Stack with ML + Docker)

## 🚀 Quick Start

```bash
# 1. Generate data
docker run --rm -v $(pwd):/app -w /app python:3.10 \
    python backend/data_gen.py

# 2. Create DB
docker run --rm -v $(pwd):/app -w /app python:3.10 \
    python backend/create_db.py

# 3. Train ML Model
docker run --rm -v $(pwd):/app -w /app python:3.10 \
    bash -c "pip install -r requirements.txt && python backend/train_model.py"

# 4. Start full system
docker-compose up --build
