# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import json
#from visualization.style_colors import getStyle
from style_colors import getStyle
import argparse
import webbrowser

parser = argparse.ArgumentParser()

parser.add_argument('filename', type=str,
                   help='analyse filename')
args = parser.parse_args()

app = dash.Dash()
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

with open (args.filename, "r") as f:
    list = json.load(f);

    stockList = list[1]
    predictionList =list[2]
    nameList = list[0]
    stockList = [e for e in reversed(stockList)]
    predictionList = [e for e in reversed(predictionList)]
    stockList = np.array(stockList).T.tolist()
    predictionList = np.array(predictionList).T.tolist()
    #predictionList = np.array(predictionList).T.tolist()

    def tableInit():
        x = np.empty(len(stockList[0]))
        b = np.arange(0, len(stockList[0]), 1)
        ind = np.arange(len(x))
        np.put(x, ind, b)
        return x


    def calculateInvestments(stockQuotes, predictions, name):
        #invest, value, profit = 0, 0, 0
        #hasBought = True
        #invest = stockQuotes[0]
        #for x in range(1, len(predictions)):
        #    if predictions[x] > stockQuotes[x]:
        #        if hasBought == False:
        #            invest += stockQuotes[x]
        #            hasBought = True
        #        else:
        #            value = stockQuotes[x]
        #    else:
        #        if hasBought == True:
        #            profit += stockQuotes[x]
        #            value = 0
        #            hasBought = False
        BHL = ["BH"]
        PRE = ["NPSK"]

        p = 1
        print(name)
        for i in range(0, len(stockQuotes) - 1):
            print(stockQuotes[i])
            if predictions[i] > stockQuotes[i]:
                p *= stockQuotes[i + 1] / stockQuotes[i]

        bhlFactor = ((stockQuotes[-1] / stockQuotes[0]) - 1) * 100
        preFactor = (p - 1) * 100
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
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))]
        )

    def makeLayout(x, stockList, predictionList, nameList):
        list = [
            html.H1(children='Determining the value of companies by the comparative method')]

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
    webbrowser.open('http://localhost:8050', new=1)
    # def addFirmVisualization(stockQuotes, predictions, investmentRates):

if __name__ == '__main__':
    app.run_server(debug=True)
