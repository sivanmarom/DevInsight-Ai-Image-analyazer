# Kubernetes & Helm – AI Image Processing Pipeline

## Overview
This project demonstrates the deployment of a scalable AI-based image processing pipeline on Kubernetes, leveraging **Helm** for application management.  
The system simulates a real-world architecture for processing radiology images, integrating **RabbitMQ** for message queuing, **Persistent Volumes** for data durability, and a **microservices** approach for modularity and scalability.

Key goals:
- Showcase Kubernetes orchestration with Helm.
- Implement reliable message queue handling.
- Enable persistent storage for shared data across services.
- Demonstrate an end-to-end image processing workflow.

---

## Architecture

### High-Level Design (Mermaid)
```mermaid
flowchart LR
    A[Web Server + API] -->|Image ID| B[RabbitMQ Queue]
    A -->|Stores image| D[Persistent Volume]
    B --> C[Consumer Service]
    C -->|Fetches image| D
```

### Visual Diagram
![Architecture Diagram](https://github.com/user-attachments/assets/0dae0613-59eb-4bc7-8e7b-1ac611352c03)

### Components
| Service        | Description | Technology Stack | Key Configurations |
|----------------|-------------|------------------|--------------------|
| **Web Server + API** | Accepts image uploads, stores them, sends IDs to queue | Python, Flask | Port **5000**, uses shared PVC `/data/images` |
| **Queue Service**  | Manages processing requests | RabbitMQ | PVC `rabbitmq-pvc` mounted at `/var/lib/rabbitmq`, durability enabled |
| **Consumer Service** | Retrieves images, analyzes them, logs results | Python | Reads from RabbitMQ, accesses `/data/images` |
| **Persistent Storage** | Shared data store for images and queue data | Kubernetes PVC | `web-server-pvc` and `rabbitmq-pvc` |

---

## Technologies Used
- **Kubernetes** (Minikube for local testing)
- **Helm** (package management & templating)
- **RabbitMQ** (message broker)
- **Docker** (containerization)
- **Python** (application logic)
- **kubectl** (cluster management)

---

## Deployment Guide

### Prerequisites
- Docker installed
- Minikube installed
- Helm installed

### Steps
1. **Start Minikube**
   ```bash
   minikube start
   ```

2. **Deploy RabbitMQ**
   ```bash
   helm install my-rabbitmq ./charts/rabbitmq-chart
   ```

3. **Deploy Web Server**
   ```bash
   helm install my-web-server ./charts/web-server-chart
   ```

4. **Deploy Consumer Service**
   ```bash
   helm install my-consumer ./charts/consumer-chart
   ```

5. **Verify Deployments**
   ```bash
   helm list
   kubectl get all
   ```

---

## Testing

### 1. Upload Image via API
First, retrieve the external URL:
```bash
minikube service web-server --url
```
Then upload an image:
```bash
curl -X POST -F 'image=@<path_to_image>' $(minikube service web-server --url)/upload
```
Expected result: success message with a correlation ID.

### 2. Check RabbitMQ Queue
```bash
kubectl port-forward svc/rabbitmq 15672:15672
```
Open `http://localhost:15672` and confirm the image ID is in the queue.

### 3. Monitor Consumer Logs
```bash
kubectl logs deployment/consumer
```
Expected logs: retrieval of the image and classification result (dog/cat).

### 4. End-to-End Flow
Upload an image → verify in RabbitMQ → check Consumer logs.

---

## Best Practices Implemented
- Persistent Volumes for durability
- Modular Helm charts for each service
- Isolated microservices for scalability
- End-to-end testing procedure
- Separation of concerns between services

---

## Compromises & Limitations
- **Single Node Cluster**: Using Minikube, not production-grade multi-node.
- **Limited Scalability**: Not tested under large-scale workloads.
- **No IaC for infrastructure**: Helm used for apps, but not for cluster creation.

---

## Potential Improvements
- **Resource Requests & Limits** for CPU/memory in deployments.
- **Liveness & Readiness Probes** for better health checks.
- **Infrastructure as Code** integration with Terraform.
- Migration to **Amazon EKS** for production scaling.
- **CI/CD Pipeline** for automated deployments.
- **Secrets Management** for RabbitMQ credentials.
- **Monitoring Stack** (Prometheus + Grafana).

---

## Learnings & Takeaways
This project strengthened my skills in:
- Deploying multi-service applications on Kubernetes.
- Using Helm for streamlined application management.
- Implementing persistent data handling in a containerized environment.
- Structuring DevOps workflows for reproducibility and scalability.

---

## Command & File Reference

| Action | Command / File | Purpose |
|--------|----------------|---------|
| Start Minikube | `minikube start` | Launch local K8s cluster |
| Deploy RabbitMQ | `helm install my-rabbitmq ./charts/rabbitmq-chart` | Message broker |
| Deploy Web Server | `helm install my-web-server ./charts/web-server-chart` | API for uploads |
| Deploy Consumer | `helm install my-consumer ./charts/consumer-chart` | Image processing |
| Check services | `kubectl get all` | View all resources |
| Check logs | `kubectl logs deployment/<name>` | View pod logs |
| PVC definition | `queue-service.yaml` / `web-server.yaml` / `consumer.yaml` | Persistent volume claims |

---

## Screenshots

### Helm and Kubernetes Resources
![Helm and K8s resources](https://github.com/sivanmarom/signalPet/assets/97241683/19517c33-f30c-4801-9b90-d1ff533bcf07)

### RabbitMQ Dashboard
![RabbitMQ Management Interface](https://github.com/sivanmarom/signalPet/assets/97241683/f078247d-9a5a-4143-85fc-514656bbc726)

### Consumer Logs Processing
![Consumer Service Logs](https://github.com/sivanmarom/signalPet/assets/97241683/e6837771-a699-48f1-a7e5-4377dfade166)

### End-to-End Flow Confirmation
![End-to-End Test Result](https://github.com/sivanmarom/signalPet/assets/97241683/16f82769-b326-4961-901a-173505dce070)

---
## 💬 Contact

For suggestions, improvements, or collaboration:
- 📧 [Sivmarom@gmail.com](mailto:Sivmarom@gmail.com)
- 🔗 [LinkedIn](https://www.linkedin.com/in/sivan-marom/)
- 💻 [GitHub](https://github.com/YOUR_USERNAME)

---
