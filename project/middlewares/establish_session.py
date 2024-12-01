class EstablishSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        """
        Sets the session key if it's missing
        """
        request.session.save()
        response = self.get_response(request)
        return response
