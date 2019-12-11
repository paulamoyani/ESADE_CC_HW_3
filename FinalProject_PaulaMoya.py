#!/usr/bin/env python
# coding: utf-8

# # Final Project
# 
# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 
# 
# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 
# 
# 

# In[ ]:


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('nama_10_gdp_1_Data.csv')
df["Value"] = [x.replace('.', '') for x in df["Value"]]
df["Value"] = [x.replace(',', '.') for x in df["Value"]]
df = df.drop(df[df["Value"] == ":"].index, axis = 0)
df["Value"] = df["Value"].astype(float)

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['NA_ITEM'].unique()
units = df["UNIT"].unique()
country = df["GEO"].unique()

app.layout = html.Div(children = [html.Div([
################ First Graph ################
    html.Br(),
    html.Br(),
    html.H1("GRAPH 1 ", style = {"textAlign": "center"}),
    html.Br(),
        
        # Indicator 1
        html.Div([
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],
        style={'width': '48%', 'display': 'inline-block'}),

        # Indicator 2
        html.Div([
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure of general government'
            ),
        ],
        style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
 
    ]),
    
    # Units (Radio Buttons)
    html.Div(
        dcc.RadioItems(id = "units", options = [{"label" : u, "value": u} for u in units],
            style = {"marginTop" : "1.5em", 'text-align': 'justify'}, 
            value = units[0], 
            labelStyle={'display': 'inline-block', 'margin-right': 20})
    ),

    dcc.Graph(id='indicator-graphic'),
    html.Br(),
    dcc.Slider(
        id='year--slider',
        min=df['TIME'].min(),
        max=df['TIME'].max(),
        value=df['TIME'].max(),
        step=None,
        marks={str(year): str(year) for year in df['TIME'].unique()}
    ),

################ Second Graph ################ 
    html.Br(),
    html.Br(),
    html.H1("GRAPH 2 ", style = {"textAlign": "center"}),
    html.Br(),
    
    # Dropdowns
    html.Div(dcc.Dropdown(id= "country_select", options = [{"label": x, "value": x} for x in country],
        value = country[0]), style = {"width": "48%", "display": "inline-block", 'marginBottom': '1.5em'}),
    html.Div(dcc.Dropdown(id= "indicator_select", options = [{"label": x, "value": x} for x in available_indicators],
        value = available_indicators[0]), style = {"width": "48%", "display": "inline-block", 'marginBottom': '1.5em'}),
                                                                    
    # Units (Radio Buttons)
    html.Div(
        dcc.RadioItems(id = "units1", options = [{"label" : u, "value": u} for u in units],
            style = {"marginTop" : "1.5em", 'text-align': 'justify'}, 
            value = units[0], 
            labelStyle={'display': 'inline-block', 'margin-right': 20})),
             
    dcc.Graph(id = "country-graphic")
    ])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
#      dash.dependencies.Input('xaxis-type', 'value'),
#      dash.dependencies.Input('yaxis-type', 'value'),
     dash.dependencies.Input('units', 'value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
                 units, year_value):
    dff = df[df['TIME'] == year_value]
    dff = dff[dff["UNIT"] == units]
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        "layout": go.Layout(
            xaxis = {"title" : xaxis_column_name}, 
            yaxis = {"title" : yaxis_column_name},
            margin = {"l": 40, "b": 40, "t": 10, "r": 10}, hovermode = "closest"
        )
    }

@app.callback( 
    dash.dependencies.Output('country-graphic', 'figure'),
    [dash.dependencies.Input('country_select', 'value'),
     dash.dependencies.Input('indicator_select', 'value'),
     dash.dependencies.Input('units1', 'value')])   

def update_graph_1(country, indicator, units):
    dff1 = df[df["GEO"] == country]
    dff1 = dff1[dff1["NA_ITEM"] == indicator]
    dff1 = dff1[dff1["UNIT"] == units]
    
    return {
        "data" : [go.Scatter(
            y = dff1["Value"],
            x = dff1["TIME"],
            mode = "lines")],
        
        "layout": go.Layout(
            xaxis = {"title": "Year" },
            yaxis =  {"title" : country },
            margin = {"l": 40, "b": 40, "t": 10, "r": 10}, hovermode = "closest")
            
        
    }

if __name__ == '__main__':
    app.run_server()


# In[ ]:




