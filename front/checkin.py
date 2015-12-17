def current_recipient(request):
    return request.session.get('recipient')


def set_current_recipient(request, recipient):
    request.session['recipient'] = recipient
