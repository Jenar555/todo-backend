from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

DATA_FILE = 'todos.json'

# Helper to read todos from file
def read_todos():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

# Helper to write todos to file
def write_todos(todos):
    with open(DATA_FILE, 'w') as f:
        json.dump(todos, f, indent=2)

@app.route('/todos', methods=['GET'])
def get_todos():
    todos = read_todos()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    todos = read_todos()
    new_todo = request.json
    new_todo['id'] = len(todos) + 1
    new_todo['completed'] = False
    todos.append(new_todo)
    write_todos(todos)
    return jsonify(new_todo), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todos = read_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            data = request.json
            todo.update(data)
            write_todos(todos)
            return jsonify(todo)
    return jsonify({'error': 'Todo not found'}), 404

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = read_todos()
    updated = [todo for todo in todos if todo['id'] != todo_id]
    if len(todos) == len(updated):
        return jsonify({'error': 'Todo not found'}), 404
    write_todos(updated)
    return jsonify({'message': 'Todo deleted'})

# ✅ Proper Render config
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render or fallback to 5000
    app.run(host='0.0.0.0', port=port)
