
class BoardGenerator:
    def __init__(self, size=6):
        self.size = size  # Zwykle 6x6 lub 8x8

    def generate(self, difficulty='medium'):
        """
        1. Wygeneruj pełne rozwiązanie
        2. Usuń część komórek (zależnie od difficulty)
        3. Dodaj ograniczenia =/×
        4. Upewnij się że jest tylko jedno rozwiązanie
        """
        pass

    def generate_solved_board(self):
        """Generuje poprawnie wypełnioną planszę"""
        # Backtracking algorithm
        pass

    def add_constraints(self, board):
        """Dodaje losowe ograniczenia =/×"""
        pass