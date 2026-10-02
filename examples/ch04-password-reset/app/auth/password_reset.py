# app/auth/password_reset.py
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


class InvalidTokenError(Exception):
    """The token was never issued."""


class TokenExpiredError(Exception):
    """The token was issued but its expiry time has passed."""


class TokenAlreadyUsedError(Exception):
    """The token was valid but has already been used once."""


@dataclass
class _ResetToken:
    user_id: int
    expires_at: datetime
    used: bool = False


# In-memory store keeps the example self-contained. A real service would
# store a hash of each token in its database instead.
_tokens: dict[str, _ResetToken] = {}


def generate_reset_token(user_id: int, expiry_minutes: int = 15) -> str:
    token = secrets.token_urlsafe(32)
    expires_at = datetime.now(timezone.utc) + timedelta(minutes=expiry_minutes)
    _tokens[token] = _ResetToken(user_id=user_id, expires_at=expires_at)
    return token


def verify_reset_token(token: str) -> int:
    """Return the user ID for a valid token and mark the token as used."""
    record = _tokens.get(token)
    if record is None:
        raise InvalidTokenError("Unknown reset token")
    if record.used:
        raise TokenAlreadyUsedError("Reset token has already been used")
    if datetime.now(timezone.utc) >= record.expires_at:
        raise TokenExpiredError("Reset token has expired")
    record.used = True
    return record.user_id
