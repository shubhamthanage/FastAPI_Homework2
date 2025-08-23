# tests/conftest.py
import tempfile
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from app.db.session import get_session
from app.core.config import settings

@pytest.fixture(autouse=True)
def set_test_env(tmp_path, monkeypatch):
    # Use a temporary sqlite DB for tests
    db_file = tmp_path / "test.db"
    url = f"sqlite:///{db_file}"
    monkeypatch.setenv("DATABASE_URL", url)
    # reload settings module values (simple)
    settings.DATABASE_URL = url
    # create engine with test file
    from app.db.session import engine as _engine
    # recreate metadata on engine
    SQLModel.metadata.create_all(_engine)
    yield
    # cleanup is automatic with tmp_path

@pytest.fixture()
def client():
    return TestClient(app)