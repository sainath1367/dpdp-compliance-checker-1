from fastapi.testclient import TestClient

from main import app
from services.scoring_engine import analyze_compliance

client = TestClient(app)


def test_analyze_text_endpoint_returns_success():
    payload = {
        "policy_text": "This privacy policy describes data collection, security, and user rights.",
        "use_ai": False
    }

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200

    result = response.json()
    assert result["status"] == "success"
    assert "data" in result
    assert "overall_score" in result["data"]
    assert result["data"]["analysis_source"] == "local"


def test_empty_policy_returns_zero_score():
    result = analyze_compliance("", use_ai=False)
    assert result["overall_score"] == 0
    assert "High" in result["risk_level"]
    assert result["analysis_source"] == "local"
