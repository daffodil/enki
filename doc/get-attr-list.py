#!/usr/bin/env python

import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.Qsci
import PyQt4.QtWebKit
import PyQt4.Qsci

for mod in [PyQt4.QtCore, PyQt4.QtGui, PyQt4.QtWebKit, PyQt4.Qsci]:
    for attr in dir(mod):
        if not attr.startswith('_'):
            print attr
