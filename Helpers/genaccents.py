#!/usr/bin/python
import string, unicodedata

ACCENTS = [
    ('0x12', u'\u0300'),
    ('0x13', u'\u0301'),
    ('0x5E', u'\u0302'),
    ('0x7E', u'\u0303'),
    ('0x16', u'\u0304'),
    ('0x7F', u'\u0308'),
    ('0x14', u'\u030C'),
    ('0x18', u'\u0327'),
]

print "accents = {}"
for texcode, combining in ACCENTS:
    print "accents[%s] = {" % texcode
    for l in string.letters:
        norm = unicodedata.normalize('NFC', l + combining)
        if len(norm) == 1:
            print ("    %s='%s'," % (l, norm)).encode('utf-8')
    print "}"

print
print "return accents"
