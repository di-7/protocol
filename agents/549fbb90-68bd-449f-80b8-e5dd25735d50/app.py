from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        if not data or 'message' not in data or 'content' not in data['message'] or 'text' not in data['message']['content']:
            return jsonify({'error': 'Invalid request format'}), 400

        text = data['message']['content']['text']
        try:
            num1, num2 = map(int, text.split('+'))
            result = num1 + num2
            response_text = str(result)
        except ValueError:
            response_text = "Invalid input. Please provide two numbers separated by '+'."

        response = {
            "message": {
                "content": {
                    "text": response_text
                }
            }
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    try:
        data = request.get_json()
        if not data or 'message' not in data or 'content' not in data['message'] or 'text' not in data['message']['content']:
            return jsonify({'error': 'Invalid request format'}), 400

        text = data['message']['content']['text']
        try:
            num1, num2 = map(int, text.split('+'))
            result = num1 + num2
            response_text = str(result)
        except ValueError:
            response_text = "Invalid input. Please provide two numbers separated by '+'."

        task_id = str(uuid.uuid4())

        response = {
            "message": {
                "content": {
                    "text": response_text
                }
            },
            "taskId": task_id
        }
        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/.well-known/agent.json')
def agent_card():
    agent_card_data = {
        "schemaVersion": "0.0.1",
        "name": "Adder Agent",
        "description": "An agent that adds two numbers provided in the format 'number1+number2'.",
        "capabilities": [
            {
                "name": "add_numbers",
                "description": "Adds two numbers.",
                "input": {
                    "type": "text",
                    "description": "Two numbers separated by a '+' sign (e.g., '5+3')."
                },
                "output": {
                    "type": "text",
                    "description": "The sum of the two numbers."
                }
            }
        ],
        "baseUrl": "/",
        "actions": [
            {
                "name": "add",
                "description": "Adds two numbers.",
                "path": "/tasks/send",
                "method": "POST",
                "accepts": "text/plain",
                "returns": "text/plain"
            },
           {
                "name": "add_with_subscription",
                "description": "Adds two numbers and returns a taskId.",
                "path": "/tasks/sendSubscribe",
                "method": "POST",
                "accepts": "text/plain",
                "returns": "text/plain"
            }
        ],
        "agentType": "Utility"
    }
    return jsonify(agent_card_data)

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
