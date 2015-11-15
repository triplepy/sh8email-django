# -*- coding: utf-8 -*-


def nomalize_recip(recip):
    before_at_sign = recip[:recip.rfind('@')]
    real = ''
    if before_at_sign.find('<') >= 0:
        real = before_at_sign[before_at_sign.find('<') + 1:]
    else:
        real = before_at_sign
    return real.strip()
        
    
def nomalize_body(body, mailfrom, peer):
    if mailfrom:
        body['from'] = mailfrom
    if peer:
        body['to'] = peer

    body['to'] = nomalize_recip(body['to'])

    return body
