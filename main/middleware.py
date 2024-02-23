from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        language = request.session.get('django_language', 'fr')

        request.GET = request.GET.copy()
        request.GET['language'] = language

        translation.activate(language)
        request.LANGUAGE_CODE = language

        response = self.get_response(request)

        return response

