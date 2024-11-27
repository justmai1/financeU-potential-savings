import plotly.graph_objects as go 

class PotentialSavings:
    '''
    '''
    def __init__(self, initial_deposit, add_payment_type, add_payment, annual_growth, time_saved):
        self.initial_deposit = initial_deposit
        self.add_payment_type = add_payment_type
        self.add_payment = add_payment
        self.annual_growth = annual_growth
        self.time_saved = time_saved

    def total_balance(self):
        '''
        '''
        current_value = 0
        if self.add_payment_type.strip().lower() not in {"monthly", "annually"}:
            return "Invalid Payment Type (must be monthly or annually)"
        else:
            if self.add_payment_type.strip().lower() == "monthly":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value = (current_value + self.add_payment * 12) * (1 + self.annual_growth)
            elif self.add_payment_type.strip().lower() == "annually":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value = (current_value + self.add_payment) * (1 + self.annual_growth)
        return round(current_value,2)
    
    def total_growth(self):
        '''
        '''
        current_value = 0
        if self.add_payment_type.strip().lower() not in {"monthly", "annually"}:
            return "Invalid Payment Type (must be monthly or annually)"
        else:
            if self.add_payment_type.strip().lower() == "monthly":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value = (current_value + self.add_payment * 12) * (1 + self.annual_growth)
                final_value = current_value - (self.initial_deposit + self.add_payment * 12 * self.time_saved)
            elif self.add_payment_type.strip().lower() == "annually":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value = (current_value + self.add_payment) * (1 + self.annual_growth)
                final_value = current_value - (self.initial_deposit + self.add_payment * self.time_saved)
        return round(final_value,2)
    
    def savings(self):
        '''
        '''
        savings_dict = dict()
        current_value = 0
        if self.add_payment_type.strip().lower() not in {"monthly", "annually"}:
            return "Invalid Payment Type (must be monthly or annually)"
        else:
            if self.add_payment_type.strip().lower() == "monthly":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        savings_dict[i] = self.initial_deposit
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value += self.add_payment*12
                        current_value *= (1 + self.annual_growth)
                        savings_dict[i] = round(current_value,2)
            elif self.add_payment_type.strip().lower() == "annually":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        savings_dict[i] = self.initial_deposit
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value += self.add_payment
                        current_value *= (1 + self.annual_growth)
                        savings_dict[i] = round(current_value,2)
            
        return savings_dict
    
    def stationary(self):
        '''
        '''
        savings_dict = dict()
        current_value = 0
        if self.add_payment_type.strip().lower() not in {"monthly", "annually"}:
            return "Invalid Payment Type (must be monthly or annually)"
        else:
            if self.add_payment_type.strip().lower() == "monthly":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        savings_dict[i] = self.initial_deposit
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value += self.add_payment*12
                        savings_dict[i] = round(current_value,2)
            elif self.add_payment_type.strip().lower() == "annually":
                for i in range(self.time_saved + 1):
                    if i == 0:
                        savings_dict[i] = self.initial_deposit
                        current_value += self.initial_deposit
                    elif i != 0:
                        current_value += self.add_payment
                        savings_dict[i] = round(current_value,2)
         
        return savings_dict
 
    def plot(self):
        '''
        '''
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = list(self.savings().keys()), y = list(self.savings().values()), 
                                mode = "lines",
                                line = dict(color= "#698F73"),
                                fill = "tozeroy", 
                                name = "Annual Investment"))
        fig.add_trace(go.Scatter(x = list(self.stationary().keys()), y = list(self.stationary().values()), 
                                mode = "lines",
                                line= dict(color= "#0A5A9C"), 
                                fill = "tozeroy",
                                name = "Annual Investment (No Return)"))
        fig.update_layout(
            title = "Savings Comparison",
            xaxis_title = "Years Saved",
            yaxis_title = "Growth Rate"
            )
        fig.show()

import pandas as pd
import yfinance as yf
from datetime import datetime
import numpy as np

# Define a list of indices
indices_tickers = [
    "^GSPC", "^DJI", "^IXIC", "^RUT", "^VIX", "^FTSE", "^N225", "^HSI",
    "^STOXX50E", "^FCHI", "^AXJO", "^BSESN", "^KS11", "^TWII",
    "^GSPTSE", "^BVSP", "^MXX",
]

def find_next_available_date(data, target_date):
    """
    Finds the next available date in the data after the target date.
    
    Parameters:
        data (pd.DataFrame): DataFrame with a datetime index.
        target_date (str): Target date in 'YYYY-MM-DD' format.
    
    Returns:
        str: The next available date in 'YYYY-MM-DD' format, or None if not found.
    """
    all_dates = sorted(data.index)
    for date in all_dates:
        if date >= target_date:
            return date
    return None  # No future date found

