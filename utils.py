#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import argv
from datetime import date, timedelta
from PyQt4 import QtGui

def generateRangeDates(date1, date2):
    '''
    Returns a list with dates beetwen date1 and date2

    @param {date} date1 = date from
    @param {date} date2 = date to
    '''
    delta = date2 - date1
    return [date1 + timedelta(days=i) for i in range(delta.days + 1)]

def getProgramFolderPath():
    '''
    '''
    return convertPath(os.path.abspath(os.path.dirname(argv[0])) + "/")

def convertPath(path):
    '''
    Convert the path to specific platform (dash)

    @param {string} path
    '''
    if os.name == 'posix':
        return "/" + apply(os.path.join, tuple(path.split('/')))
    elif os.name == 'nt':
        return apply(os.path.join, tuple(path.split('/')))

def centerOnScreen(self):
    resolution = QtGui.QDesktopWidget().screenGeometry()
    self.move((resolution.width() / 2) - (self.frameSize().width() / 2),
              (resolution.height() / 2) - (self.frameSize().height() / 2))