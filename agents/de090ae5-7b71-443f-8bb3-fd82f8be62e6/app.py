from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
    "agent": "string-reverser",
    "displayName": "String Reverser Agent",
    "description": "Reverses the input string.",
    "a2a:version": "0.1",
    "homepage": "https://example.com/string-reverser",
    "tasks": {
        "reverse": {
            "name": "reverse",
            "description": "Reverses the input string.",
            "input": {
                "type": "string",
                "description": "The string to reverse."
            },
            "output": {
                "type": "string",
                "description": "The reversed string."
            }
        }
    }
}


@app.route("/tasks/send", methods=["POST"])
def tasks_send():
    try:
        data = request.get_json()
        task_name = data.get("task")
        input_data = data.get("input")

        if task_name == "reverse":
            input_string = input_data.get("value")
            reversed_string = input_string[::-1]
            response = {"output": {"value": reversed_string}}
            return jsonify(response), 200
        else:
            return jsonify({"error": "Unknown task"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
    # This is a placeholder.  Real implementation requires handling subscriptions.
    return jsonify({"message": "Subscription not implemented"}), 501


@app.route("/.well-known/agent.json")
def agent_card():
    return jsonify(AGENT_CARD)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
```

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
