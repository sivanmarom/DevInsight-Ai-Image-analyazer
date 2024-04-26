# DevOps Home Assignment - Kubernetes Cluster Setup Documentation

## 1. Introduction

This document outlines the setup and configuration of a Kubernetes cluster for SignalPET, utilizing Helm to streamline deployments. This system, designed for processing radiology images using AI, leverages a robust microservices architecture to handle high workloads efficiently.

## 2. System Architecture

### Components Overview:
- **Queue Service**: Manages incoming image processing requests, ensuring that they are handled in an orderly and efficient manner.
- **Web Server with API**: Accepts image uploads, assigns correlation IDs, and queues the images for processing.
- **Consumer Service**: Processes the images from the queue, performing analysis to determine image characteristics.

### Data Flow:
1. The **Web Server** receives an image via the API and stores it in the persistent storage, then sends the image ID to the queue.
2. The **Queue Service** receives and manages the order of processing requests.
3. The **Consumer Service** retrieves image IDs from the queue, fetches the corresponding images from storage, analyzes them, and logs the results.

## 3. Setup and Configuration

### Kubernetes Cluster:
- The cluster is implemented using Minikube, which simplifies the setup for development and testing purposes.

### Helm Integration:
- Helm, as a package manager for Kubernetes, simplifies application deployment and management:

  - **Charts:**  Define, install, and manage Kubernetes applications.
  - **Simplification and Manageability:** Encapsulates Kubernetes resources, manages dependencies, and provides easy updates and rollbacks.

### Persistent Storage:
Persistent storage is crucial for ensuring that the images and queue data are preserved across restarts. This resilience is key to maintaining the state of the system.

- **RabbitMQ Persistent Volume Claim (PVC)**:
  - **File**: `queue-service.yaml`
  - **Details**: A PVC named `rabbitmq-pvc` is created with a request for 1GB of storage. This storage is mounted at `/var/lib/rabbitmq` within the RabbitMQ container to hold all message data, ensuring durability and persistence across pod restarts.

- **Web Server and Consumer Service Shared PVC**:
  - **File**: `web-server.yaml` and part of the `consumer.yaml`
  - **Details**: A shared PVC named `web-server-pvc` is created with a request for 1GB of storage. This PVC is mounted at `/data/images` in both the web server and consumer containers. The web server uses this mount point to save uploaded images, and the consumer accesses the same location to retrieve images for processing.

### Queue Service:
- RabbitMQ is used as the queue service, deployed within Kubernetes to manage the high volume of requests. It is set up with durability and persistence configurations to ensure message safety across pod restarts.

### Web Server with API:
- The web server is a simple Python HTTP server running in a Docker container, exposed on port 5000. It provides an `/upload` endpoint for image uploads, with images stored on the persistent volume and their IDs pushed to the RabbitMQ queue.

### Consumer Service:
- This service polls RabbitMQ for new image IDs, retrieves the images from the persistent storage, analyzes their size and content, and logs whether each image contains a dog or a cat.


## 4. Deployment Steps Using Helm
To deploy this system, follow these detailed steps:
1. **Start Minikube**:
   - Ensure Minikube is installed and start it with sufficient resources. Example command:
     ```
     minikube start 
     ```
2. **Install Helm**:
   - Ensure Helm is installed on your machine. You can install it by following the official Helm installation guide.   
3. **Deploy RabbitMQ**:
   - Use Helm to deploy RabbitMQ:
     ```shell
     helm install my-rabbitmq ./charts/rabbitmq-chart
     ```
4. **Deploy the Web Server**:
   - Use Helm to deploy the web server:
     ```shell
     helm install my-web-server ./charts/web-server-chart
     ```
5. **Deploy the Consumer Service**:
   - Use Helm to deploy the consumer service:
     ```shell
     helm install my-consumer ./charts/consumer-chart
     ```

6. **Verify All Components Are Running**:
   - Check the status of all deployments, services and Helm relases:
     ```
     helm list
     kubectl get all
     helm status <release_name>
     ```

![image](https://github.com/sivanmarom/signalPet/assets/97241683/19517c33-f30c-4801-9b90-d1ff533bcf07)


![image](https://github.com/sivanmarom/signalPet/assets/97241683/f078247d-9a5a-4143-85fc-514656bbc726)

## 5. Testing the System
To validate that each component of the Kubernetes setup functions correctly, follow these detailed testing steps:

1. **Test Web Server API Upload Endpoint**:
   - Retrieve the external URL of your web server using Minikube:
     ```
     minikube service web-server --url
     ```
   - Use the following curl command to upload an image. Replace {{image_path}} with the path to your image file:
     ```
     curl -X POST -F 'image=@{{image_path}}' $(minikube service web-server --url)/upload
     ```
   - Ensure the response from this command includes a success message and a correlation ID for the uploaded image. This confirms that the web server is properly receiving images and interacting with the persistent storage.

2. **Check Queue in RabbitMQ**:
   - Confirm that the image ID has been queued in RabbitMQ for processing. You can access the RabbitMQ management interface via port-forwarding:
     ```
     kubectl port-forward svc/rabbitmq 15672:15672
     ```
   - Visit `http://localhost:15672` in your browser to check the queue status. You should see the image ID listed in the queue, indicating that it's ready for processing by the consumer service.

3. **Test Consumer Service Processing**:
   - Check the logs of the consumer service to verify it is processing the uploaded image:
     ```
     kubectl logs deployment/consumer
     ```
   - The logs should display messages indicating that the consumer is retrieving and analyzing the image, including details such as whether the image contains a dog or a cat.

4. **End-to-End Functionality**:
   - Conduct an end-to-end test by uploading an image and then monitoring the consumer logs to ensure the analysis matches expectations. This test checks that each component (web server, RabbitMQ, consumer service) interacts properly and that data flows seamlessly through the system as designed.

![image](https://github.com/sivanmarom/signalPet/assets/97241683/e6837771-a699-48f1-a7e5-4377dfade166)

![image](https://github.com/sivanmarom/signalPet/assets/97241683/16f82769-b326-4961-901a-173505dce070)
## 6. Compromises and Limitations

### Compromises:
- **Single Node Cluster**: The use of Minikube limits the deployment to a single node, which is not ideal for a production environment that requires high availability and scalability.

### Limitations:
- **Reproducibility and Scalability**: While Helm has improved the reproducibility of deployments, further enhancements can be made by integrating more comprehensive Infrastructure as Code (IaC) tools like Terraform for full infrastructure setup.

## 7. Future Enhancements

### Expanding IaC Coverage:
- **Comprehensive IaC Integration**: Enhance the use of Infrastructure as Code (IaC) tools by incorporating Terraform alongside Helm. This will allow for comprehensive management of both applications and the underlying cloud infrastructure. The goal is to automate and streamline deployment processes across multiple environments, ensuring consistency and reducing the potential for human error.

### Enhancing Cloud and Multi-Node Capabilities:
- **Transition to Amazon EKS**: Migrate from Minikube to a robust, scalable multi-node Kubernetes cluster using Amazon Elastic Kubernetes Service (EKS). EKS provides high availability, scalability, and security, making it suitable for production environments.


