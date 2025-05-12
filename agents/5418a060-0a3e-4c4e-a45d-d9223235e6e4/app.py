from flask import Flask, request, jsonify

app = Flask(__name__)

import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_ID = "add-agent"
AGENT_NAME = "Adder Agent"
AGENT_DESCRIPTION = "An agent that adds two numbers."
AGENT_VERSION = "1.0"
AGENT_A2A_VERSION = "0.2"

@app.route('/.well-known/agent.json')
def agent_card():
    agent_data = {
        "id": AGENT_ID,
        "name": AGENT_NAME,
        "description": AGENT_DESCRIPTION,
        "version": AGENT_VERSION,
        "a2a_version": AGENT_A2A_VERSION,
        "capabilities": [
            {
                "name": "add",
                "description": "Adds two numbers.",
                "parameters": [
                    {"name": "num1", "type": "number", "description": "The first number."},
                    {"name": "num2", "type": "number", "description": "The second number."}
                ],
                "returns": {"type": "number", "description": "The sum of the two numbers."},
                "type": "fn"
            }
        ],
        "communication": {
            "protocols": [
                {"name": "http"}
            ],
            "url": request.url_root
        }
    }
    return jsonify(agent_data)


@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    data = request.get_json()
    try:
        task = data["task"]
        inputs = task["inputs"]
        capability = task["capability"]
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid request format"}), 400

    if capability != "add":
        return jsonify({"error": "Unsupported capability"}), 400

    try:
        num1 = float(inputs["num1"])
        num2 = float(inputs["num2"])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input parameters"}), 400

    result = num1 + num2

    response = {
        "id": str(uuid.uuid4()),
        "result": result,
        "status": "succeeded"
    }
    return jsonify(response)


@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    data = request.get_json()
    try:
        task = data["task"]
        inputs = task["inputs"]
        capability = task["capability"]
        callback_url = data["callback"]
    except (KeyError, TypeError):
        return jsonify({"error": "Invalid request format"}), 400

    if capability != "add":
        return jsonify({"error": "Unsupported capability"}), 400

    try:
        num1 = float(inputs["num1"])
        num2 = float(inputs["num2"])
    except (KeyError, ValueError):
        return jsonify({"error": "Invalid input parameters"}), 400

    result = num1 + num2

    response = {
        "id": str(uuid.uuid4()),
        "result": result,
        "status": "succeeded"
    }

    # 3In a real implementation, you would asynchronously send the response
    # to the callback_url.  This example only returns the response.
    return jsonify(response)


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
