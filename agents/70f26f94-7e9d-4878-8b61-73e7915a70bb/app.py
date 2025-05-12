from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from flask import Flask, request, jsonify
import uuid
from datetime import datetime

app = Flask(__name__)

# 2In-memory to-do list storage (replace with a database in a real application)
todo_list = {}

AGENT_CARD = {
    "name": "ToDoListAgent",
    "description": "An agent that manages a to-do list.",
    "version": "1.0",
    "provider": {
        "name": "Example Provider",
        "url": "https://example.com"
    },
    "actions": [
        {
            "name": "addTask",
            "description": "Adds a task to the to-do list.",
            "parameters": [
                {"name": "task", "type": "string", "description": "The task to add."}
            ],
            "resultValueType": "string",
            "resultDescription": "The ID of the newly added task."
        },
        {
            "name": "getTasks",
            "description": "Retrieves all tasks from the to-do list.",
            "resultValueType": "array",
            "resultDescription": "A list of tasks."
        },
        {
            "name": "completeTask",
            "description": "Marks a task as complete.",
            "parameters": [
                {"name": "taskId", "type": "string", "description": "The ID of the task to complete."}
            ],
            "resultValueType": "boolean",
            "resultDescription": "True if the task was successfully completed, False otherwise."
        }
    ],
    "events": [
        {
            "name": "taskAdded",
            "description": "Event triggered when a new task is added.",
            "resultValueType": "string",
            "resultDescription": "The ID of the newly added task."
        },
        {
            "name": "taskCompleted",
            "description": "Event triggered when a task is completed.",
            "resultValueType": "string",
            "resultDescription": "The ID of the completed task."
        }
    ]
}

@app.route('/.well-known/agent.json')
def agent_card():
    return jsonify(AGENT_CARD)

@app.route('/tasks/send', methods=['POST'])
def tasks_send():
    request_data = request.get_json()
    intent = request_data.get('intent')
    arguments = request_data.get('arguments', {})

    if intent == 'addTask':
        task = arguments.get('task')
        if not task:
            return jsonify({"error": "Missing task argument"}), 400
        task_id = str(uuid.uuid4())
        todo_list[task_id] = {"task": task, "completed": False, "created_at": str(datetime.now())}
        result = {"resultValue": task_id}
        return jsonify(result)

    elif intent == 'getTasks':
        tasks = [{"id": task_id, **task_data} for task_id, task_data in todo_list.items()]
        result = {"resultValue": tasks}
        return jsonify(result)

    elif intent == 'completeTask':
        task_id = arguments.get('taskId')
        if not task_id:
            return jsonify({"error": "Missing taskId argument"}), 400
        if task_id in todo_list:
            todo_list[task_id]['completed'] = True
            result = {"resultValue": True}
            return jsonify(result)
        else:
            result = {"resultValue": False}
            return jsonify(result)
    else:
        return jsonify({"error": "Unknown intent"}), 400

@app.route('/tasks/sendSubscribe', methods=['POST'])
def tasks_send_subscribe():
    request_data = request.get_json()
    intent = request_data.get('intent')
    # Placeholder for subscription handling (e.g., storing subscriptions)
    print(f"Subscription requested for intent: {intent}")
    return jsonify({"result": "Subscription request received"})

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
