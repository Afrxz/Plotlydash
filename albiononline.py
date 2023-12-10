import requests
import pandas as pd
from dash import Dash,dcc,Output,Input
import dash_bootstrap_components as dbc
import plotly.express as px

PRICEURL = "https://west.albion-online-data.com/api/v2/stats/prices/"
ITEMS = 'T4_2H_KNUCKLES_HELL'
LOCATIONS = ['Lymhurst','Caerleon','Thetford',]
QUALITY = "0"

# Create an empty list to store DataFrames for each location
dfs = []

for loc in LOCATIONS:
    current_price_response = requests.get(
        PRICEURL + ITEMS + '.json?&locations=' + loc + '&qualities=' + QUALITY)

    if current_price_response.status_code == 200:
        market_prices = current_price_response.json()
        df = pd.DataFrame(market_prices, columns=['item_id', 'city','sell_price_min'])

        dfs.append(df)  # Append the DataFrame to the list

    else:
        print("Error in URL for location:", loc)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Print the merged DataFrame
print("Merged DataFrame:")
print(merged_df)

#data


#making components
app=Dash(__name__,external_stylesheets=[dbc.themes.VAPOR])
title=dcc.Markdown(children="App that shows " +ITEMS+" data")
mygraph=dcc.Graph(figure={})
dropdown=dcc.Dropdown(options=['Bar plot','Scatter plot'],value='Bar plot' #this is the value that displays when the app first opens
,clearable='false')

#making app layout
app.layout=dbc.Container([title,mygraph,dropdown])

#making callback

@app.callback(
    Output(mygraph,component_property='figure' ),
    Input(dropdown,component_property='value')

)

def update_graph(userinp):
    if userinp == 'Bar plot':
        fig = px.bar(data_frame=merged_df, x="city", y="sell_price_min", color="city")
    elif userinp == 'Scatter plot':  # Changed 'Scatter plot' to 'Line plot'
        fig = px.line(data_frame=merged_df, x="sell_price_min", y="city", color="item_id")

    return fig


if __name__=='__main__':
    app.run_server(port=8051)
