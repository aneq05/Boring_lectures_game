"""
Solver i narzedzia do analizowania planszy Tango.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.board.board import Board
from src.cell.cell_setup import CellState
from src.core.validator import Validator


@dataclass(frozen=True)
class Hint:
    """Podpowiedz dla gracza oparta o znane rozwiazanie."""

    row: int
    col: int
    state: CellState
    reason: str


class BoardSolver:
    """Rozwiazuje plansze i liczy liczbe rozwiazan."""

    def solve(self, board: Board) -> Optional[Board]:
        """Zwraca pierwsze znalezione rozwiazanie albo None."""
        solutions = self._search(board.clone(), solution_limit=1)
        return solutions[0] if solutions else None

    def count_solutions(self, board: Board, limit: int = 2) -> int:
        """Liczy rozwiazania do wskazanego limitu."""
        return len(self._search(board.clone(), solution_limit=limit))

    def next_hint(self, board: Board, solution: Board) -> Optional[Hint]:
        """Zwraca pierwsza niezgodna z rozwiazaniem komorke."""
        for row, col in board.iter_positions():
            current = board.cells[row][col]
            solved = solution.cells[row][col]
            if current.is_fixed:
                continue
            if current.state != solved.state:
                return Hint(
                    row=row,
                    col=col,
                    state=solved.state,
                    reason="To pole powinno miec przeciwny symbol lub zostac uzupelnione.",
                )
        return None

    def _search(self, board: Board, solution_limit: int) -> list[Board]:
        solutions: list[Board] = []

        def backtrack():
            if len(solutions) >= solution_limit:
                return

            next_pos = self._find_best_empty_cell(board)
            if next_pos is None:
                if Validator.is_board_valid(board):
                    solutions.append(board.clone())
                return

            row, col = next_pos
            for state in (CellState.SUN, CellState.MOON):
                if Validator.is_move_valid(board, row, col, state):
                    board.cells[row][col].state = state
                    backtrack()
                    if len(solutions) >= solution_limit:
                        return
            board.cells[row][col].state = CellState.EMPTY

        backtrack()
        return solutions

    def _find_best_empty_cell(self, board: Board) -> Optional[tuple[int, int]]:
        best_pos: Optional[tuple[int, int]] = None
        best_score: Optional[int] = None

        for row, col in board.iter_positions():
            cell = board.cells[row][col]
            if cell.state != CellState.EMPTY:
                continue

            legal_states = 0
            for state in (CellState.SUN, CellState.MOON):
                if Validator.is_move_valid(board, row, col, state):
                    legal_states += 1

            if legal_states == 0:
                return row, col

            if best_score is None or legal_states < best_score:
                best_score = legal_states
                best_pos = (row, col)

        return best_pos
