#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Converts mbox patches generated by git-format-patch into DEP-3 patches
#
# Copyright (C) 2011 Benoît Knecht <benoit.knecht@fsfe.org>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the University nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# Usage: ./mbox2dep3.py patches/*.patch
#
#        Assuming patches/*.patch have been created with
#
#          git format-patch -k --no-signature
#
#        mbox2dep3.py converts them to a minimal DEP-3-compliant format,
#        containing only the required 'From' and 'Subject' fields, with a long
#        description (if available).
#        The paths of the converted patches are written to standard output.

import sys
from email.parser import HeaderParser
from email.message import Message
from email.header import Header, decode_header
from email.generator import Generator
from email.charset import Charset

class Field(Header):
    @classmethod
    def make_header(cls, decoded_seq):
        h = cls()
        for s, charset in decoded_seq:
            if charset is not None and not isinstance(charset, Charset):
                charset = Charset(charset)
            h.append(s, charset)
        return h

    def encode(self):
        return unicode(self).encode('utf-8')

parser = HeaderParser()

for patch in sys.argv[1:]:
    f = file(patch, 'r')
    old = parser.parse(f)
    f.close()

    author = Field.make_header(decode_header(old['From']))
    description = Field.make_header(decode_header(old['Subject']))

    new = Message()
    new['From'] = author
    new['Subject'] = description
    new.set_payload(old.get_payload())

    f = file(patch, 'w')
    g = Generator(f, mangle_from_=False)
    g.flatten(new)
    f.close()
    print patch
