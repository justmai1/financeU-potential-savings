import plotly.graph_objects as go 
import math

class PotentialSavings:
    def __init__(self, initial_deposit, add_payment_type, add_payment, annual_growth, time_saved):
        '''
        Class returns information on total balance, total growth, how much
        someone is saving annually and how much you are putting in annually

        Parameters: initial_deposit - how much you put in at the start
        add_payment_type - monthly or yearly, what type of additional payments
        are you making?
        add_payment - how much additional are you depositing
        annual_growth - how much your money is projected to grow
        time_saved - how much time are you planning to leave your money in
        '''
        self.initial_deposit = initial_deposit
        self.add_payment_type = add_payment_type
        self.add_payment = add_payment
        self.annual_growth = annual_growth/100
        self.time_saved = time_saved


    def total_balance(self):
        '''
        Returns the total balance after x amount of years
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
        Returns how much your money grew, subtracting the
        total balance by how much you put in
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
        Returns a dictionary with your total balance after every year
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
        Returns how much total money you put in after every year
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
        Returns a plotly plot that shows the difference between
        your total earnings and the money that is put in by year.
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

def goal_savings(years, goal_balance, growth_rate):
    return round((goal_balance * ((growth_rate/100) / 12))/(math.pow(1 + ((growth_rate/100) / 12), years*12) - 1),2)

def plot_goal_savings(years, goal_balance, growth_rate):
    monthly_contribution = (goal_balance * ((growth_rate/100) / 12))/(math.pow(1 + ((growth_rate/100) / 12), years*12) - 1)
    current = 0
    d_growth = dict()
    d_growth[0] = goal_balance
    for i in range(years):
        current += monthly_contribution * 12
        current = current * (1 + growth_rate/100)
        d_growth[i+1] = max(0, goal_balance - current)
    
    current_no = 0
    d_no_growth = dict()
    d_no_growth[0] = goal_balance
    for i in range(years):
        current_no += monthly_contribution * 12
        d_no_growth[i+1] = max(0, goal_balance - current_no)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(d_growth.keys()), y=list(d_growth.values()),
                             mode="lines", line=dict(color="#698F73"), name='Savings (With Passive Growth)'))
    fig.add_trace(go.Scatter(x=list(d_no_growth.keys()), y=list(d_no_growth.values()),
                            mode="lines", name='Savings (Without Passive Growth)'))
    fig.update_layout(
        hovermode='x unified',
        title="Savings Progress Over Time",
        xaxis_title="Years",
        yaxis_title="Remaining Balance",
        title_font_color="#22333B",
        paper_bgcolor="#E1EAD5",
        plot_bgcolor="#E1EAD5"
    )
    return fig

'''
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
'''
    
from dash import Dash, dcc, html, Input, Output, callback, dash_table

# Assuming the PotentialSavings class is already defined here
# If it's in another file, you can import it.

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    style={'backgroundColor': "#F8F1E1", 'height': '210vh', 'padding': '20px', 'margin': '0'},
    children=[
        html.H1("FinanceU: Potential Savings", style={'marginLeft':'10px', 'color': '#004225'}),
        html.H2("Check out the potential of your money over time based off expected annual returns of your indexes or savings account", 
                style={'marginLeft':'10px', 'color': '#004225', 'fontSize':'20px', 'marginBottom':'15px'}),
        html.Hr(style={'borderWidth': '2px', 'borderColor': '#004225', 'width': '100%', 'margin': '0px auto'}),
        html.Div([
            html.Div([
                html.H3("Savings Comp", style = {'color': '#004225', 'fontSize':'30px', 'marginBottom':'0px'}),
                html.H4("(Calculate your potential balance with consistent savings and growth).",
                        style = {'color': '#004225', 'fontSize':'15px', 'marginBottom':'15px'}),
                html.Label("Initial Deposit ($):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='initial-deposit', type='number', min=0, value = 500.00, style={'width': '210px', 
                                                                                                        'height': '40px', 
                                                                                                        'fontSize': '20px',
                                                                                                        'border-radius': '5px', 
                                                                                                        'marginBottom': '10px'}),
                html.Br(),
                html.Label("Add Payment Type: ", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Dropdown(['Monthly', 'Annually'], id='add-payment-type', value='Monthly', style={'width': '210px', 
                                                                                                                            'height': '40px', 
                                                                                                                            'fontSize': '20px',
                                                                                                                            'border-radius': '5px', 
                                                                                                                            'marginBottom': '10px'}),
                html.Br(),
                html.Label("Additional Payment ($):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='add-payment', type='number', min=0, value= 20.00 , style={'width': '210px', 
                                                                                                   'height': '40px', 
                                                                                                   'fontSize': '20px',
                                                                                                   'border-radius': '5px', 
                                                                                                   'marginBottom': '10px'}),
                html.Br(),
                html.Label("Annual Growth Rate:", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='annual-growth', type='number', value = 5, min=0, max=100, step="any", style={'width': '210px', 
                                                                                                                              'height': '40px', 
                                                                                                                              'fontSize': '20px',
                                                                                                                              'border-radius': '5px',
                                                                                                                              'marginBottom': '10px'}),
                html.Br(),
                html.Label("Time Saved (years):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='time-saved', type='number', value = 45, step=1, style={'width': '210px', 
                                                                                                'height': '40px', 
                                                                                                'fontSize': '20px',
                                                                                                'border-radius': '5px', 
                                                                                                'marginBottom': '10px'}),
            ], style={'display': 'flex', 'flexDirection': 'column', 'width': '300px', 'marginLeft':'10px', 'marginTop': '120px'}),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3("Potential Balance: ", style={'fontSize':'25px', 'color': '#004225'}),
                        html.Div(id='total-balance', style={'fontSize': '25px', 'fontWeight': 'bold', 'color': '#004225',
                                    'border': '2px black solid', 'padding': '5px', 'minWidth': '100px', 'textAlign': 'center'})
                    ], style={'display':'flex', 'flexDirection': 'column'}),

                    html.Div([
                        html.H3("Potential Growth: ", style={'fontSize':'25px', 'color': '#004225'}),
                        html.Div(id='total-growth', style={'fontSize': '25px', 'fontWeight': 'bold', 'color': '#004225',
                                    'border': '2px black solid', 'padding': '5px', 'minWidth': '100px', 'textAlign': 'center'}),
                    ], style={'display':'flex', 'flexDirection': 'column'})
                ], style={'display':'flex', 'flexDirection': 'row', 'marginLeft': '150px', 'gap': '290px'}),

                html.Div([
                    dcc.Graph(id='savings-graph',
                              style={'marginLeft': '10px', 'width': '1100px', 'height': '630px', 'marginTop': '20px'})
                ])
            ], style={'display': 'flex', 'flexDirection':'column'}),
        ], style={'display': 'flex', 'flexDirection': 'row', 'marginBottom':'20px'}),

        html.Div([
            html.Div([
                html.H3("Savings Goal", style = {'color': '#004225', 'fontSize':'30px', 'marginBottom':'0px'}),
                html.H4("(Calculate your monthly deposits to achieve your financial goals.)",
                        style = {'color': '#004225', 'fontSize':'15px', 'marginBottom':'15px'}),
                html.Label("Savings Goal ($):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='savings-goal', type='number', min=0, value= 10000.00 , style={'width': '210px', 
                                                                                                   'height': '40px', 
                                                                                                   'fontSize': '20px',
                                                                                                   'border-radius': '5px', 
                                                                                                   'marginBottom': '10px'}),
                html.Br(),
                html.Label("Goal Time (Years):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='goal-time-saved', type='number', value = 15, step=1, style={'width': '210px', 
                                                                                          'height': '40px',
                                                                                          'fontSize': '20px',
                                                                                          'border-radius': '5px',
                                                                                          'marginBottom': '10px'}),
                html.Br(),
                html.Label("Expected Growth Rate (%):", style={'color':'#698F73', 'fontSize':'25px'}),
                dcc.Input(id='potential-growth-rate', type='number', value = 8, min=0, max=100, step="any", style={'width': '210px', 
                                                                                                                              'height': '40px', 
                                                                                                                              'fontSize': '20px',
                                                                                                                              'border-radius': '5px',
                                                                                                                              'marginBottom': '10px'})
            ], style={'display': 'flex', 'flexDirection': 'column', 'width': '300px', 'marginLeft':'10px', 'marginTop': '120px'}),

            html.Div([
                html.Div([
                    html.H3("Required Monthly Deposit ($):", 
                            style={'fontSize': '25px', 'color': '#004225', 'marginRight': '10px'}),
                    html.Div(id='monthly-deposit', 
                            style={'fontSize': '25px', 'fontWeight': 'bold', 'color': '#004225',
                                    'border': '2px black solid', 'padding': '5px', 'minWidth': '100px', 'textAlign': 'center'})
                ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'center', 'marginTop': '15px'}),
                dcc.Graph(id='savings-graph-2',
                            style={'marginLeft': '10px', 'width': '1100px', 'height': '500px', 'marginTop': '5px'})
            ], style={'display': 'flex', 'flexDirection':'column'})
        ], style={'display': 'flex', 'flexDirection': 'row'})
    ]
)

@app.callback(
    [Output('total-balance', 'children'),
     Output('total-growth', 'children'),
     Output('savings-graph', 'figure'),
     Output('monthly-deposit','children'),
     Output('savings-graph-2','figure')],
    [Input('initial-deposit', 'value'),
     Input('add-payment-type', 'value'),
     Input('add-payment', 'value'),
     Input('annual-growth', 'value'),
     Input('time-saved', 'value'),
     Input('goal-time-saved','value'),
     Input('savings-goal','value'),
     Input('potential-growth-rate','value')]
)
def update_results(initial_deposit, add_payment_type, add_payment, annual_growth, time_saved, goal_time, savings_goal, potential_growth_rate):
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
    fig.update_layout(hovermode = "x unified", title="Savings Comparison", xaxis_title="Years Saved", yaxis_title="Value in Dollars ($)",
                      title_font_color="#22333B", paper_bgcolor="#E1EAD5", plot_bgcolor="#E1EAD5")
    
    # Calculate required monthly deposit for goal savings
    monthly_deposit = goal_savings(goal_time, savings_goal, potential_growth_rate)

    # Plot savings goal progress
    fig2 = plot_goal_savings(goal_time, savings_goal, potential_growth_rate)

    return f"${total_balance:,.2f}", f"${total_growth:,.2f}", fig, monthly_deposit, fig2

if __name__ == '__main__':
    app.run_server()

            # Second Div (Results)
'''
            html.Div([
                html.H3("Total Balance: ", style={'fontSize':'25px'}),
                html.Div(id='total-balance', style={'fontSize': '25px', 'fontWeight': 'bold'}),
                
                html.H3("Total Growth: ", style={'fontSize':'25px'}),
                html.Div(id='total-growth', style={'fontSize': '25px', 'fontWeight': 'bold'}),
            ], style={'display': 'flex', 'flexDirection': 'column', 'marginLeft': '50px'}),  # Results section, with margin
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}),

        
        html.Br(),
        
        dcc.Graph(id='savings-graph')
'''
