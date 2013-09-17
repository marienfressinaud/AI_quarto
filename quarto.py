#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) > 1 and sys.argv[1] == "--test":
	import Quarto.test
	Quarto.test.main()
else:
	import Quarto.quarto
	Quarto.quarto.main()

print "\nBye bye"
