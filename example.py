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

import sys, random
from PyQt4 import QtGui, QtCore, uic
from utils import *
from charts import DEFAULT_COLORS
from morris import Morris
from datetime import date

class Window(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('window.ui', self)
        centerOnScreen(self)
        QtGui.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Escape), self, self.close)

        # example rendering Line chart
        self.chart1 = Morris(self.widgetChart1, 'Line')
        self.chart1.xkey = 'label'
        self.chart1.ykeys = ['value']
        self.chart1.labels = ['Amount']
        self.chart1.raw = 'preUnits: "$ "'
        self.chart1.show()

        # example rendering Donut chart
        self.chart2 = Morris(self.widgetChart2, 'Donut')
        self.chart2.data = [
            {'label':'Customer 1', 'value':30},
            {'label':'Customer 2', 'value':60},
            {'label':'Customer 3', 'value':10},
        ]
        self.chart2.show()

        # example rendering Bar chart
        self.chart3 = Morris(self.widgetChart3, 'Bar')
        self.chart3.xkey = 'label'
        self.chart3.ykeys = ['value']
        self.chart3.labels = ['Amount']

        # use 'raw' key to set another keys out of [data, xkey, ykeys, labels] keys
        self.chart3.raw = '''
        preUnits: "$ ",
        barColors: function (row, series, type) {
            if (type === 'bar') {
              var red = Math.ceil(255 * row.y / this.ymax);
              return 'rgb(' + red + ',0,0)';
            }
            else {
              return '#000';
            }
          }
        '''
        self.chart3.show()

        # example rendering Area chart
        self.chart4 = Morris(self.widgetChart4, 'Area',
            xkey='x', ykeys=['y', 'z'], labels=['Y', 'Z'])
        self.chart4.data = [
          {'x': '2011 Q1', 'y': 3, 'z': 3},
          {'x': '2011 Q2', 'y': 2, 'z': 0},
          {'x': '2011 Q3', 'y': 2, 'z': 5},
          {'x': '2011 Q4', 'y': 4, 'z': 4}
        ]
        self.chart4.show()

        self.on_btGenerateData_clicked()

    def generateRandomData(self):
        today = date.today()
        start_month = date(today.year, today.month, 1)
        dates = generateRangeDates(start_month, today)

        data = []
        for dt in dates:
            data.append({
                'label':dt.strftime('%Y-%m-%d'),
                'value':random.randint(10000, 1000000)
            })
        data.reverse()
        return data

    @QtCore.pyqtSlot()
    def on_btGenerateData_clicked(self):

        # example of how update your charts
        data = self.generateRandomData()

        self.chart1.updateData(data)
        self.chart3.updateData(data)

        data = []
        count = random.randint(1, 5)
        for i in range(count):
            data.append({'label':'Customer ' + str(i+1), 'value':random.randint(0, 99)})
        self.chart2.updateData(data)

        self.chart4.updateData([
          {'x': '2011 Q1', 'y': random.randint(0, 5), 'z': random.randint(0, 5)},
          {'x': '2011 Q2', 'y': random.randint(0, 5), 'z': random.randint(0, 5)},
          {'x': '2011 Q3', 'y': random.randint(0, 5), 'z': random.randint(0, 5)},
          {'x': '2011 Q4', 'y': random.randint(0, 5), 'z': random.randint(0, 5)}
        ])

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
