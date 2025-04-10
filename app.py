from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = 'tasks.json'


def load_tasks():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return []
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []


def save_tasks(tasks):
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        print(f"Ошибка записи файла: {e}")


@app.route('/')
@app.route('/tasks')
def list_tasks():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/tasks/create', methods=['POST'])
def create_task():
    title = request.form.get('title')
    description = request.form.get('description')

    if title:
        tasks = load_tasks()
        new_task = {
            'id': len(tasks) + 1 if tasks else 1,
            'title': title,
            'description': description
        }
        tasks.append(new_task)
        save_tasks(tasks)

    return redirect(url_for('list_tasks'))


@app.route('/tasks/edit/<int:task_id>', methods=['GET'])
def edit_task_form(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return redirect(url_for('list_tasks'))
    return render_template('edit_task.html', task=task)


@app.route('/tasks/update/<int:task_id>', methods=['POST'])
def update_task(task_id):
    tasks = load_tasks()
    task = next((t for t in tasks if t['id'] == task_id), None)

    if task:
        task['title'] = request.form.get('title')
        task['description'] = request.form.get('description')
        save_tasks(tasks)

    return redirect(url_for('list_tasks'))


@app.route('/tasks/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    updated_tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(updated_tasks)
    return redirect(url_for('list_tasks'))


if __name__ == '__main__':
    app.run(debug=True)