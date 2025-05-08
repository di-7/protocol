from flask import Flask, request, jsonify

app = Flask(__name__)

#1
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

AGENT_CARD = {
  "name": "Reverse String Agent",
  "description": "An agent that reverses strings based on user input.",
  "version": "1.0.0",
  "capabilities": [
    {
      "name": "reverse_string",
      "description": "Reverses a given string.",
      "input": {
        "type": "object",
        "properties": {
          "text": {
            "type": "string",
            "description": "The string to reverse."
          }
        },
        "required": ["text"]
      },
      "output": {
        "type": "object",
        "properties": {
          "reversed_text": {
            "type": "string",
            "description": "The reversed string."
          }
        },
        "required": ["reversed_text"]
      }
    }
  ],
  "url": "https://your-agent-url.com" # Replace with your agent's URL
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
    text = inputs.get("text")

    if text is None:
      return jsonify({"error": "Missing 'text' input."}), 400

    reversed_text = text[::-1]
    response = {
        "response": {
            "outputs": {
                "reversed_text": reversed_text
            }
        },
        "status": "completed"
    }
    return jsonify(response)
  except Exception as e:
    return jsonify({"error": str(e)}), 500


@app.route("/tasks/sendSubscribe", methods=["POST"])
def tasks_send_subscribe():
  try:
    data = request.get_json()
    task = data.get("task")
    inputs = task.get("inputs")
    text = inputs.get("text")
    callback_url = data.get("callbackUrl")

    if text is None:
      return jsonify({"error": "Missing 'text' input."}), 400
    if callback_url is None:
      return jsonify({"error": "Missing 'callbackUrl'."}), 400

    reversed_text = text[::-1]

    # Simulate asynchronous processing (replace with actual async logic)
    import time
    time.sleep(1)

    import requests
    try:
        requests.post(callback_url, json={
            "response": {
                "outputs": {
                    "reversed_text": reversed_text
                }
            },
            "status": "completed"
        })
    except requests.exceptions.RequestException as e:
         print(f"Error sending callback: {e}") # Log the error

    return jsonify({"status": "accepted"})

  except Exception as e:
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  app.run(debug=True, port=8080)

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
