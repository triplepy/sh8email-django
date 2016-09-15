from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sh8core.models import Mail


class RestAPITest(APITestCase):
    fixtures = ['mails.yaml']

    def test_retrieve_a_mail(self):
        mail_pk = 1
        mail = Mail.objects.get(pk=mail_pk)
        response = self.client.get(reverse('rest:rest-mail-detail', args=[mail.recipient, mail.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {
            'pk': mail.pk,
            'recipient': mail.recipient,
            'sender': mail.sender,
            'subject': mail.subject,
            'contents': mail.contents,
            'recip_date': mail.recip_date,
            'isSecret': mail.is_secret,
            'is_read': mail.is_read,
        })
