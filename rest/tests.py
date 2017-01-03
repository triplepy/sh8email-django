from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from sh8core.models import Mail
from sh8core.tests.utils import add_recip_to_session


class RestAPITest(APITestCase):
    fixtures = ['rest/mails.yaml']

    def test_retrieve_a_mail(self):
        # given
        mail_pk = 1
        mail = Mail.objects.get(pk=mail_pk)
        add_recip_to_session(self.client, mail.recipient)
        # when
        response = self.client.get(reverse('rest:mail_detail', args=[mail.recipient, mail.pk]))
        # then
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         "response.content was {}".format(response.content.decode()))
        self.assertEqual(mail.pk, response.data['pk'])
        self.assertEqual(mail.recipient, response.data['recipient'])
        self.assertEqual(mail.sender, response.data['sender'])
        self.assertEqual(mail.subject, response.data['subject'])
        self.assertEqual(mail.contents, response.data['contents'])
        self.assertDatetimeEqual(mail.recip_date, response.data['recipDate'])
        # is_read should be True after the api response (the 'api response' means that someone read the mail.)
        self.assertEqual(True, response.data['isRead'])

    def test_retrieve_mail_list(self):
        # given
        recipient = 'silver'
        mails = Mail.objects.filter(recipient=recipient)
        # when
        response = self.client.get(reverse('rest:mail_list', args=[recipient]))
        # then
        self.assertEqual(status.HTTP_200_OK, response.status_code,
                         "response.content was {}".format(response.content.decode()))
        for index, d in enumerate(response.data):
            self.assertEqual(mails[index].pk, d['pk'])
            self.assertEqual(mails[index].recipient, d['recipient'])
            self.assertEqual(mails[index].sender, d['sender'])
            self.assertEqual(mails[index].subject, d['subject'])
            if mails[index].is_secret():
                self.assertEqual('', d['contents'])
            else:
                self.assertEqual(mails[index].contents, d['contents'])
            self.assertDatetimeEqual(mails[index].recip_date, d['recipDate'])
            self.assertEqual(mails[index].is_secret(), d['isSecret'])
            self.assertEqual(mails[index].is_read, d['isRead'])

    def test_secret_mail_detail_with_wrong_password(self):
        # given
        recipient = 'silver'
        all_mails = Mail.objects.filter(recipient=recipient)
        secret_mails = list(filter(lambda x: x.is_secret() == True, all_mails))
        secret_mail = secret_mails[0]
        self.client.get(reverse('rest:mail_list', args=[recipient]))
        data = {'secret_code': 'wrong_password'}
        # when
        url = reverse('rest:mail_detail', args=[recipient, secret_mail.pk])
        response = self.client.post(reverse(url), data=data)
        # then
        self.assertEquals(401, response.status_code)

    def test_secret_mail_detail_with_correct_password(self):
        # given
        recipient = 'silver'
        all_mails = Mail.objects.filter(recipient=recipient)
        secret_mails = list(filter(lambda x: x.is_secret() is True, all_mails))
        secret_mail = secret_mails[0]
        self.client.get(reverse('rest:mail_list', args=[recipient]))
        data = {'secret_code': 'secret'}
        # when
        url = reverse('rest:mail_detail', args=[recipient, secret_mail.pk])
        response = self.client.post(reverse(url), data=data)
        # then
        self.assertEquals(200, response.status_code)
        self.assertEquals(secret_mail.title, response.data['title'])
        self.assertEquals(secret_mail.sender, response.data['sender'])
        self.assertEquals(secret_mail.subject, response.data['subject'])
        self.assertEquals(secret_mail.contents, response.data['contents'])

    # TODO move to mixin.
    def assertDatetimeEqual(self, datetime_obj, datetime_str):
        self.assertEqual(datetime_obj.strftime("%Y-%m-%dT%H:%M:%SZ"), datetime_str)
