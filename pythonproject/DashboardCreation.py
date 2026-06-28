#Dashboard Creation

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# 1. Load the cleaned data
df = pd.read_csv('cleaned_sales_data.csv')

# 2. Initialize the Dash App
app = dash.Dash(__name__)

# 3. Define the App Layout
app.layout = html.Div(style={'fontFamily': 'Arial, sans-serif', 'padding': '20px'}, children=[
    
    html.H1("E-Commerce Sales Performance Dashboard", style={'textAlign': 'center', 'color': '#2C3E50'}),
    html.Hr(),
    
    # Filter Dropdown
    html.Div([
        html.Label("Select Product Category:", style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': cat, 'value': cat} for cat in df['Product_Category'].unique()],
            value=df['Product_Category'].unique()[0], # Default value
            clearable=False
        )
    ], style={'width': '30%', 'margin': '0 auto 30px auto'}),
    
    # Charts Layout (Side-by-Side)
    html.Div([
        html.Div([
            dcc.Graph(id='sales-trend-graph')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='quantity-pie-graph')
        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'})
    ])
])

# 4. Define Callbacks for Interactivity
@app.callback(
    [Output('sales-trend-graph', 'figure'),
     Output('quantity-pie-graph', 'figure')],
    [Input('category-dropdown', 'value')]
)
def update_graphs(selected_category):
    # Filter dataset based on dropdown selection
    filtered_df = df[df['Product_Category'] == selected_category]
    
    # Chart 1: Monthly Sales Trend (Line Chart)
    monthly_sales = filtered_df.groupby('Year_Month')['Sales'].sum().reset_index()
    fig_line = px.line(
        monthly_sales, 
        x='Year_Month', 
        y='Sales', 
        title=f'Monthly Sales Trend for {selected_category}',
        markers=True
    )
    fig_line.update_layout(transition_duration=500)
    
    # Chart 2: Top Selling Products (Bar Chart instead of Pie if data is dense)
    top_products = filtered_df.groupby('Product_Name')['Quantity'].sum().reset_index().nlargest(5, 'Quantity')
    fig_bar = px.bar(
        top_products, 
        x='Quantity', 
        y='Product_Name', 
        orientation='h',
        title=f'Top 5 Products by Quantity sold ({selected_category})',
        color='Quantity'
    )
    fig_bar.update_layout(yaxis={'categoryorder':'total ascending'}, transition_duration=500)
    
    return fig_line, fig_bar

# 5. Run the Server
if __name__ == '__main__':
    app.run_server(debug=True)