from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Mail
from .checkin import current_recipient, set_current_recipient


def detail(request, pk):
    mail = get_object_or_404(Mail, pk=pk)

    if mail.is_own(request):
        mail.read()
        return render(request, 'front/detail.html', {'mail': mail})
    else:
        return HttpResponseForbidden()


def checkin(request):
    try:
        recipient = request.POST['recipient']
    except KeyError as e:
        recipient = None

    Mail.delete_read(request)
    set_current_recipient(request, recipient)

    return HttpResponseRedirect(reverse('front:list'))


def list_(request):
    recipient = current_recipient(request)
    if recipient:
        mail_list = Mail.objects.filter(recipient=recipient)
    else:
        mail_list = []

    return render(request, 'front/list.html', {
        'mail_list': mail_list,
        'recipient': recipient,
    })

