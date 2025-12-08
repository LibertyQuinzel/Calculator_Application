from app.db import get_db
from sqlalchemy.orm import Session


def test_get_db_generator_closes():
    gen = get_db()
    db = next(gen)
    assert isinstance(db, Session)
    # closing the generator should execute the finally branch and close the session
    gen.close()
