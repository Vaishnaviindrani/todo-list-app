from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database initialization
def init_db():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = [{'id': row[0], 'title': row[1], 'done': bool(row[2])} for row in cursor.fetchall()]
    conn.close()
    return jsonify(tasks)

@app.route("/")
def home():
    return app.send_static_file("index.html")

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    new_task = request.get_json()
    title = new_task.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Task title is required'}), 400

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO tasks (title, done) VALUES (?, ?)', (title, False))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task added successfully'}), 201

# Mark a task as complete
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    updates = request.get_json()
    done = updates.get('done', None)

    if done is None:
        return jsonify({'error': 'Field "done" is required'}), 400

    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE tasks SET done = ? WHERE id = ?', (done, task_id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Task updated successfully'})

# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
