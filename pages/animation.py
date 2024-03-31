import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import cv2
import plotly.express as px

# Register the current module as a Dash page
dash.register_page(__name__)

# Read the dataset
df = pd.read_csv('train_data_processed.csv')

# Define page components
pagetitle = dcc.Markdown('Please allow some time to load...')
graphtitle = dcc.Markdown(children='')
animated_figure = dcc.Graph(figure={})
case_dropdown = dcc.Dropdown(options=sorted(df['case'].unique()), value=123, clearable=False)

# Define layout
layout = dbc.Container([
    dbc.Row([
        dbc.Col([pagetitle], width=12)
    ], justify='left'),
    dbc.Row([
        dbc.Col([graphtitle], width=6)
    ], justify='left'),
    dbc.Row([
        dbc.Col([
            dcc.Loading(
                id='loading',
                type='circle',
                children=html.Div(id='loading_output')
            )
        ], style={'height': '1.8cm'})
    ]),
    dbc.Row([
        dbc.Col([animated_figure], width=9)
    ]),
    dbc.Row([
        dbc.Col([case_dropdown], width=6),
    ], justify='center')
], fluid=True)

@callback(
    Output('loading_output', 'children'),
    Output(animated_figure, 'figure'),
    Output(graphtitle, 'children'),
    Input(case_dropdown, 'value'),
)
def update_animation(case):
    '''
    Update the animation based on the selected case.

    Parameters:
        case (int): Selected case.

    Returns:
        str: Empty string.
        plotly.graph_objects.Figure: Updated animation figure.
        str: Text indicating successful animation load.
    '''
    # Filter dataframe for the selected case
    case_df = df.loc[df['case'] == case]
    idxs = case_df.index
    img_paths = case_df['path'].values
    
    imgs = []
    for path, idx in zip(img_paths, idxs):            
        # Read image from path
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        # Resize the image to 224 x 224
        img = cv2.resize(img, (224, 224))
        imgs.append(img)

    # Convert list of images to numpy array
    imgs = np.array(imgs)

    # Create animation figure
    fig = px.imshow(imgs, animation_frame=0, binary_string=True, labels=dict(animation_frame="slice"))

    return '', fig, 'Animation Loaded Successfully'
