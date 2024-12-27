import pyodbc
import pandas as pd
import plotly.graph_objects as go

from datetime import date
from dash import Dash, dcc, html, Input, Output, callback, dash_table, State, no_update

app = Dash(__name__)



def get_connection():
    # Database connection string (avoid hardcoding sensitive credentials in production)
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=justmai.database.windows.net;"
        "DATABASE=financial-tracker;"
        "UID=justinmai1;"
        "PWD=*****;"
    )
    return pyodbc.connect(conn_str)


def add_transaction(date, type, amount, category, description):
    # Insert a new transaction into the database
    conn = get_connection()
    cursor = conn.cursor()
    query = '''
        INSERT INTO test_finances ([Date], [Type], Amount, Category, [Description])
        VALUES (?, ?, ?, ?, ?)
    '''
    try:
        cursor.execute(query, (date, type, amount, category, description))
        conn.commit()
        print("Transaction added successfully.")
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()


def table():
    # Fetch all records from the database and load them into a DataFrame
    conn = get_connection()
    query = 'SELECT * FROM test_finances'
    try:
        df = pd.read_sql(query, conn)  # Pass the raw query and connection to `pd.read_sql`
        return df
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def balance():
    conn = get_connection()
    query = '''
    WITH new_table as (
        SELECT [Date], 
            CASE 
                WHEN Type = 'spent' THEN -Amount 
                ELSE Amount 
            END AS Adj_amount, 
        Category, 
        [Description]
    FROM test_finances
    )
    SELECT ROUND(SUM(adj_amount),2) as balance FROM new_table
    '''
    try:
        value = pd.read_sql(query, conn).iloc[0][0]
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def total_spendings():
    conn = get_connection()
    query = '''
    SELECT ROUND(SUM(Amount),2) as total_spendings 
    FROM test_finances
    WHERE Type = 'spent'
    '''
    try:
        value = pd.read_sql(query, conn).iloc[0][0]
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def total_earnings():
    conn = get_connection()
    query = '''
    SELECT ROUND(SUM(Amount),2) as total_earnings 
    FROM test_finances
    WHERE Type = 'earned'
    '''
    try:
        value = pd.read_sql(query, conn).iloc[0][0]
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def most_spent_cat():
    conn = get_connection()
    query = '''
    WITH cat AS (
        SELECT Category, COUNT(*) AS count
        FROM test_finances
        WHERE Type = 'spent'
        GROUP BY Category
    ),
    ranking AS (
        SELECT *, RANK() OVER (ORDER BY count DESC) AS rank
        FROM cat
    )
    SELECT Category
    FROM ranking
    WHERE rank = 1;
    '''
    try:
        df = pd.read_sql(query, conn)
        if df.empty:
            return "No spendings recorded"
        return df.iloc[0]['Category']
    except Exception as e:
        print(f"Error: {e}")
        return "Error retrieving data"
    finally:
        conn.close()

def plot_values():
    conn = get_connection()
    query = '''
    WITH new_table as (
        SELECT [Date], 
        CASE 
            WHEN Type = 'spent' THEN -Amount 
            ELSE Amount 
        END AS Adj_amount, 
        Category, 
        [Description]
        FROM test_finances
    ),
        sum_table as (
        SELECT Date, SUM(Adj_amount) as sum_amount FROM new_table
        GROUP BY [Date]
    )
    SELECT Date, SUM(sum_amount) OVER (ORDER BY Date) as running_total
    FROM sum_table
    '''
    try:
        value = pd.read_sql(query, conn)
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def plot_balance():
    fig = go.Figure()
    fig.add_trace(go.Bar(x=plot_values()['Date'],
                         y=plot_values()['running_total'],
                         marker=dict(color="#004225")))
    fig.update_layout(
        xaxis=dict(rangeslider=dict(visible=True,
                                    bgcolor="#698F73")),
        title= "Total Balance",
        xaxis_title= "Date",
        yaxis_title= "Amount in Dollars ($)",
        xaxis_tickangle = -45,
        title_font_color="#22333B", 
        paper_bgcolor="#E1EAD5", 
        plot_bgcolor="#E1EAD5"
    )
    return fig

