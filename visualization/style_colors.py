# -*- coding: utf-8 -*-
def getStyle(value):
    if float(value) < 0:
        style = {
            'color': COLORS[0]['bg']
        }
    elif float(value) == 0:
        style = {
            'color': COLORS[1]['bg']
        }
    else:
        style = {
            'color': COLORS[2]['bg']
        }
    return style

COLORS = [
    {
        'bg': '#ff0000'
    },
    {
        'bg': '#f2f2f2'
    },
    {
        'bg': '#66ff33'
    }
]
