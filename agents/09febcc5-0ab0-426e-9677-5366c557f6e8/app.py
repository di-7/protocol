from flask import Flask, request, jsonify

app = Flask(__name__)

import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory to-do list (replace with persistent storage for production)
todo_list = {}

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    try:
        data = request.get_json()
        intent = data.get('intent')

        if intent == 'add_item':
            item = data.get('item')
            if item:
                task_id = str(uuid.uuid4())
                todo_list[task_id] = item
                response = {
                    'success': True,
                    'task_id': task_id,
                    'message': f"Added '{item}' to the to-do list."
                }
            else:
                response = {
                    'success': False,
                    'error': 'Missing item to add.'
                }
        elif intent == 'remove_item':
            task_id = data.get('task_id')
            if task_id in todo_list:
                del todo_list[task_id]
                response = {
                    'success': True,
                    'message': f"Removed item with ID '{task_id}' from the to-do list."
                }
            else:
                response = {
                    'success': False,
                    'error': f"No item with ID '{task_id}' found in the to-do list."
                }
        elif intent == 'list_items':
            items = [{"task_id": task_id, "item": item} for task_id, item in todo_list.items()]
            response = {
                'success': True,
                'items': items
            }
        else:
            response = {
                'success': False,
                'error': 'Unknown intent.'
            }

        return jsonify(response)

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    data = request.get_json()
    # Implement subscription logic here (e.g., store user details for future updates)
    # For simplicity, we'll just return a success message
    return jsonify({'success': True, 'message': 'Subscription successful (not actually implemented).'})

@app.route('/.well-known/agent.json')
def agent_card():
    agent_data = {
        "agentId": "todo-list-agent",
        "displayName": "To-Do List Agent",
        "description": "An agent to manage your to-do list.",
        "primaryLanguage": "en",
        "availableActions": [
            {
                "name": "add_item",
                "description": "Adds an item to the to-do list.",
                "parameters": [
                    {
                        "name": "item",
                        "description": "The item to add.",
                        "type": "string",
                        "required": True
                    }
                ]
            },
            {
                "name": "remove_item",
                "description": "Removes an item from the to-do list.",
                "parameters": [
                    {
                        "name": "task_id",
                        "description": "The ID of the item to remove.",
                        "type": "string",
                        "required": True
                    }
                ]
            },
            {
                "name": "list_items",
                "description": "Lists all items in the to-do list."
            }
        ],
        "intents": [
            {
                "name": "add_item",
                "description": "Add an item to the todo list",
                "parameters": [
                    {
                        "name": "item",
                        "schema": {"type": "string"},
                        "description": "The item to add"
                    }
                ]
            },
            {
                "name": "remove_item",
                "description": "Remove an item from the todo list",
                 "parameters": [
                    {
                        "name": "task_id",
                        "schema": {"type": "string"},
                        "description": "The id of the item to remove"
                    }
                ]
            },
            {
                "name": "list_items",
                "description": "List all items"
            }
        ]
    }
    return jsonify(agent_data)

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
