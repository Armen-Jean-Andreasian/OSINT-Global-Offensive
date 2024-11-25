from sessions import set_session_key


class EstablishSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        """
        Sets the session key if it's missing
        """
        set_session_key(request)
        response = self.get_response(request)
        return response
