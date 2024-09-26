import sqlite3 as sq
import pandas as pd

# Création de la connexion à la base de données SQLite
conn = sq.connect("ClassicModel.sqlite")

# Définition des requêtes SQL
queries = {
    "Clients n'ayant jamais effectué une commande": """
        SELECT c.customerNumber, c.customerName, c.contactLastName, c.contactFirstName, c.country
        FROM Customers c
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        WHERE o.customerNumber IS NULL
        ORDER BY c.customerNumber;
    """,
    
    "Nombre de clients, commandes, et montant total par employé": """
        SELECT e.employeeNumber, e.lastName, e.firstName,
               COUNT(DISTINCT c.customerNumber) AS number_of_clients,
               COUNT(DISTINCT o.orderNumber) AS number_of_orders,
               SUM(od.quantityOrdered * od.priceEach) AS total_amount
        FROM Employees e
        LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        GROUP BY e.employeeNumber
        ORDER BY e.employeeNumber;
    """,
    
    "Nombre de clients, commandes, montant total, et clients d'un pays différent par bureau": """
        SELECT b.officeCode, 
               COUNT(DISTINCT c.customerNumber) AS number_of_clients,
               COUNT(DISTINCT o.orderNumber) AS number_of_orders,
               SUM(od.quantityOrdered * od.priceEach) AS total_amount,
               COUNT(DISTINCT CASE WHEN c.country != b.country THEN c.customerNumber END) AS clients_different_country
        FROM Offices b
        LEFT JOIN Employees e ON b.officeCode = e.officeCode
        LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        GROUP BY b.officeCode
        ORDER BY b.officeCode;
    """,
    
    "Nombre de commandes, quantité totale commandée, et nombre de clients différents par produit": """
        SELECT p.productCode, p.productName,
               COUNT(DISTINCT o.orderNumber) AS number_of_orders,
               SUM(od.quantityOrdered) AS total_quantity,
               COUNT(DISTINCT o.customerNumber) AS number_of_customers
        FROM Products p
        LEFT JOIN OrderDetails od ON p.productCode = od.productCode
        LEFT JOIN Orders o ON od.orderNumber = o.orderNumber
        GROUP BY p.productCode
        ORDER BY p.productCode;
    """,
    
    "Nombre de commandes, montant total des commandes, et montant total payé par pays du client": """
        SELECT c.country,
               COUNT(DISTINCT o.orderNumber) AS number_of_orders,
               SUM(od.quantityOrdered * od.priceEach) AS total_order_amount,
               SUM(p.amount) AS total_paid
        FROM Customers c
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        LEFT JOIN Payments p ON c.customerNumber = p.customerNumber
        GROUP BY c.country
        ORDER BY c.country;
    """,
    
    "Table de contingence du nombre de commandes entre ligne de produits et pays du client": """
        SELECT p.productLine, c.country,
               COUNT(DISTINCT o.orderNumber) AS number_of_orders
        FROM Customers c
        JOIN Orders o ON c.customerNumber = o.customerNumber
        JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        JOIN Products p ON od.productCode = p.productCode
        GROUP BY p.productLine, c.country
        ORDER BY p.productLine, c.country;
    """,
    
    "Table de contingence du montant total payé entre ligne de produits et pays du client": """
        SELECT p.productLine, c.country,
               SUM(od.quantityOrdered * od.priceEach) AS total_paid
        FROM Customers c
        JOIN Orders o ON c.customerNumber = o.customerNumber
        JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        JOIN Products p ON od.productCode = p.productCode
        GROUP BY p.productLine, c.country
        ORDER BY p.productLine, c.country;
    """,
    
    "Les 10 produits avec la marge moyenne la plus importante": """
        SELECT p.productCode, p.productName, 
               AVG(od.priceEach - p.buyPrice) AS avg_margin
        FROM Products p
        JOIN OrderDetails od ON p.productCode = od.productCode
        GROUP BY p.productCode
        ORDER BY avg_margin DESC
        LIMIT 10;
    """,
    
    "Produits vendus à perte avec nom et code du client": """
        SELECT p.productCode, p.productName, o.customerNumber
        FROM Products p
        JOIN OrderDetails od ON p.productCode = od.productCode
        JOIN Orders o ON od.orderNumber = o.orderNumber
        WHERE od.priceEach < p.buyPrice
        ORDER BY p.productCode, o.customerNumber;
    """,
    
    "Clients dont le montant total payé est inférieur au montant total des achats": """
        WITH TotalPurchases AS (
            SELECT o.customerNumber,
                   SUM(od.quantityOrdered * od.priceEach) AS total_purchase_amount
            FROM Orders o
            JOIN OrderDetails od ON o.orderNumber = od.orderNumber
            GROUP BY o.customerNumber
        ),
        TotalPayments AS (
            SELECT p.customerNumber,
                   SUM(p.amount) AS total_paid
            FROM Payments p
            GROUP BY p.customerNumber
        )
        SELECT tp.customerNumber,
               tp.total_purchase_amount,
               COALESCE(tpa.total_paid, 0) AS total_paid
        FROM TotalPurchases tp
        LEFT JOIN TotalPayments tpa ON tp.customerNumber = tpa.customerNumber
        WHERE COALESCE(tpa.total_paid, 0) < tp.total_purchase_amount
        ORDER BY tp.customerNumber;
    """
}

# Exécution de chaque requête et affichage des résultats
for title, query in queries.items():
    print(f"--- {title} ---")
    df = pd.read_sql_query(query, conn)
    print(df)
    print("\n")

# Fermeture de la connexion à la base de données
conn.close()
