from flask import Blueprint, request, jsonify, Response
from app import db
from app.models.goal import Goal

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


def validate_goal(goal_id):
    goal = db.session.get(Goal, goal_id)

    if not goal:
        return None

    return goal


@goals_bp.get("")
def get_goals():
    goals = db.session.scalars(db.select(Goal)).all()
    return jsonify([goal.to_dict() for goal in goals]), 200


@goals_bp.get("/<int:goal_id>")
def get_goal(goal_id):
    goal = validate_goal(goal_id)

    if not goal:
        return jsonify({"message": "Goal not found"}), 404

    return jsonify(goal.to_dict()), 200


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if not request_body or "title" not in request_body:
        return jsonify({"details": "Invalid data"}), 400

    goal = Goal.from_dict(request_body)

    db.session.add(goal)
    db.session.commit()

    return jsonify(goal.to_dict()), 201


@goals_bp.put("/<int:goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)

    if not goal:
        return jsonify({"message": "Goal not found"}), 404

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    return Response(status=204, mimetype="application/json")


@goals_bp.delete("/<int:goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)

    if not goal:
        return jsonify({"message": "Goal not found"}), 404

    db.session.delete(goal)
    db.session.commit()

    return Response(status=204, mimetype="application/json")