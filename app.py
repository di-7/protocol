from flask import Flask, request, jsonify
import os
import importlib.util
import sys
from pathlib import Path

app = Flask(__name__)

# Base directory for agents
AGENTS_DIR = Path("agents")

@app.route('/<agent_id>/', methods=['GET', 'POST'])
def handle_agent(agent_id):
    try:
        # Check if the agent directory exists
        agent_dir = AGENTS_DIR / agent_id
        if not agent_dir.exists() or not agent_dir.is_dir():
            return jsonify({"error": f"Agent {agent_id} not found"}), 404

        # Path to the agent's app.py
        agent_file = agent_dir / "app.py"
        if not agent_file.exists():
            return jsonify({"error": f"Agent {agent_id} has no app.py"}), 404

        # Dynamically load the agent's module
        module_name = f"agents.{agent_id}.app"
        spec = importlib.util.spec_from_file_location(module_name, str(agent_file))
        if spec is None:
            return jsonify({"error": "Failed to load agent module"}), 500

        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        # Check if the agent module has a process_request function
        if not hasattr(module, 'process_request'):
            return jsonify({"error": "Agent module missing process_request function"}), 500

        # Handle the request
        if request.method == 'GET':
            return jsonify({"status": f"Agent {agent_id} is running"})

        # For POST requests, parse JSON input and pass to agent's process_request
        input_data = request.json if request.is_json else {}
        result = module.process_request(input_data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def list_agents():
    try:
        # List all agent directories
        agent_dirs = [d.name for d in AGENTS_DIR.iterdir() if d.is_dir() and (d / "app.py").exists()]
        return jsonify({"agents": agent_dirs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
