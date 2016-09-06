#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest

from prod_lib import *

class TextoutputTests(unittest.TestCase):

    def test_ff_disc(self):
        self.assertEquals('different\n', get_text('test/textoutput.tex'))

    def test_accent(self):
        self.assertEquals('Kihō pokémon\n', get_text('test/accent.tex'))

if __name__ == "__main__":
    unittest.main()
