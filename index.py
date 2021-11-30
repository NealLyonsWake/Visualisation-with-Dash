# dependencies
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State

import pandas as pd
import plotly.express as px


# initialisation
app = dash.Dash('')
dataframe = pd.read_csv('data/airline_2m.csv', encoding='ISO-8859-1')

# set layouts
app.layout = html.Div([
html.H1('Airline Reporting Carier Ontime Performance'),
html.H2('Average Monthly Delays Per Year'),
html.Br(),
html.H3('Select Delay Type'),
dcc.Dropdown(options=[
            { 'label' : 'Carrier Delay', 'value': 'CarrierDelay'},
            { 'label' : 'Weather Delay', 'value': 'WeatherDelay'},
            { 'label' : 'National Air System Delay', 'value': 'NASDelay'},
        ], id='type_of_delay'),
html.Br(),
html.H3('Select Year'),
dcc.Slider(
    id='my-range-slider',
    min=2010,
    max=2020,
    step=1,
    value=2013
    ),
html.Div(id='output-container-range-slider'),
html.Br(),
dcc.Graph(id='airline-data', figure={})
])


# callbacks
@app.callback(
    Output(component_id='output-container-range-slider', component_property='children'),
    Output(component_id='airline-data', component_property='figure'),
    Input(component_id='type_of_delay', component_property='value'),
    Input(component_id='my-range-slider', component_property='value'),
  )
def calldata(delay_type, year):
    if delay_type is not None:
        filter_by_year = dataframe[dataframe['Year'] == year]
        monthly_av_carrier_delay = filter_by_year.groupby(['Month','Reporting_Airline']).mean().reset_index()
        figure = px.line(monthly_av_carrier_delay, x='Month', y=delay_type, color='Reporting_Airline')
        return year, figure
    else:
        return year, {}


# run server
app.run_server()