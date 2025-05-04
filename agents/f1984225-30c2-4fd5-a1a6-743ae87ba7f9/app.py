import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
  "description": "An agent that calculates the multiplication of two digits provided by the user.",
  "name": "Multiplication Agent",
  "version": "1.0",
  "homepage": "http://localhost:5000",
  "capabilities": {
    "multiply": {
      "description": "Multiplies two digits.",
      "input": {
        "type": "object",
        "properties": {
          "digit1": {
            "type": "integer",
            "description": "The first digit to multiply."
          },
          "digit2": {
            "type": "integer",
            "description": "The second digit to multiply."
          }
        },
        "required": ["digit1", "digit2"]
      },
      "output": {
        "type": "object",
        "properties": {
          "result": {
            "type": "integer",
            "description": "The result of the multiplication."
          }
        },
        "required": ["result"]
      }
    }
  }
}


@app.route("/tasks/send", methods=["POST"])
def tasks_send():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    task = data.get("task")
    if not task:
        return jsonify({"error": "Missing 'task' field"}), 400

    if task.get("name") == "multiply":
        try:
            digit1 = task["input"]["digit1"]
            digit2 = task["input"]["digit2"]
            result = digit1 * digit2
            return jsonify({"response": {"result": result}})
        except (KeyError, TypeError) as e:
            return jsonify({"error": f"Invalid input: {e}"}), 400
    else:
        return jsonify({"error": f"Unknown task: {task.get('name')}"}), 400


@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
  # Placeholder, implement if needed
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid request"}), 400
  print("tasks/sendSubscribe called with data:", data)
  return jsonify({"status": "accepted", "message": "Subscription request received"}), 202


@app.route("/.well-known/agent.json")
def agent_card():
    return jsonify(AGENT_CARD)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)