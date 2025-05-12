from flask import Flask, request, jsonify

app = Flask(__name__)

#2
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
  "agentId": "adder-agent",
  "description": "An agent that adds two numbers.",
  "displayName": "Adder Agent",
  "modelInfo": {
    "name": "Simple Adder",
    "version": "1.0"
  },
  "termsOfService": "https://example.com/tos",
  "privacyPolicy": "https://example.com/privacy",
  "taskTopics": ["calculator", "arithmetic"],
  "contributions": {
    "actions": [
      {
        "name": "add",
        "description": "Adds two numbers.",
        "input": {
          "properties": {
            "num1": {"type": "number", "description": "The first number."},
            "num2": {"type": "number", "description": "The second number."}
          },
          "required": ["num1", "num2"]
        },
        "output": {
          "properties": {
            "sum": {"type": "number", "description": "The sum of the two numbers."}
          },
          "required": ["sum"]
        }
      }
    ]
  }
}

@app.route("/.well-known/agent.json")
def agent_card():
  return jsonify(AGENT_CARD)

@app.route("/tasks/send", methods=["POST"])
def tasks_send():
  data = request.get_json()
  action = data.get("action")

  if action and action["name"] == "add":
    num1 = action["inputs"]["num1"]
    num2 = action["inputs"]["num2"]
    result = num1 + num2

    response = {
      "response": {
        "outputs": {"sum": result}
      },
      "status": "completed"
    }
    return jsonify(response)
  else:
    return jsonify({"status": "failed", "error": "Unsupported action"})

@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
    data = request.get_json()
    action = data.get("action")

    if action and action["name"] == "add":
      num1 = action["inputs"]["num1"]
      num2 = action["inputs"]["num2"]
      result = num1 + num2

      response = {
          "response": {
              "outputs": {"sum": result}
          },
          "status": "completed"
      }
      return jsonify(response)
    else:
      return jsonify({"status": "failed", "error": "Unsupported action"})


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=8080)

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
