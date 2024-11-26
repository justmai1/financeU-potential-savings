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



from dash import Dash, dcc, html, Input, Output, callback

# Assuming the PotentialSavings class is already defined here
# If it's in another file, you can import it.

app = Dash(__name__)

app.layout = html.Div(
    style={'backgroundColor': "#F8F1E1", 'height': '150vh', 'padding': '20px', 'margin': '0'},
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
        
        dcc.Graph(id='savings-graph')
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
