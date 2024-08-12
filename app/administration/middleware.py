from django.http import Http404


class UserHaveToBeStaffMiddleware:
    ADMIN_URL_PATTERN = "/admin"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if not request.path.startswith(self.ADMIN_URL_PATTERN):
            # skip the middleware
            return self.get_response(request)

        if (
            request.path.startswith(self.ADMIN_URL_PATTERN)
            and not request.user.is_staff
        ):
            raise Http404()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
