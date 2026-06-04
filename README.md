# Flask + Redis Visitor Counter

A production-style web application that tracks visitor count in real time, deployed on AWS EC2 using Docker Compose and automated CI/CD with GitHub Actions.

```
Browser → Elastic IP → EC2 → nginx → Flask → Redis
```

---

## Architecture

```
┌─────────────────────────────────────────────┐
│                  AWS EC2                    │
│                                             │
│  ┌──────────┐    ┌──────────┐   ┌────────┐ │
│  │  nginx   │───▶│  Flask   │──▶│ Redis  │ │
│  │ 80/443   │    │  :5000   │   │ :6379  │ │
│  └──────────┘    └──────────┘   └────────┘ │
│       ▲           Docker Compose           │
└───────┼────────────────────────────────────┘
        │
   Elastic IP
        │
     Browser
```

---

## Components

| Component          | Role                                                                                        |
| ------------------ | ------------------------------------------------------------------------------------------- |
| **nginx**          | Reverse proxy that receives incoming traffic on ports 80/443 and forwards requests to Flask |
| **Flask**          | Python web application that handles requests and updates the visitor counter                |
| **Redis**          | In-memory data store used to persist the visitor count                                      |
| **Docker Compose** | Orchestrates the multi-container application                                                |
| **GitHub Actions** | Automates deployment to AWS EC2                                                             |

---

## Tech Stack

* Python 3.10
* Flask
* Redis
* nginx
* Docker
* Docker Compose
* AWS EC2
* Elastic IP
* GitHub Actions

---

## Architecture Flow

```
Browser
   ↓
Elastic IP
   ↓
nginx (80/443)
   ↓
Flask (5000)
   ↓
Redis (6379)
```

---

## Project Structure

```
flask-redis-app/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── nginx.conf
├── requirements.txt
└── .github/
    └── workflows/
        └── docker.yml
```

---

## Docker Compose Services

### nginx

* Exposed to the internet on ports 80 and 443
* Acts as a reverse proxy
* Forwards requests to Flask

```nginx
location / {
    proxy_pass http://web:5000;
}
```

### Flask

* Custom Docker image built from the Dockerfile
* Uses Redis as the backend datastore
* Reads Redis hostname from environment variables

```python
redis_host = os.environ.get("REDIS_HOST", "redis")
```

### Redis

* Stores visitor count
* Data persisted using a Docker named volume

```yaml
volumes:
  - redis-data:/data
```

---

## Docker Networking

Docker Compose automatically creates a private network for all services.

Containers communicate using service names:

```text
nginx  →  web
web    →  redis
```

Example:

```nginx
proxy_pass http://web:5000;
```

and

```python
redis.Redis(host=redis_host, port=6379)
```

No IP addresses are hardcoded.

---

## Persistent Storage

Redis data is stored using a named volume:

```yaml
volumes:
  redis-data:
```

Benefits:

* Data survives container restarts
* Visitor count remains available after redeployment
* Demonstrates Docker volume persistence

---

## Running Locally

### Prerequisites

* Docker
* Docker Compose

### Start Application

```bash
git clone https://github.com/<your-username>/flask-redis-app.git

cd flask-redis-app

docker compose up -d --build
```

Visit:

```text
http://localhost
```

### Stop Application

```bash
docker compose down
```

### Stop and Remove Data

```bash
docker compose down -v
```

This removes the Redis volume and resets the visitor counter.

---

## CI/CD Pipeline

Every push to the `master` branch automatically deploys the application to EC2.

Workflow:

```text
git push
    ↓
GitHub Actions
    ↓
SSH into EC2
    ↓
git pull
    ↓
docker compose up -d --build
```

### Required GitHub Secrets

| Secret      | Description                    |
| ----------- | ------------------------------ |
| EC2_HOST    | Elastic IP or public IP of EC2 |
| EC2_USER    | SSH username                   |
| EC2_SSH_KEY | Private SSH key contents       |

---

## AWS Deployment

1. Launch Ubuntu EC2 instance
2. Allocate and associate an Elastic IP
3. Configure Security Group to allow:

   * Port 22 (SSH)
   * Port 80 (HTTP)
   * Port 443 (HTTPS)
4. Install Docker and Docker Compose
5. Clone repository
6. Run:

```bash
docker compose up -d --build
```

7. Configure GitHub Actions secrets for automated deployment

---

## Key Concepts Demonstrated

* Docker Images and Containers
* Multi-Container Applications
* Docker Compose Orchestration
* Docker Networking
* Service Discovery using Container Names
* Reverse Proxy with nginx
* Redis Data Persistence using Named Volumes
* Environment Variables
* AWS EC2 Deployment
* Elastic IP Usage
* CI/CD with GitHub Actions
* Automated Deployment using SSH

---

## What I Learned

* Building and deploying multi-container applications using Docker Compose
* Configuring nginx as a reverse proxy
* Using Redis for persistent application state
* Managing container communication through Docker networking
* Persisting data using Docker named volumes
* Deploying containerized applications on AWS EC2
* Using Elastic IPs for stable public access
* Implementing CI/CD pipelines using GitHub Actions
* Automating application deployment through SSH-based workflows
