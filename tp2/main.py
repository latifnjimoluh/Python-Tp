from src.utils import generate_random_players
from src.tournament_manager import TournamentManager

def main():
    # Demande le nombre de participants au tournoi
    num_players = int(input("Entrez le nombre de participants pour le tournoi : "))
    
    # Génère les joueurs avec des noms aléatoires
    players = generate_random_players(num_players)
    
    # Affiche le nombre de joueurs générés
    print(f"\n{num_players} joueurs ont été générés pour le tournoi.")
    
    # Crée une instance de TournamentManager et commence le tournoi
    manager = TournamentManager(players)
    manager.start_tournament()

if __name__ == "__main__":
    main()
