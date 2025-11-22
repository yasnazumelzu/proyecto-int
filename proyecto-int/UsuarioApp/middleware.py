from django.conf import settings
from django.contrib.auth import logout
from django.contrib.sessions.models import Session

class OneSessionPerUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_session_key = request.session.session_key
            user_sessions = Session.objects.filter(expire_date__gte=request.session.get_expiry_date())
            for ses in user_sessions:
                data = ses.get_decoded()
                if data.get('_auth_user_id') == str(request.user.id) and ses.session_key != current_session_key:
                    ses.delete()
        response = self.get_response(request)
        return response
