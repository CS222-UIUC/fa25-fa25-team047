import json
import types
import pytest

import app as flask_app


@pytest.fixture(autouse=True)
def patch_openai_client():
    """Provide a truthy dummy OpenAI client so /api/chat does not 500."""
    dummy = types.SimpleNamespace()
    dummy.chat = types.SimpleNamespace(completions=types.SimpleNamespace(create=lambda *args, **kwargs: None))
    original = flask_app.openai_client
    flask_app.openai_client = dummy
    yield
    flask_app.openai_client = original


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_regular_message_returns_assistant_reply(client):
    resp = client.post(
        "/api/chat",
        json={"message": "hello", "history": []},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data
    assert "challenge" not in data


def test_challenge_request_returns_structured_challenge(client, monkeypatch):
    # Force generator failure so fallback challenge is used deterministically.
    def boom(*args, **kwargs):
        raise RuntimeError("no quota")

    monkeypatch.setattr(flask_app, "generate_coding_challenge", boom)

    resp = client.post(
        "/api/chat",
        json={"message": "Give me a binary tree challenge", "history": []},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "challenge" in data
    challenge = data["challenge"]
    for field in ["title", "difficulty", "description", "function_signature", "starter_code", "visible_tests", "hidden_tests"]:
        assert field in challenge
    assert isinstance(challenge["visible_tests"], list)
    assert isinstance(challenge["hidden_tests"], list)


def test_regular_message_returns_mock_when_no_openai(client):
    # Simulate missing API key to ensure we return a mock message instead of a 500.
    flask_app.openai_client = None
    resp = client.post(
        "/api/chat",
        json={"message": "hello", "history": []},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert "message" in data
    assert "(mock)" in data["message"]
    assert data.get("warning")


def test_challenge_request_returns_fallback_when_no_openai(client):
    flask_app.openai_client = None
    resp = client.post(
        "/api/chat",
        json={"message": "generate a graph challenge", "history": []},
    )
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("message", "").lower().startswith("using a fallback challenge")
    challenge = data["challenge"]
    for field in ["title", "difficulty", "description", "function_signature", "starter_code", "visible_tests", "hidden_tests"]:
        assert field in challenge
