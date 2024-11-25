from django.middleware.csrf import CsrfViewMiddleware


class NoCsrfForLocalhostMiddleware(CsrfViewMiddleware):
    """
    Skips CSRF checks for requests from localhost (127.0.0.1 or ::1).
    Used for development purposes only.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META['REMOTE_ADDR'] in ['127.0.0.1', '::1']:
            return None
        return super().process_view(request, view_func, view_args, view_kwargs)
