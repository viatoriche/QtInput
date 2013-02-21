#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""QtInput - ultra minimal text editor with pipes

typical example:
xsel -o | qtinput > /etc/config.cfg
"""

from PyQt4 import uic, QtGui, QtCore

import sys
import select
import locale
import getopt

form_class, base_class = uic.loadUiType("window.ui")

class App(QtGui.QApplication):
    pass

app = App(sys.argv)

class UiForm(base_class, form_class):

    def __init__(self):
        super(UiForm, self).__init__()
        self.setupUi(self)
        self.enc = locale.getdefaultlocale()[1]
        try:
            self.filename = unicode(sys.argv[1], self.enc)
        except IndexError:
            self.filename = None

        if select.select([sys.stdin,],[],[],0.0)[0]:
            self.text_edit.setPlainText(unicode(''.join\
                    (sys.stdin.readlines()), self.enc))
        elif self.filename is not None:
            text = ''.join\
                    (open(self.filename, 'r').readlines())
            text = unicode(text, self.enc)
            self.text_edit.setPlainText(text)

    def write_text(self):
        text = unicode(self.text_edit.toPlainText().toUtf8(), 'UTF-8')
        if text != u'':
            sys.stdout.write(text.encode(self.enc))
            if self.filename is not None:
                open(self.filename, 'w').write(text.encode(self.enc))

    def closeEvent(self, event):
        self.write_text()
        event.accept()

    def reject(self):
        self.write_text()
        return super(UiForm, self).reject()

window = UiForm()
window.show()

sys.exit(app.exec_())

# vi: ft=python:tw=0:ts=4

