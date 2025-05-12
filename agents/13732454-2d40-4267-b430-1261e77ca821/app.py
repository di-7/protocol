from flask import Flask, request, jsonify

app = Flask(__name__)

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class ToDoListAgent(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.todo_list = []
        super().__init__(*args, **kwargs)

    def do_GET(self):
        if self.path == '/.well-known/agent.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            agent_card = {
                "name": "ToDoListAgent",
                "description": "An AI agent that manages a to-do list.",
                "methods": [
                    {
                        "name": "tasks/send",
                        "description": "Adds a task to the to-do list.",
                        "input": {
                            "type": "object",
                            "properties": {
                                "task": {
                                    "type": "string",
                                    "description": "The task to add."
                                }
                            },
                            "required": ["task"]
                        },
                        "output": {
                            "type": "object",
                            "properties": {
                                "success": {
                                    "type": "boolean",
                                    "description": "Indicates if the task was successfully added."
                                }
                            }
                        }
                    },
                    {
                        "name": "tasks/sendSubscribe",
                        "description": "Retrieves the current to-do list.",
                        "output": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "description": "A task in the to-do list."
                            }
                        }
                    }
                ]
            }
            self.wfile.write(json.dumps(agent_card).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")

    def do_POST(self):
        if self.path == '/tasks/send':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode())
                task = data.get('task')
                if task:
                    self.todo_list.append(task)
                    response = {"success": True}
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Task not provided"}).encode())

            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())

        elif self.path == '/tasks/sendSubscribe':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.todo_list).encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"Not Found")

def run(server_class=HTTPServer, handler_class=ToDoListAgent, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting server on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()

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
