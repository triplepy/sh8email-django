from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Mail


def detail(request, pk):
    mail = get_object_or_404(Mail, pk=pk)
    return render(request, 'front/detail.html', {'mail': mail})


class ListView(generic.ListView):
    template_name = 'front/list.html'

    def get_queryset(self):
        return Mail.objects.all()


