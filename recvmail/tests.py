# -*- coding: utf-8 -*-
import platform
import re
import smtplib
import time
import unittest
from email.parser import Parser

from django.conf import settings
from django.test import TestCase

from recvmail.msgparse import raw_to_mail, reproduce_mail, Address, readablize_header
from recvmail.recv_server import Sh8MailProcess
from sh8core.models import Mail


@unittest.skipIf(platform.system() == 'Windows',
                 "There is a gap with subprocessing mechanism of Linux/Windows." +
                 " So, we will skip tests using subprocessing.\n")
class RecvMailTest(TestCase):
    p = None

    msg = None
    frommail = None
    recipients = None

    @classmethod
    def setUpClass(cls):
        super(RecvMailTest, cls).setUpClass()
        RecvMailTest.start_mail_server()
        # for wait running server
        time.sleep(1)
        RecvMailTest.send_test_mail()

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()

    @classmethod
    def send_test_mail(cls):
        cls.set_self_msg()

        with smtplib.SMTP('127.0.0.1', settings.MAIL_SERVER_PORT) as conn:
            # show communication with the server
            conn.sendmail(cls.frommail,
                          cls.recipients,
                          cls.msg.as_string())
        # for wait to process mail
        time.sleep(0.1)

    @classmethod
    def set_self_msg(cls):
        cls.msg = Parser().parsestr(open('recvmail/fixtures/recvmail/daum_base64_multipart.eml').read())
        cls.frommail = 'author@example.com'
        cls.recipients = ['recipient@sh8.email',
                          'recp2@sh8.email',
                          'recp3@sh8.email',
                          'secret__secsec@sh8.email']

    @classmethod
    def start_mail_server(cls):
        cls.p = Sh8MailProcess()
        cls.p.daemon = True
        cls.p.start()

    def test_count_mails(self):
        mails = Mail.objects.all()
        self.assertEquals(len(mails), len(self.recipients))

    def test_multi_recip(self):
        self._check_mail_is_exist_with_recipient("recipient")
        self._check_mail_is_exist_with_recipient("recp2")
        self._check_mail_is_exist_with_recipient("recp3")

    def test_secret_mail(self):
        self._check_mail_is_exist_with_recipient("secret")
        sec_mail = Mail.objects.get(recipient="secret")
        self.assertEquals('secsec', sec_mail.secret_code)

    def _check_mail_is_exist_with_recipient(self, recipient):
        mail = Mail.objects.get(recipient=recipient)
        self.assertTrue(mail)


class AddressTest(TestCase):
    def _assert_local_domain(self, address, local, domain):
        self.assertEqual(local, address.local)
        self.assertEqual(domain, address.domain)

    def test_basic_init(self):
        # given
        local = 'getogrand__silversuffer'
        recipient = 'getogrand'
        secret_code = 'silversuffer'
        domain = 'google.com'

        # when
        address = Address(local=local, domain=domain)

        # then
        self._assert_local_domain(address, local, domain)
        self.assertEqual(recipient, address.recipient)
        self.assertEqual(secret_code, address.secret_code)

    def test_as_str(self):
        # given
        expected_address = 'getogrand__silversuffer@google.com'
        local = 'getogrand__silversuffer'
        domain = 'google.com'

        # when
        address = Address(local=local, domain=domain)
        address_str = address.as_str()

        # then
        self.assertEqual(expected_address, address_str)

    def test_str_magicmethod(self):
        # given
        expected_address = 'getogrand__silversuffer@google.com'
        local = 'getogrand__silversuffer'
        domain = 'google.com'

        # when
        address = Address(local=local, domain=domain)
        address_str = str(address)

        # then
        self.assertEqual(expected_address, address_str)

    def test_rawaddress_to_address(self):
        # given
        local = 'getogrand__silversuffer'
        domain = 'google.com'
        name = 'Geto'
        header_to = 'Geto <getogrand__silversuffer@google.com>'

        # when
        address = Address(header_to=header_to)

        # then
        self._assert_local_domain(address, local, domain)
        self.assertEqual(name, address.name)

    def test_address_to_rawaddress(self):
        # given
        local = 'getogrand__silversuffer'
        domain = 'google.com'
        name = 'Geto'
        header_to = 'Geto <getogrand__silversuffer@google.com>'

        # when
        address = Address(local=local, domain=domain, name=name)

        # then
        self.assertEqual(header_to, address.as_headerstr())


