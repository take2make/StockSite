import pandas as pd 

df = pd.read_csv('data/stockdata.csv', index_col=0, parse_dates=True)
df.index = pd.to_datetime(df['Date'])

print(df)

import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div()

def get_options(list_stocks):
	dict_list = []
	for i in list_stocks:
		dict_list.append({'label': i, 'value': i})

	return dict_list

app.layout = html.Div(children=[
	html.Div(className = 'row',
		children=[
			html.Div(className="four columns div-user-controls",
				children=[
				      html.H2('Прогноз гос-закупок'),
				      html.P('''Визуализация цен'''),
				      html.Div(className='div-for-dropdown',
			          children=[
			              dcc.Dropdown(id='stockselector',
			                           options=get_options(df['stock'].unique()),
			                           multi=False,
			                           value=[df['stock'].sort_values()[0]],
			                           style={'backgroundColor': '#1E1E1E'},
			                           className='stockselector')
			                    ],
			          style={'color': '#1E3E1E', 'backgroundColor': '#1E1E1E'})
				]),
			html.Div(className="eight columns div-for-charts bg-grey",
				children=[
					  dcc.Graph(id='timeseries', config={'displayModeBar': False}),
                      dcc.Graph(id='change', config={'displayModeBar': False})
				]),
			])
		])

@app.callback(Output('timeseries', 'figure'),
	[Input('stockselector', 'value')])
def update_timeseries(selected_dropdown_value):
    ''' Draw traces of the feature 'value' based one the currently selected stocks '''
    # STEP 1
    trace = []  
    df_sub = df
    # STEP 2
    # Draw and append traces for each stock
    #for stock in selected_dropdown_value:
    stock = selected_dropdown_value
    if type(stock) == list:
    	stock = stock[0]
    print('your stock = ', type(stock)==list)
    trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                            y=df_sub[df_sub['stock'] == stock]['value'],
                            mode='lines',
                            opacity=0.7,
                            name=stock,
                            textposition='bottom center'))  
    # STEP 3
    #traces = [trace]
    data = trace
    print('your data = ', data)
    #data = [val for val in trace]
    #data = [val for sublist in traces for val in sublist]
    # Define Figure
    # STEP 4
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=['#FF4F00', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 30)',
                  plot_bgcolor='rgba(0, 0, 0, 200)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub.index.min(), df_sub.index.max()]},
              ),

              }

    return figure

@app.callback(Output('change', 'figure'),
              [Input('stockselector', 'value')])
def update_change(selected_dropdown_value):
    ''' Draw traces of the feature 'change' based one the currently selected stocks '''
    trace = []
    df_sub = df
    # Draw and append traces for each stock
    stock = selected_dropdown_value
    if type(stock) == list:
    	stock = stock[0]
    print('your stock = ', type(stock)==list)
    #for stock in selected_dropdown_value:
    trace.append(go.Scatter(x=df_sub[df_sub['stock'] == stock].index,
                             y=df_sub[df_sub['stock'] == stock]['change'],
                             mode='lines',
                             opacity=0.7,
                             name=stock,
                             textposition='bottom center'))
    data = trace
    #data = [val for sublist in traces for val in sublist]
    # Define Figure
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=['#FF4F00', '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='plotly_dark',
                  paper_bgcolor='rgba(0, 0, 0, 30)',
                  plot_bgcolor='rgba(0, 0, 0, 200)',
                  margin={'t': 50},
                  height=250,
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Daily Change', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'showticklabels': False, 'range': [df_sub.index.min(), df_sub.index.max()]},
              ),
              }

    return figure

if __name__=="__main__":
	app.run_server(debug=True)