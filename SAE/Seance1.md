# SAÉ NoSQL

## Base de données utilisée

Nous disposons de la base de données suivante ClassicModel :

![ClassicModel ER](https://github.com/alannadevgen/resources-nosql/blob/main/SAE/img/ClassicModel-ER.png)


## Idée de la SAE

Nous voulons changer de technologie pour stocker les données. Et donc le choix a été fait de passer de ce format SQLite à un format NoSQL. Il va donc falloir préparer la migration de la BD à l’aide Python.

### Cette migration va se faire en 4 étapes :

Création de requêtes SQL sur la BD initiale ;
Réflexion sur le format des données à obtenir et l’algorithme à réaliser ;
Ecriture du script Python permettant le passage de SQLite à NoSQL ;
Création des requêtes initiales au nouveau format NoSQL pour s’assurer que la migration s’est bien passée.

### Accès à SQLite dans Python

Nous allons utiliser le modele sqlite3 pour créer la connexion à la base de données. Ensuite, le module pandas permet d’exécuter une requête SELECT sur une BD et de récupérer le résultat dans un DataFrame.

Voici le code pour créer la connexion et récupérer le contenu de la table Customers par exemple :

```python
# Importation des modules utilisés
import sqlite3
import pandas

# Création de la connexion
conn = sqlite3.connect("ClassicModel.sqlite")

# Récupération du contenu de Customers avec une requête SQL
customers = pandas.read_sql_query("SELECT * FROM Customers;", conn)
print(customers)

# Fermeture de la connexion : IMPORTANT à faire dans un cadre professionnel
conn.close()
```

###  Requêtes à programme en SQL

Voici les requêtes qui vont nous servir de test pour la réussite ou non de la migration. Pour chaque requête, faites un choix d’ordonnencement du résultat, s’il n’est pas précisé ou naturel. Cela permettra de mieux comparer les résultats après migration.

1. Lister les clients n’ayant jamais effecuté une commande ;
2. Pour chaque employé, le nombre de clients, le nombre de commandes et le montant total de celles-ci ;
3. Idem pour chaque bureau (nombre de clients, nombre de commandes et montant total), avec en plus le nombre de clients d’un pays différent, s’il y en a ;
4. Pour chaque produit, donner le nombre de commandes, la quantité totale commandée, et le nombre de clients différents ;
5. Donner le nombre de commande pour chaque pays du client, ainsi que le montant total des commandes et le montant total payé : on veut conserver les clients n’ayant jamais commandé dans le résultat final ;
6. On veut la table de contigence du nombre de commande entre la ligne de produits et le pays du client ;
7. On veut la même table croisant la ligne de produits et le pays du client, mais avec le montant total payé dans chaque cellule ;
8. Donner les 10 produits pour lesquels la marge moyenne est la plus importante (cf buyPrice et priceEach) ;
9. Lister les produits (avec le nom et le code du client) qui ont été vendus à perte :
    - Si un produit a été dans cette situation plusieurs fois, il doit apparaître plusieurs fois,
    - Une vente à perte arrive quand le prix de vente est inférieur au prix d’achat ;
10. (bonus) Lister les clients pour lesquels le montant total payé est inférieur aux montants totals des achats ;

A FAIRE : Ecrire donc les requêtes SQL ci-dessus dans un programme Python. Pour certaines, il est nécessaire de ré-organiser le résultat de la requête avec du code Python ensuite.