from flask import Flask, request, jsonify

app = Flask(__name__)

#1
import json
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

AGENT_CARD = {
    "agent": "MultiplyAgent",
    "version": "1.0",
    "description": "An agent that multiplies two numbers.",
    "instructions": "Provide two numbers, and I will multiply them.",
    "capabilities": [
        {
            "name": "multiply",
            "description": "Multiplies two numbers.",
            "input": {
                "type": "object",
                "properties": {
                    "num1": {"type": "number", "description": "The first number."},
                    "num2": {"type": "number", "description": "The second number."}
                },
                "required": ["num1", "num2"]
            },
            "output": {
                "type": "object",
                "properties": {
                    "result": {"type": "number", "description": "The product of the two numbers."}
                },
                "required": ["result"]
            }
        }
    ]
}

@app.route("/.well-known/agent.json")
def agent_card():
    return jsonify(AGENT_CARD)

@app.route("/tasks/send", methods=["POST"])
def tasks_send():
    data = request.get_json()
    try:
        num1 = data["input"]["num1"]
        num2 = data["input"]["num2"]
        result = num1 * num2
        response = {
            "output": {"result": result},
            "state": "SUCCEEDED"
        }
        return jsonify(response)
    except (KeyError, TypeError) as e:
        return jsonify({"state": "FAILED", "error": str(e)}), 400
    except Exception as e:
        return jsonify({"state": "FAILED", "error": str(e)}), 500

@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
    data = request.get_json()
    task_id = str(uuid.uuid4())

    try:
        num1 = data["input"]["num1"]
        num2 = data["input"]["num2"]
        result = num1 * num2

        response = {
            "output": {"result": result},
            "state": "SUCCEEDED",
            "taskId": task_id
        }
        return jsonify(response)
    except (KeyError, TypeError) as e:
        return jsonify({"state": "FAILED", "error": str(e), "taskId": task_id}), 400
    except Exception as e:
        return jsonify({"state": "FAILED", "error": str(e), "taskId": task_id}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

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
