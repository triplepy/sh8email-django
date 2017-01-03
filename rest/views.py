from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.views import APIView

from sh8core.checkin import CheckinManager
from sh8core.models import Mail
from sh8core.readauth import CannotReadReasons
from sh8core.serializers import MailDetailSerializer
from sh8core.serializers import MailListSerializer


class MailList(APIView):
    def get(self, request, nickname, format=None):
        checkin_manager = CheckinManager(request)
        checkin_manager.checkin(nickname)

        Mail.delete_read(checkin_manager)

        mail_list = Mail.objects.filter(recipient=nickname).order_by('-recip_date')
        # TODO I think this logic should be moved to MailListSerializer.
        for mail in mail_list:
            mail.contents = mail.contents[:50]
            if mail.is_secret():
                mail.contents = ''

        serializer = MailListSerializer(mail_list, many=True)
        return Response(serializer.data)


class MailDetail(APIView):
    @staticmethod
    def _get_object(request, nickname, pk):
        # TODO DUP CODE. Must refactor this.
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

    def get(self, request, nickname, pk, format=None):
        mail = self._get_object(request, nickname, pk)
        if mail is None:
            return Response(mail, status=HTTP_401_UNAUTHORIZED)
        serializer = MailDetailSerializer(mail)
        return Response(serializer.data)

    def post(self, request, nickname, pk):
        mail = self._get_object(request, nickname, pk)
        if mail is None:
            return Response(mail, status=HTTP_401_UNAUTHORIZED)
        serializer = MailDetailSerializer(mail)
        return Response(serializer.data)
