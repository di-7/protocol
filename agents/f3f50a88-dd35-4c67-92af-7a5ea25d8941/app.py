from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
  "name": "Number Adder Agent",
  "description": "An agent that adds two numbers.",
  "a2a:Service": [
    {
      "api": {
        "a2a:Operation": [
          {
            "a2a:method": "tasks/send",
            "a2a:path": "/tasks/send",
            "description": "Add two numbers",
            "input": {
              "type": "object",
              "properties": {
                "num1": {
                  "type": "number",
                  "description": "The first number to add."
                },
                "num2": {
                  "type": "number",
                  "description": "The second number to add."
                }
              },
              "required": [
                "num1",
                "num2"
              ]
            },
            "output": {
              "type": "object",
              "properties": {
                "sum": {
                  "type": "number",
                  "description": "The sum of the two numbers."
                }
              },
              "required": [
                "sum"
              ]
            }
          },
          {
            "a2a:method": "tasks/sendSubscribe",
            "a2a:path": "/tasks/sendSubscribe",
            "description": "Add two numbers and trigger a subscription event.",
            "input": {
              "type": "object",
              "properties": {
                "num1": {
                  "type": "number",
                  "description": "The first number to add."
                },
                "num2": {
                  "type": "number",
                  "description": "The second number to add."
                },
                 "a2a:callback":{
                  "type":"string",
                  "format": "URL",
                  "description": "URL to send back the sum result"
                  }
              },
              "required": [
                "num1",
                "num2",
                "a2a:callback"
              ]
            },
            "output": {
              "type": "object",
              "properties": {
                "sum": {
                  "type": "number",
                  "description": "The sum of the two numbers."
                }
              },
              "required": [
                "sum"
              ]
            }
          }
        ]
      }
    }
  ]
}


@app.route("/.well-known/agent.json")
def agent_card():
  return jsonify(AGENT_CARD)


@app.route("/tasks/send", methods=["POST"])
def tasks_send():
  try:
    data = request.get_json()
    num1 = data["num1"]
    num2 = data["num2"]
    sum_result = num1 + num2
    return jsonify({"sum": sum_result})
  except (KeyError, TypeError) as e:
    return jsonify({"error": "Invalid request. Please provide num1 and num2."}), 400


@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
  try:
    data = request.get_json()
    num1 = data["num1"]
    num2 = data["num2"]
    callback_url = data["a2a:callback"]
    sum_result = num1 + num2

    # In a real implementation, you would asynchronously call the callback_url
    # For this example, we'll just print it and return the result.
    print(f"Sending result to: {callback_url} with sum: {sum_result}")
    return jsonify({"sum": sum_result})

  except (KeyError, TypeError) as e:
    return jsonify({"error": "Invalid request. Please provide num1, num2 and a2a:callback."}), 400

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
