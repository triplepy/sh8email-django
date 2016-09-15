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
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "response.content was {}".format(response.content.decode()))
        self.assertEqual(response.data['pk'], mail.pk)
        self.assertEqual(response.data['recipient'], mail.recipient)
        self.assertEqual(response.data['sender'], mail.sender)
        self.assertEqual(response.data['subject'], mail.subject)
        self.assertEqual(response.data['contents'], mail.contents)
        self.assertDatetimeEqual(response.data['recip_date'], mail.recip_date)
        # is_read should be True after the api response (the 'api response' means that someone read the mail.)
        self.assertEqual(response.data['is_read'], True)

    def test_retrieve_mail_list(self):
        # given
        recipient = 'silver'
        mails = Mail.objects.filter(recipient=recipient)
        # add_recip_to_session(self.client, recipient)
        # when
        response = self.client.post(reverse('rest:rest-mail-list', args=[recipient]), data={'recipient': recipient})
        # then
        self.assertEqual(response.status_code, status.HTTP_200_OK,
                         "response.content was {}".format(response.content.decode()))
        for index, d in enumerate(response.data):
            self.assertEqual(d['pk'], mails[index].pk)
            self.assertEqual(d['recipient'], mails[index].recipient)
            self.assertEqual(d['sender'], mails[index].sender)
            self.assertEqual(d['subject'], mails[index].subject)
            if mails[index].is_secret():
                self.assertEqual(d['contents'], '')
            else:
                self.assertEqual(d['contents'], mails[index].contents)
            self.assertDatetimeEqual(d['recip_date'], mails[index].recip_date)
            self.assertEqual(d['isSecret'], mails[index].is_secret())
            self.assertEqual(d['is_read'], mails[index].is_read)

    # TODO move to mixin.
    def assertDatetimeEqual(self, datetime_str, datetime_obj):
        self.assertEqual(datetime_str, datetime_obj.strftime("%Y-%m-%dT%H:%M:%SZ"))
