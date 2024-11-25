def set_session_key(request):
    """Sets session key if it's not set"""
    if not request.session.session_key:
        request.session.save()
