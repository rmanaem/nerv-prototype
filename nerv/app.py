import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from nerv import utility as util


def local_start(path):
    files = util.pull_files(path)
    dfs = []
    for i, j in enumerate(files):
        dfs.append(util.process_file(j, i))
    df = pd.concat(dfs)

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
    app.title = 'NeRV'
    app.layout = html.Div(
        [
            html.Br(),
            dcc.Tabs
            (
                [
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        dcc.Graph
                                        (
                                            id='histogram',
                                            figure=px.histogram
                                            (
                                                df[df['Result'] != -1],
                                                x='Result',
                                                color='Dataset-Pipeline',
                                                color_discrete_map={k: v for k, v in zip(
                                                    df['Dataset-Pipeline'].unique().tolist(), df['Color'].unique().tolist())},
                                                barmode='overlay',
                                                marginal='rug',
                                                hover_data=df.columns
                                            ).update_layout
                                            (
                                                xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$',
                                                yaxis_title='Count',
                                                template='plotly_dark',
                                                xaxis={
                                                    'rangeslider': {'visible': True}
                                                }
                                            ),
                                            config={'displaylogo': False},
                                            style={'height': 855},
                                            mathjax=True
                                        ),
                                        id='histogram-div',
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                util.generate_summary(df),
                                                id='summary-div'
                                            ),
                                            html.Br(),
                                            html.Div(id='info-div')
                                        ],
                                        style={'width': '25%',
                                               'margin-left': '30px'}
                                    )
                                ],
                                style={
                                    'display': 'flex'
                                }
                            )
                        ]
                    ),
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                [
                                                    dcc.Dropdown
                                                    (
                                                        id='x',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px'},
                                                        value=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        placeholder='x'
                                                    ),
                                                    dcc.Dropdown
                                                    (
                                                        id='y',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px'},
                                                        value=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1],
                                                        placeholder='y'
                                                    )
                                                ],
                                                style={
                                                    'display': 'flex',
                                                    'margin-left': 'auto',
                                                    'margin-right': 'auto',
                                                    'width': '50%'
                                                }
                                            ),
                                            html.Div
                                            (
                                                dcc.Graph
                                                (
                                                    id='scatter',
                                                    figure=px.scatter
                                                    (
                                                        df,
                                                        x=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[0]]['Result'],
                                                        y=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[-1]]['Result'],
                                                        marginal_x='histogram',
                                                        marginal_y='histogram',
                                                        template='plotly_dark',
                                                        color_discrete_sequence=px.colors.qualitative.G10[::-1]
                                                    ).update_layout
                                                    (
                                                        xaxis={
                                                            'rangeslider': {'visible': True}
                                                        },
                                                        xaxis_title=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        yaxis_title=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1]
                                                    ),
                                                    config={
                                                        'displaylogo': False},
                                                    style={'height': 819}
                                                ),
                                            )
                                        ],
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        id='info-div-scatter',
                                        style={
                                            'width': '25%',
                                            'margin-left': '30px'
                                        }
                                    )
                                ],
                                style={'display': 'flex'}
                            )
                        ]
                    )
                ],
                colors={
                    'border': '#343a40',
                    'primary': '#343a40',
                    'background': '#f8f9fa'
                }
            )
        ]
    )

    init_callbacks(app, path, df)
    app.run_server()


# def test(path):
#     experiments = util.helper(path)
#     app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
#     # app = dash.Dash(server=server, routes_pathname_prefix='/nerv/',
#     #                 external_stylesheets=[dbc.themes.SLATE])
#     app = dash.Dash()
#     app.title = 'NeRV'

#     index_layout = html.Div(util.generate_index_layout(experiments))

#     app.layout = html.Div(
#         [
#             dcc.Location(id='url'),
#             html.Div(id='main-page')
#         ]
#     )

#     layouts = [index_layout]
#     for i in experiments:
#         layouts.append(util.generate_layout(i[1]))

#     app.validation_layout = html.Div(layouts)

#     init_callbacks(app, path)
#     return app.run_server(debug=True)


