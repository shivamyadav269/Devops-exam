from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_openapi():
    response = client.get("/openapi.json")
    assert response.status_code == 200


def test_student_routes_exist():
    response = client.get("/openapi.json")
    paths = response.json()["paths"]

    assert "/student" in paths
    assert "/student/{id}" in paths