from flask import Flask, jsonify, request
from config import Config

from dash import Dash, html, dcc, dash_table, callback, Output, Input, State
import pandas as pd

# add config switch later
def create_app():

    # create flask instance
    app = Flask(__name__)
    

    # set config from config.py
    app.config.from_object(Config)



    # dash stuff
    # Sample data for the DataTable
    df = pd.DataFrame({
        'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [24, 30, 22, 35],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']
    })

    # Initialize Dash app with specific url_base_pathname
    dash_app = Dash(__name__, server=app, url_base_pathname='/dash/')

    # Dash layout
    dash_app.layout = html.Div([
        html.H1('Dash Application'),
        dcc.Input(id='input-box', type='text'),
        html.Button('Submit', id='button'),
        html.Div(id='output'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            sort_action='native',
            filter_action='native'
        )
    ])

    # Dash callback
    @callback(
        Output('output', 'children'),
        [Input('button', 'n_clicks')],
        [State('input-box', 'value')]
    )
    def update_output(n_clicks, value):
        return f'You have entered: {value}'





    # import routes
    from . import routes

    # register blueprints
    app.register_blueprint(routes.routes)


    return app