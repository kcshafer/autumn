def is_authenticated(request):
    is_authenticated = True if 'access_token' in request.session else False

    return {'is_authenticated': is_authenticated}