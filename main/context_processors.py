def selectedLanguage(request):
    if request.GET.get('language'):
        return {'selectedLanguage': request.GET.get('language')}
    else:
        return {'selectedLanguage': 'fr'}