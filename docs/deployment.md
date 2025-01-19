# Deployment Guide

## Prerequisites

- Docker 20.10+
- Kubernetes 1.21+
- Helm 3.0+

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/AuronEvander/ADAC-Blockchain-Complete.git
cd ADAC-Blockchain-Complete
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run development server:
```bash
uvicorn src.main:app --reload
```

## Docker Deployment

1. Build the Docker image:
```bash
docker build -t adac-blockchain:latest -f deployment/docker/Dockerfile .
```

2. Run with docker-compose:
```bash
docker-compose -f deployment/docker/docker-compose.yml up -d
```

## Kubernetes Deployment

1. Apply Kubernetes configurations:
```bash
kubectl apply -f deployment/kubernetes/
```

2. Verify deployment:
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## Configuration

The application can be configured using environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `LOG_LEVEL`: Logging level (default: INFO)
- `API_KEY`: API authentication key
- `NODE_TYPE`: Type of node (validator/full/light)

## Monitoring

The application exposes metrics at `/metrics` endpoint in Prometheus format.

Graphana dashboards are available in `deployment/monitoring/dashboards/`.