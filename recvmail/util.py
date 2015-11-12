# -*- coding: utf-8 -*-


def nomalize_recip(recip):
    splits = recip.split('@')
    if not len(splits) == 1:
        splits.pop()
    real = ''
    for s in splits:
        real += s

    return real
        
    
