# app/routes.py
from flask import Blueprint, request, jsonify
from app.services import analyze_response

feedback_blueprint = Blueprint("feedback", __name__)

@feedback_blueprint.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    question = data.get("question", "")
    response = data.get("response", "")
    
    feedback = analyze_response(question, response)
    
    return jsonify(feedback)
