import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("books.csv")

# Convertir la colonne 'price' en float (elle est déjà propre dans scrape.py, mais on vérifie)
df["price"] = df["price"].astype(float)

# Calcul du prix moyen des livres
average_price = df["price"].mean()

# Filtrer les livres à moins de 20 NAN
cheap_books = df[df["price"] < 20]

# Trier les livres du moins cher au plus cher
sorted_books = df.sort_values(by="price", ascending=True)

# Transformer la colonne rating en nombres (si ce n'est pas déjà fait)
if df["rating"].dtype != int:
    df["rating"] = df["rating"].astype(int)

# Répartition des notes
rating_counts = df["rating"].value_counts().sort_index()

# Retourner les résultats pour les utiliser dans app.py
def get_analysis_results():
    # Préparer les livres triés par prix sous forme de liste de dictionnaires
    sorted_books_list = sorted_books[['title', 'price']].to_dict(orient='records')

    return {
        "average_price": average_price,
        "cheap_books_count": cheap_books.shape[0],
        "sorted_books": sorted_books_list,  # Renvoi de la liste des livres triés
        "rating_counts": rating_counts.to_dict()  # Renvoi de la répartition des notes sous forme de dictionnaire
    }
