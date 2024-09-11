# On garde nos imports de base, et on ajoute pymongo pour gérer MongoDB
import sqlite3
import pandas as pd
from pymongo import MongoClient

# Connexion à SQLite
sqlite_conn = sqlite3.connect("ClassicModel.sqlite")

# Connexion à MongoDB (assure-toi d'avoir un serveur MongoDB qui tourne)
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['ClassicModelNoSQL']

# Fonction pour convertir les données SQLite en documents MongoDB
def sqlite_to_mongo(table_name):
    # On récupère les données de SQLite
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", sqlite_conn)
    
    # On convertit le DataFrame en liste de dictionnaires
    records = df.to_dict('records')
    
    # On insère dans MongoDB
    mongo_db[table_name].insert_many(records)
    print(f"Table {table_name} migrée avec succès !")

# Liste des tables à migrer
tables = ['Customers', 'Employees', 'Offices', 'Orders', 'OrderDetails', 'Payments', 'Products', 'ProductLines']

# On migre chaque table
for table in tables:
    sqlite_to_mongo(table)

# Fermeture des connexions
sqlite_conn.close()
mongo_client.close()

print("Migration finalisée ! Vérifions maintenant si tout à été migrés depuis mongoDB Compass:")

# Reconnexion à MongoDB pour les vérifications
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['ClassicModelNoSQL']

# Quelques requêtes de vérification
print("\nNombre de clients :")
print(mongo_db.Customers.count_documents({}))

print("\nPremier employé :")
print(mongo_db.Employees.find_one())

print("\nNombre de commandes par client :")
pipeline = [
    {"$group": {"_id": "$customerNumber", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    {"$limit": 5}
]
for doc in mongo_db.Orders.aggregate(pipeline):
    print(doc)

# N'oublie pas de fermer la connexion à la fin
mongo_client.close()

#commande MongoDB Shell
    
# exem 1 : Pour s'assurer que les données sont bien migrées
"""db.Employees.find().pretty()
db.Orders.find().pretty()
db.Customers.find().pretty()"""

# exem 2 : Compter les documents
"""db.Customers.countDocuments()
db.Employees.countDocuments()
db.Orders.countDocuments()"""

# Exem 3 : Aggrégation pour compter le nombre de clients par pays
"""db.Customers.aggregate([
    { $group: { _id: "$country", totalClients: { $sum: 1 } } }
])"""

# exem 4 : execution des requêtes 
""""db.Customers.find({country: "Norway"})"""

# ------------ ADAPTATION DES REQUETES SQL EN AGGREGATION MONGODB ---------

#Comptage du nombre de clients par pays
"""db.Customers.aggregate([
    { $group: { _id: "$country", totalClients: { $sum: 1 } } }
])"""

