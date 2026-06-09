SELECT 
    CustomerID,
    SUM(TotalAmount) AS LTV,
    COUNT(DISTINCT Invoice) AS Frequency,
    MIN(InvoiceDate) AS FirstPurchase,
    MAX(InvoiceDate) AS LastPurchase
FROM online_retail
WHERE CustomerID IS NOT NULL
  AND Quantity > 0
  AND TotalAmount > 0
GROUP BY CustomerID
ORDER BY LTV DESC;

SELECT 
    CustomerID,
    DATEDIFF(day, MAX(InvoiceDate), '2010-12-09') AS Recency,
    COUNT(DISTINCT Invoice) AS Frequency,
    SUM(TotalAmount) AS Monetary
FROM online_retail
WHERE CustomerID IS NOT NULL 
  AND Quantity > 0
GROUP BY CustomerID;

SELECT MAX(InvoiceDate) as maxdate
FROM online_retail

SELECT 
    SUM(TotalAmount) / COUNT(DISTINCT Invoice) AS AOV
FROM online_retail
WHERE Quantity > 0;

SELECT 
    DATEADD(MONTH, DATEDIFF(MONTH, 0, InvoiceDate), 0) AS month_start,
    SUM(TotalAmount) / COUNT(DISTINCT Invoice) AS AOV
FROM online_retail
WHERE Quantity > 0
GROUP BY DATEADD(MONTH, DATEDIFF(MONTH, 0, InvoiceDate), 0)
ORDER BY month_start;

SELECT 
    DATEADD(MONTH, DATEDIFF(MONTH, 0, InvoiceDate), 0) AS month_start,
    COUNT(DISTINCT CustomerID) AS unique_customers
FROM online_retail
WHERE CustomerID IS NOT NULL AND Quantity > 0
GROUP BY DATEADD(MONTH, DATEDIFF(MONTH, 0, InvoiceDate), 0)
ORDER BY month_start;


SELECT TOP 10
    StockCode,
    Description,
    SUM(Quantity) AS total_quantity,
    SUM(TotalAmount) AS total_revenue
FROM online_retail
WHERE Quantity > 0
GROUP BY StockCode, Description
ORDER BY total_revenue DESC;

WITH first_purchase AS (
    SELECT CustomerID, MIN(InvoiceDate) AS first_date
    FROM online_retail
    WHERE CustomerID IS NOT NULL AND Quantity > 0
    GROUP BY CustomerID
)
SELECT 
    COUNT(DISTINCT fp.CustomerID) AS total_customers,
    COUNT(DISTINCT r.CustomerID) AS repeat_customers,
    100.0 * COUNT(DISTINCT r.CustomerID) / COUNT(DISTINCT fp.CustomerID) AS repeat_rate
FROM first_purchase fp
LEFT JOIN online_retail r ON fp.CustomerID = r.CustomerID AND r.InvoiceDate > fp.first_date AND r.Quantity > 0;