def start(path, server):
    files = util.pull_files(path)
    dfs = []
    for i, j in enumerate(files):
        dfs.append(util.process_file(j, i))
    df = pd.concat(dfs)

    app = dash.Dash(server=server, routes_pathname_prefix='/nerv/',
                    external_stylesheets=[dbc.themes.SLATE])
    app.title = 'NeRV'
    app.layout = html.Div(
        [
            html.Br(),
            dcc.Tabs
            (
                [
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        dcc.Graph
                                        (
                                            id='histogram',
                                            figure=px.histogram
                                            (
                                                df[df['Result'] != -1],
                                                x='Result',
                                                color='Dataset-Pipeline',
                                                color_discrete_map={k: v for k, v in zip(
                                                    df['Dataset-Pipeline'].unique().tolist(), df['Color'].unique().tolist())},
                                                barmode='overlay',
                                                marginal='rug',
                                                hover_data=df.columns
                                            ).update_layout
                                            (
                                                xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$',
                                                yaxis_title='Count',
                                                template='plotly_dark',
                                                xaxis={
                                                    'rangeslider': {'visible': True}
                                                }
                                            ),
                                            config={'displaylogo': False},
                                            style={'height': 855},
                                            mathjax=True
                                        ),
                                        id='histogram-div',
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                util.generate_summary(df),
                                                id='summary-div'
                                            ),
                                            html.Br(),
                                            html.Div(id='info-div')
                                        ],
                                        style={'width': '25%',
                                               'margin-left': '30px'}
                                    )
                                ],
                                style={
                                    'display': 'flex'
                                }
                            )
                        ]
                    ),
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                [
                                                    dcc.Dropdown
                                                    (
                                                        id='x',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px'},
                                                        value=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        placeholder='x'
                                                    ),
                                                    dcc.Dropdown
                                                    (
                                                        id='y',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px'},
                                                        value=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1],
                                                        placeholder='y'
                                                    )
                                                ],
                                                style={
                                                    'display': 'flex',
                                                    'margin-left': 'auto',
                                                    'margin-right': 'auto',
                                                    'width': '50%'
                                                }
                                            ),
                                            html.Div
                                            (
                                                dcc.Graph
                                                (
                                                    id='scatter',
                                                    figure=px.scatter
                                                    (
                                                        df,
                                                        x=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[0]]['Result'],
                                                        y=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[-1]]['Result'],
                                                        marginal_x='histogram',
                                                        marginal_y='histogram',
                                                        template='plotly_dark',
                                                        color_discrete_sequence=px.colors.qualitative.G10[::-1]
                                                    ).update_layout
                                                    (
                                                        xaxis={
                                                            'rangeslider': {'visible': True}
                                                        },
                                                        xaxis_title=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        yaxis_title=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1]
                                                    ),
                                                    config={
                                                        'displaylogo': False},
                                                    style={'height': 819}
                                                ),
                                            )
                                        ],
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        id='info-div-scatter',
                                        style={
                                            'width': '25%',
                                            'margin-left': '30px'
                                        }
                                    )
                                ],
                                style={'display': 'flex'}
                            )
                        ]
                    )
                ],
                colors={
                    'border': '#343a40',
                    'primary': '#343a40',
                    'background': '#f8f9fa'
                }
            )
        ]
    )

    init_callbacks(app, path, df)
    return app.server


