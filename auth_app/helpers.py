import re
from shared_scripts import ServiceResponse


def check_password_strength(password: str) -> ServiceResponse:
    """
    Check the strength of a password and return a ServiceResponse.
    """
    unmet_criteria = []

    if len(password) < 8:
        unmet_criteria.append("Password must be at least 8 characters long.")
    if not re.search(r'\d', password):
        unmet_criteria.append("Password must contain at least one digit (0-9).")
    if not re.search(r'[A-Z]', password):
        unmet_criteria.append("Password must contain at least one uppercase letter (A-Z).")
    if not re.search(r'[a-z]', password):
        unmet_criteria.append("Password must contain at least one lowercase letter (a-z).")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        unmet_criteria.append("Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>).")

    if unmet_criteria:
        return ServiceResponse(status=False, error={"unmet_criteria": unmet_criteria})

    return ServiceResponse(status=True)
