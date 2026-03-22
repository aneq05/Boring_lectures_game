from enum import Enum
from src.cell.cell_setup import CellState

class ConstraintType(Enum):
    EQUAL = "="
    NOT_EQUAL = "*"

class Constraint:
    def __init__(self, cell1, cell2, constraint_type):
        self.cell1 = cell1
        self.cell2 = cell2
        self.constraint_type = constraint_type

    def is_satisfied(self, board):
        """Check if the constraint is satisfied on the given board."""
        state1 = board.get_cell_state(self.cell1).state
        state2 = board.get_cell_state(self.cell2).state

        if state1 == CellState.EMPTY or state2 == CellState.EMPTY:
            return True

        if self.constraint_type == ConstraintType.EQUAL:
            return state1 == state2
        else:
            return state1 != state2