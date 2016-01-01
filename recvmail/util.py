# -*- coding: utf-8 -*-
from email.parser import Parser


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
    return recip.find("$$") != -1

def split_secret(recip):
    return recip.split("$$")