def daily_earnings():
    conn = get_connection()
    query = '''
    SELECT Date, Category, SUM(Amount) as sum FROM test_finances
    WHERE Type = 'earned'
    AND Category != 'Bank Balance'
    GROUP BY Date, Category
    ORDER BY Date
    '''
    try:
        value = pd.read_sql(query, conn)
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

def daily_spendings():
    conn = get_connection()
    query = '''
    SELECT Date, Category, SUM(Amount) as sum FROM test_finances
    WHERE Type = 'spent'
    GROUP BY Date, Category
    ORDER BY Date
    '''
    try:
        value = pd.read_sql(query, conn)
        return value
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()


def plot_earnings_vs_spendings():
    cat_list_earnings = []
    for cat in daily_earnings()['Category']:
        cat_list_earnings.append(cat)

    cat_list_spendings = []
    for cat in daily_spendings()['Category']:
        cat_list_spendings.append(cat)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=daily_earnings()['Date'],
                        y=daily_earnings()['sum'],
                        name='Earnings',
                        hovertext=cat_list_earnings,
                        marker=dict(color='green')))
    fig.add_trace(go.Bar(x=daily_spendings()['Date'],
                        y=daily_spendings()['sum'],
                        name='Spendings',
                        hovertext=cat_list_spendings,
                        marker=dict(color='red')))
    fig.update_layout(
        title = "Daily Earnings vs. Spendings",
        xaxis_title = "Date",
        yaxis_title = "Amount in Dollars ($)",
        xaxis=dict(rangeslider=dict(visible=True,
                                    bgcolor="#698F73")),
        xaxis_tickangle = -45,
        barmode = 'group',
        title_font_color="#22333B",
        paper_bgcolor="#E1EAD5",
        plot_bgcolor="#E1EAD0"
    )
    return fig

