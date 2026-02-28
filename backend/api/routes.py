from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from domain.schemas import IdeaCreate, IdeaResponse, ReportResponse
from services.analyzer import AnalyzerService
from services.scoring import get_architecture
from db.database import db
from db.models import Idea, Report

api_bp = Blueprint('api', __name__)
analyzer = AnalyzerService()

@api_bp.route('/ideas', methods=['POST'])
def create_idea():
    try:
        data = request.get_json()
        validated_data = IdeaCreate(**data)
        idea = analyzer.create_idea(validated_data.structured_idea)
        return jsonify(IdeaResponse.model_validate(idea).model_dump()), 201
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/ideas/<int:idea_id>/analyze', methods=['POST'])
def analyze_idea(idea_id):
    try:
        report = analyzer.analyze_idea(idea_id)
        if not report:
            # Check if idea just failed
            idea = analyzer.get_idea(idea_id)
            if idea and idea.status == "failed":
                return jsonify({"error": "Analysis failed", "status": "failed"}), 500
            if idea and idea.status == "analyzing":
                return jsonify({"error": "Analysis already in progress", "status": "analyzing"}), 409
            return jsonify({"error": "Idea not found"}), 404
        return jsonify(ReportResponse.model_validate(report).model_dump()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/ideas/<int:idea_id>/report', methods=['GET'])
def get_report(idea_id):
    report = analyzer.get_latest_report(idea_id)
    if not report:
        # Check idea status
        idea = analyzer.get_idea(idea_id)
        if idea:
            return jsonify({"status": idea.status, "message": "No report yet"}), 404
        return jsonify({"error": "Report not found"}), 404
    return jsonify(ReportResponse.model_validate(report).model_dump()), 200

@api_bp.route('/metrics', methods=['GET'])
def get_metrics():
    try:
        total_ideas = db.session.query(Idea).count()
        total_reports = db.session.query(Report).count()
        failed_ideas = db.session.query(Idea).filter_by(status='failed').count()
        
        return jsonify({
            "total_ideas": total_ideas,
            "total_reports": total_reports,
            "failed_analyses": failed_ideas
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@api_bp.route('/architecture/scoring', methods=['GET'])
def architecture_scoring():
    return jsonify({"rules": get_architecture()}), 200
