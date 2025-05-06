from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
    "name": "Multiplier Agent",
    "description": "Multiplies two numbers provided by the user.",
    "model": "Simple Multiplication",
    "termsOfService": "https://example.com/terms",
    "privacyPolicy": "https://example.com/privacy",
    "authenticationSchemes": [],
    "contact": "support@example.com",
    "agentEndpoints": [
        {
            "method": "tasks/send",
            "url": "/tasks/send",
            "input": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "number1": {"type": "number"},
                        "number2": {"type": "number"}
                    },
                    "required": ["number1", "number2"]
                }
            },
            "output": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "result": {"type": "number"}
                    },
                    "required": ["result"]
                }
            }
        },
        {
            "method": "tasks/sendSubscribe",
            "url": "/tasks/sendSubscribe",
            "input": {
                "schema": {
                    "type": "object",
                    "properties": {
                        "number1": {"type": "number"},
                        "number2": {"type": "number"},
                        "callbackUrl": {"type": "string", "format": "url"}
                    },
                    "required": ["number1", "number2", "callbackUrl"]
                }
            }
        }
    ]
}

@app.route('/.well-known/agent.json')
def agent_card():
    return jsonify(AGENT_CARD)

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        number1 = float(data['number1'])
        number2 = float(data['number2'])
        result = number1 * number2
        return jsonify({'result': result})
    except (TypeError, KeyError) as e:
        return jsonify({'error': 'Invalid input'}), 400

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    try:
        data = request.get_json()
        number1 = float(data['number1'])
        number2 = float(data['number2'])
        callback_url = data['callbackUrl']

        # In a real application, you would trigger an asynchronous task
        # to perform the multiplication and then POST the result to the
        # callback_url.  This is a simplified example.
        result = number1 * number2

        # In a real scenario, implement the callback to send the result
        # to the provided callback URL.  This could use libraries like 'requests'.
        # Example (not a complete implementation):
        # import requests
        # response = requests.post(callback_url, json={'result': result})

        # For this example, we just log the result (synchronously), and pretend the callback happened.
        print(f"Multiplication result: {result}.  Pretending to send to {callback_url}")
        return jsonify({'status': 'Subscription received, processing.'}), 202
    except (TypeError, KeyError) as e:
        return jsonify({'error': 'Invalid input'}), 400


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
