from src.board.board import Board
from src.cell.cell_setup import CellState
from src.core.validator import Validator


class TestValidator:
    def test_validate_three_consecutive_empty_cell(self):
        board = Board(6)
        assert Validator.validate_three_consecutive(board, 0, 0) is True

    def test_validate_three_consecutive_horizontal_invalid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        board.cells[0][2].state = CellState.SUN
        assert Validator.validate_three_consecutive(board, 0, 1) is False

    def test_validate_three_consecutive_valid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        assert Validator.validate_three_consecutive(board, 0, 1) is True

    def test_validate_count_balance_empty_board(self):
        board = Board(6)
        assert Validator.validate_count_balance(board) is True

    def test_validate_count_balance_exceeds_half(self):
        board = Board(6)
        for i in range(4):
            board.cells[0][i].state = CellState.SUN
        assert Validator.validate_count_balance(board) is False

    def test_validate_count_balance_valid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        board.cells[0][2].state = CellState.MOON
        board.cells[0][3].state = CellState.MOON
        assert Validator.validate_count_balance(board) is True

    def test_validate_unique_rows_all_empty(self):
        board = Board(6)
        assert Validator.validate_unique_rows(board) is True

    def test_validate_unique_rows_duplicate(self):
        board = Board(6)
        for i in range(6):
            board.cells[0][i].state = CellState.SUN
            board.cells[1][i].state = CellState.SUN
        assert Validator.validate_unique_rows(board) is False

    def test_validate_unique_cols_all_empty(self):
        board = Board(6)
        assert Validator.validate_unique_cols(board) is True
