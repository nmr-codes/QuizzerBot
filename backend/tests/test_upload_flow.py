import io

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_endpoint_accepts_file(monkeypatch, tmp_path):
    # Monkeypatch storage path to tmp
    monkeypatch.setenv("STORAGE_LOCAL_PATH", str(tmp_path))
    data = {"file": (io.BytesIO(b"hello world"), "test.txt")}
    resp = client.post("/api/v1/uploads", files=data)
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert "id" in body and body.get("status") == "queued"
