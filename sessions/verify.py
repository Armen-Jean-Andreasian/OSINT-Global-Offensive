from django.contrib.sessions.models import Session
from django.utils import timezone


def response(status: bool, reason: str = None):
    return {"status": status, "reason": reason}


def verify_authorized_session(request):
    user_id = request.session.get('user_id')
    session_id = request.session.session_key

    try:
        session = Session.objects.get(session_key=session_id)
    except Session.DoesNotExist:
        return response(status=False, reason="session key not found in db.")

    session_data = session.get_decoded()

    # Ensure the session's user ID matches the session's stored user ID
    if session_data.get('_auth_user_id') != str(user_id):
        return response(status=False, reason="user ID doesn't match the db session data")

    # Check if the session has expired
    if session.expire_date < timezone.now():
        return response(status=False, reason="expired session")

    return response(status=True)
