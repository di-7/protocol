from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify

app = Flask(__name__)

todo_list = []

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    data = request.get_json()
    intent = data.get('intent')
    arguments = data.get('arguments', {})

    if intent == 'add_item':
        item = arguments.get('item')
        if item:
            todo_list.append(item)
            response = {
                "status": "OK",
                "result": f"Added '{item}' to the to-do list."
            }
        else:
            response = {
                "status": "ERROR",
                "error_message": "Item to add is missing."
            }
    elif intent == 'delete_item':
        item = arguments.get('item')
        if item:
            try:
                todo_list.remove(item)
                response = {
                    "status": "OK",
                    "result": f"Deleted '{item}' from the to-do list."
                }
            except ValueError:
                response = {
                    "status": "ERROR",
                    "error_message": f"Item '{item}' not found in the list."
                }
        else:
            response = {
                "status": "ERROR",
                "error_message": "Item to delete is missing."
            }
    elif intent == 'show_list':
        if todo_list:
            response = {
                "status": "OK",
                "result": {"items": todo_list}
            }
        else:
            response = {
                "status": "OK",
                "result": "The to-do list is empty."
            }
    else:
        response = {
            "status": "ERROR",
            "error_message": "Unknown intent."
        }

    return jsonify(response)

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    # 1In this example, we don't handle subscriptions.
    # You would typically store the subscription information here.
    return jsonify({"status": "OK", "result": "Subscription request received."})

@app.route('/.well-known/agent.json')
def agent_card():
    agent_info = {
        "name": "ToDoListAgent",
        "description": "An agent to manage a to-do list.",
        "intents": [
            {
                "name": "add_item",
                "description": "Adds an item to the to-do list.",
                "parameters": [
                    {"name": "item", "type": "string", "description": "The item to add."}
                ]
            },
            {
                "name": "delete_item",
                "description": "Deletes an item from the to-do list.",
                "parameters": [
                    {"name": "item", "type": "string", "description": "The item to delete."}
                ]
            },
            {
                "name": "show_list",
                "description": "Shows the current to-do list.",
                "parameters": []
            }
        ],
        "baseUrl": "/",
        "apiEndpoint": "/tasks/send",
        "subscribeEndpoint": "/tasks/sendSubscribe"
    }
    return jsonify(agent_info)

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
