import pytest
from fastapi.testclient import TestClient
try:
    from api.inference import app
except ModuleNotFoundError:
    import sys
    sys.path.append(".")
    from api.inference import app


@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    return client


def test_get(client):
    """Test standard get"""
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"Message": "Stroke Prediction API"}


def test_post_above(client):
    """Test for stroke patient"""
    res = client.post("/predict", json={
        "id": 1,
        "gender": "Female",
        "age": 63,
        "hypertension": 0,
        "heart_disease": 0,
        "ever_married": "Yes",
        "work_type": "Govt_job",
        "Residence_type": "Rural",
        "avg_glucose_level": 205.35,
        "bmi": 42.2,
        "smoking_status": "formerly smoked"
    })

    assert res.status_code == 200
    assert res.json() == {'Output': 'stroke'}


def test_post_below(client):
    """Test for non-stroke patient"""
    res = client.post("/predict", json={
        "id": 2,
        "gender": "Male",
        "age": 12,
        "hypertension": 0,
        "heart_disease": 0,
        "ever_married": "No",
        "work_type": "children",
        "Residence_type": "Rural",
        "avg_glucose_level": 117.04,
        "bmi": 18.1,
        "smoking_status": "Unknown"
    })

    assert res.status_code == 200
    assert res.json() == {'Output': 'no stroke'}
