from service_response import ServiceResponse
from django.contrib.sessions.models import Session
from django.utils import timezone


def verify_session(request) -> ServiceResponse:
    """
    Verifies if the session is valid and corresponds to an authorized user.

    Saves the session state, which is the main benefit over request.user.is_authenticated

    Designed for GET requests, this function:
    - Ensures the user_id exists in the session. If not, saves the session state.
    - Checks the session key's validity. If undefined, saves the session state.
    - Verifies that the session key matches a valid session in the database.
    - Confirms that the session user_id matches the user_id in the database.
    - Ensures that the session has not expired.

    If the session is in an invalid state (e.g., missing user_id or session_key),
    `request.session.save()` is called to persist the session state.

    In other words, proceed - if this function returns true ServiceResponse.

    Returns:
        ServiceResponse: Indicating success or failure with error details.
    """
    # Check 1: User is authorized
    if not (user_id := request.session.get('user_id')):
        request.session.save()
        return ServiceResponse(status=False, error='User unknown. Reload the page.')

    # Check 2: Session key exists
    if not (session_key := request.session.session_key):
        request.session.save()
        return ServiceResponse(status=False, error='Undefined session key. Reload the page.')

    # Check 3: Session key is valid
    try:
        session = Session.objects.get(session_key=session_key)
    except Session.DoesNotExist:
        request.session.flush()
        return ServiceResponse(status=False, error="Session key not found in DB.")

    # Check 4: Session user_id matches
    session_data = session.get_decoded()
    if session_data.get('user_id') != user_id:
        request.session.flush()
        return ServiceResponse(status=False, error="User ID doesn't match session data.")

    # Check 5: Session has not expired
    if session.expire_date < timezone.now():
        request.session.flush()
        return ServiceResponse(status=False, error="Session expired.")

    # All checks passed
    return ServiceResponse(status=True)
