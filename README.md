# PlotlyDashProject
This repository contains a dashboard application built using the Dash Plotly framework

Here a list of libraries that are used: requests, StringIO, pandas, numpy, dash, dash_core_components, dash_html_components, plotly.express

First of all, the dataset is loaded via a url link. This dataset contains various information about video games, including platform, release year, genre, critic rating, player rating, age rating, sales data, etc. This file is taken from the Kaggle website.
Before building a responsive dashboard in Plotly Dash, we need to prepare the data. Data preparation includes editing NaN, filtering for specific period (from 2005+), checking some descriptive statistics.

To create filters for dashboards, let's find unique values in Genre, Rating, Year_of_Release columns

In order to create visualisation, Plotly Dash framework is used. 