def init_callbacks(app, path, df):
    # for local start
    # files = util.pull_files(path)
    # dfs = []
    # for i, j in enumerate(files):
    #     dfs.append(util.process_file(j, i))
    # df = pd.concat(dfs)

    # For test
    # experiments = util.helper(path)
    # layouts = [util.generate_index_layout(experiments)]
    # for i in experiments:
    #     layouts.append(util.generate_layout(i[1]))

    # @app.callback(
    #     Output('main-page', 'children'),
    #     Input('url', 'pathname')
    # )
    # def display_page(pathname):
    #     for i, j in enumerate(experiments):
    #         if pathname == '/'+j[0]:
    #             return layouts[i+1]
    #     return layouts[0]

    @app.callback(
        Output('info-div', 'children'),
        Input('histogram', 'clickData')
    )
    def process_click(clickData):
        if not clickData:
            return dash.no_update
        subject = "Subject: " + \
            clickData['points'][0]['customdata'][0]
        pipeline = "Pipeline: " + clickData['points'][0]['y']
        result = "Result: N/A" if clickData['points'][0]['x'] == - \
            1 else "Result: " + str(clickData['points'][0]['x'])
        header = html.H4('Information', style={'textAlign': 'center'})
        info = [header, subject, html.Br(), pipeline, html.Br(),
                result, html.Br()]

        for k, v in list(clickData['points'][0]['customdata'][2].items())[:-1]:
            status = "Incomplete" if v['status'] == None else v['status']
            inp = "N/A" if v['inputID'] == None else html.A(str(
                v['inputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['inputID']))
            out = "N/A" if v['outputID'] == None else html.A(str(
                v['outputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['outputID']))
            task = "N/A" if v['taskID'] == None else html.A(str(
                v['taskID']), href='https://portal.cbrain.mcgill.ca/tasks/inser_ID_here' + str(v['taskID']))
            config = "N/A" if v['toolConfigID'] == None else str(
                v['toolConfigID'])
            step = html.Details(
                [
                    html.Summary(k),
                    "Status: " + status,
                    html.Br(),
                    "Input ID: ", inp,
                    html.Br(),
                    "Output ID: ", out,
                    html.Br(),
                    "Task ID: ", task,
                    html.Br(),
                    "Tool Configuration ID: " + config
                ]
            )
            info.append(step)

        return html.Div(
            html.P
            (
                info,
                style={'margin-left': '10px', 'word-wrap': 'break-word'}),
            style={
                'width': '90%',
                'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
                'border-radius': '7px',
                'border': '0.25px solid'
            }
        )

    @app.callback(
        Output('scatter', 'figure'),
        Input('x', 'value'),
        Input('y', 'value')
    )
    def plot_scatter(x, y):
        if not x or not y:
            return dash.no_update
        fig = px.scatter(
            df,
            x=df[df['Dataset-Pipeline'] == x]['Result'],
            y=df[df['Dataset-Pipeline'] == y]['Result'],
            marginal_x='histogram',
            marginal_y='histogram',
            template='plotly_dark',
            color_discrete_sequence=px.colors.qualitative.G10[::-1]
        ).update_layout(
            xaxis={'rangeslider': {'visible': True}},
            xaxis_title=x,
            yaxis_title=y
        )
        return fig

    @app.callback(
        Output('info-div-scatter', 'children'),
        Input('scatter', 'clickData'),
        Input('x', 'value'),
        Input('y', 'value'),
    )
    def process_click_scatter(clickData, x, y):
        if not clickData:
            return dash.no_update

        header = html.H4('Information', style={'textAlign': 'center'})
        x_subject = "Subject: " + df[(df['Dataset-Pipeline'] == x) & (
            df['Result'] == clickData['points'][0]['x'])]['Subject'].iloc[0]
        x_pipeline = "Pipeline: " + x
        x_result = "Result: N/A" if clickData['points'][0]['x'] == - \
            1 else "Result: " + str(clickData['points'][0]['x'])
        info = [header, x_subject, html.Br(), x_pipeline, html.Br(),
                x_result, html.Br()]
        x_info = df[(df['Dataset-Pipeline'] == x) & (df['Result'] ==
                                                     clickData['points'][0]['x'])]['Info'].iloc[0]
        for k, v in list(x_info.items())[:-1]:
            status = "Incomplete" if v['status'] == None else v['status']
            inp = "N/A" if v['inputID'] == None else html.A(str(
                v['inputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['inputID']))
            out = "N/A" if v['outputID'] == None else html.A(str(
                v['outputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['outputID']))
            task = "N/A" if v['taskID'] == None else html.A(str(
                v['taskID']), href='https://portal.cbrain.mcgill.ca/tasks/inser_ID_here' + str(v['taskID']))
            config = "N/A" if v['toolConfigID'] == None else str(
                v['toolConfigID'])
            step = html.Details(
                [
                    html.Summary(k),
                    "Status: " + status,
                    html.Br(),
                    "Input ID: ", inp,
                    html.Br(),
                    "Output ID: ", out,
                    html.Br(),
                    "Task ID: ", task,
                    html.Br(),
                    "Tool Configuration ID: " + config
                ]
            )
            info.append(step)

        y_subject = "Subject: " + df[(df['Dataset-Pipeline'] == y) & (
            df['Result'] == clickData['points'][0]['y'])]['Subject'].iloc[0]
        y_pipeline = "Pipeline: " + y
        y_result = "Result: N/A" if clickData['points'][0]['y'] == - \
            1 else "Result: " + str(clickData['points'][0]['y'])
        info += [html.Br(), y_subject, html.Br(), y_pipeline, html.Br(),
                 y_result, html.Br()]
        y_info = df[(df['Dataset-Pipeline'] == y) & (df['Result'] ==
                                                     clickData['points'][0]['y'])]['Info'].iloc[0]
        for k, v in list(y_info.items())[:-1]:
            status = "Incomplete" if v['status'] == None else v['status']
            inp = "N/A" if v['inputID'] == None else html.A(str(
                v['inputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['inputID']))
            out = "N/A" if v['outputID'] == None else html.A(str(
                v['outputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['outputID']))
            task = "N/A" if v['taskID'] == None else html.A(str(
                v['taskID']), href='https://portal.cbrain.mcgill.ca/tasks/inser_ID_here' + str(v['taskID']))
            config = "N/A" if v['toolConfigID'] == None else str(
                v['toolConfigID'])
            step = html.Details(
                [
                    html.Summary(k),
                    "Status: " + status,
                    html.Br(),
                    "Input ID: ", inp,
                    html.Br(),
                    "Output ID: ", out,
                    html.Br(),
                    "Task ID: ", task,
                    html.Br(),
                    "Tool Configuration ID: " + config
                ]
            )
            info.append(step)

        return html.Div(
            html.P
            (
                info,
                style={'margin-left': '10px', 'word-wrap': 'break-word'}
            ),
            style={
                'width': '90%',
                'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
                'border-radius': '7px',
                'border': '0.25px solid'
            }
        )
