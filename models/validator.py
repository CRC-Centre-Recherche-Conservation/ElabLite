import validators
from validators import ValidationError

def validate_url(url: str) -> bool:
    try:
        result = validators.url(url)
        return result
    except ValidationError:
        return False

def validate_email(email: str) -> bool:
    try:
        result = validators.email(email)
        return result
    except ValidationError:
        return False