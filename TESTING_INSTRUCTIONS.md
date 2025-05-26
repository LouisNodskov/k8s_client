# Testing Instructions for the Kubernetes Flask Web App

This document provides instructions on how to set up the environment and test the Flask web application endpoint for managing Kubernetes deployments.

## 1. Prerequisites

*   **Minikube:** Install Minikube by following the official instructions for your operating system: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)
*   **kubectl:** Install kubectl, the Kubernetes command-line tool: [https://kubernetes.io/docs/tasks/tools/install-kubectl/](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
*   **Python:** Ensure Python (3.8+) is installed.
*   **Git:** Ensure Git is installed to clone the repository.

## 2. Setup Kubernetes Cluster and Deploy Application

1.  **Start Minikube:**
    ```bash
    minikube start
    ```
    *(Wait for the cluster to be ready. This might take a few minutes.)*

2.  **Set kubectl context to Minikube (usually done automatically by `minikube start`):**
    ```bash
    kubectl config use-context minikube
    ```

3.  **Deploy the 'hello-minikube' application:**
    This is the application we will test against.
    ```bash
    kubectl create deployment hello-minikube --image=kicbase/echo-server:1.0
    ```

4.  **Expose the 'hello-minikube' deployment (Optional, but good for verification):**
    ```bash
    kubectl expose deployment hello-minikube --type=NodePort --port=8080
    ```
    You can get the URL to access it via:
    ```bash
    minikube service hello-minikube --url
    ```

5.  **Verify deployment:**
    Check if the `hello-minikube` pods are running:
    ```bash
    kubectl get pods
    ```
    You should see pods with names like `hello-minikube-<some-hash>-<some-id>`.

## 3. Setup and Run the Flask Application

**Important:** All commands in this section should be executed from the root directory of the project (the one containing the `k8s_client` directory and `requirements.txt`).

1.  **Clone the repository (if you haven't already):**
    ```bash
    # git clone <repository-url>
    # cd <repository-directory>
    ```

2.  **Install dependencies:**
    Navigate to the root of the project directory (where `requirements.txt` is located).
    It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Run the Flask application:**
    ```bash
    # From the project root directory:
    python -m k8s_client.web_app
    ```
    ```bash
    # Alternatively, from the project root directory, you can use the `flask` command:
    # Ensure FLASK_APP points to the web_app.py file relative to your current directory.
    FLASK_APP=k8s_client/web_app.py flask run --host=0.0.0.0 --port=5000
    ```
    ```bash
    # As another alternative, from the project root directory:
    python k8s_client/web_app.py
    ```
    The application will typically start on `http://0.0.0.0:5000/`.

## 4. Test the API Endpoints

Use a tool like `curl` or Postman to send requests to the Flask application. Replace `hello-minikube` with your target deployment if different. The default namespace is assumed.

**Target Deployment:** `hello-minikube`

**Endpoints:**

*   **List Pods:**
    ```bash
    curl http://localhost:5000/api/deployment/hello-minikube/list_pods
    ```
    *(Expected: JSON response indicating success. Pod details will be printed in the Flask app's console output.)*

*   **Pause Deployment:**
    ```bash
    curl -X POST http://localhost:5000/api/deployment/hello-minikube/pause_deployment
    ```
    *(Expected: JSON response indicating success. Verify by checking deployment status with `kubectl get deployment hello-minikube` - replicas should go to 0 if observed immediately, or new rollouts will be paused.)*
    To see the effect, you might try scaling after pausing:
    ```bash
    kubectl scale deployment hello-minikube --replicas=3 # This change will be pending
    kubectl get pods # You might not see new pods immediately
    ```

*   **Resume Deployment:**
    ```bash
    curl -X POST http://localhost:5000/api/deployment/hello-minikube/resume_deployment
    ```
    *(Expected: JSON response indicating success. If you paused and scaled, the new replicas should now start creating.)*
    ```bash
    kubectl get pods # You should see new pods if you scaled up while paused
    ```

*   **Restart Deployment:**
    ```bash
    curl -X POST http://localhost:5000/api/deployment/hello-minikube/restart_deployment
    ```
    *(Expected: JSON response indicating success. Pods for `hello-minikube` will be terminated and new ones created. Check with `kubectl get pods`.)*

*   **Invalid Command:**
    ```bash
    curl http://localhost:5000/api/deployment/hello-minikube/invalid_command
    ```
    *(Expected: JSON response with an error message and a 400 status code.)*

## 5. Cleanup

1.  **Delete the deployment:**
    ```bash
    kubectl delete deployment hello-minikube
    kubectl delete service hello-minikube
    ```

2.  **Stop Minikube:**
    ```bash
    minikube stop
    ```

3.  **Deactivate virtual environment (if used):**
    ```bash
    deactivate
    ```
