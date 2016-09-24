from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404

from sh8core.checkin import CheckinManager
from sh8core.models import Mail
from sh8core.readauth import CannotReadReasons


def intro(request):
    return render(request, 'web/intro.html')


def detail(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    can_read = mail.can_read(request)
    if can_read == (True, None):
        mail.read()
        return render(request, 'web/detail.html', {
            'mail': mail, 'recipient': mail.recipient
        })
    elif can_read == (False, {CannotReadReasons.secret_code}):
        return render(request, 'web/secretcode_form.html', {
            'mail': mail, 'recipient': mail.recipient
        })
    else:
        return HttpResponseForbidden()


def checkin(request):
    recipient = request.POST.get('recipient')

    checkin_manager = CheckinManager(request)

    Mail.delete_read(checkin_manager)

    checkin_manager.set_current_recipient(recipient)

    return HttpResponseRedirect(reverse('web:list'))


def list_(request):
    checkin_manager = CheckinManager(request)

    recipient = checkin_manager.current_recipient()

    if recipient:
        mail_list = Mail.objects.filter(recipient=recipient)\
            .order_by('-recip_date')
    else:
        mail_list = []

    return render(request, 'web/list.html', {
        'mail_list': mail_list,
        'recipient': recipient,
    })


def help_(request):
    return render(request, 'web/help.html')
