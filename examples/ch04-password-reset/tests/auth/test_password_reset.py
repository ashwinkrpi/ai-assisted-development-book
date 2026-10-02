# tests/auth/test_password_reset.py
import pytest

from app.auth.password_reset import (
    InvalidTokenError,
    TokenAlreadyUsedError,
    TokenExpiredError,
    generate_reset_token,
    verify_reset_token,
)


class TestPasswordResetToken:
    def test_token_is_generated(self):
        token = generate_reset_token(user_id=1)
        assert token is not None
        assert len(token) >= 32

    def test_token_verifies_correctly(self):
        token = generate_reset_token(user_id=1)
        assert verify_reset_token(token) == 1

    def test_expired_token_is_rejected(self):
        token = generate_reset_token(user_id=1, expiry_minutes=-1)
        with pytest.raises(TokenExpiredError):
            verify_reset_token(token)

    def test_token_is_single_use(self):
        token = generate_reset_token(user_id=1)
        verify_reset_token(token)
        with pytest.raises(TokenAlreadyUsedError):
            verify_reset_token(token)

    def test_malformed_token_is_rejected(self):
        with pytest.raises(InvalidTokenError):
            verify_reset_token("not-a-real-token")
