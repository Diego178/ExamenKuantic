from fastapi import FastAPI
from fastapi.testclient import TestClient
app = FastAPI()

client = TestClient(app)

def test_delete_movie_invalid_id():
    invalid_id = "5eb7cf5a"
    response = client.delete(f"/movies/{invalid_id}")
    assert response.status_code == 422
    response_body = response.json()
    assert response_body["detail"]["message"] == "Invalid id"
    assert response_body["detail"]["error"] is True

def test_delete_movie_not_found():
    valid_but_nonexistent_id = "5eb7cf5a86d9755df3a6c593"
    response = client.delete(f"/movies/{valid_but_nonexistent_id}")
    print(response.json())
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["detail"]["message"] == "Movie dont found"
    assert response_body["detail"]["error"] is True