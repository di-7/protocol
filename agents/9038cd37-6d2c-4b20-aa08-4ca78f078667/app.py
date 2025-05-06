from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

AGENT_ID = "addition-agent"
AGENT_NAME = "Addition Agent"
AGENT_DESCRIPTION = "An agent that adds two numbers provided by the user."
AGENT_VERSION = "1.0"

@app.route('/.well-known/agent.json')
def agent_card():
    agent_card = {
        "agentId": AGENT_ID,
        "name": AGENT_NAME,
        "description": AGENT_DESCRIPTION,
        "version": AGENT_VERSION,
        "capabilities": [
            {
                "name": "Add two numbers",
                "description": "Adds two numbers provided by the user.",
                "model": "addition_model",
                "input": {
                    "type": "object",
                    "properties": {
                        "number1": {"type": "number", "description": "The first number."},
                        "number2": {"type": "number", "description": "The second number."}
                    },
                    "required": ["number1", "number2"]
                },
                "output": {
                    "type": "object",
                    "properties": {
                        "sum": {"type": "number", "description": "The sum of the two numbers."}
                    },
                    "required": ["sum"]
                }
            }
        ]
    }
    return jsonify(agent_card)

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        number1 = data['input']['number1']
        number2 = data['input']['number2']
        sum_result = number1 + number2

        response = {
            "id": str(uuid.uuid4()),
            "response": {
                "status": "completed",
                "output": {"sum": sum_result}
            }
        }
        return jsonify(response), 200
    except (TypeError, KeyError) as e:
        return jsonify({"error": "Invalid input format", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    try:
        data = request.get_json()
        number1 = data['input']['number1']
        number2 = data['input']['number2']
        sum_result = number1 + number2

        callback_url = data['callbackUrl']
        response_data = {
            "id": str(uuid.uuid4()),
            "response": {
                "status": "completed",
                "output": {"sum": sum_result}
            }
        }

        import requests
        try:
            requests.post(callback_url, json=response_data, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Error sending callback: {e}")


        return jsonify({"id": str(uuid.uuid4()), "status": "accepted"}), 202
    except (TypeError, KeyError) as e:
        return jsonify({"error": "Invalid input format", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

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
