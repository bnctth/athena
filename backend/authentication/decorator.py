import functools
from django.http import HttpResponse


def login_required(func):
    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        response = HttpResponse(status=401)
        response['WWW-Authenticate'] = 'Bearer'
        return response
    return wrapper


def permission_required(permission):
    def real_decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                response = HttpResponse(status=401)
                response['WWW-Authenticate'] = 'Bearer'
                return response

            if not request.user.has_perm(permission):
                return HttpResponse(status=403)

            return func(request, *args, **kwargs)

        return wrapper

    return real_decorator
