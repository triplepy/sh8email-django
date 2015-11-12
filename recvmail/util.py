# -*- coding: utf-8 -*-


def nomalize_recip(recip):
    before_at_sign = recip[:recip.rfind('@')]
    if before_at_sign.find('<') >= 0:
        return before_at_sign[before_at_sign.find('<') + 1:]
    else:
        return before_at_sign
        
        
    
