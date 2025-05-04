from flask import Flask, request, jsonify
import os

app = Flask(__name__)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
    "name": "Multiplication Agent",
    "description": "An agent that multiplies two numbers based on user input.",
    "version": "1.0",
    "developer": {
        "name": "Your Name",
        "url": "https://your-website.com"
    },
    "capabilities": [
        {
            "name": "Multiply Numbers",
            "description": "Multiplies two numbers provided by the user.",
            "input": {
                "type": "object",
                "properties": {
                    "number1": {
                        "type": "number",
                        "description": "The first number to multiply."
                    },
                    "number2": {
                        "type": "number",
                        "description": "The second number to multiply."
                    }
                },
                "required": ["number1", "number2"]
            },
            "output": {
                "type": "object",
                "properties": {
                    "result": {
                        "type": "number",
                        "description": "The product of the two numbers."
                    }
                },
                "required": ["result"]
            }
        }
    ],
    "privacy_policy_url": "https://your-website.com/privacy",
    "terms_of_service_url": "https://your-website.com/terms"
}

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        number1 = data['input']['number1']
        number2 = data['input']['number2']
        result = number1 * number2
        response = {
            "output": {
                "result": result
            },
            "state": "completed"
        }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"error": str(e), "state": "failed"}), 400

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
   try:
        data = request.get_json()
        number1 = data['input']['number1']
        number2 = data['input']['number2']
        result = number1 * number2
        response = {
            "output": {
                "result": result
            },
            "state": "completed"
        }
        return jsonify(response), 200
   except Exception as e:
        return jsonify({"error": str(e), "state": "failed"}), 400

@app.route('/.well-known/agent.json')
def agent_card():
    return jsonify(AGENT_CARD)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)

# Add a Flask endpoint that will call the agent's main function
@app.route('/', methods=['GET', 'POST'])
def main_endpoint():
    try:
        if request.method == 'GET':
            return jsonify({"status": "Agent is running"})
        
        # For POST requests, parse JSON input and pass to agent function
        input_data = request.json if request.is_json else {}
        result = process_request(input_data)  # Assuming the agent has a process_request function
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