class MsgParseTest(TestCase):
    fixtures = ['recvmail/mails.yaml']

    def test_raw_to_mail(self):
        self.maxDiff = None

        # given
        rawemail = open('recvmail/fixtures/recvmail/aws_quoted_multipart_html_plain.eml').read()
        expected = Mail.objects.get(pk=1)

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertHTMLEqual(mail.contents, expected.contents)

    def test_raw_to_mail__euckr_html(self):
        self.maxDiff = None

        # given
        rawemail = open('recvmail/fixtures/recvmail/iphone_mail_euckr_html.eml').read()
        expected = Mail.objects.get(pk=2)

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertHTMLEqual(mail.contents, expected.contents)

    def test_raw_to_mail__euckr_plain(self):
        self.maxDiff = None

        # given
        rawemail = open('recvmail/fixtures/recvmail/iphone_mail_euckr_plain.eml').read()
        expected = Mail.objects.get(pk=3)

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqualExceptCarriageReturnEndNewLine(mail.contents, expected.contents)

    def test_raw_to_mail__unicode_sender(self):
        # given
        rawemail = open('recvmail/fixtures/recvmail/unicode_sender.eml').read()
        expected = Mail.objects.get(pk=4)

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqualExceptCarriageReturnEndNewLine(mail.contents.strip(), expected.contents)

    def test_raw_to_mail__without_content_type_header(self):
        """This is a test case of '#20 Exception occurred when the 'Content-Type' header not exists.'."""

        # given
        rawemail = open('recvmail/fixtures/recvmail/no_content_type_header.eml').read()
        expected = Mail.objects.get(pk=5)
        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.secret_code, expected.secret_code)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents, expected.contents)

    def test_raw_to_mail__complex_content_type_header(self):
        # given
        rawemail = open('recvmail/fixtures/recvmail/complex_content_type_header.eml').read()
        expected = Mail.objects.get(pk=5)
        # when
        mail = raw_to_mail(rawemail)
        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.secret_code, expected.secret_code)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents, expected.contents)

    def test_raw_to_mail__secretcode(self):
        # given
        rawemail = open('recvmail/fixtures/recvmail/secret.eml').read()
        expected = Mail.objects.get(pk=6)
        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.secret_code, expected.secret_code)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents.strip(), expected.contents)

    def test_raw_to_mail__content_disposition_inline(self):
        # given
        rawemail = open('recvmail/fixtures/recvmail/content_disposition_inline.eml').read()
        expected = Mail.objects.get(pk=5)
        # when
        mail = raw_to_mail(rawemail)
        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.secret_code, expected.secret_code)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents, expected.contents)

    def test_reproduce_mail(self):
        # given
        rcpttos = ['getogrand <getogrand1@sh8.email>', 'getogrand <getogrand2@sh8.email>']
        expected_recipients = ['getogrand1', 'getogrand2']
        orgin_mail = Mail.objects.get(pk=7)

        # when
        mails = reproduce_mail(orgin_mail, rcpttos)

        # then
        for m, rcpt in zip(mails, expected_recipients):
            self.assertEqual(m.recipient, rcpt)
            self.assertEqual(m.sender, orgin_mail.sender)
            self.assertEqual(m.subject, orgin_mail.subject)
            self.assertEqual(m.contents, orgin_mail.contents)

    def test_reproduce_mail__filter(self):
        # given
        rcpttos = ['getogrand <getogrand1@sh8.email>', 'getogrand <getogrand2@bad.com>']
        expected_recipients = ['getogrand1']
        orgin_mail = Mail.objects.get(pk=7)
        # when
        mails = reproduce_mail(orgin_mail, rcpttos)
        # then
        self.assertEqual(len(expected_recipients), len(mails))
        for m, rcpt in zip(mails, expected_recipients):
            self.assertEqual(m.recipient, rcpt)
            self.assertEqual(m.sender, orgin_mail.sender)
            self.assertEqual(m.subject, orgin_mail.subject)

    def test_readablize_header(self):
        # given
        header = '=?UTF-8?B?QVdT7J2YIOy2nOyLnCDqs7Xsp4A=?='
        expected_readable_header = 'AWS의 출시 공지'

        # when
        readable_header = readablize_header(header)

        # then
        self.assertEqual(expected_readable_header, readable_header)

    def assertEqualExceptCarriageReturnEndNewLine(self, expected, actual):
        end_newline_regex = r'\n$'
        expected_no_cr = expected.replace("\r", "")
        expected_no_cr_nl = re.sub(end_newline_regex, '', expected_no_cr)
        actual_no_cr = actual.replace("\r", "")
        actual_no_cr_nl = re.sub(end_newline_regex, '', actual_no_cr)
        self.assertMultiLineEqual(expected_no_cr_nl, actual_no_cr_nl)
