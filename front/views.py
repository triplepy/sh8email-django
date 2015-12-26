from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from front.readauth import CannotReadReasons
from .models import Mail
from .checkin import CheckinManager


def detail(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    can_read = mail.can_read(request)
    if can_read == (True, None):
        mail.read()
        return render(request, 'front/detail.html', {
            'mail': mail, 'recipient': mail.recipient
        })
    elif can_read == (False, {CannotReadReasons.secret_code}):
        return render(request, 'front/secretcode_form.html', {
            'mail': mail, 'recipient': mail.recipient
        })
    else:
        return HttpResponseForbidden()


def checkin(request):
    recipient = request.POST.get('recipient')

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
