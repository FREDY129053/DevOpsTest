# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from src.server import create_app
from pathlib import Path
from uuid import uuid4

@pytest.fixture(scope="function")
def client(tmp_path: Path):
    db_file = tmp_path / f"test_{uuid4().hex}.db"
    app = create_app()

    app.state.db_url = f"sqlite:///{db_file.resolve()}"

    with TestClient(app) as c:
        yield c
