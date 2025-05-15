# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

options = [{'label': 'All Sites', 'value': 'ALL'}]
options.extend([{'label': site, 'value': site} for site in spacex_df["Launch Site"].unique()])

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=options, value="ALL", placeholder="place holder here", searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0, max=10000, step=1000, value=[min_payload, max_payload], marks={0: '0',100: '100'}, tooltip={"placement": "bottom", "always_visible": True}),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie(site_name):
    if site_name == "ALL":
        df_Gall = spacex_df.groupby("Launch Site")["class"].sum().reset_index()
        fig = px.pie(df_Gall, names="Launch Site", values="class", title = "Total successfull landings by site")
        return fig
    else:
        df_Csite = spacex_df[spacex_df["Launch Site"]==site_name]
        df_Csite['class'] = df_Csite['class'].map({1: 'Success', 0: 'Failure'})
        fig = px.pie(df_Csite, names='class', title='Total successfull landings for site {}'.format(site_name))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id="payload-slider", component_property="value")]
)
def get_scatter(site_name, payload_val):
    if site_name == "ALL":
        df_payload = spacex_df[spacex_df['Payload Mass (kg)'].between(payload_val[0], payload_val[1])]
        fig = px.scatter(df_payload, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Launch Success')
        return fig
    else:
        df_Csite2 = spacex_df[spacex_df["Launch Site"]==site_name]
        df_Csite2_pay = df_Csite2[df_Csite2['Payload Mass (kg)'].between(payload_val[0], payload_val[1])]
        fig = px.scatter(df_Csite2_pay, x='Payload Mass (kg)', y='class', color='Booster Version Category', title='Correlation between Payload and Launch Success for site {}'.format(site_name))
        return fig
# Run the app
if __name__ == '__main__':
    app.run()
