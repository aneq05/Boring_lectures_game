from __future__ import annotations

from dataclasses import dataclass

from src.cell.cell_setup import CellState


@dataclass(frozen=True)
class Move:
    row: int
    col: int
    previous_state: CellState
    new_state: CellState


class MoveHistory:
    def __init__(self, limit: int = 200):
        self.limit = limit
        self.undo_stack: list[Move] = []
        self.redo_stack: list[Move] = []

    def record(self, move: Move):
        self.undo_stack.append(move)
        self.redo_stack.clear()
        if len(self.undo_stack) > self.limit:
            self.undo_stack.pop(0)

    def pop_undo(self) -> Move | None:
        if not self.undo_stack:
            return None
        move = self.undo_stack.pop()
        self.redo_stack.append(move)
        return move

    def pop_redo(self) -> Move | None:
        if not self.redo_stack:
            return None
        move = self.redo_stack.pop()
        self.undo_stack.append(move)
        return move

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()

    @property
    def can_undo(self) -> bool:
        return bool(self.undo_stack)

    @property
    def can_redo(self) -> bool:
        return bool(self.redo_stack)
