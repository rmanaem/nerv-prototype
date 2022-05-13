
from distutils.log import debug
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from nerv import utility as util


def test(path, server):
    experiments = util.helper(path)
    app = dash.Dash(server=server, routes_pathname_prefix='/',
                    external_stylesheets=[dbc.themes.SLATE])
    # app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
    app.title = 'NeRV'

    layouts = util.generate_layouts(experiments)
    app.layout = layouts[0]
    app.validation_layout = html.Div(layouts)

    init_callbacks(app, path)
    return app.server


def init_callbacks(app, path):
    experiments = util.helper(path)
    layouts = [util.generate_index_layout(experiments)]
    for i in experiments:
        layouts.append(util.generate_layout(i[1]))

    @app.callback(
        Output('main-page', 'children'),
        Input('url', 'pathname')
    )
    def display_page(pathname):
        for i, j in enumerate(experiments):
            if pathname == '/'+j[0]:
                df = j[1]
                return layouts[i+1]

        return layouts[0]

    @app.callback(
        Output('storage', 'data'),
        Input('url', 'pathname')
    )
    def store_df(pathname):
        for i, j in enumerate(experiments):
            if pathname == '/'+j[0]:
                return j[1].to_json(orient='split')

        return None

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
        Input('y', 'value'),
        Input('storage', 'data')
    )
    def plot_scatter(x, y, data):
        if not x or not y:
            return dash.no_update
        df = pd.read_json(data, orient='split')
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
        Input('storage', 'data')
    )
    def process_click_scatter(clickData, x, y, data):
        if not clickData:
            return dash.no_update
        df = pd.read_json(data, orient='split')
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
