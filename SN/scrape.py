import requests
from bs4 import BeautifulSoup
import csv

# URL de base du site
BASE_URL = "http://books.toscrape.com/catalogue/page-{}.html"
HEADERS = ["title", "price", "stock", "rating"]

def get_books():
    """
    Scrape toutes les pages de Books to Scrape et extrait :
    - Titre du livre
    - Prix du livre (converti en float)
    - Disponibilité (quantité en stock)
    - Note (1 à 5 étoiles)
    Retourne une liste de dictionnaires contenant les livres de toutes les pages.
    """
    page_number = 1  # Commence à la première page
    books = []  # Liste pour stocker tous les livres

    while True:
        # Créer l'URL pour la page actuelle
        url = BASE_URL.format(page_number)
        print(f"Scraping de la page {page_number}...")  # Indique quelle page est en cours de scraping
        response = requests.get(url)
        
        if response.status_code != 200:
            print(f"Erreur {response.status_code}: Impossible d'accéder à la page {url}.")
            break  # Si on ne peut pas accéder à la page, on arrête le scraping

        soup = BeautifulSoup(response.text, "html.parser")

        # Scraper les livres de cette page
        page_books = []  # Liste temporaire pour les livres de la page

        for book in soup.select("article.product_pod"):
            # Récupérer le titre
            title = book.h3.a["title"]

            # Récupérer le prix (supprimer les symboles £ et convertir en float)
            price_text = book.select_one(".price_color").text.strip()
            price = float(price_text.replace("Â£", "").replace("£", "").strip())

            # Récupérer la disponibilité (extraction du stock si mentionné)
            stock_info = book.select_one(".instock.availability").text.strip()
            stock = int(stock_info.split("(")[-1].split()[0]) if "(" in stock_info else 0

            # Récupérer la note (convertir en nombre d'étoiles)
            rating_text = book.select_one("p.star-rating")["class"][1]  # Ex: "Three"
            ratings_map = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            rating = ratings_map.get(rating_text, 0)  # Convertir en nombre

            # Ajouter aux résultats sous forme de dictionnaire
            page_books.append({"title": title, "price": price, "stock": stock, "rating": rating})

        books.extend(page_books)  # Ajouter les livres de cette page à la liste générale

        # Vérifier si la page suivante existe en recherchant un lien vers la page suivante
        next_page = soup.select_one(".next > a")
        if next_page:
            page_number += 1  # Passer à la page suivante
            print(f"Passage à la page {page_number}...")  # Indiquer que le scraping passe à la page suivante
        else:
            print("Aucune page suivante trouvée. Fin du scraping.")  # Signal que c'est la dernière page
            break  # Si pas de page suivante, on arrête le scraping

    return books

def save_to_csv(books, filename="books.csv"):
    """
    Enregistre la liste des livres dans un fichier CSV.
    """
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(books)
    print(f"Données enregistrées dans {filename}.")

if __name__ == "__main__":
    print("Début du scraping des livres...")
    books = get_books()
    if books:
        save_to_csv(books)
        print("Scraping terminé avec succès !")
