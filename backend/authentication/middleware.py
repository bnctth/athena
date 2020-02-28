from django.contrib.auth import authenticate


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'Authorization' in request.headers and len(request.headers['Authorization'].split(" ")) == 2 and \
                request.headers['Authorization'].split(" ")[0] == "Bearer":
            token = request.headers['Authorization'].split(" ")[1]
            authenticate(request, token=token)
        return self.get_response(request)
