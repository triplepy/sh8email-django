from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .exceptions import BackdoorIntendedError


@csrf_exempt
def raise_error(request):
    key_input = request.POST.get('key')
    if not bool(key_input):
        return HttpResponse('Please input key via POST method.')
    elif key_input == settings.BACKDOOR_KEY:
        raise BackdoorIntendedError("Let\'s raise an error!")
    else:
        return HttpResponse('Wrong key.')
