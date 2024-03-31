import dash
from dash import Dash, Input, Output, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import cv2
from utils import get_id_mask, rle_decode, create_mask_image
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
df = pd.read_csv('train_data_processed.csv')

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR], use_pages=True)

# Define page title, dropdowns, and graphs
pagetitle = dcc.Markdown('# OncoScan AI: Advanced Imaging for Stomach and Intestine Cancer')
graphtitle = dcc.Markdown(children='')

animated_figure = dcc.Graph(figure={})
visualize_figure = dcc.Graph(figure={})
case_dropdown = dcc.Dropdown(options=sorted(df['case'].unique()), value=123, clearable=False)
day_dropdown = dcc.Dropdown(options=sorted(df[df['case']==123]['day'].unique()), value=20, clearable=False)
slice_dropdown = dcc.Dropdown(options=sorted(df[(df['case']==123) & (df['day']==20)]['slice_no'].unique()), value=0, clearable=False)

# Navbar setup
navbar = dbc.NavbarSimple(
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
        ],
        nav=True,
        label="Pages",
    ),
    brand="OncoScan: Image Segmentation for Gastrointestinal Tract Cancer",
    color="primary",
    dark=True,
    className="mb-2",
)

# Layout setup
app.layout = dbc.Container([navbar, dash.page_container], fluid=True)

if __name__ == "__main__":
    app.run_server(port=8064, debug=False)
