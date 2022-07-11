import time

import jwt
from django.contrib import messages
from django.contrib.auth.models import User
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    """
    Retrieve User model and creates 'refresh' and 'token'
    """
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'token': str(refresh.access_token),
    }


def get_keys(keys, ddict):
    new_d = {}
    for k in keys:
        if ddict.get(k):
            new_d[k] = ddict.get(k)
    return new_d


def check_expiration(token, refresh):
    """
    Retrieve 'token' and 'refresh', decodes it and check if time is expired.
    Refresh 'token' and return 'refresh' and 'token'
                                        OR return "token has been expired"
    """
    decoded_token = jwt.decode(token, options={"verify_signature": False})
    if decoded_token.get('exp') > time.time():
        return None
    decoded_refresh = jwt.decode(refresh, options={"verify_signature": False})
    if decoded_refresh.get('exp') > time.time():
        refresh = RefreshToken(token=refresh)
        return {
            'refresh': str(refresh),
            'token': str(refresh.access_token),
        }
    return {
        'error': "token has been expired"
    }


def refresh_token_or_redirect(request):
    """
    Get token from COOKIE
    Checking expiration using method 'check_expiration'

    """
    token = request.COOKIES.get('token')
    refresh = request.COOKIES.get('refresh')
    try:
        validation_result = check_expiration(token, refresh)

        if validation_result:
            token = validation_result.get('token')
            error = validation_result.get('error')
            if token:
                str(token)
            elif error:
                messages.error(request,
                               'Your token has been expired. Please login again.')
                return {
                    'error': 'token has been expired'
                }
        return token
    except:
        messages.error(request,
                       'Your token has been expired. Please login again.')
        return {
            'error': 'token has been expired'
        }


def user_from_token(token):
    """
    Return User model from token by decoded id in token
    """

    try:
        valid_data = TokenBackend(algorithm='HS256').decode(token,
                                                            verify=False)
        user_id = valid_data['user_id']
        user = User.objects.get(pk=user_id)
        return user
    except:
        return None
