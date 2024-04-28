import dash
import numpy as np
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load data from CSV file
df = pd.read_csv("data.csv")

bins = np.arange(65, 105, 5)

df['rating_interval'] = pd.cut(df['rating'], bins=bins, labels=[f'{i}-{i+4}' for i in bins[:-1]])

rating_counts = df['rating_interval'].value_counts().sort_index()

app = dash.Dash(__name__)

team_stats = df.groupby('team').agg({'height': 'mean', 'weight': 'mean', 'salary': 'mean', 'rating': 'mean', 'BMI': 'mean'}).reset_index()

app.layout = html.Div([
    html.H1("NBA PLAYERS DASHBOARD", style={"text-align": "center"}),
    
    html.Div([
        html.Div(style={"width": "2%", "display": "inline-block"}),
        html.Div(
            dcc.Graph(id="age-histogram"),
            style={"width": "28%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}
        ),
        html.Div(style={"width": "2%", "display": "inline-block"}),
        html.Div(
            dcc.Graph(id="ratings-bar"),
            style={"width": "30%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}
        ),
        html.Div(style={"width": "2%", "display": "inline-block"}),
        html.Div(
            dcc.Graph(id="position-pie"),
            style={"width": "28%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}
        ),
        html.Div(style={"width": "100%", "display": "inline-block"}),
        html.Div([
            html.Div(style={"width": "2%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="height-line"),
            ], style={"width": "22%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
            html.Div(style={"width": "1%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="weight-line"),
            ], style={"width": "22%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
            html.Div(style={"width": "1%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="salary-line"),
            ], style={"width": "22%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
            html.Div(style={"width": "1%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="rating-line"),
            ], style={"width": "22%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
        ]),
        html.Div(style={"width": "100%", "display": "inline-block"}),
        html.Div([
            html.Div(style={"width": "2%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="country-map"),
            ], style={"width": "45%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
            html.Div(style={"width": "1%", "display": "inline-block"}),
            html.Div([
                dcc.Graph(id="bmi-line"),
            ], style={"width": "45%", "display": "inline-block", "padding": "10px", "border": "1px solid black"}),
        ])
    ]),
])

@app.callback(
    Output('age-histogram', 'figure'),
    [Input('age-histogram', 'id')]
)
def update_histogram(_):
    fig = px.histogram(df, x="age", nbins=20, title="Histogram of Age")
    return fig

@app.callback(
    Output('ratings-bar', 'figure'),
    [Input('ratings-bar', 'id')]
)
def update_bar(_):
    fig = px.bar(x=rating_counts.index, y=rating_counts.values, title='Player Ratings')
    return fig

@app.callback(
    Output('position-pie', 'figure'),
    [Input('position-pie', 'id')]
)
def update_pie(_):
    fig = px.pie(df, names='position', title='Player Positions')
    return fig

@app.callback(
    Output('height-line', 'figure'),
    [Input('height-line', 'id')]
)
def update_height_line(_):
    fig = px.line(team_stats, x='team', y='height', title='Average Height by Team', hover_data={'team': False, 'height': True})
    fig.update_xaxes(title_text='Team')
    return fig

@app.callback(
    Output('weight-line', 'figure'),
    [Input('weight-line', 'id')]
)
def update_weight_line(_):
    fig = px.line(team_stats, x='team', y='weight', title='Average Weight by Team', hover_data={'team': False, 'weight': True})
    fig.update_xaxes(title_text='Team')
    return fig

@app.callback(
    Output('salary-line', 'figure'),
    [Input('salary-line', 'id')]
)
def update_salary_line(_):
    fig = px.line(team_stats, x='team', y='salary', title='Average Salary by Team', hover_data={'team': False, 'salary': True})
    fig.update_xaxes(title_text='Team')
    return fig

@app.callback(
    Output('rating-line', 'figure'),
    [Input('rating-line', 'id')]
)
def update_rating_line(_):
    fig = px.line(team_stats, x='team', y='rating', title='Average Rating by Team', hover_data={'team': False, 'rating': True})
    fig.update_xaxes(title_text='Team')
    return fig

@app.callback(
    Output('country-map', 'figure'),
    [Input('country-map', 'id')]
)
def update_country_map(_):
    country_counts = df['country'].value_counts()
    country_counts_df = country_counts.reset_index()
    country_counts_df.columns = ['country', 'count']
    fig = px.scatter_geo(country_counts_df, locations="country", locationmode="country names", size='count',
                         title="Player Distribution by Country",
                         hover_name="country", color='count',
                         projection="natural earth", size_max=40)
    fig.update_layout(geo=dict(showcoastlines=True))
    return fig

@app.callback(
    Output('bmi-line', 'figure'),
    [Input('bmi-line', 'id')]
)
def update_bmi_line(_):
    fig = px.line(team_stats, x='team', y='BMI', title='Average BMI by Team', hover_data={'team': False, 'BMI': True})
    fig.update_xaxes(title_text='Team')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)