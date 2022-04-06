import os
import json
import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px

colors = [px.colors.sequential.Teal, px.colors.sequential.Brwnyl,
          px.colors.sequential.Burg, px.colors.sequential.Purp]


def pull_files(path):
    files = []
    for i in os.listdir(path):
        files.append((os.path.join(path, i), i[:len(i)-5]))
    return files


def process_file(file, color):
    data = None
    with open(file[0], 'r') as dataset:
        data = json.load(dataset)
    x = []
    for k in data.keys():
        z = len(colors[color]) - 1
        for v in data[k].keys():
            x.append((k, v, data[k][v]['Result']['result'],
                     data[k][v], colors[color][z]))
            z -= 1
    x = [(i[0], i[1], -1, i[3], i[4]) if i[2] ==
         None else (i[0], i[1], float(i[2]), i[3], i[4]) for i in x]
    df = pd.DataFrame({'Subject': [i[0] for i in x], 'Dataset-Pipeline': [
                      file[1]+'-'+i[1] for i in x], 'Result': [i[2] for i in x], 'Info': [i[3] for i in x], 'Color': [i[4] for i in x]})
    return df


def generate_summary(df):
    total = str(df.shape[0])
    miss = str(df[df['Result'] == -1].shape[0])
    header = html.H4('Summary', style={'textAlign': 'center'})
    summary = [header, "Total number of datapoints: " + total, html.Br(), "Total number of missing datapoints: "
               + miss, html.Br()]
    pipelines = df['Dataset-Pipeline'].unique().tolist()
    for p in pipelines:
        s = p + ': ' + str(df[(df['Dataset-Pipeline'] == p) &
                              (df['Result'] == -1)].shape[0])
        summary.append(s)
        summary.append(html.Br())
    return html.Div(html.P(summary, style={'margin-left': '10px'}),
                    style={
        'width': '90%',
        'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
        'border-radius': '7px',
        'border': '0.25px solid'})


def helper(path):
    files = []
    for directory in os.listdir(path):
        files.append((directory, pull_files(
            os.path.join(path, directory)), []))
    for i in files:
        for z, w in enumerate(i[1]):
            i[2].append(process_file(w, z))
    return [(i[0], pd.concat(i[2])) for i in files]


def generate_index_layout(ls):
    index = []
    for i in ls:
        index.append(dcc.Link(i[0], href='/'+i[0]))
        index.append(html.Br())

    return index


def generate_layout(df):
    return html.Div(
        [
            dcc.Link('Back', href='/'),
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
                                                generate_summary(df),
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


def generate_layouts(experiments):
    nav_bar_main_page = html.Div(
        [
            dcc.Store(id='storage'),
            dcc.Location(id='url'),
            html.Div(id='main-page')
        ]
    )

    layouts = [nav_bar_main_page, generate_index_layout(experiments)]
    for e in experiments:
        layouts.append(generate_layout(e[1]))

    return layouts
