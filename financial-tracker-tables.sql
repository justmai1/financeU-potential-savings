CREATE TABLE Accounts(
    UserID int IDENTITY(1,1) PRIMARY KEY,
    Fname nvarchar(50),
    Lname nvarchar(50),
    UserName nvarchar(100) UNIQUE,
    UserPassword nvarchar(100)
);

CREATE TABLE FinanceInputs (
    UserID int NOT NULL,
    TransactionID int,
    Date date NOT NULL,
    Type_ nvarchar(10) NOT NULL,
    ActivityDescription nvarchar(100) NOT NULL,
    Amount float NOT NULL,
    ReturnRate float,
    PRIMARY KEY(UserID, TransactionID),
    FOREIGN KEY(UserID) REFERENCES Users(UserID) -- Define the foreign key
);

SELECT * FROM dbo.Users
SELECT * FROM dbo.UserFinanceInputs

drop table test_finances

CREATE TABLE test_finances (
    TransactionID INT IDENTITY(1,1) PRIMARY KEY,
    Date DATE,
    [Type] NVARCHAR(10),
    Amount FLOAT,
    Category NVARCHAR(50),
    [Description] NVARCHAR(75)
)

-- Balance

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
SELECT SUM(adj_amount) as balance FROM new_table

-- Total Spendings
SELECT SUM(Amount) as total_spendings FROM test_finances
WHERE Type = 'spent'

-- Total Earnings
SELECT SUM(Amount) as total_earnings FROM test_finances
WHERE Type = 'earned'

-- Most Spent Category
WITH cat as(
    SELECT Category, COUNT(*) as count FROM test_finances
    WHERE Type = 'spent'
    GROUP BY Category
), ranking as(
    SELECT *, RANK() OVER (ORDER BY count DESC) as rank
    FROM cat
)
SELECT Category 
FROM ranking
WHERE rank = 1

-- Plot values, trace 1
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

-- Plot values, earned trace
SELECT Date, Category, SUM(Amount) as sum FROM test_finances
WHERE Type = 'earned'
GROUP BY Date, Category
ORDER BY Date

-- Plot values, spent trace
SELECT Date, Category, SUM(Amount) as sum FROM test_finances
WHERE Type = 'spent'
GROUP BY Date, Category
ORDER BY Date

SELECT * FROM test_finances

