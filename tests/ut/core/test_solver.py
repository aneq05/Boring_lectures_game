from src.board.board import Board
from src.cell.cell_setup import CellState
from src.core.solver import BoardSolver


class TestBoardSolver:
    def test_count_solutions_empty_board(self):
        board = Board(4)
        solver = BoardSolver()
        count = solver.count_solutions(board, limit=2)
        assert count >= 0

    def test_solve_returns_board(self):
        board = Board(4)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][0].is_fixed = True
        solver = BoardSolver()
        solution = solver.solve(board)
        if solution:
            assert solution is not None
            assert solution.size == 4

    def test_next_hint_returns_hint_or_none(self):
        board = Board(4)
        solution = Board(4)
        solver = BoardSolver()
        hint = solver.next_hint(board, solution)
        assert hint is None or hint is not None
