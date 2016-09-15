from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sh8core.models import Mail
from sh8core.tests.utils import add_recip_to_session


class RestAPITest(APITestCase):
    fixtures = ['mails.yaml']

    def test_retrieve_a_mail(self):
        # given
        mail_pk = 1
        mail = Mail.objects.get(pk=mail_pk)
        add_recip_to_session(self.client, mail.recipient)
        # when
        response = self.client.get(reverse('rest:rest-mail-detail', args=[mail.recipient, mail.pk]))
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['pk'], mail.pk)
        self.assertEqual(response.data['recipient'], mail.recipient)
        self.assertEqual(response.data['sender'], mail.sender)
        self.assertEqual(response.data['subject'], mail.subject)
        self.assertEqual(response.data['contents'], mail.contents)
        self.assertDatetimeEqual(response.data['recip_date'], mail.recip_date)
        # is_read should be True after the api response (the 'api response' means that someone read the mail.)
        self.assertEqual(response.data['is_read'], True)
        self.assertEqual(response.data['isSecret'], mail.is_secret)

    # TODO move to mixin.
    def assertDatetimeEqual(self, datetime_str, datetime_obj):
        self.assertEqual(datetime_str, datetime_obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
