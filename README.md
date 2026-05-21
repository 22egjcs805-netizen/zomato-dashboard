# 🍕 Zomato Sales Analysis Dashboard

A full-stack web application that visualises Zomato sales data with interactive charts.

**Tech Stack:** Python · Flask · Pandas · Chart.js · Docker · Kubernetes · GitHub Actions · Render

---

## 📁 Project Structure

```
zomato-dashboard/
├── app/
│   ├── app.py                  ← Flask backend (all API routes)
│   └── templates/
│       └── index.html          ← Frontend dashboard (HTML + Chart.js)
├── data/
│   └── zomato_sales.csv        ← Sales dataset
├── k8s/
│   ├── deployment.yaml         ← Kubernetes Deployment (2 replicas)
│   ├── service.yaml            ← Kubernetes LoadBalancer Service
│   └── hpa.yaml                ← Horizontal Pod Autoscaler
├── .github/
│   └── workflows/
│       └── deploy.yml          ← GitHub Actions CI/CD pipeline
├── Dockerfile                  ← Multi-stage Docker build
├── .dockerignore
├── render.yaml                 ← Render.com deploy config
├── requirements.txt
└── README.md
```

---

## ⚙️ SETUP INSTRUCTIONS

### ─────────────────────────────────────
### STEP 1 — Local Development
### WHERE TO RUN: VS Code Terminal (bash/zsh) or Ubuntu Terminal
### ─────────────────────────────────────

```bash
# 1. Clone the repo (after you push to GitHub)
git clone https://github.com/<YOUR_USERNAME>/zomato-dashboard.git
cd zomato-dashboard

# 2. Create a virtual environment
python3 -m venv venv
source venv/bin/activate          # Mac/Linux
# OR on Windows PowerShell:
# .\venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Run the Flask app locally
cd app
python app.py

# Open http://localhost:5000 in your browser
```

---

### ─────────────────────────────────────
### STEP 2 — Push to GitHub
### WHERE TO RUN: VS Code Terminal or Ubuntu Terminal
### ─────────────────────────────────────

```bash
# Inside your project folder:
git init
git add .
git commit -m "Initial commit: Zomato dashboard"

# Create a new repo on github.com, then:
git remote add origin https://github.com/<YOUR_USERNAME>/zomato-dashboard.git
git branch -M main
git push -u origin main
```

---

### ─────────────────────────────────────
### STEP 3 — Docker (Build & Run locally)
### WHERE TO RUN: Ubuntu Terminal or PowerShell (Docker Desktop must be installed)
### ─────────────────────────────────────

```bash
# 1. Build the Docker image (run from project root)
docker build -t zomato-dashboard .

# 2. Run the container locally
docker run -p 5000:5000 zomato-dashboard

# Open http://localhost:5000

# 3. Push image to Docker Hub (create account at hub.docker.com first)
docker login
docker tag zomato-dashboard <YOUR_DOCKERHUB_USERNAME>/zomato-dashboard:latest
docker push <YOUR_DOCKERHUB_USERNAME>/zomato-dashboard:latest
```

---

### ─────────────────────────────────────
### STEP 4 — Deploy on Render (Free Cloud Hosting)
### WHERE TO DO: Browser (render.com) — no terminal needed
### ─────────────────────────────────────

1. Go to https://render.com and sign up / log in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account and select the `zomato-dashboard` repo
4. Render detects `render.yaml` automatically — click **Deploy**
5. Wait ~3 minutes. Your live URL will be:
   `https://zomato-dashboard.onrender.com`

> **Free tier note:** The app sleeps after 15 min of inactivity — first load may take ~30 sec.

---

### ─────────────────────────────────────
### STEP 5 — GitHub Actions CI/CD (Automatic deploy)
### WHERE TO DO: GitHub website (Settings → Secrets)
### ─────────────────────────────────────

1. Go to your GitHub repo → **Settings → Secrets and variables → Actions**
2. Click **"New repository secret"** and add:
   - `DOCKER_USERNAME` → your Docker Hub username
   - `DOCKER_PASSWORD` → your Docker Hub password or access token
3. Now every `git push` to `main` will:
   - Run tests automatically
   - Build a new Docker image
   - Push it to Docker Hub

---

### ─────────────────────────────────────
### STEP 6 — Kubernetes (Local with Minikube)
### WHERE TO RUN: Ubuntu Terminal
### ─────────────────────────────────────

```bash
# 1. Install Minikube (Ubuntu)
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# 2. Start Minikube
minikube start

# 3. Edit k8s/deployment.yaml — replace <YOUR_DOCKERHUB_USERNAME> with your username
#    Example: image: johndoe/zomato-dashboard:latest

# 4. Apply all Kubernetes configs
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/hpa.yaml

# 5. Check that pods are running
kubectl get pods
kubectl get services

# 6. Open the app in browser (Minikube)
minikube service zomato-dashboard-service

# 7. Useful kubectl commands
kubectl get deployments           # check deployment status
kubectl describe pod <pod-name>   # debug a pod
kubectl logs <pod-name>           # view logs
kubectl delete -f k8s/            # tear everything down
```

---

## 🔑 GitHub Secrets Quick Reference

| Secret Name       | Value                        | Used In              |
|-------------------|------------------------------|----------------------|
| DOCKER_USERNAME   | Your Docker Hub username     | GitHub Actions       |
| DOCKER_PASSWORD   | Your Docker Hub password     | GitHub Actions       |

---

## 🌐 API Endpoints

| Endpoint                  | Description                        |
|---------------------------|------------------------------------|
| `GET /`                   | Dashboard HTML page                |
| `GET /health`             | Health check (Kubernetes/Render)   |
| `GET /api/kpis`           | 6 top-level KPI metrics            |
| `GET /api/revenue-by-month`| Monthly revenue trend             |
| `GET /api/revenue-by-city` | Revenue split by city             |
| `GET /api/orders-by-cuisine`| Orders grouped by cuisine        |
| `GET /api/payment-modes`  | Payment mode distribution          |
| `GET /api/top-restaurants` | Top 8 restaurants by revenue      |
| `GET /api/rating-distribution`| Rating histogram               |
| `GET /api/weekday-heatmap` | Avg order value per weekday       |
| `GET /api/weekend-vs-weekday`| Weekend vs weekday order count  |
