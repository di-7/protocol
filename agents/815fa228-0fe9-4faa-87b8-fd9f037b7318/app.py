from flask import Flask, request, jsonify

app = Flask(__name__)

from flask import Flask, request, jsonify
import uuid
import json

app = Flask(__name__)

# In-memory to-do list (replace with persistent storage for production)
todo_list = {}

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    data = request.get_json()
    task_request = data.get('taskRequest', {})
    surface = task_request.get('surface', {})
    capabilities = surface.get('capabilities', [])
    text_capability = next((cap for cap in capabilities if cap.get('name') == "TEXT"), None)

    if not text_capability:
        return jsonify({"error": "TEXT capability required"}), 400

    inputs = task_request.get('inputs', [])
    main_input = next((inp for inp in inputs if inp.get('name') == "main"), None)

    if not main_input:
        return jsonify({"error": "Main input required"}), 400

    raw_inputs = main_input.get('rawInputs', [])
    if not raw_inputs:
        return jsonify({"error": "Raw input required"}), 400

    query = raw_inputs[0].get('query', '')
    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Process the query and update the to-do list
    if query.lower().startswith("add"):
        item = query[4:].strip()
        if item:
            item_id = str(uuid.uuid4())
            todo_list[item_id] = item
            response_text = f"Added '{item}' to the to-do list."
        else:
            response_text = "What do you want to add?"
    elif query.lower().startswith("list"):
        if todo_list:
            response_text = "To-do list:\n" + "\n".join([f"- {item}" for item in todo_list.values()])
        else:
            response_text = "Your to-do list is empty."
    elif query.lower().startswith("remove"):
        item_to_remove = query[6:].strip()
        removed = False
        for item_id, item in list(todo_list.items()):
            if item.lower() == item_to_remove.lower():
                del todo_list[item_id]
                response_text = f"Removed '{item}' from the to-do list."
                removed = True
                break
        if not removed:
            response_text = f"Item '{item_to_remove}' not found in the to-do list."
    else:
        response_text = "I can add, list, or remove items from your to-do list."

    return jsonify({
        "taskResult": {
            "resultType": "RESULT_TYPE_OK",
            "content": {
                "card": {
                    "title": "To-Do List Agent",
                    "subtitle": "Managing your tasks",
                    "sections": [
                        {
                            "textContent": response_text
                        }
                    ]
                }
            },
            "extensions": {}
        }
    })

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    # Placeholder for subscription handling (not required for this basic example)
    return jsonify({"result": "Subscription not supported"}), 501

@app.route('/.well-known/agent.json')
def agent_card():
    agent_card_data = {
        "agentId": "todo-list-agent",
        "displayName": "To-Do List Agent",
        "shortDescription": "A simple agent to manage your to-do list.",
        "longDescription": "This agent allows you to add, list, and remove items from your to-do list.",
        "capabilities": [
            {
                "name": "TEXT"
            }
        ],
        "termsOfServiceUrl": "https://example.com/terms",
        "privacyPolicyUrl": "https://example.com/privacy",
        "taskTopics": [
            "PRODUCTIVITY"
        ]
    }
    return jsonify(agent_card_data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

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
