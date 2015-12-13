from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse
from .models import Mail


def detail(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    return render(request, 'front/detail.html', {'mail': mail})


def checkin(request):
    try:
        recipient = request.POST['recipient']
    except KeyError as e:
        recipient = None

    request.session['recipient'] = recipient

    return HttpResponseRedirect(reverse('front:list'))


def list_(request):
    recipient = request.session.get('recipient')
    if recipient is None:
        mail_list = []
    else:
        mail_list = Mail.objects.filter(recipient=recipient)

    return render(request, 'front/list.html', {
        'mail_list': mail_list,
        'recipient': recipient,
    })

