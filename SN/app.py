from flask import Flask, render_template, request, redirect, url_for
from scrape import get_books, save_to_csv
import os
import csv
import analysis
import subprocess  # Pour exécuter visualization.py

app = Flask(__name__)

def read_from_csv(filename="books.csv"):
    books = []
    if os.path.exists(filename):
        with open(filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            books = [row for row in reader]
    return books

@app.route("/", methods=["GET", "POST"])
def index():
    books_table = None
    analysis_results = {}

    if request.method == "POST":
        # Lancer le scraping et sauvegarder dans CSV
        print("Début du scraping des livres...")
        books = get_books()  # Scraping des livres
        save_to_csv(books)  # Sauvegarde des livres dans CSV
        print("Scraping terminé avec succès !")

    # Lire les livres à partir du CSV
    books = read_from_csv() 
    if books:
        # Générer le tableau HTML des livres
        books_table = "<table class='table'><thead><tr><th>Titre</th><th>Prix</th><th>Stock</th><th>Note</th></tr></thead><tbody>"
        for book in books:
            books_table += f"<tr><td>{book['title']}</td><td>{book['price']}</td><td>{book['stock']}</td><td>{book['rating']}</td></tr>"
        books_table += "</tbody></table>"

    # Obtenir les résultats de l'analyse
    analysis_results = analysis.get_analysis_results()

    return render_template("index.html", books_table=books_table, analysis_results=analysis_results)

@app.route("/generate_graphs", methods=["POST"])
def generate_graphs():
    # Exécuter le script visualization.py pour générer les graphiques
    subprocess.run(["python", "visualization.py"])

    # Après la génération des graphiques, rediriger vers la page d'accueil
    return redirect(url_for("index"))
