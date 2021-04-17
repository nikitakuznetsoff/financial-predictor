from flask import Blueprint, make_response, jsonify

from app import repo

bp = Blueprint('tasks', __name__, url_prefix='/api/tasks')

@bp.route('', methods=['GET'])
def tasks():
    return 'pong', 200


@app.route('/<int:id>', methods=['GET'])
def get_task_status(id):
    task = repo.get_task_status(id)
    if not id:
        return "incorrect id", 400
    else:
        return task.is_completed, 200


