from django.http import Http404
from django.http import HttpResponseForbidden

from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response

from sh8core.checkin import CheckinManager
from sh8core.models import Mail
from sh8core.readauth import CannotReadReasons
from sh8core.serializers import MailListSerializer
from sh8core.serializers import MailDetailSerializer


class MailList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def post(self, request, nickname, format=None):
        recipient = request.data.get('recipient')
        if nickname != recipient:
            return HttpResponseForbidden
        checkin_manager = CheckinManager(request)
        Mail.delete_read(checkin_manager)
        checkin_manager.set_current_recipient(recipient)
        recipient = checkin_manager.current_recipient()

        if recipient:
            mail_list = Mail.objects.filter(recipient=recipient).order_by('-recip_date')
        else:
            mail_list = []

        for mail in mail_list:
            mail.isSecret = mail.is_secret()
            mail.contents = mail.contents[:50]
            if mail.isSecret:
                mail.contents = None
                mail.subject = None



        serializer = MailListSerializer(mail_list, many=True)
        return Response(serializer.data)


class MailDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, request, pk):
        try:
            mail = get_object_or_404(Mail, pk=pk)
            can_read = mail.can_read(request)
            if mail.recipient != nickname:
                return None
            if can_read == (True, None):
                mail.read()
                return mail
            elif can_read == (False, {CannotReadReasons.secret_code}):
                return None
            return None
        except Mail.DoesNotExist:
            return None

    def get(self, request, pk, format=None):
        mail = self.get_object(request, pk)
        serializer = MailDetailSerializer(mail)
        return Response(serializer.data)
