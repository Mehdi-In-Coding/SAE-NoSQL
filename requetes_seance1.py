# Importation des modules nécessaires
import sqlite3  # Pour interagir avec une base de données SQLite
import pandas as pd  # Pour la manipulation et l'analyse de données

# Connexion à la base de données SQLite
conn = sqlite3.connect("ClassicModel.sqlite") # WARNING aux importations au format ".data" supprimer et remettre à jour

# Dictionnaire contenant 10 requêtes SQL différentes
requetes_sql = {
    "Clients sans commandes": """
        SELECT c.customerNumber, c.customerName, c.contactLastName, c.contactFirstName, c.country
        FROM Customers c
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        WHERE o.customerNumber IS NULL
        ORDER BY c.customerNumber;
    """,

    "Performances des employés": """
        SELECT e.employeeNumber, e.lastName, e.firstName,
               COUNT(DISTINCT c.customerNumber) AS nb_clients,
               COUNT(DISTINCT o.orderNumber) AS nb_commandes,
               SUM(od.quantityOrdered * od.priceEach) AS total_ventes
        FROM Employees e
        LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        GROUP BY e.employeeNumber
        ORDER BY e.employeeNumber;
    """,

    "Analyse par bureau": """
        SELECT b.officeCode, 
               COUNT(DISTINCT c.customerNumber) AS nb_clients,
               COUNT(DISTINCT o.orderNumber) AS nb_commandes,
               SUM(od.quantityOrdered * od.priceEach) AS montant_total,
               COUNT(DISTINCT CASE WHEN c.country != b.country THEN c.customerNumber END) AS clients_internationaux
        FROM Offices b
        LEFT JOIN Employees e ON b.officeCode = e.officeCode
        LEFT JOIN Customers c ON e.employeeNumber = c.salesRepEmployeeNumber
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        GROUP BY b.officeCode
        ORDER BY b.officeCode;
    """,

    "Commandes par produit": """
        SELECT p.productCode, p.productName,
               COUNT(DISTINCT o.orderNumber) AS nb_commandes,
               SUM(od.quantityOrdered) AS quantité_totale,
               COUNT(DISTINCT o.customerNumber) AS nb_clients
        FROM Products p
        LEFT JOIN OrderDetails od ON p.productCode = od.productCode
        LEFT JOIN Orders o ON od.orderNumber = o.orderNumber
        GROUP BY p.productCode
        ORDER BY p.productCode;
    """,

    "Ventes par pays": """
        SELECT c.country,
               COUNT(DISTINCT o.orderNumber) AS nb_commandes,
               SUM(od.quantityOrdered * od.priceEach) AS montant_total_ventes,
               SUM(p.amount) AS total_paiements
        FROM Customers c
        LEFT JOIN Orders o ON c.customerNumber = o.customerNumber
        LEFT JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        LEFT JOIN Payments p ON c.customerNumber = p.customerNumber
        GROUP BY c.country
        ORDER BY c.country;
    """,

    "Tables de Contingence des commandes en fonction pays du client": """
        SELECT p.productLine, c.country,
               COUNT(DISTINCT o.orderNumber) AS nb_commandes
        FROM Customers c
        JOIN Orders o ON c.customerNumber = o.customerNumber
        JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        JOIN Products p ON od.productCode = p.productCode
        GROUP BY p.productLine, c.country
        ORDER BY p.productLine, c.country;
    """,

    "Tables de Contingence des commandes sur les produits achetés \n et le pays du client": """
        SELECT p.productLine, c.country,
               SUM(od.quantityOrdered * od.priceEach) AS montant_total
        FROM Customers c
        JOIN Orders o ON c.customerNumber = o.customerNumber
        JOIN OrderDetails od ON o.orderNumber = od.orderNumber
        JOIN Products p ON od.productCode = p.productCode
        GROUP BY p.productLine, c.country
        ORDER BY p.productLine, c.country;
    """,

    "Top 10 produits à forte marge": """
        SELECT p.productCode, p.productName, 
               AVG(od.priceEach - p.buyPrice) AS marge_moyenne
        FROM Products p
        JOIN OrderDetails od ON p.productCode = od.productCode
        GROUP BY p.productCode
        ORDER BY marge_moyenne DESC
        LIMIT 10;
    """,

    "Produits vendus à perte": """
        SELECT p.productCode, p.productName, o.customerNumber
        FROM Products p
        JOIN OrderDetails od ON p.productCode = od.productCode
        JOIN Orders o ON od.orderNumber = o.orderNumber
        WHERE od.priceEach < p.buyPrice
        ORDER BY p.productCode, o.customerNumber;
    """,

    "Les Clients sont effectivement en retard de paiement": """
        WITH AchatsTotaux AS (
            SELECT o.customerNumber,
                   SUM(od.quantityOrdered * od.priceEach) AS total_achats
            FROM Orders o
            JOIN OrderDetails od ON o.orderNumber = od.orderNumber
            GROUP BY o.customerNumber
        ),
        PaiementsTotaux AS (
            SELECT p.customerNumber,
                   SUM(p.amount) AS total_paiements
            FROM Payments p
            GROUP BY p.customerNumber
        )
        SELECT a.customerNumber,
               a.total_achats,
               COALESCE(p.total_paiements, 0) AS total_paiements
        FROM AchatsTotaux a
        LEFT JOIN PaiementsTotaux p ON a.customerNumber = p.customerNumber
        WHERE COALESCE(p.total_paiements, 0) < a.total_achats
        ORDER BY a.customerNumber;
    """
}

# Exécution des requêtes et affichage des résultats
for titre, requête in requetes_sql.items():
    print(f"--- {titre} ---")
    df = pd.read_sql_query(requête, conn)
    print(df)
    print("\n")

# Fermeture de la connexion
conn.close()
