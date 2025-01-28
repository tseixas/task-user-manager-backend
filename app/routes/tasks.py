from flask import Blueprint, request, jsonify
from app.models.task import Task

tasks = Blueprint('tasks', __name__)


@tasks.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')

    if not title or not description or not due_date:
        return jsonify({'error': 'Missing required fields'}), 400

    task = Task.create_task(title, description, due_date)

    return jsonify({'task_id': task['task_id'], 'title': task['title'], 'due_date': task['due_date']}), 201


@tasks.route('/', methods=['GET'])
def get_tasks():
    tasks = Task.get_all_tasks()

    return jsonify(tasks), 200


@tasks.route('/<task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.get_task_by_id(task_id)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify(task), 200


@tasks.route('/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date')
    status = data.get('status')

    task = Task.update_task(task_id, title, description, due_date, status)

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    return jsonify(task), 200


@tasks.route('/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    if Task.delete_task(task_id):
        return jsonify({'message': 'Task deleted successfully'}), 200

    return jsonify({'error': 'Task not found'}), 404
