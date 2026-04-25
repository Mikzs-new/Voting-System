import re
from typing import Optional

from config import ALLOWED_YEAR_LEVELS


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def require_text(value: str, field_name: str, min_length: int = 1, max_length: int = 255) -> Optional[str]:
    cleaned = (value or "").strip()
    if len(cleaned) < min_length:
        return f"{field_name} is required."
    if len(cleaned) > max_length:
        return f"{field_name} must be at most {max_length} characters."
    return None


def validate_login(username: str, password: str) -> Optional[str]:
    username_error = require_text(username, "Username", min_length=3, max_length=150)
    if username_error:
        return username_error

    if not password or len(password) < 4:
        return "Password must be at least 4 characters."

    return None


def validate_student_payload(data: dict) -> Optional[str]:
    for key, field_name in (
        ("first_name", "First name"),
        ("last_name", "Last name"),
        ("student_school_id", "Student ID"),
        ("course", "Course"),
    ):
        value = data.get(key)
        if key == "course":
            if not value:
                return "Course is required."
            continue
        error = require_text(value, field_name)
        if error:
            return error

    year_level = str(data.get("year_level", "")).strip()
    if year_level and year_level not in ALLOWED_YEAR_LEVELS:
        return "Year level must be one of: 1, 2, 3, 4, 5, 6."

    email = (data.get("email") or "").strip()
    if email and not EMAIL_PATTERN.match(email):
        return "Email format is invalid."

    return None


def validate_candidate_payload(data: dict) -> Optional[str]:
    for key, field_name in (
        ("student_id", "Student"),
        ("position", "Position"),
        ("election", "Election"),
    ):
        if not data.get(key):
            return f"{field_name} is required."

    description = (data.get("description") or "").strip()
    if len(description) > 2000:
        return "Description must be at most 2000 characters."

    link = (data.get("link") or "").strip()
    if link and not (link.startswith("http://") or link.startswith("https://")):
        return "Link must start with http:// or https://."

    return None


def validate_vote_payload(student_id: str, election_id: str) -> Optional[str]:
    if not student_id:
        return "Student is required."
    if not election_id:
        return "Election is required."
    return None
