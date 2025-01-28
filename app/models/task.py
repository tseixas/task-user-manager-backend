from flask import current_app
from datetime import datetime
from bson import ObjectId


class Task:
    def __init__(self, title, description, due_date, status='pending'):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.created_at = datetime.utcnow()

    @staticmethod
    def create_task(title, description, due_date, task_id=None):
        mongo = current_app.mongo

        task_data = {
            'task_id': task_id,
            'title': title,
            'description': description,
            'due_date': due_date,
            'status': 'pending',
            'created_at': datetime.utcnow()
        }

        result = mongo.db.tasks.insert_one(task_data)
        task_data['_id'] = str(result.inserted_id)

        return task_data

    @staticmethod
    def get_task_by_id(task_id):
        mongo = current_app.mongo

        task = mongo.db.tasks.find_one({'_id': ObjectId(task_id)})

        if task:
            task['_id'] = str(task['_id'])

            return task
        
        return None

    @staticmethod
    def get_all_tasks():
        mongo = current_app.mongo
        tasks = mongo.db.tasks.find()

        return [{
            '_id': str(task['_id']),
            'title': task['title'],
            'due_date': task['due_date'],
            'status': task['status']
        } for task in tasks]

    @staticmethod
    def update_task(task_id, title=None, description=None, due_date=None, status=None):
        mongo = current_app.mongo

        update_data = {}

        if title:
            update_data['title'] = title

        if description:
            update_data['description'] = description

        if due_date:
            update_data['due_date'] = due_date

        if status:
            update_data['status'] = status

        result = mongo.db.tasks.update_one(
            {'task_id': task_id}, {'$set': update_data})

        if result.matched_count > 0:
            return mongo.db.tasks.find_one({'_id': ObjectId(task_id)})

        return None

    @staticmethod
    def delete_task(task_id):
        mongo = current_app.mongo

        result = mongo.db.tasks.delete_one({'_id': ObjectId(task_id)})

        return result.deleted_count > 0
