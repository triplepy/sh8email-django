# -*- coding: utf-8 -*-
import smtplib
import time
from email.parser import Parser
from email.utils import formataddr

from django.test import TestCase
from front.models import Mail
from recvmail.msgparse import raw_to_mail, reproduce_mail, Address, readablize_header
from .recv_server import Sh8MailProcess


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

        with smtplib.SMTP('127.0.0.1', 25) as conn:
            # show communication with the server
            conn.sendmail(cls.frommail,
                          cls.recipients,
                          cls.msg.as_string())
        # for wait to process mail
        time.sleep(0.1)

    @classmethod
    def set_self_msg(cls):
        cls.msg = Parser().parsestr("""Content-Type: multipart/alternative;
	boundary="----=_Part_399822_750742711.1457150967169"
Content-Transfer-Encoding: base64
X-Originating-IP: [218.51.1.226]
From: "=?utf-8?B?7KO87JuQ7JiB?=" <getogrand@paran.com>
Organization:
To: "getogrand" <getogrand1__silversuffer@sh8.email>
Subject: test
X-Mailer: Daum Web Mailer 1.2
Date: Sat, 23 Jan 2016 23:49:52 +0900 (KST)
Message-Id: <20160123234952.HM.C000000000FV3pd@dnjsdud1111.wwl1746.hanmail.net>
Errors-To: <dnjsdud1111@daum.net>
X-HM-UT: i0Yy1lQLTQ+AcyobeCye+inQzLKz6VHelNJrvZDCttk=
X-HM-FIGURE: i0Yy1lQLTQ/7FlCfj3oLn+xD9XCyy4Cl
MIME-Version: 1.0
X-Hanmail-Attr: fc=1

------=_Part_399822_750742711.1457150967169
Content-Type: text/plain;
	charset=UTF-8
Content-Transfer-Encoding: base64

dGVzdAo=""")
        cls.frommail = 'author@example.com'
        cls.recipients = ['recipient@example.com',
                          'recp2@example.com',
                          'recp3@example.com',
                          'secret__secsec@example.com']
        recipients_name = ['recipient',
                           'recp2',
                           'recp3',
                           'secret__secsec']

        header_to = ', '.join(map(formataddr, zip(recipients_name, cls.recipients)))
        cls.msg.replace_header('To', header_to)
        cls.msg.replace_header('From', formataddr(('author', cls.frommail)))

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
    def test_raw_to_mail(self):
        self.maxDiff = None

        # given
        rawemail = open('recvmail/tools/aws_simple.eml').read()
        expected = Mail.objects.create(
                recipient='getogrand',
                secret_code=None,
                sender='Amazon Web Services <aws-marketing-email-replies@amazon.com>',
                subject='AWS의 출시 공지',
                contents="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width">
</head>
<body yahoo='fix' style='margin-top:0;margin-bottom:0;margin-left:0;margin-right:0;'>
<img src="https://www.amazon.com/gp/r.html?C=1JF1R0SY4HT0H&R=H3QBGNBIQ749&T=O&U=http%3A%2F%2Fimages.amazon.com%2Fimages%2FG%2F01%2Fnav%2Ftransp.gif&A=ONQSC50VFP3FZWOPY8YS4AQEEDCA&H=SNDTUUGDMOBHOQ6ITQESCNEFGX0A&ref_=pe_612980_160090880" />
<img src="https://www.amazon.com/gp/r.html?C=1JF1R0SY4HT0H&R=H3QBGNBIQ749&T=E&U=http%3A%2F%2Fimages.amazon.com%2Fimages%2FG%2F01%2Fnav%2Ftransp.gif&A=SOQ8AZTCEHCYSDHRU7LCLA6J4LEA&H=N7JT3YAVYRAXQTERCCBJLV5NXMMA" /></body>
</html>"""
        )

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertHTMLEqual(mail.contents, expected.contents)

    def test_raw_to_mail__unicode_sender(self):
        # given
        rawemail = open('recvmail/tools/unicode_sender.eml').read()
        expected = Mail.objects.create(
                recipient='getogrand1',
                secret_code=None,
                sender='" 주원영 " <getogrand@paran.com>',
                subject='test',
                contents='test'
        )

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents.strip(), expected.contents)

    def test_raw_to_mail__secretcode(self):
        # given
        rawemail = open('recvmail/tools/secret.eml').read()
        expected = Mail.objects.create(
                recipient='getogrand1',
                secret_code='silversuffer',
                sender='" 주원영 " <getogrand@paran.com>',
                subject='test',
                contents='test'
        )

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.secret_code, expected.secret_code)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertEqual(mail.contents.strip(), expected.contents)

    def test_reproduce_mail(self):
        # given
        rcpttos = ['getogrand <getogrand1@sh8.email>', 'getogrand <getogrand2@sh8.email>']
        expected_recipients = ['getogrand1', 'getogrand2']
        orgin_mail = Mail(
                recipient='getogrand1',
                secret_code=None,
                sender='" 주원영 " <getogrand@paran.com>',
                subject='test',
                contents='test'
        )

        # when
        mails = reproduce_mail(orgin_mail, rcpttos)

        # then
        for m, rcpt in zip(mails, expected_recipients):
            self.assertEqual(m.recipient, rcpt)
            self.assertEqual(m.sender, orgin_mail.sender)
            self.assertEqual(m.subject, orgin_mail.subject)
            self.assertEqual(m.contents, orgin_mail.contents)

    def test_readablize_header(self):
        # given
        header = '=?UTF-8?B?QVdT7J2YIOy2nOyLnCDqs7Xsp4A=?='
        expected_readable_header = 'AWS의 출시 공지'

        # when
        readable_header = readablize_header(header)

        # then
        self.assertEqual(expected_readable_header, readable_header)