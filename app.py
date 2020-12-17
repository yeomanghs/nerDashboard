
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
import json
from itertools import count
# from dash_table import DataTable

#predefine parameters
metricList = ['Precision', 'Recall', 'F1Score']
#metrics from munirah's model
munirahFile = "./data/2020-12-17_MunirahMetrics.csv"
#metrics from crf's model
crfFile = "./data/2020-12-17_CRFMetrics.csv"

#writing list of dicts in a json file
# jsonFile = "D:\\Users\\figohjs\\Documents\\NLP\\NER\\data\\training\\2020-10-22_TrainDataWithPred.json"
# tagCol = ['RealTag', 'PredTagMunirah']
# realTagCol = ['RealTag', 'RealTagType']
# predTagCol = ['PredTagMunirah', 'PredTagMunirahType']
# recordDictBack = []
# with open(jsonFile, 'r', encoding='utf-8') as input_file:
#     for row in input_file.readlines():
#         recordDictBack.append(json.loads(row))
        
# #build a generator of description
# descIter = iter([i['Description'] for i in recordDictBack])
# #only want tagCol for list of dict - build 2 similar iter to get same 
# tagDictList = iter([{key:val for key,val in i.items() if key in tagCol} for i in recordDictBack])
# tagDictList2 = iter([{key:val for key,val in i.items() if key in tagCol} for i in recordDictBack])
# row = count()

#munirah model table
df = pd.read_csv(munirahFile)
#munirah model dict
resultDictMunirah = {}
for col in ['PERSON', 'ORG', 'Overall', 'NE']:
    resultDictMunirah[col] = df.query('Metric in @metricList')[col].values

#crf model table
df2 = pd.read_csv(crfFile)
#new model dict
resultDictCrf = {}
for col in ['PERSON', 'ORG', 'Overall', 'NE']:
    resultDictCrf[col] = df2.query('Metric in @metricList')[col].values
    
#Bootstrap themes
app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP], meta_tags=[{"name": "viewport", "content": "width=device-width"}])
server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "14rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "14rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
#         html.H2('Dashboard', className="display-4"),
        html.Hr(),
        html.P(
            "NER Dashboard", className="lead"
              ),
        dbc.Nav(
            [
                dbc.NavLink("Models Comparison", href="/page-1", id = "page-1-link"),
                dbc.NavLink("CRF Flow", href="/page-2", id = "page-2-link"),
                dbc.NavLink("CRF Features", href="/page-3", id = "page-3-link"),
                dbc.NavLink("Evaluation", href="/page-4", id = "page-4-link"),
                dbc.NavLink("Conclusion & Suggestion", href="/page-5", id = "page-5-link")
            ],
            vertical = True,
            pills = True,
        ),
    ],
    style = SIDEBAR_STYLE,
)


graphPage = [
        html.Div(children = [
        dbc.Row(dbc.Col(html.Div("Please select dimension"))),        
        dcc.Dropdown(
            id = 'dimension',
            options = [{'label': i, 'value': i} for i in ['Overall', 'By Label Types']],
            value = 'Overall'
                    ),
        dbc.Row(dbc.Col(html.Div(id = "graphTitle1"))),
        html.Div(id ='output-graph1'),
        dbc.Row(dbc.Col(html.Div(id = "graphTitle2"))),
        html.Div(id ='output-graph2'),
        dbc.Row(dbc.Col(html.Div(id = "graphTitle3"))),
        html.Div(id ='output-graph3'),        
                            ])
            ]

imagePage1 = html.Div(
                [
                    html.Img(
                        src = app.get_asset_url("comparison.png"),
                        style={'height':'50%', 'width':'80%'}
                            ),
                ])

imagePage2 = html.Div(
                [
                    html.Img(
                        src = app.get_asset_url("processing.png"),
                        style={'height':'50%', 'width':'70%'}
                            ),
                ])

imagePage3 = html.Div(
                [
                    html.Img(
                        src = app.get_asset_url("crfFeatures.png"),
                        style={'height':'100%', 'width':'100%'}
                            ),
                ])

section1 = "Conclusion"
S1point1 = "SpaCy outperforms CRF in both ORG and PERSON labels,"\
            " but both models perform quite similar in identification of named entities (wrong label)"
S1point2 = "CRF performs slightly better in Recall for identification of named entities (wrong label)"

section2 = "Suggestion of improvement"
S2point1 = "Fine tune process of changing case"
S2point2 = "Find out reason of mislabelling - rebuild feature engineering"
S2point3 = "Train using own labelled data - possibly redo preprocessing and feature engineering"

lastPage =  html.Div(
                    [
                        html.H6("%s"%section1),
                        html.Br([]),
                        html.Div(
                            [
                                html.Li("%s"%S1point1),
                                html.Li("%s"%S1point2),
                            ],
                                ),
                        html.Br([]),
                        html.Br([]),
                        html.H6("%s"%section2),
                        html.Br([]),
                        html.Div(
                            [
                                html.Li("%s"%S2point1),
                                html.Li("%s"%S2point2),
                                html.Li("%s"%S2point3),
                            ],
                                )
                    ],
                    )


