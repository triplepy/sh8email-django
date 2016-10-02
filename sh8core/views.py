from .models import Mail
from django.http import HttpResponse


def create_dummies(request):
    for i in range(0, 30):
        Mail.objects.create(
            recipient="sh8dummy",
            sender="chm073@gmail.com",
            subject="tettettetst",
            contents="arstoiaensrtaoiersnt"
        )
    return HttpResponse("Yes, It was created")
