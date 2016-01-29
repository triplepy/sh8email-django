# -*- coding: utf-8 -*-
import email.utils
import smtplib
import time
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import formataddr

from django.test import TestCase
from front.models import Mail
from recvmail.msgparse import raw_to_mail, reproduce_mail, Address
from recvmail.util import extract_recipient
from .recv_server import Sh8MailProcess
from .util import nomalize_recip, nomalize_body, is_secret, split_secret


class RecvMailTest(TestCase):
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
        # TODO msg를 이런식으로 만들지 않아도 되었을 듯? 확인해서 수정하기.
        cls.msg = Parser().parsestr("""Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: base64
X-Originating-IP: [218.51.1.226]
From: "=?utf-8?B?7KO87JuQ7JiB?=" <getogrand@paran.com>
Organization:
To: "getogrand" <getogrand1$$silversuffer@sh8.email>
Subject: test
X-Mailer: Daum Web Mailer 1.2
Date: Sat, 23 Jan 2016 23:49:52 +0900 (KST)
Message-Id: <20160123234952.HM.C000000000FV3pd@dnjsdud1111.wwl1746.hanmail.net>
Errors-To: <dnjsdud1111@daum.net>
X-HM-UT: i0Yy1lQLTQ+AcyobeCye+inQzLKz6VHelNJrvZDCttk=
X-HM-FIGURE: i0Yy1lQLTQ/7FlCfj3oLn+xD9XCyy4Cl
MIME-Version: 1.0
X-Hanmail-Attr: fc=1

test""")
        cls.frommail = 'author@example.com'
        cls.recipients = ['recipient@example.com',
                          'recp2@example.com',
                          'recp3@example.com',
                          'secret$$secsec@example.com']
        recipients_name = ['recipient',
                           'recp2',
                           'recp3',
                           'secret$$secsec']

        cls.msg.replace_header('To', ', '.join(map(formataddr,
                                                   zip(recipients_name, cls.recipients))))
        cls.msg.replace_header('From', formataddr(('author', cls.frommail)))

    @classmethod
    def start_mail_server(cls):
        cls.p = Sh8MailProcessForTest()
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


class MailUtilTest(TestCase):
    empty_mailfrom = ""
    empty_peer = ""

    def _assert_after_nomalize_recipent(self, param_email, expected):
        result = nomalize_recip(param_email)
        self.assertEquals(expected, result)

    def _make_default_parameter_body(self):
        body = {}
        body['From'] = "From <from@example.com>"
        body['To'] = "recipient@exam.com"
        return body

    def test_nomalize_reciepent(self):
        self._assert_after_nomalize_recipent(
                "recipient@example.com", "recipient")
        self._assert_after_nomalize_recipent(
                "recip@ent@example.com", "recip@ent")
        self._assert_after_nomalize_recipent(
                "Recipient : <recipient@example.com>", "recipient")
        self._assert_after_nomalize_recipent(
                "Recipient : < recipient@example.com >", "recipient")

    def test_nomalize_body_case_with_only_body(self):
        p_body = self._make_default_parameter_body()

        result_body = nomalize_body(p_body, self.empty_mailfrom)

        self.assertEquals("From <from@example.com>", result_body['From'])
        self.assertEquals("recipient", result_body['To'])

    def test_nomalize_body_case_with_mailfrom(self):
        p_body = self._make_default_parameter_body()
        p_mailfrom = "mailfrom@example.com"

        result_body = nomalize_body(p_body, p_mailfrom)

        self.assertEquals("From <from@example.com>", result_body['From'])
        self.assertEquals("recipient", result_body['To'])

    def test_is_secret_mail(self):
        not_secret_recip = "not_secret"
        is_not_secret = is_secret(not_secret_recip)
        self.assertFalse(is_not_secret)

        is_secret_recip = "this_is$$secret"
        this_is_secret = is_secret(is_secret_recip)
        self.assertTrue(this_is_secret)

    def test_extract_secret(self):
        is_secret_recip = "this_is$$secret"
        recip, secret_code = split_secret(is_secret_recip)
        self.assertEquals("this_is", recip)
        self.assertEquals("secret", secret_code)

    def test_extract_recipient__using_message(self):
        # given
        rawemail = open('recvmail/tools/aws_simple.eml').read()
        msg = Parser().parsestr(rawemail)

        # when
        recipient = extract_recipient(msg)

        # then
        expected_recipient = "getogrand"
        self.assertEqual(recipient, expected_recipient)

    def test_extract_recipient__using_raw_rcptto(self):
        # given
        raw_rcptto = "wonyoungju <getogrand@sh8.email>"

        # when
        recipient = extract_recipient(raw_rcptto)

        # then
        expected_recipient = "getogrand"
        self.assertEqual(recipient, expected_recipient)


