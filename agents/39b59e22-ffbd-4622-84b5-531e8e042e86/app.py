from flask import Flask, request, jsonify

app = Flask(__name__)

#1
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
    "agent": "add2numbers",
    "name": "Adder Agent",
    "description": "An agent that adds two numbers.",
    "version": "1.0",
    "homepage": "http://localhost:5000",
    "capabilities": {
        "add": {
            "description": "Adds two numbers and returns the sum.",
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
                    "sum": {"type": "number", "description": "The sum of the two numbers."}
                },
                "required": ["sum"]
            }
        }
    }
}


@app.route("/.well-known/agent.json")
def agent_card():
    return jsonify(AGENT_CARD)


@app.route("/tasks/send", methods=["POST"])
def tasks_send():
    try:
        data = request.get_json()
        task = data.get("task")
        inputs = task.get("inputs")

        if task.get("name") == "add":
            num1 = inputs.get("num1")
            num2 = inputs.get("num2")

            if num1 is None or num2 is None:
                return jsonify({"error": "Missing input parameters."}), 400

            try:
                num1 = float(num1)
                num2 = float(num2)
            except ValueError:
                return jsonify({"error": "Invalid input parameters. Must be numbers."}), 400
                
            sum_result = num1 + num2
            response = {
                "response": {
                    "outputs": {"sum": sum_result}
                },
                "status": "completed"
            }
            return jsonify(response)
        else:
            return jsonify({"error": "Unknown task."}), 400

    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error."}), 500


@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
    try:
        data = request.get_json()
        task = data.get("task")
        subscription = data.get("subscription") # For A2A, we just acknowledge

        response = {
                "response": {
                    "subscription_id": "dummy_subscription_id" #simulate id
                },
                "status": "accepted"
            }
        return jsonify(response)


    except Exception as e:
        print(e)
        return jsonify({"error": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(debug=True)

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
