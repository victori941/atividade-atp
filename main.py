from flask import Flask, render_template, request, redirect, Flask
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('todo.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, task TEXT)')

@app.route('/')
def index():
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.execute('SELECT * FROM tasks')
        tasks = cursor.fetchall()
    return render_template("index.html", tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task = request.form['task']
    with sqlite3.connect('todo.db') as conn:
        conn.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
    return redirect('/')

@app.route('/delete/<int:id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)


