import requests
from io import StringIO
import pandas as pd
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

url='https://drive.google.com/file/d/1ronWjzfgUcqbhwYGZjfNKvK2yt0tfUAZ/view?usp=sharing'

url='https://drive.google.com/uc?id=' + url.split('/')[-2]

df = pd.read_csv(url)

df.head()

df.info()

df = df.dropna()

df.head()

df = df[df['Year_of_Release']>=2005]

df.describe()

df['Genre'].unique()

df['Rating'].unique()

df['Year_of_Release'].unique()

years = df['Year_of_Release'].unique()

years = df['Year_of_Release'].unique().astype(int)

df['Year_of_Release'] = df['Year_of_Release'].astype(int)

app = dash.Dash()

app.layout = html.Div([
            html.H1(children="Gaming Dashboard",className="hello",
    style={'color':'#00361c','text-align':'center'
          }),
    dcc.Dropdown(
        id = 'genre-filter',
        options = [
            {'label': 'Adventure', 'value': 'Adventure'},
            {'label': 'Action', 'value': 'Action'},
            {'label': 'Fighting', 'value': 'Fighting'},
            {'label': 'Misc', 'value': 'Misc'},
            {'label': 'Platform', 'value': 'Platform'},
            {'label': 'Puzzle', 'value': 'Puzzle'},
            {'label': 'Racing', 'value': 'Racing'},
            {'label': 'Role-Playing', 'value': 'Role-Playing'},
            {'label': 'Shooter', 'value': 'Shooter'},
            {'label': 'Simulation', 'value': 'Simulation'},
            {'label': 'Sports', 'value': 'Sports'},
            {'label': 'Strategy', 'value': 'Strategy'}
        ],
        value=[],
        multi = True,
        clearable = True,
        style={"width": "50%"}
    ),
        dcc.Dropdown(
        id = 'rating-filter',
        options = [
            {'label': 'AO', 'value': 'AO'},
            {'label': 'E', 'value': 'E'},
            {'label': 'E10+', 'value': 'E10+'},
            {'label': 'M', 'value': 'M'},
            {'label': 'RP', 'value': 'RP'},
            {'label': 'T', 'value': 'T'}
        ],
        value=[],
        multi = True,
        clearable = True,
        style={"width": "50%"}
    ),
        dcc.RangeSlider(
        id = 'years-filter',
        min=min(years),
        max=max(years),
        marks={int(i):str(i) for i in years},
        value=[min(years), max(years)]
    ),
        # Interactive Text
        html.Div(id='interactive-text'),

        # Graph 1
        dcc.Graph(id='games-by-year-and-platform'),

        # Graph 2
        dcc.Graph(id='games-by-genre')
      ])

@app.callback(
    Output(component_id= 'games-by-year-and-platform', component_property= 'figure'),
    [Input(component_id= 'genre-filter', component_property= 'value'),
    Input(component_id= 'rating-filter', component_property= 'value'),
    Input(component_id= 'years-filter', component_property= 'value')]
)
def update_figure_1(selected_genre, selected_rating,selected_year):
    filtered_df = df[(df['Genre'].isin(selected_genre))
                     & (df['Rating'].isin(selected_rating))
                    & ((df['Year_of_Release'] >= selected_year[0]) & (df['Year_of_Release'] <= selected_year[1]))]
    figure = px.bar(filtered_df, x='Year_of_Release',
                     y='Global_Sales', color='Platform',
                     title='Games Global Sales by Year of Release and Platforms')

    return figure

@app.callback(
    Output(component_id= 'games-by-genre', component_property= 'figure'),
    [Input(component_id= 'genre-filter', component_property= 'value'),
    Input(component_id= 'rating-filter', component_property= 'value'),
    Input(component_id= 'years-filter', component_property= 'value')]
)
def update_figure_2(selected_genre, selected_rating, selected_year):
    filtered_df = df[(df['Genre'].isin(selected_genre))
                     & (df['Rating'].isin(selected_rating))
                    & ((df['Year_of_Release'] >= selected_year[0]) & (df['Year_of_Release'] <= selected_year[1]))]
    figure = px.scatter(filtered_df, x='User_Score',
                        y='Critic_Score', color='Genre',
                        title='Users and Critic score by genres')
    return figure

@app.callback(
    Output(component_id='interactive-text', component_property='children'),
    [Input(component_id='genre-filter', component_property='value'),
     Input(component_id='rating-filter', component_property='value'),
     Input(component_id='years-filter', component_property='value')]
)
def update_interactive_text(selected_genres, selected_ratings, selected_years):
    interacitve_text = 'Выбранные фильтры: '
    if selected_genres is not None and len(selected_genres) > 0:
        interacitve_text = interacitve_text + f'Genre: {", ".join(selected_genres)}; '
    if selected_ratings is not None and len(selected_ratings) > 0:
        interacitve_text = interacitve_text + f'Rating: {", ".join(selected_ratings)}; '
    if selected_years is not None and len(selected_years) == 2:
        interacitve_text = interacitve_text + f'Year: {selected_years[0]}-{selected_years[1]}'
    return interacitve_text

if __name__=='__main__':
    app.run_server(debug=True)

