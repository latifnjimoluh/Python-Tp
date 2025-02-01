import random

class Duel:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2

    def simulate(self):
        """Simule un duel entre les deux joueurs."""
        print(f"Le duel commence entre {self.player1.name} et {self.player2.name}!")
        
        # Lancer un dé pour déterminer le gagnant
        result = random.randint(1, 6)
        
        if result > 3:
            print(f"{self.player1.name} gagne le duel!")
            self.player1.gain_points(1)
            self.player2.lose_points(1)
        else:
            print(f"{self.player2.name} gagne le duel!")
            self.player2.gain_points(1)
            self.player1.lose_points(1)

        # Vérifie si un joueur a atteint un score de 0
        if self.player1.score == 0:
            print(f"{self.player1.name} a perdu!")
        elif self.player2.score == 0:
            print(f"{self.player2.name} a perdu!")
