import os
from datetime import timedelta
from app import security


def test_prepare_password_bytes_type_error():
    import pytest
    with pytest.raises(TypeError):
        security._prepare_password_bytes(123)


def test_hash_and_verify_short_password():
    pw = 'shortpass'
    h = security.hash_password(pw)
    assert isinstance(h, str)
    assert security.verify_password(pw, h)


def test_hash_and_verify_long_password():
    # create a long password > 100 chars to force SHA-256 prehash
    pw = 'x' * 200
    h = security.hash_password(pw)
    assert isinstance(h, str)
    assert security.verify_password(pw, h)


def test_jwt_create_decode_valid():
    data = {'sub': '1', 'email': 'a@b.com'}
    token = security.create_access_token(data, expires_delta=timedelta(minutes=1))
    decoded = security.decode_access_token(token)
    assert decoded is not None
    assert decoded.get('email') == 'a@b.com'


def test_jwt_decode_invalid():
    # tamper token
    token = 'not.a.valid.token'
    assert security.decode_access_token(token) is None


def test_jwt_wrong_secret():
    # create token with different secret
    orig = os.environ.get('SECRET_KEY')
    try:
        os.environ['SECRET_KEY'] = 'other-secret'
        tok = security.create_access_token({'sub': '2'})
        # decode with module-level SECRET_KEY still points to the previous env var at import time,
        # so to emulate invalid secret decoding, call jwt.decode directly with wrong key
        import jwt
        try:
            jwt.decode(tok, 'wrong-secret', algorithms=[security.ALGORITHM])
            assert False, 'should not decode with wrong secret'
        except jwt.PyJWTError:
            pass
    finally:
        if orig is None:
            os.environ.pop('SECRET_KEY', None)
        else:
            os.environ['SECRET_KEY'] = orig
