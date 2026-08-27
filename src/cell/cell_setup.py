from enum import Enum

class CellState(Enum):
    EMPTY = 0
    SUN = 1
    MOON = 2


class Cell:
    def __init__(self, row: int, col: int, state: CellState = CellState.EMPTY, is_fixed: bool = False):
        self.row = row
        self.col = col
        self.state = state
        self.is_fixed = is_fixed

    def toggle(self):
        if self.is_fixed:
            return
        if self.state == CellState.EMPTY:
            self.state = CellState.SUN
        elif self.state == CellState.SUN:
            self.state = CellState.MOON
        else:
            self.state = CellState.EMPTY

    def set_state(self, state: CellState):
        if not self.is_fixed:
            self.state = state

    def __repr__(self):
        return f"Cell({self.row}, {self.col}, {self.state.name}, fixed={self.is_fixed})"
