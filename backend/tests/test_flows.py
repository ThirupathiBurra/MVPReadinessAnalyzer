import json
import pytest
from app import create_app
from db.database import db

@pytest.fixture
def test_app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(test_app):
    return test_app.test_client()

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'

def test_create_idea(client):
    payload = {
        "structured_idea": {
            "problem": "People forget to water their plants.",
            "target_user": "Busy millennials with indoor plants.",
            "current_solution": "Setting phone alarms or relying on memory.",
            "proposed_mvp": "An app that connects to a soil sensor and sends push notifications."
        }
    }
    response = client.post('/api/ideas', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['status'] == "pending"
    assert 'id' in data

def test_create_idea_validation(client):
    payload = {
        "structured_idea": {
            "problem": "short",
            "target_user": "u",
            "current_solution": "sys",
            "proposed_mvp": "mvp"
        }
    }
    response = client.post('/api/ideas', json=payload)
    assert response.status_code == 400
    assert 'errors' in response.get_json()

def test_full_analysis_flow(client):
    # 1. Create Idea
    payload = {
        "structured_idea": {
            "problem": "People forget to water their plants.",
            "target_user": "Busy millennials with indoor plants.",
            "current_solution": "Setting phone alarms or relying on memory.",
            "proposed_mvp": "An app that connects to a soil sensor and sends push notifications."
        }
    }
    idea_resp = client.post('/api/ideas', json=payload)
    assert idea_resp.status_code == 201
    idea_id = idea_resp.get_json()['id']

    # 2. Trigger Analysis (Should use AI mock via empty OPENAI_API_KEY environment)
    analyze_resp = client.post(f'/api/ideas/{idea_id}/analyze')
    assert analyze_resp.status_code == 200
    report_data = analyze_resp.get_json()
    
    assert report_data['idea_id'] == idea_id
    assert 'scores' in report_data
    assert 'structured_data' in report_data
    
    # 3. Check Explainability presence 
    assert 'overall_readiness' in report_data['scores']
    assert 'why_this_score' in report_data['structured_data']
    assert 'next_actions' in report_data['structured_data']

    # 4. Fetch Report
    fetch_resp = client.get(f'/api/ideas/{idea_id}/report')
    assert fetch_resp.status_code == 200
    assert fetch_resp.get_json() == report_data

def test_metrics_endpoint(client):
    # Just verify path exists and returns numbers
    resp = client.get('/api/metrics')
    assert resp.status_code == 200
    data = resp.get_json()
    assert "total_ideas" in data
    assert "failed_analyses" in data
