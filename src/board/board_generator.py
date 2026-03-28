from __future__ import annotations

import random
from dataclasses import dataclass

from src.board.board import Board
from src.cell.cell_setup import CellState
from src.core.solver import BoardSolver
from src.core.validator import Validator


@dataclass
class GeneratedPuzzle:
    puzzle: Board
    solution: Board


class BoardGenerator:
    def __init__(self, size: int = 6, seed: int | None = None):
        self.size = size
        self.random = random.Random(seed)
        self.solver = BoardSolver()

    def generate(self, remove_ratio: float) -> GeneratedPuzzle:
        solution = self.generate_solved_board()
        puzzle = self.create_puzzle(solution, remove_ratio)
        return GeneratedPuzzle(puzzle=puzzle, solution=solution)

    def generate_solved_board(self) -> Board:
        board = Board(self.size)

        def backtrack() -> bool:
            next_pos = self._find_next_empty(board)
            if next_pos is None:
                return Validator.is_board_valid(board)

            row, col = next_pos
            states = [CellState.SUN, CellState.MOON]
            self.random.shuffle(states)

            for state in states:
                if Validator.is_move_valid(board, row, col, state):
                    board.cells[row][col].state = state
                    if backtrack():
                        return True

            board.cells[row][col].state = CellState.EMPTY
            return False

        if not backtrack():
            raise RuntimeError("Failed to generate a valid solved board.")

        return board

    def create_puzzle(self, solution: Board, remove_ratio: float) -> Board:
        puzzle = solution.clone()
        for row, col in puzzle.iter_positions():
            puzzle.cells[row][col].is_fixed = True

        target_remove = max(1, int(round(self.size * self.size * remove_ratio)))
        positions = list(puzzle.iter_positions())
        self.random.shuffle(positions)

        removed = 0
        for row, col in positions:
            if removed >= target_remove:
                break

            cell = puzzle.cells[row][col]
            original_state = cell.state
            cell.state = CellState.EMPTY
            cell.is_fixed = False

            solution_count = self.solver.count_solutions(puzzle, limit=2)
            if solution_count != 1:
                cell.state = original_state
                cell.is_fixed = True
                continue

            removed += 1

        return puzzle

    def _find_next_empty(self, board: Board) -> tuple[int, int] | None:
        for row, col in board.iter_positions():
            if board.cells[row][col].state == CellState.EMPTY:
                return row, col
        return None
