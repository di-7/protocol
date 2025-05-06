from flask import Flask, request, jsonify
import os
import importlib.util
import sys
from pathlib import Path
from supabase import create_client, Client

app = Flask(__name__)

# Base directory for agents
AGENTS_DIR = Path("agents")

# Supabase configuration
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://lcgzszeurmhxpxuhdyvk.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxjZ3pzemV1cm1oeHB4dWhkeXZrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc0NTE0MjE0NCwiZXhwIjoyMDYwNzE4MTQ0fQ.9nA8g7tIgWCpP9-uasXggn6061WgQueE7fhX_nWycio")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

@app.route('/<agent_id>/.well-known/agent.json', methods=['GET'])
def get_agent_card(agent_id):
    try:
        # Fetch the agent from Supabase
        response = supabase.table("agents").select("agent_card").eq("id", agent_id).single().execute()
        if not response.data:
            return jsonify({"error": f"Agent {agent_id} not found in database"}), 404

        agent_card = response.data["agent_card"]
        return jsonify(agent_card)

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
