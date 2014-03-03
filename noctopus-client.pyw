#!/usr/bin/env python2
import os
import sys

#rDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#lDir = os.path.join(rDir, "src")
lDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "src")
sys.path.insert(0, lDir)

import TkorderMain

TkorderMain.main(sys.argv)
