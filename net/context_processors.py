

def base_url(request):
    if request.is_secure():
        scheme = 'https://'
    else:
        scheme = 'http://'
    return {'BASE_URL': scheme + request.get_host()}
