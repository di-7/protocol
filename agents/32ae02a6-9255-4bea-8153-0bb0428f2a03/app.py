from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify
from uuid import uuid4

app = Flask(__name__)

# In-memory todo list (replace with persistent storage for production)
todo_list = []

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    data = request.get_json()
    intent = data.get('intent')

    if intent == 'add_todo':
        item = data.get('item')
        if item:
            todo_list.append({'id': str(uuid4()), 'task': item, 'completed': False})
            return jsonify({'status': 'OK', 'response': f'Added "{item}" to the todo list.'})
        else:
            return jsonify({'status': 'ERROR', 'error': 'Missing "item" parameter for add_todo intent.'}), 400

    elif intent == 'list_todos':
        return jsonify({'status': 'OK', 'todos': todo_list})

    elif intent == 'complete_todo':
        item_id = data.get('item_id')
        if item_id:
            for item in todo_list:
                if item['id'] == item_id:
                    item['completed'] = True
                    return jsonify({'status': 'OK', 'response': f'Marked todo item {item_id} as completed.'})
            return jsonify({'status': 'ERROR', 'error': f'Todo item with id {item_id} not found.'}), 404
        else:
            return jsonify({'status': 'ERROR', 'error': 'Missing "item_id" parameter for complete_todo intent.'}), 400

    elif intent == 'delete_todo':
        item_id = data.get('item_id')
        if item_id:
            original_length = len(todo_list)
            todo_list[:] = [item for item in todo_list if item['id'] != item_id]
            if len(todo_list) < original_length:
                return jsonify({'status': 'OK', 'response': f'Deleted todo item {item_id}.'})
            else:
                return jsonify({'status': 'ERROR', 'error': f'Todo item with id {item_id} not found.'}), 404
        else:
            return jsonify({'status': 'ERROR', 'error': 'Missing "item_id" parameter for delete_todo intent.'}), 400

    else:
        return jsonify({'status': 'ERROR', 'error': f'Unknown intent: {intent}'}), 400

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    data = request.get_json()
    # Implementation for subscribing to todo list changes (e.g., using websockets or polling)
    # This is a placeholder and needs to be implemented based on your desired subscription mechanism
    return jsonify({'status': 'OK', 'message': 'Subscription request received.  Subscription not yet implemented.'})

@app.route('/.well-known/agent.json')
def agent_card():
    agent_card_data = {
        "agentId": "todo-list-agent",
        "displayName": "To-Do List Agent",
        "description": "An agent that manages a to-do list.",
        "provider": "Your Organization",
        "authentication": {
            "type": "NONE"
        },
        "apiEndpoints": [
            {
                "name": "tasks/send",
                "url": "/tasks/send",
                "method": "POST",
                "description": "Endpoint for adding, listing, completing, and deleting todo items.",
                "params": [
                    {"name": "intent", "type": "string", "description": "The intent to execute (add_todo, list_todos, complete_todo, delete_todo)."},
                    {"name": "item", "type": "string", "description": "The todo item to add (required for add_todo)."},
                    {"name": "item_id", "type": "string", "description": "The ID of the todo item (required for complete_todo and delete_todo)."}
                ]
            },
            {
                "name": "tasks/sendSubscribe",
                "url": "/tasks/sendSubscribe",
                "method": "POST",
                "description": "Endpoint for subscribing to updates to the todo list.",
                "params": []
            }
        ],
        "intents": [
            {
                "name": "add_todo",
                "description": "Adds a new item to the todo list.",
                "params": [
                    {"name": "item", "type": "string", "description": "The todo item to add."}
                ]
            },
            {
                "name": "list_todos",
                "description": "Lists all items in the todo list.",
                "params": []
            },
            {
                "name": "complete_todo",
                "description": "Marks an item in the todo list as completed.",
                "params": [
                    {"name": "item_id", "type": "string", "description": "The ID of the todo item to complete."}
                ]
            },
              {
                "name": "delete_todo",
                "description": "Deletes an item from the todo list.",
                "params": [
                    {"name": "item_id", "type": "string", "description": "The ID of the todo item to delete."}
                ]
            }
        ]
    }
    return jsonify(agent_card_data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

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