def ticker_data(indices_tickers):
    """
    Retrieves closing prices for specific indices over a 5-year period, 
    for the same day (or next available day) each year.
    
    Parameters:
        indices_tickers (list): List of index ticker symbols.
        
    Returns:
        pd.DataFrame: DataFrame containing index names, symbols, dates, and closing prices.
    """
    today = datetime.today()
    dates = [datetime(year, today.month, today.day).strftime("%Y-%m-%d") 
             for year in range(today.year - 5, today.year + 1)]
    
    # Initialize lists to hold results
    all_closing_prices = []
    date_list = []
    names = []
    
    for ticker in indices_tickers:
        names.append(yf.Ticker(ticker).info["longName"])
        try:
            # Fetch historical data for the entire range
            data = yf.download(ticker, start=f"{today.year - 5}-01-01", end=f"{today.year + 1}-01-01")
            data.index = data.index.strftime("%Y-%m-%d")
            
            # Retrieve ticker info
            ticker_info = yf.Ticker(ticker)
            closing_prices = []
            # Process each date
            for date in dates:
                if date in data.index:
                    actual_date = date
                else:
                    # Find the next available date
                    actual_date = find_next_available_date(data, date)
                
                if actual_date:
                    closing_prices.append(data.loc[actual_date, "Close"])
                    date_list.append(actual_date)
                else:
                    # Append None if no next available date is found
                    closing_prices.append(None)
            all_closing_prices.append(closing_prices)
                    
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    # Calculate average ratio for each list of closing prices
    avg_ratios = []
    
    for closing_prices in all_closing_prices:
        if None in closing_prices:  # Skip if there's a None value in the sublist
            avg_ratios.append(None)
            continue
        
        ratios = []
        for i in range(1, len(closing_prices)):
            # Calculate the ratio of consecutive elements
            ratio = closing_prices[i] / closing_prices[i - 1]
            ratios.append(ratio)
        
        # Calculate the average of the ratios
        avg_ratio = np.mean(ratios) if ratios else None
        avg_ratios.append(avg_ratio-1)
    
    # Create DataFrame
    return pd.DataFrame({
        "Index Ticker": indices_tickers,
        "Name": names,
        "Average Ratio": avg_ratios
    })

# Get the average ratios for each index

df = ticker_data(indices_tickers)

from dash import Dash, dcc, html, Input, Output, callback, dash_table

# Assuming the PotentialSavings class is already defined here
# If it's in another file, you can import it.

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={'backgroundColor': "#F8F1E1", 'height': '200vh', 'padding': '20px', 'margin': '0'},
    children=[
        html.H1("FinanceU: Potential Savings", style={'textAlign': 'center', 'color': '#004225'}),
        html.Div([
            # First Div (inputs)
            html.Div([
                html.Label("Initial Deposit ($):", style={'color':'#698F73', 'fontSize':'20px'}),
                dcc.Input(id='initial-deposit', type='number', min=0, placeholder="e.g. 500.00", style={'marginRight': '10px'}),
                html.Br(),
                html.Label("Add Payment Type: ", style={'color':'#698F73', 'fontSize':'20px'}),
                dcc.Input(id='add-payment-type', type='text', placeholder="e.g. monthly or annually", style={'marginRight': '10px'}),
                html.Br(),
                html.Label("Additional Payment ($):", style={'color':'#698F73', 'fontSize':'20px'}),
                dcc.Input(id='add-payment', type='number', min=0, placeholder="e.g. 20.00", style={'marginRight': '10px'}),
                html.Br(),
                html.Label("Annual Growth Rate:", style={'color':'#698F73', 'fontSize':'20px'}),
                dcc.Input(id='annual-growth', type='number', placeholder="e.g. 0.05 for 5%", min=0, max=1, step="any", style={'marginRight': '10px'}),
                html.Br(),
                html.Label("Time Saved (years):", style={'color':'#698F73', 'fontSize':'20px'}),
                dcc.Input(id='time-saved', type='number', placeholder="e.g. 30", step=1, style={'marginRight': '10px'}),
            ], style={'display': 'flex', 'flexDirection': 'column', 'width': '300px', 'marginLeft':'400px', 'marginRight':'50px'}),  # Input section

            # Second Div (Results)
            html.Div([
                html.H3("Total Balance: ", style={'fontSize':'25px'}),
                html.Div(id='total-balance', style={'fontSize': '25px', 'fontWeight': 'bold'}),
                
                html.H3("Total Growth: ", style={'fontSize':'25px'}),
                html.Div(id='total-growth', style={'fontSize': '25px', 'fontWeight': 'bold'}),
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginLeft': '50px'}),  # Results section, with margin
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}),

        
        html.Br(),
        
        dcc.Graph(id='savings-graph'),

        html.Br(),
        html.Br(),

        dash_table.DataTable(
            id='table',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            style_cell={'textAlign': 'center','backgroundColor':'#E1EAD5'},
            style_header={'fontWeight':'bold','backgroundColor':'#698F73'}
        )
    ]
)

@app.callback(
    [Output('total-balance', 'children'),
     Output('total-growth', 'children'),
     Output('savings-graph', 'figure')],
    [Input('initial-deposit', 'value'),
     Input('add-payment-type', 'value'),
     Input('add-payment', 'value'),
     Input('annual-growth', 'value'),
     Input('time-saved', 'value')]
)
def update_results(initial_deposit, add_payment_type, add_payment, annual_growth, time_saved):
    # Create an instance of PotentialSavings
    ps = PotentialSavings(
        initial_deposit=float(initial_deposit),
        add_payment_type=add_payment_type,
        add_payment=float(add_payment),
        annual_growth=annual_growth,
        time_saved=int(time_saved)
    )

    # Calculate results
    total_balance = ps.total_balance()
    total_growth = ps.total_growth()

    # Plot data
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(ps.savings().keys()), y=list(ps.savings().values()),
                            mode="lines", line=dict(color="#698F73"), fill="tozeroy", name="Annual Investment"))
    fig.add_trace(go.Scatter(x=list(ps.stationary().keys()), y=list(ps.stationary().values()),
                            mode="lines", line=dict(color="#0A5A9C"), fill="tozeroy", name="Annual Investment (No Return)"))
    fig.update_layout(title="Savings Comparison", xaxis_title="Years Saved", yaxis_title="Value in Dollars ($)",
                      title_font_color="#22333B", paper_bgcolor="#E1EAD5", plot_bgcolor="#E1EAD5")
    
    return f"${total_balance}", f"${total_growth}", fig

if __name__ == '__main__':
    app.run_server()