class AddressTest(TestCase):
    def _assert_local_domain(self, address, local, domain):
        self.assertEqual(local, address.local)
        self.assertEqual(domain, address.domain)

    def test_basic_init(self):
        # given
        local = 'getogrand$$silversuffer'
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
        expected_address = 'getogrand$$silversuffer@google.com'
        local = 'getogrand$$silversuffer'
        domain = 'google.com'

        # when
        address = Address(local=local, domain=domain)
        address_str = address.as_str()

        # then
        self.assertEqual(expected_address, address_str)

    def test_str_magicmethod(self):
        # given
        expected_address = 'getogrand$$silversuffer@google.com'
        local = 'getogrand$$silversuffer'
        domain = 'google.com'

        # when
        address = Address(local=local, domain=domain)
        address_str = str(address)

        # then
        self.assertEqual(expected_address, address_str)

    def test_rawaddress_to_address(self):
        # given
        local = 'getogrand$$silversuffer'
        domain = 'google.com'
        name = 'Geto'
        header_to = 'Geto <getogrand$$silversuffer@google.com>'

        # when
        address = Address(header_to=header_to)

        # then
        self._assert_local_domain(address, local, domain)
        self.assertEqual(name, address.name)

    def test_address_to_rawaddress(self):
        # given
        local = 'getogrand$$silversuffer'
        domain = 'google.com'
        name = 'Geto'
        header_to = 'Geto <getogrand$$silversuffer@google.com>'

        # when
        address = Address(local=local, domain=domain, name=name)

        # then
        self.assertEqual(header_to, address.as_headerstr())


# TODO refactor required
class Sh8MailProcessForTest(Sh8MailProcess):
    def run(self):
        super(Sh8MailProcessForTest, self).run()


class MsgParseTest(TestCase):
    def test_raw_to_mail(self):
        # given
        rawemail = open('recvmail/tools/aws_simple.eml').read()
        expected = Mail.objects.create(
                recipient='getogrand',
                secret_code=None,
                sender='Amazon Web Services <aws-marketing-email-replies@amazon.com>',
                subject='AWS의 출시 공지',
                contents="""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.=
w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
    <meta http-equiv=3D"Content-Type" content=3D"text/html; charset=3DUTF-8=
">
    <meta name=3D"viewport" content=3D"width=3Ddevice-width">
</head>
<body yahoo=3D'fix' style=3D'margin-top:0;margin-bottom:0;margin-left:0;mar=
gin-right:0;'><img src=3D"https://www.amazon.com/gp/r.html?C=3D1JF1R0SY4HT0=
H&R=3DH3QBGNBIQ749&T=3DO&U=3Dhttp%3A%2F%2Fimages.amazon.com%2Fimages%2FG%2F=
01%2Fnav%2Ftransp.gif&A=3DONQSC50VFP3FZWOPY8YS4AQEEDCA&H=3DSNDTUUGDMOBHOQ6I=
TQESCNEFGX0A&ref_=3Dpe_612980_160090880" />
<img src=3D"https://www.amazon.com/gp/r.html?C=3D1JF1R0SY4HT0H&R=3DH3QBGNBI=
Q749&T=3DE&U=3Dhttp%3A%2F%2Fimages.amazon.com%2Fimages%2FG%2F01%2Fnav%2Ftra=
nsp.gif&A=3DSOQ8AZTCEHCYSDHRU7LCLA6J4LEA&H=3DN7JT3YAVYRAXQTERCCBJLV5NXMMA" =
/></body>
</html>"""
        )

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected.recipient)
        self.assertEqual(mail.sender, expected.sender)
        self.assertEqual(mail.subject, expected.subject)
        self.assertHTMLEqual(mail.contents, expected.contents)

    def test_raw_to_mail__multiple_to(self):
        # given
        rawemail = open('recvmail/tools/multipleTo.eml').read()
        expected1 = Mail.objects.create(
                recipient='getogrand1',
                secret_code=None,
                sender='" 주원영 " <getogrand@paran.com>',
                subject='test',
                contents='test'
        )

        # when
        mail = raw_to_mail(rawemail)

        # then
        self.assertEqual(mail.recipient, expected1.recipient)
        self.assertEqual(mail.sender, expected1.sender)
        self.assertEqual(mail.subject, expected1.subject)
        self.assertEqual(mail.contents, expected1.contents)

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
        self.assertEqual(mail.contents, expected.contents)

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
