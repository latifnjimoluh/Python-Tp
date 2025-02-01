import csv
import math
import random
import time
import pygame  # Import de pygame pour jouer les sons

# Initialiser pygame pour gérer les sons
pygame.mixer.init()

# Fichier CSV pour stocker les scores
CSV_FILE = "scores.csv"

# Fonction pour charger les scores depuis le fichier CSV
def load_scores():
    scores = []
    try:
        with open(CSV_FILE, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores.append({
                    "Nom": row["Nom"],
                    "Tentatives": int(row["Tentatives"]),
                    "Temps": float(row["Temps"]),
                    "Niveau": row["Niveau"]
                })
    except FileNotFoundError:
        pass
    return scores

# Fonction pour sauvegarder les scores dans le fichier CSV
def save_scores(scores):
    with open(CSV_FILE, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["Nom", "Tentatives", "Temps", "Niveau"])
        writer.writeheader()
        writer.writerows(scores)

# Fonction pour vérifier si un joueur existe déjà
def get_existing_player(name, scores):
    for score in scores:
        if score["Nom"] == name:
            return score
    return None

# Fonction pour afficher les meilleurs scores
def display_best_scores(scores):
    if not scores:
        print("\nAucun score enregistré pour le moment.")
        return
    scores.sort(key=lambda x: (x["Tentatives"], x["Temps"]))
    print("\nMeilleurs scores :")
    for score in scores[:5]:  # Affiche les 5 meilleurs scores
        print(f"{score['Nom']} - {score['Tentatives']} tentatives, {score['Temps']:.2f} secondes ({score['Niveau']})")

# Fonction pour jouer un son
def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

# Fonction principale du jeu
def play_game():
    scores = load_scores()
    name = input("Entrez votre nom : ")

    # Vérifier si le joueur existe déjà
    existing_player = get_existing_player(name, scores)
    if existing_player:
        print(f"\nBienvenue de retour, {name} !")
        print(f"Votre dernier score : {existing_player['Tentatives']} tentatives en {existing_player['Temps']:.2f} secondes ({existing_player['Niveau']}).")

    # Définir l'intervalle
    print("Définissez l'intervalle des nombres à deviner.")
    while True:
        min_val = int(input("Valeur minimale : "))
        max_val = int(input("Valeur maximale : "))
        
        if min_val >= max_val:
            print("Erreur : La valeur minimale ne peut pas être supérieure ou égale à la valeur maximale. Veuillez réessayer.")
        else:
            break  # Sortir de la boucle si les valeurs sont valides

    # Calcul du nombre maximal de tentatives pour le niveau Normal
    amplitude = max_val - min_val + 1
    normal_attempts = math.floor(math.log2(amplitude)) + 1

    # Calcul des tentatives pour les niveaux Facile et Difficile
    easy_attempts = math.ceil(normal_attempts * 1.25)
    hard_attempts = math.floor(normal_attempts * 0.75)

    # Définir le niveau de difficulté
    print("\nChoisissez un niveau de difficulté :")
    print(f"1. Facile ({easy_attempts} tentatives)")
    print(f"2. Normal ({normal_attempts} tentatives)")
    print(f"3. Difficile ({hard_attempts} tentatives)")
    print("0. Retour")
    print("00. Quitter")
    level_choice = input("Votre choix : ")

    if level_choice == "1":
        level = "Facile"
        attempts_allowed = easy_attempts
    elif level_choice == "2":
        level = "Normal"
        attempts_allowed = normal_attempts
    elif level_choice == "3":
        level = "Difficile"
        attempts_allowed = hard_attempts
    elif level_choice == "00":
        print("Merci d'avoir joué ! À bientôt.")
        exit()
    elif level_choice == "0":
        return
    else:
        print("Choix invalide. Retour au menu principal.")
        return

    print(f"\nVous avez {attempts_allowed} tentatives pour deviner le nombre.")

    # Jouer le son de début
    play_sound("start_sound.mp3")  # Assurez-vous d'avoir un fichier son 'start_sound.mp3'

    # Générer un nombre aléatoire dans l'intervalle
    target = random.randint(min_val, max_val)

    # Démarrer le chronomètre
    start_time = time.time()
    attempts = 0

    # Jeu
    while attempts < attempts_allowed:
        guess = input(f"Tentative {attempts + 1}/{attempts_allowed} : Entrez un nombre : ")
        if guess == "00":
            print("Merci d'avoir joué ! À bientôt.")
            exit()
        elif guess == "0":
            return
        guess = int(guess)
        attempts += 1

        if guess == target:
            print("\nFélicitations ! Vous avez deviné le nombre.")
            # Arrêter le chronomètre
            elapsed_time = time.time() - start_time

            # Jouer le son de victoire
            play_sound("start_sound.mp3")  # Assurez-vous d'avoir un fichier son 'win_sound.mp3'

            # Mettre à jour ou ajouter un score
            if existing_player:
                if attempts < existing_player["Tentatives"] or (attempts == existing_player["Tentatives"] and elapsed_time < existing_player["Temps"]):
                    print("\nBravo ! Vous avez amélioré votre score.")
                    existing_player["Tentatives"] = attempts
                    existing_player["Temps"] = elapsed_time
                    existing_player["Niveau"] = level
            else:
                scores.append({"Nom": name, "Tentatives": attempts, "Temps": elapsed_time, "Niveau": level})

            # Sauvegarder les scores
            save_scores(scores)
            print("\nVotre score a été enregistré.")
            return
        elif guess < target:
            print("Le nombre est plus grand.")
        else:
            print("Le nombre est plus petit.")
    else:
        print(f"\nDommage ! Vous avez utilisé toutes vos tentatives. Le nombre était {target}.")
        # Jouer le son de défaite
        play_sound("start_sound.mp3")  # Assurez-vous d'avoir un fichier son 'lose_sound.mp3'

# Menu principal
def main_menu():
    while True:
        print("\n=== Jeu de Devinette ===")
        print("1. Jouer")
        print("2. Meilleurs scores")
        print("0. Retour")
        print("00. Quitter")
        choice = input("Votre choix : ")

        if choice == "1":
            play_game()
        elif choice == "2":
            display_best_scores(load_scores())
        elif choice == "00":
            print("Merci d'avoir joué ! À bientôt.")
            break
        elif choice == "0":
            continue
        else:
            print("Choix invalide. Veuillez réessayer.")

# Lancer le jeu
if __name__ == "__main__":
    main_menu()
