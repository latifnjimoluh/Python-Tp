class Player:
    def __init__(self, name, score=10):
        self.name = name
        self.score = score

    def gain_points(self, points):
        """Ajoute des points au joueur."""
        self.score += points

    def lose_points(self, points):
        """Enlève des points au joueur."""
        self.score -= points
        if self.score < 0:
            self.score = 0  # Le score ne peut pas descendre sous 0

    def __repr__(self):
        return f"{self.name} (Score: {self.score})"
