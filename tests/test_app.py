
import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    database_path = tmp_path / "test.db"

    app = create_app({
        "TESTING": True,
        "DATABASE": str(database_path),
    })

    return app.test_client()


def test_home_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"New experiment" in response.data


def test_run_experiment_saves_result(client):
    response = client.post(
        "/run",
        data={
            "workload": "list",
            "iterations": "10",
            "measurement_interval": "5",
        },
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"Memory timeline" in response.data
    assert b"Memory growth" in response.data


def test_invalid_run_shows_error(client):
    response = client.post(
        "/run",
        data={
            "workload": "list",
            "iterations": "0",
            "measurement_interval": "5",
        },
    )

    assert response.status_code == 400
    assert b"positive integer" in response.data


def test_missing_experiment_returns_404(client):
    response = client.get("/experiments/9999")

    assert response.status_code == 404