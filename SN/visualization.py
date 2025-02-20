import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Charger le fichier CSV
df = pd.read_csv("books.csv")

# Configurer Seaborn pour une meilleure visualisation
sns.set(style="whitegrid")

# 1. Histogramme des prix
plt.figure(figsize=(10, 6))
sns.histplot(df["price"], bins=20, kde=True, color="skyblue")
plt.title("Distribution des prix des livres", fontsize=16)
plt.xlabel("Prix (NAN)", fontsize=12)
plt.ylabel("Nombre de livres", fontsize=12)
plt.tight_layout()
plt.savefig("price_histogram.png")  # Sauvegarde le graphique en PNG
plt.show()

# 2. Countplot de la répartition des notes
plt.figure(figsize=(8, 6))
sns.countplot(x="rating", data=df, palette="viridis")
plt.title("Répartition des notes des livres", fontsize=16)
plt.xlabel("Note", fontsize=12)
plt.ylabel("Nombre de livres", fontsize=12)
plt.tight_layout()
plt.savefig("rating_countplot.png")  # Sauvegarde le graphique en PNG
plt.show()

# 3. Bar chart des stocks
plt.figure(figsize=(10, 6))
sns.barplot(x="title", y="stock", data=df, palette="Blues_d")
plt.title("Stocks des livres", fontsize=16)
plt.xlabel("Livre", fontsize=12)
plt.ylabel("Stock", fontsize=12)
plt.xticks(rotation=90)
plt.tight_layout()
plt.savefig("static/stock_bar_chart.png")  # Sauvegarde dans le dossier static
plt.show()
