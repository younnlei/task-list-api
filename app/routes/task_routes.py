from flask import Blueprint, request, jsonify, Response
from app.db import db
from app.models.task import Task
from app.routes.route_utilities import validate_model, create_model
from datetime import datetime, timezone
import os
import requests


tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not data.get("title") or not data.get("description"):
        return jsonify({"details": "Invalid data"}), 400

    return create_model(Task, data)


@tasks_bp.get("")
def get_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")

    if sort_param == "asc":
        query = query.order_by(Task.title.asc())

    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query).all()

    tasks_response = []

    for task in tasks:
        tasks_response.append(task.to_dict())

    return tasks_response, 200


@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    task = validate_model(Task, task_id)

    return jsonify(task.to_dict()), 200


@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    data = request.get_json()

    task.title = data["title"]
    task.description = data["description"]

    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return "", 204, {"Content-Type": "application/json"}


@tasks_bp.patch("/<int:task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now(timezone.utc)

    db.session.commit()

    slack_token = os.environ.get("SLACK_BOT_TOKEN")

    headers = {
        "Authorization": f"Bearer {slack_token}"
    }

    data = {
        "channel": "task-notifications-c26",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(
        "https://slack.com/api/chat.postMessage",
        headers=headers,
        json=data
    )

    return Response(status=204, mimetype="application/json")


@tasks_bp.patch("/<int:task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None

    db.session.commit()

    return Response(status=204, mimetype="application/json")