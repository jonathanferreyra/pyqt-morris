#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Jonathan Ferreyra <jalejandroferreyra@gmail.com>
#
# MIT Licence
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import os
from itertools import cycle
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings
from utils import generateRangeDates, convertPath, getProgramFolderPath


class WebPage(QWebPage):
    def javaScriptConsoleMessage(self, msg, line, source):
        print '> %s line %d: %s' % (source, line, msg)

class Morris:

    def __init__(self, widget, chart='Line', data=[], xkey='',
        ykeys=[], labels=[], raw='', **attrs):
        '''
        @param {QWidget} widget = instance of QWidget
        @param {string} name = namefile chart
        @param {string} chart = morris type chart: Line, Bar, Donnut
        @param {list} data = list of data to show
        @param {string} xkey = a string containing the name of the attribute that contains X labels
        @param {string} ykeys = a list of strings containing names of attributes that contain Y values
        @param {list} labels = a list of strings containing labels for the data series to be plotted
        @param {string} raw = string params to append in morris options
        '''
        self.widget = widget
        self.name = 'chart.html' # chart name file
        self.chart = chart.capitalize() # Line | Bar | Donut
        self.data = data # []
        self.xkey = xkey
        self.ykeys = ykeys # ['a', 'b']
        self.labels = labels # ['label a', 'label b']
        self.attrs = attrs
        self.raw = raw
        self.program_folder = getProgramFolderPath()
        self.tmpl = convertPath(self.program_folder + 'morris/template.html')
        self.path_file = convertPath(self.program_folder + self.name)

        self.webview = QWebView()
        self.webview.setPage(WebPage())
        self.webview.page().settings().setAttribute( QWebSettings.JavascriptEnabled, True)
        self.widget.setLayout(QtGui.QVBoxLayout())
        self.widget.layout().setContentsMargins(0, 0, 0, 0)
        self.widget.layout().addWidget(self.webview)

    def __getAttrs(self):
        attrs = {}
        attrs['data'] = self.data
        if self.chart in ['Line', 'Bar', 'Area']:
            attrs['xkey'] = self.xkey
            attrs['ykeys'] = self.ykeys
            attrs['labels'] = self.labels
        stattrs = unicode(attrs)[:-1]
        if len(self.attrs.keys()) > 0:
            attrs = unicode(self.attrs)
            stattrs += ', ' + attrs[1:-1]
        if self.chart == 'Donut':
            stattrs += ', formatter: function (x) { return x + "%"}'
        if self.raw:
            stattrs += ', ' + self.raw
        return stattrs[1:]

    def __render(self):
        html = open(self.tmpl).read()
        html = html.replace('{chart}', self.chart)
        html = html.replace('{attrs}', self.__getAttrs())
        html = html.replace('{path}', self.program_folder.replace('\\', '//'))
        f = open(self.path_file, 'w')
        f.write(html)
        f.close()

    def show(self):
        keys = ['widget']
        if self.chart in ['Line', 'Bar', 'Area']:
            keys += ['xkey', 'ykeys', 'labels']
        for k in keys:
            if not self.__dict__[k]:
                raise ValueError("'%s' key has not seted" % k)

        self.__render()
        self.webview.load(QtCore.QUrl("file:///" + convertPath(self.path_file)))
        self.webview.show()
        try:
            # remove the html generated file
            os.remove(convertPath(self.path_file))
        except Exception, e:
            pass

    def updateData(self, data):
        self.data = data
        self.show()