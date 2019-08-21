from tracking.models import TrackingInfo


class TrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user and request.user.is_authenticated:
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            info, created = TrackingInfo.objects.get_or_create(
                user=request.user,
                defaults={'user_agent': user_agent}
            )
            if not created and user_agent:
                info.user_agent = user_agent
                info.save(update_fields=['user_agent'])

        return self.get_response(request)
