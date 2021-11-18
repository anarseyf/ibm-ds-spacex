# Import required libraries
import pandas as pd
import numpy as np
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
df = pd.read_csv("spacex_launch_dash.csv")
df['Const'] = [1] * len(df)

PAYLOAD = 'Payload Mass (kg)'
LAUNCH_SITE = 'Launch Site'
OUTCOME_CLASS = 'Outcome Class'

max_payload = df[PAYLOAD].max()
min_payload = df[PAYLOAD].min()

launch_sites = np.unique(df[LAUNCH_SITE].to_list())
launch_options = list(map(lambda s: {'label': s, 'value': s}, launch_sites))
launch_options = [{'label': 'All Sites', 'value': 'ALL'}] + launch_options

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    # TASK 1: Add a dropdown list to enable Launch Site selection
    # The default select value is for ALL sites
    dcc.Dropdown(
        id='site-dropdown',
        options=launch_options,
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0', 100: '100'},
                    value=[min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback([Output('success-pie-chart', 'figure'),
               Output('success-payload-scatter-chart', 'figure')],
              [Input('site-dropdown', 'value'),
              Input('payload-slider', 'value')])
def get_pie_chart(site, payload):

    data = df if site == 'ALL' else df[df[LAUNCH_SITE] == site]

    if site == 'ALL':
        fig1 = px.pie(data,
                      values=OUTCOME_CLASS,
                      names=LAUNCH_SITE,
                      title='All Launch Sites')
    else:
        fig1 = px.pie(data,
                      values='Const',
                      names=OUTCOME_CLASS,
                      title='Success/Failure for %s' % site)

    [from_payload, to_payload] = payload

    payload_data = data[(data[PAYLOAD] >=
                        from_payload) & (data[PAYLOAD] <= to_payload)]

    fig2 = px.scatter(payload_data,
                      x=PAYLOAD,
                      y=OUTCOME_CLASS,
                      color='Booster Version Category')

    fig2.update_traces(marker={'size': 12})

    return [fig1, fig2]

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
