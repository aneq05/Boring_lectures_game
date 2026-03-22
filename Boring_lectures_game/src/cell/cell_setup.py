"""
Cell module - reprezentacja komórki na planszy
"""
from enum import Enum


class CellState(Enum):
    """Stany komórki na planszy"""
    EMPTY = 0
    STATE_A = 1      # Pierwszy symbol (sun/cat/circle/apple)
    STATE_B = 2      # Drugi symbol (moon/dog/square/orange)


class Cell:
    """
    Klasa reprezentująca pojedynczą komórkę na planszy.

    Attributes:
        row (int): Numer wiersza komórki
        col (int): Numer kolumny komórki
        state (CellState): Aktualny stan komórki (EMPTY, STATE_A, STATE_B)
        is_fixed (bool): Czy komórka jest ustalona (nie można zmienić)
    """

    def __init__(self, row: int, col: int, state: CellState = CellState.EMPTY, is_fixed: bool = False):
        self.row = row
        self.col = col
        self.state = state
        self.is_fixed = is_fixed

    def toggle(self):
        """
        Przełącza stan komórki: EMPTY -> STATE_A -> STATE_B -> EMPTY
        Działa tylko jeśli komórka nie jest ustalona (is_fixed=False)
        """
        if not self.is_fixed:
            if self.state == CellState.EMPTY:
                self.state = CellState.STATE_A
            elif self.state == CellState.STATE_A:
                self.state = CellState.STATE_B
            else:
                self.state = CellState.EMPTY

    def set_state(self, state: CellState):
        """
        Ustawia stan komórki (jeśli nie jest ustalona)

        Args:
            state (CellState): Nowy stan komórki
        """
        if not self.is_fixed:
            self.state = state

    def __repr__(self):
        return f"Cell({self.row}, {self.col}, {self.state.name}, fixed={self.is_fixed})"
