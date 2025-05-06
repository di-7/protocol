from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

AGENT_ID = "adder-agent"
AGENT_NAME = "Adder Agent"
AGENT_DESCRIPTION = "Adds two numbers based on user input."
AGENT_VERSION = "1.0.0"

@app.route('/.well-known/agent.json')
def agent_card():
    return jsonify({
        "id": AGENT_ID,
        "name": AGENT_NAME,
        "description": AGENT_DESCRIPTION,
        "version": AGENT_VERSION,
        "capabilities": {
            "tasks": {
                "send": {
                    "accepts": "application/json",
                    "returns": "application/json"
                },
                "sendSubscribe": {
                    "accepts": "application/json",
                    "returns": "application/json"
                }
            }
        }
    })

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')

        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            return jsonify({"error": "Invalid input. Please provide numbers."}), 400

        result = num1 + num2
        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    try:
        data = request.get_json()
        num1 = data.get('num1')
        num2 = data.get('num2')
        callback_url = data.get('callback_url')

        if not isinstance(num1, (int, float)) or not isinstance(num2, (int, float)):
            return jsonify({"error": "Invalid input. Please provide numbers."}), 400

        if not callback_url:
            return jsonify({"error": "Callback URL is required."}), 400

        task_id = str(uuid.uuid4())

        # Simulate asynchronous processing (replace with actual async2 logic)
        result = num1 + num2

        # Simulate sending the result to the callback URL
        import requests
        try:
            requests.post(callback_url, json={"task_id": task_id, "result": result})
        except requests.exceptions.RequestException as e:
            print(f"Error sending callback: {e}")
            return jsonify({"task_id": task_id, "status": "queued", "error": "Callback failed"}), 202


        return jsonify({"task_id": task_id, "status": "queued"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

# Ensure the process_request function exists
def process_request(input_data):
    try:
        # If the agent code already defines process_request, use it
        if 'process_request' in globals():
            return globals()['process_request'](input_data)
        # Otherwise, provide a default implementation
        return {"status": "Agent processed request", "input": input_data}
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
