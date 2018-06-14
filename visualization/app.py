# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

from visualization.style_colors import getStyle

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
stockList = [[70.20, 71.10, 70.20, 69.70, 71.60, 72.70, 73.00, 71.60, 73.10],
             [70.20, 71.10, 70.20, 59.70, 71.60, 72.70, 73.00, 71.60, 73.10]]
predictionList =[[72.70, 73.00, 71.60, 73.10, 70.20, 71.10, 70.20, 69.70, 71.60],
              [72.70, 73.00, 71.60, 58.10, 70.20, 71.10, 70.20, 69.70, 71.60]]
nameList = ['name1', 'name2']

def tableInit():
    x = np.empty(9)
    b = np.arange(0, 9, 1)
    ind = np.arange(len(x))
    np.put(x, ind, b)
    return x


def calculateInvestments(stockQuotes, predictions, name):
    invest, value, profit = 0, 0, 0
    hasBought = False
    for x in range(0, len(predictions)):
        if predictions[x] > stockQuotes[x]:
            if hasBought == False:
                invest += stockQuotes[x]
                hasBought = True
            else:
                value = stockQuotes[x]
        else:
            if hasBought == True:
                profit += stockQuotes[x]
                value = 0
                hasBought = False
    BHL = [stockQuotes[0]]
    PRE = [invest]
    bhlFactor = ((stockQuotes[-1] / stockQuotes[0]) - 1) * 100
    preFactor = (((value + profit) / invest) - 1) * 100
    BHL.append(str("%.2f" % round(bhlFactor, 3)))
    PRE.append(str("%.2f" % round(preFactor, 3)))
    dict = {}
    dict[name] = BHL
    dict[name +'_prediction'] = PRE
    return dict


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col], style = getStyle(dataframe.iloc[i][col])) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )

def makeLayout(x, stockList, predictionList, nameList):
    list = [
        html.H1(children='New quality of Business'),

        html.Div(children='''
            Some clever words to begin with
        ''')]
    for i in range(0, len(stockList)):
        list.append(html.Div(children=generate_table(pd.DataFrame(data=calculateInvestments(stockList[i], predictionList[i], nameList[i]))),
                     style={'width': '20%', 'float': 'left'}))
        list.append(dcc.Graph(
                id='graph' + nameList[i],
                figure={
                    'data': [
                        {'x': x, 'y': stockList[i], 'type': 'scatter', 'name': 'Stock'},
                        {'x': x, 'y': predictionList[i], 'type': 'scatter', 'name': 'Predictions'},
                    ],
                    'layout': {
                        'title': 'Quotes Visualization'
                    }
                }, style={'width': '78%', 'float': 'left', 'display': 'inline-block'}
            ))
    return list

x = tableInit()

app.layout = html.Div(children= makeLayout(x, stockList, predictionList, nameList))

# def addFirmVisualization(stockQuotes, predictions, investmentRates):

if __name__ == '__main__':
    app.run_server(debug=True)
