from flask import Blueprint

from flask import Blueprint, request, jsonify, abort
from app.db import db
from app.models.task import Task

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


def validate_task(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        abort(404)

    return task


@tasks_bp.post("")
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data.get("title") or not data.get("description"):
        return jsonify({"details": "Invalid data"}), 400

    task = Task.from_dict(data)

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


@tasks_bp.get("")
def get_tasks():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return jsonify([task.to_dict() for task in tasks]), 200


@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    task = validate_task(task_id)
    return jsonify(task.to_dict()), 200


@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    data = request.get_json()

    task.title = data["title"]
    task.description = data["description"]

    db.session.commit()
    return "", 204, {"Content-Type": "application/json"}


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}