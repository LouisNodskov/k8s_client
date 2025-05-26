from flask import Flask, request, jsonify
from k8s_client.controller.kubernetes_controller import KubernetesController

app = Flask(__name__)

@app.route('/api/deployment/<string:deployment_name>/<string:command>', methods=['GET', 'POST'])
def manage_deployment(deployment_name: str, command: str):
    controller = KubernetesController()
    try:
        if command == "list_pods":
            controller.list_pods_with_logs(namespace_filter="default")
            return jsonify({"status": "success", "command": "list_pods", "message": "Pods listed. Check application logs for details."}), 200
        elif command == "pause_deployment":
            controller.pause_deployment(namespace="default", deployment_name=deployment_name)
            return jsonify({"status": "success", "command": "pause_deployment", "deployment_name": deployment_name}), 200
        elif command == "restart_deployment":
            controller.restart_deployment(namespace="default", deployment_name=deployment_name)
            return jsonify({"status": "success", "command": "restart_deployment", "deployment_name": deployment_name}), 200
        elif command == "resume_deployment":
            controller.resume_deployment(namespace="default", deployment_name=deployment_name)
            return jsonify({"status": "success", "command": "resume_deployment", "deployment_name": deployment_name}), 200
        else:
            return jsonify({"status": "error", "message": "Invalid command"}), 400
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    import os
    import sys
    # Add the project root to sys.path to allow direct execution of web_app.py
    # and resolve imports like 'from k8s_client.controller...'
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Note: For development only. For production, use a WSGI server.
    app.run(debug=True, host='0.0.0.0', port=5000)
