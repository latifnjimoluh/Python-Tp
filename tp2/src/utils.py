import random
from src.player import Player

def generate_random_players(num_players):
    """Génère une liste de joueurs avec des noms aléatoires."""
    names = [f"Player{i + 1}" for i in range(num_players)]
    players = [Player(name) for name in names]
    return players
