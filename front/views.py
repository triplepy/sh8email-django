from django.shortcuts import render
from django.views import generic
from front.models import Mail


class ListView(generic.ListView):
    template_name = 'front/list.html'

    def get_queryset(self):
        return Mail.objects.all()
