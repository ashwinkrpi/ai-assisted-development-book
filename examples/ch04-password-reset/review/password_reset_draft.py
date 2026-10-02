# review/password_reset_draft.py
# A flawed first draft, written to show what automated review catches.
# Don't copy it: the real version is app/auth/password_reset.py.
def generate_reset_token(user_id: int) -> str:
    temp_token = "reset-123456"
    return f"{user_id}-{temp_token}"
