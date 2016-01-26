# -*- coding: utf-8 -*-
import pdb
from email.message import Message
from email.parser import Parser
from email.utils import parseaddr


def nomalize_recip(recip):
    before_at_sign = recip[:recip.rfind('@')]
    real = ''
    if before_at_sign.find('<') >= 0:
        real = before_at_sign[before_at_sign.find('<') + 1:]
    else:
        real = before_at_sign
    return real.strip()


def nomalize_body(body, mailfrom):
    if not body['From']:
        del body['From']
        body['From'] = mailfrom
        
    recipient = body['To']
    del body['To']
    body['To'] = nomalize_recip(recipient)

    return body


def mail_template_to_save(data, mailfrom):
    body = Parser().parsestr(data)
    return nomalize_body(body, mailfrom)
        

def is_secret(recip):
    return '$$' in recip


def split_secret(recip):
    return recip.split("$$")


def extract_secretcode(source):
    if isinstance(source, Message):
        msg = source
        # TODO refactor
        name, address = parseaddr(msg.get('To'))
        recipient_with_secret = address.split('@')[0]
    else:
        recipient_with_secret = source

    if is_secret(recipient_with_secret):
        return recipient_with_secret.split('$$')[1]
    else:
        return None


def extract_recipient(source):
    if isinstance(source, Message):
        msg = source
        raw_rcptto = msg.get('To')
    else:
        raw_rcptto = source

    # TODO refactor
    name, address = parseaddr(raw_rcptto)
    recipient = address.split('@')[0]

    # TODO refactor required
    if is_secret(recipient):
        recipient = split_secret(recipient)[0]

    return recipient
