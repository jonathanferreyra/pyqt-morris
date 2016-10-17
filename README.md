# PyQt + Morris.js

Binding class to use [Morris.js](http://morrisjs.github.io/) charts in a PyQt environment.

## Tested with versions:

* jQuery v2.0.3
* Morris.js v0.5.0
* Raphaël v2.1.2
* PyQt 4.7

## API


> Morris(self, widget, chart='Line', data=[], xkey='',
        ykeys=[], labels=[], raw='', **attrs)

Class constructor

Key 'widget' must be an instance of QWidget

> show(self)

Render the chart

> updateData(self, data)

Update the data ploted in the chart

## Examples to use

Instancing the chart with init data

```python
from morris import Morris


self.chart = Morris(self.widgetChart, 'Line')
self.chart.data = [
    {'label':'2014', 'value':30},
    {'label':'2015', 'value':60},
    {'label':'2016', 'value':10},
]
self.chart.xkey = 'label'
self.chart.ykeys = ['value']
self.chart.labels = ['Amount']
# use 'raw' key to set another keys out of [data, xkey, ykeys, labels] keys
self.chart.raw = 'preUnits: "$ "'
self.chart.show()

```

Updating the data
```python
self.chart.updateData([
    {'label':'2014', 'value':120},
    {'label':'2015', 'value':150},
    {'label':'2016', 'value':260},
])
```

## Screenshot

<img src="https://raw.github.com/jonathanferreyra/pyqt-morris/master/screen.png" />

## Licence

MIT
