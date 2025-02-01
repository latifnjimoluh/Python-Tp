import random
from concurrent.futures import ThreadPoolExecutor
from src.duel import Duel

class Tournament:
    def __init__(self, players):
        self.players = players  # Liste des joueurs
        self.round = 1  # Le premier tour commence à 1
        self.max_threads = 16  # Nombre maximal de threads, correspondant à tes unités logiques

    def start_round(self):
        """Démarre un tour du tournoi, en simulant des duels entre tous les joueurs."""
        print(f"--- Tour {self.round} ---")
        random.shuffle(self.players)  # Mélange les joueurs pour garantir des matchs aléatoires

        # Crée des duels entre les joueurs par paires
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for i in range(0, len(self.players), 2):
                if i + 1 < len(self.players):  # Assurer qu'il y a bien une paire
                    duel = Duel(self.players[i], self.players[i + 1])
                    # Exécuter chaque duel en parallèle, avec un maximum de threads
                    futures.append(executor.submit(duel.simulate))

            # Attendre que tous les duels soient terminés
            for future in futures:
                future.result()  # Bloque jusqu'à ce que le duel soit terminé

        self.round += 1

    def get_ranking(self):
        """Retourne les joueurs triés par score (décroissant)."""
        return sorted(self.players, key=lambda x: x.score, reverse=True)

    def display_ranking(self):
        """Affiche les 20 premiers joueurs du classement actuel."""
        ranking = self.get_ranking()[:20]  # Limiter à 20 joueurs
        print("\nClassement actuel des 20 premiers joueurs :")
        for i, player in enumerate(ranking):
            print(f"{i + 1}. {player.name} (Score: {player.score})")
