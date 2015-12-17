def current_recipient(request):
    return request.session.get('recipient')


