from typing import List
import logging

from django.http import HttpRequest, JsonResponse

from base.services import authentication


logger = logging.getLogger('django')


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        setattr(request, '_dont_enforce_csrf_checks', True)
        token: str = request.headers.get('authorization')
        if token:
            token_obj: List[str] = token.split(' ')
            if token_obj[0].lower() != 'bearer':
                return JsonResponse(data={
                        'message': 'invalid token type',
                        'success': False,
                    }, status=400)
            user = authentication(token=token_obj[1])
            if not user:
                return JsonResponse(data={
                        'message': 'invalid user token',
                        'success': False,
                    }, status=401)
            setattr(request, 'user', user)
        response = self.get_response(request)
        return response
