from django.shortcuts import redirect

from budget_django.settings import SKIP_TOKEN_PATHS
from budget_django.utils import refresh_token_or_redirect, user_from_token


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        self._token = None
        formatted_path = str(request.path).replace("/", "")
        skip_to_logout = [i for i in SKIP_TOKEN_PATHS if i in formatted_path]
        if skip_to_logout:
            _token = refresh_token_or_redirect(request)
            if not isinstance(_token, str):
                return redirect('logout')
            user = user_from_token(_token)
            request.jwt_user = user
            request._token = _token

        response = self.get_response(request)

        return response