content = html.Div(id="page-content", style = CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id = "url"), sidebar, content])
                    
#callback on link
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 6)],
    [Input("url", "pathname")],
            )
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/page-{i}" for i in range(1, 6)]
                
#callback on page
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        return imagePage1
    elif pathname == "/page-2":
        return imagePage2
    elif pathname == "/page-3":
        return imagePage3
    elif pathname == "/page-4":
        return graphPage
    elif pathname == "/page-5":
        return lastPage
#         return textPage
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
                        )

#callback on text description, labels
# @app.callback(
#     [
#     Output("rowCount", "children"),
#     Output("text-description", 'children'),
#     Output("realTable", "data"),
#     Output("predTable", "data")
#     ],
#     [Input('clickNext', 'n_clicks')]
#             )
# def updateDescription(n_clicks):
#     if n_clicks:
#         return "Row: %s"%str(next(row) + 1), next(descIter), convertForm(next(tagDictList), 'RealTag'), \
#     convertForm(next(tagDictList2), 'PredTagMunirah')

#callback on graphs
@app.callback(
    [Output('graphTitle1', 'children'),
    Output('output-graph1', 'children'),
    Output('graphTitle2', 'children'),
    Output('output-graph2', 'children'),
    Output('graphTitle3', 'children'),
    Output('output-graph3', 'children'),],
    [Input('dimension', 'value')])
def churnOutGraphraph(value):
    if value == "Overall":
        title = 'Overall comparison'
        child = [dcc.Graph(
            id = 'histogram',
            figure = {"data":[go.Bar(
                                    x = metricList,
                                    y = resultDictMunirah['Overall'],
                                marker={
                                    "color": "#97151c",
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                             },
                                        },
                                        name = "SpaCy Model",
                                     ),
                                go.Bar(
                                      x = metricList,
                                      y = resultDictCrf['Overall'],
                                marker={
                                    #dddddd
                                    "color": "lightslategrey",
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                            },
                                        },
                                    name = "CRF Model",
                                    )
                                 ],
                             }
                            )]
        title2 = ''
        child2 = ''
        title3 = ''
        child3 = ''
    elif value == "By Label Types":
        title = 'Person Label Comparison'
        child = [dcc.Graph(
            id = 'histogram',
            figure = {"data":[go.Bar(
                                    x = metricList,
                                    y = resultDictMunirah['PERSON'],
                                marker={
                                    "color": "#97151c",
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                             },
                                        },
                                        name = "SpaCy Model",
                                     ),
                                go.Bar(
                                      x = metricList,
                                      y = resultDictCrf['PERSON'],
                                marker={
                                    #dddddd
                                    "color": "lightslategrey",
                                    "line": {
                                        "color": "rgb(255, 255, 255)",
                                        "width": 2,
                                            },
                                        },
                                    name = "CRF Model",
                                    )
                                 ],
                             }
                            )]
        title2 = 'ORG Label Comparison'
        child2 =  [dcc.Graph(
        id = 'histogram2',
        figure = {"data":[go.Bar(
                                x = metricList,
                                y = resultDictMunirah['ORG'],
                            marker={
                                "color": "#97151c",
                                "line": {
                                    "color": "rgb(255, 255, 255)",
                                    "width": 2,
                                         },
                                    },
                                    name = "SpaCy Model",
                                 ),
                            go.Bar(
                                  x = metricList,
                                  y = resultDictCrf['ORG'],
                            marker={
                                #dddddd
                                "color": "lightslategrey",
                                "line": {
                                    "color": "rgb(255, 255, 255)",
                                    "width": 2,
                                        },
                                    },
                                name = "CRF Model",
                                )
                             ],
                         }
                        )]
        title3 = 'Named Entities Comparison (Wrong Label)'
        child3 =  [dcc.Graph(
        id = 'histogram3',
        figure = {"data":[go.Bar(
                                x = metricList,
                                y = resultDictMunirah['NE'],
                            marker={
                                "color": "#97151c",
                                "line": {
                                    "color": "rgb(255, 255, 255)",
                                    "width": 2,
                                         },
                                    },
                                    name = "SpaCy Model",
                                 ),
                            go.Bar(
                                  x = metricList,
                                  y = resultDictCrf['NE'],
                            marker={
                                #dddddd
                                "color": "lightslategrey",
                                "line": {
                                    "color": "rgb(255, 255, 255)",
                                    "width": 2,
                                        },
                                    },
                                name = "CRF Model",
                                )
                             ],
                         }
                        )]
    #if value is not empty
    if value:
        return title, child, title2, child2, title3, child3
    else: 
        raise PreventUpdate     
            
            
if __name__ == '__main__':
    app.run_server(debug=True)
