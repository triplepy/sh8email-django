from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from .models import Mail
from .checkin import CheckinManager


def detail(request, pk):
    checkin_manager = CheckinManager(request)

    mail = get_object_or_404(Mail, pk=pk)
    if mail.is_own(checkin_manager):
        mail.read()
        return render(request, 'front/detail.html', {'mail': mail})
    else:
        return HttpResponseForbidden()


def checkin(request):
    try:
        recipient = request.POST['recipient']
    except KeyError as e:
        recipient = None

    checkin_manager = CheckinManager(request)

    Mail.delete_read(checkin_manager)

    checkin_manager.set_current_recipient(recipient)

    return HttpResponseRedirect(reverse('front:list'))


def list_(request):
    checkin_manager = CheckinManager(request)

    recipient = checkin_manager.current_recipient()

    if recipient:
        mail_list = Mail.objects.filter(recipient=recipient)
    else:
        mail_list = []

    return render(request, 'front/list.html', {
        'mail_list': mail_list,
        'recipient': recipient,
    })

