from fastapi.testclient import TestClient
from main import app
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_calc_errors.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def get_auth_headers():
    # register a user and return headers
    email = 'errs@example.com'
    r = client.post('/users/register', json={'email': email, 'password': 'password123'})
    assert r.status_code == 200
    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


def test_get_nonexistent_calc_returns_404():
    headers = get_auth_headers()
    r = client.get('/calculations/999', headers=headers)
    assert r.status_code == 404
