import re

import srt
from bidi import algorithm

LTR_CHARS = 'a-zA-Z0-9!\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ '
PUNCTUATIONS = '"!@#$%^&*()-_=+\\/\'.,<>?~{}[]|:` '
NUMBERS = '1234567890'
ALLOWED_WITH_HEB = PUNCTUATIONS + NUMBERS


def is_ltr_char(char: str) -> bool:
    return bool(re.match(f'[{LTR_CHARS}]', char))


def next_ltr_term(bidi_out: str):
    term = ''
    for c in bidi_out:
        if is_ltr_char(c):
            term += c
        else:
            break
    return term


def next_rtl_term(bidi_out: str):
    term = ''
    for c in bidi_out:
        if not is_ltr_char(c):
            term += c
        else:
            break
    return algorithm.get_display(term)


def reverse_punctuations(term: str) -> str:
    prefix = ''
    for c in term:
        if c in PUNCTUATIONS:
            prefix += c
        else:
            break
    rev_prefix = ''.join(reversed(prefix))
    term = term[len(rev_prefix):]
    return term + rev_prefix


def merge_rtl_parts(terms):
    new_terms = []
    terms_count = len(terms)
    to_combine = []
    for i in range(terms_count):
        term = terms[i]
        next_term = terms[i + 1] if i + 1 < terms_count else None
        if not is_ltr_char(term[0]):
            # hebrew
            to_combine.append(term)
        elif all([c in ALLOWED_WITH_HEB for c in term]) and next_term and not is_ltr_char(next_term[0]) and i > 0:
            # all allowed in heb (numbers, punctuations), and next is hebrew
            to_combine.append(reverse_punctuations(term))
        else:
            if any(to_combine):
                to_combine = reversed(to_combine)
                new_terms.append(''.join(to_combine))
                to_combine = []

            new_terms.append(term)

    if any(to_combine):
        to_combine = reversed(to_combine)
        new_terms.append(''.join(to_combine))
    return new_terms


def fix_line(line: str) -> str:
    # Remove HTML tags ?
    # line = re.sub(r'<.*?>', '', line)
    bidi_out = algorithm.get_display(line)

    parts = []
    while bidi_out:
        char = bidi_out[0]
        if is_ltr_char(char):
            term = next_ltr_term(bidi_out)
        else:
            term = next_rtl_term(bidi_out)

        # trim the bidi out, so we can find the next term
        bidi_out = bidi_out[len(term):]
        parts.append(term)

    parts = merge_rtl_parts(parts)
    return ''.join(parts)
    # return str(parts)


def fix_srt(srt_data: str):
    subs = list(srt.parse(srt_data))
    for sub in subs:
        lines = [
            fix_line(l)
            for l
            in sub.content.split('\n')
        ]
        sub.content = '\n'.join(lines)
    return srt.compose(subs)
