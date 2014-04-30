#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

<<<<<<< HEAD
####################################################################
# URL of the github repository website associated with the fork
# of this repository  (Replace accordingly)
####################################################################
SITEURL = 'http://hiro722722.github.io/Stat-Project-2'
####################################################################
=======
SITEURL = 'http://jodreen.github.io/googletrends-stocks/'
>>>>>>> 6db6961d43b2c2c991b7c5c115b5ad1e642751ac

RELATIVE_URLS = False

FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

#DISQUS_SITENAME = ""
#GOOGLE_ANALYTICS = ""
