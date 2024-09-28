from flask import Flask, render_template, request, redirect
import sqlite3
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'SEU_WEBHOOK_URL_AQUI'


def send_discord_alert(message):
    payload = {
        'content': message
    }
    requests.post(DISCORD_WEBHOOK_URL, json=payload)


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

    # Enviar alerta para o Discord
    send_discord_alert(f'Tarefa adicionada: {task}')

    return redirect('/')


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect('todo.db') as conn:
        cursor = conn.execute('SELECT task FROM tasks WHERE id = ?', (task_id,))
        task = cursor.fetchone()
        if task:
            conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
            # Enviar alerta para o Discord
            send_discord_alert(f'Tarefa removida: {task[0]}')
    return redirect('/')


@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        new_task = request.form['task']
        with sqlite3.connect('todo.db') as conn:
            conn.execute('UPDATE tasks SET task = ? WHERE id = ?', (new_task, task_id))
            # Enviar alerta para o Discord
            send_discord_alert(f'Tarefa editada: {new_task}')
        return redirect('/')
    else:
        with sqlite3.connect('todo.db') as conn:
            cursor = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,))
            task = cursor.fetchall()
        return render_template('edit.html', task=task[0], task_id=task_id)


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