app.layout = html.Div(style={'backgroundColor': "#F8F1E1", 'height': '200vh', 'padding': '20px', 'margin': '0'},
    children=[
        html.H1("FinanceU: Cash Flow", style={'textAlign': 'center', 'color': '#004225'}),
        html.H2("Visualize your spending habits. See where your cash is flowing.", 
                style={'textAlign': 'center', 'color': '#004225', 'fontSize':'20px', 'marginBottom':'15px'}),
        # Parent box
        html.Div([
            html.Div([
                html.Label("Date: ", style={'color':'#698F73', 'fontSize':'25px', 'marginBottom': '5px'}),
                dcc.DatePickerSingle(
                    id='date',
                    max_date_allowed=date.today(),
                    date=date.today(),
                    clearable=True,
                    with_portal=True,
                    style = {'border-radius': '10px', 'marginBottom': '10px'}
                ),
                html.Br(),
                html.Label("Type: ", style={'color':'#698F73', 'fontSize':'25px', 'marginBottom': '5px'}),
                dcc.Dropdown(
                    ["Spent", "Earned"],
                    id='transaction_type',
                    placeholder="Choose Your Transaction Type",
                    style = {'width': '280px', 'height': '40px', 'fontSize': '20px','border-radius': '5px',
                            'marginBottom': '15px'}
                ),
                html.Br(),
                html.Label("Amount ", style={'color':'#698F73', 'fontSize':'25px', 'marginBottom': '5px'}),
                dcc.Input(
                    id='amount',
                    placeholder='Input Transaction Amount',
                    type='number',
                    min=0,
                    style = {'width': '270px', 'height': '40px', 'fontSize': '20px','border-radius': '5px',
                            'marginBottom': '15px'}
                ),
                html.Br(),
                html.Label("Category: ", style={'color':'#698F73', 'fontSize':'25px', 'marginBottom': '5px'}),
                dcc.Input(
                    id='category',
                    placeholder='Input Transaction Category',
                    type='text',
                    style = {'width': '270px', 'height': '40px', 'fontSize': '20px','border-radius': '5px',
                            'marginBottom': '15px'}
                ),
                html.Br(),
                html.Label("Activity Description: ", style={'color':'#698F73', 'fontSize':'25px', 'marginBottom': '5px'}),
                dcc.Input(
                    id='description',
                    placeholder='Brief Transaction Description',
                    type='text',
                    maxLength=50,
                    style = {'width': '270px', 'height': '40px', 'fontSize': '20px','border-radius': '5px', 'marginBottom': '15px'}
                ),
                html.Br(),
                html.Button(
                    id='submit_transaction',
                    children='Submit Transaction',
                    style = {'width': '270px', 'height': '40px', 'fontSize': '20px','border-radius': '5px',
                            'marginBottom': '15px','cursor':'pointer'}
                    
                ),
                html.Div(id='submission_output', n_clicks=0, style={'fontSize':'20px', 'color': '#004225'})
            ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'flex-start', 
                    'marginLeft': '40px', 'marginTop': '25px'}),

            html.Div([
                dcc.Graph(
                    id='trend_graph',
                    style={'marginLeft': '50px', 'width': '1000px', 'height': '500px'}
                ),
                dcc.Graph(
                    id='spending_graph',
                    style={'marginLeft': '50px', 'width': '1000px', 'height': '500px', 'marginTop': '20px'}    
                )
            ], style={'display': 'flex', 'flexDirection': 'column'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start'}),
        
        html.Div([
            html.Div([
                html.H3("Current Balance: ", style={'fontSize':'20px', 'color': '#004225'}),
                html.Div(id='balance', style={'fontSize':'40px', 'border': '2px black solid', 'color': '#004225'})
        ], style={'display':'flex', 'flexDirection':'column', 'alignItems':'flex-start'}),

            html.Div([
                html.H3('Total Spendings: ', style={'marginLeft': '80px', 'fontSize':'20px', 'color': '#004225'}),
                html.Div(id='total-spendings', style={'fontSize':'40px',
                                                    'marginLeft':'80px',
                                                    'border': '2px black solid', 'color': '#004225'})
            ], style={'display':'flex', 'flexDirection':'column', 'alignItems':'flex-start'}),

            html.Div([
                html.H3('Total Earnings: ', style={'marginLeft': '80px', 'fontSize':'20px', 'color': '#004225'}),
                html.Div(id='total-earnings', style={'fontSize':'40px',
                                                    'marginLeft':'80px',
                                                    'border': '2px black solid', 'color': '#004225'})
            ], style={'display':'flex', 'flexDirection':'column', 'alignItems':'flex-start'}),

            html.Div([
                html.H3('Most Spent Catergory: ', style={'marginLeft': '80px', 'fontSize':'20px', 'color': '#004225'}),
                html.Div(id='most-spent', style={'fontSize':'40px',
                                                    'marginLeft':'80px',
                                                    'border': '2px black solid', 'color': '#004225'})
            ], style={'display':'flex', 'flexDirection':'column', 'alignItems':'flex-start'})
        ], style={'display': 'flex', 'flexDirection': 'row', 'alignItems': 'flex-start',
                    'alignItems': 'center', 'justifyContent':'center'})
    ]
)

@app.callback(
    [Output('trend_graph', 'figure'),
     Output('spending_graph', 'figure'),
     Output('balance', 'children'),
     Output('total-spendings', 'children'),
     Output('total-earnings', 'children'),
     Output('most-spent', 'children'),
     Output('submission_output', 'children'),  # Update the output message
     Output('date', 'date'),                   # Clear the date input
     Output('transaction_type', 'value'),     # Clear the dropdown
     Output('amount', 'value'),               # Clear the amount input
     Output('category', 'value'),             # Clear the category input
     Output('description', 'value')],         # Clear the description input
    [Input('submit_transaction', 'n_clicks')],  # Button click triggers the callback
    [State('date', 'date'),                    # Capture the value of other fields
     State('transaction_type', 'value'),
     State('amount', 'value'),
     State('category', 'value'),
     State('description', 'value')]
)
def update_submission_output(n_clicks, date, transaction_type, amount, category, description):
    if n_clicks and n_clicks > 0:
        if all([date, transaction_type, amount, category, description]):
            # Add the transaction to the database
            add_transaction(date, transaction_type, amount, category, description)
            message = f"Transaction submitted: You {transaction_type} ${amount} on {date}"

            # Generate the updated graphes
            fig = plot_balance()
            fig2 = plot_earnings_vs_spendings()
            

            # Clear the input fields
            return fig, fig2, message, None, None, None, None, None
    # Initial state before any submission
    fig = plot_balance()  # Initial plot
    fig2 = plot_earnings_vs_spendings()
    return fig, fig2, f'${balance()}', f'${total_spendings()}', f'${total_earnings()}', most_spent_cat(),"Fill out all fields before submitting", date, None, None, None, None


if __name__ == '__main__':
    app.run_server()