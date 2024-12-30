<!-- Title -->
<div align="center">
    <h1>FinanceU: Spending Habit Tracker / Savings App</h1>
    <h2>
        A databased app to track spending habits and guide actions toward passive income.
    </h2>
    <a href='https://live-financeu-potential-savings.onrender.com/'>
        FinanceU: App
    </a>
    <p>
        <em>Navigate to my app to learn how compound interest on savings accounts or linear index funds can help you passively save towards your big goals.</em>
    </p>
    <div align='center'>
        <h3>
            <b>Technologies Used</b>
        </h3>
        <div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azuresqldatabase/azuresqldatabase-original.svg" alt="Azure SQL Database" width="200">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" alt="Python" width="200">
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg" alt="HTML" width="200"/>
            <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg" alt="CSS" width="200"/>
        </div>
    </div>
</div>

## Sections
- [Features](#features)
- [Development Process](#development-process)
- [Showcase](#showcase)

## Showcase
<div align=center>
    <div style="display:flex; align-items: flex-start; flex-direction: column">
        <img src="https://github.com/justmai1/financeU-potential-savings/blob/img/potential-savings.png">
        <img src="https://github.com/justmai1/financeU-potential-savings/blob/img/newplot%20(2).png">
        <img src="https://github.com/justmai1/financeU-potential-savings/blob/img/newplot%20(1).png">
        <img src="https://github.com/justmai1/financeU-potential-savings/blob/img/summaries.png">
    </div>
</div>


## Features
1. Potential Savings
    - Customizable user inputs for a **compounded interest calculator**
    - Plot made using *Plotly* library to compare savings with and without compound interest
    - Live changes to plot based on user inputs
    - Functions displaying a user's potential growth and total balance
    - Customizable user inputs for a **savings goal calculator**
    - Shows users the amount they need to invest monthly to reach their savings goals with a time interval
    - Comparison plot that demonstrates the impact of compound interest rates
2. Spending Habit Tracker
    - Spending inputs directly imported to SQL Database
    - Live changes to *Plotly* graphs that shows users the effect of their spendings and earnings
    - Live histogram for users to visualize the changes in their balance 
    - Live bar graph for users to visualize their daily spendings vs. daily earnings
    - Live updates to user summary statistics (using SQL queries) displayed
  
## Development Process
The app was created using the *Dash* library in Python to seamlessly connect *Plotly* graphs to the interface.

1. Potential Savings
    - Create functions retrieving total values (balance and growth) base off inputs
    - Create functions that returns a dictionary of savings by the year (for plot)
    - Develop mathematical formula to get the amount a user must invest a month to meet their goal
    - Using *Dash* library in Python (which contains CSS and HTML), to connect the inputs to stationary outputs and graph outputs
2. Spending Habit Tracker
    - Connect Python to SQL Database using *pyodbc* library
    - Connect insert statements within the query to inputs displayed on the client side
    - Writing queries to display neccessary information about the table inserted to retrieve necessary statistics
    - Use *Dash* to update plots and other summary statistics live as users submit their spendings and earnings

          
