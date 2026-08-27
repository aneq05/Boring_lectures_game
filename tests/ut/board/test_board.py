from src.board.board import Board
from src.cell.cell_setup import CellState


class TestBoard:
    def test_initialization(self):
        board = Board(6)
        assert board.size == 6
        assert len(board.cells) == 6
        assert all(len(row) == 6 for row in board.cells)
        assert all(cell.state == CellState.EMPTY for row in board.cells for cell in row)

    def test_default_size(self):
        board = Board()
        assert board.size == 6

    def test_clone(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][0].is_fixed = True
        cloned = board.clone()
        
        assert cloned.size == board.size
        assert cloned.cells[0][0].state == CellState.SUN
        assert cloned.cells[0][0].is_fixed == True
        cloned.cells[0][0].state = CellState.MOON
        assert board.cells[0][0].state == CellState.SUN

    def test_get_cell_valid(self):
        board = Board(6)
        cell = board.get_cell(0, 0)
        assert cell is not None
        assert cell.row == 0
        assert cell.col == 0

    def test_get_cell_out_of_bounds(self):
        board = Board(6)
        assert board.get_cell(-1, 0) is None
        assert board.get_cell(0, -1) is None
        assert board.get_cell(6, 0) is None
        assert board.get_cell(0, 6) is None

    def test_set_state(self):
        board = Board(6)
        result = board.set_state(0, 0, CellState.SUN)
        assert result is True
        assert board.cells[0][0].state == CellState.SUN

    def test_set_state_fixed_cell(self):
        board = Board(6)
        board.cells[0][0].is_fixed = True
        result = board.set_state(0, 0, CellState.SUN, fixed=None)
        assert result is False
        assert board.cells[0][0].state == CellState.EMPTY

    def test_get_row_states(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.MOON
        states = board.get_row_states(0)
        assert states[0] == CellState.SUN
        assert states[1] == CellState.MOON

    def test_get_col_states(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[1][0].state = CellState.MOON
        states = board.get_col_states(0)
        assert states[0] == CellState.SUN
        assert states[1] == CellState.MOON

    def test_count_in_row(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        board.cells[0][2].state = CellState.MOON
        assert board.count_in_row(0, CellState.SUN) == 2
        assert board.count_in_row(0, CellState.MOON) == 1
        assert board.count_in_row(0, CellState.EMPTY) == 3

    def test_count_in_col(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[1][0].state = CellState.SUN
        board.cells[2][0].state = CellState.MOON
        assert board.count_in_col(0, CellState.SUN) == 2
        assert board.count_in_col(0, CellState.MOON) == 1

    def test_check_three_consecutive_horizontal_valid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        assert board.check_three_consecutive(0, 1) is True

    def test_check_three_consecutive_horizontal_invalid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        board.cells[0][2].state = CellState.SUN
        assert board.check_three_consecutive(0, 2) is False

    def test_check_three_consecutive_vertical_invalid(self):
        board = Board(6)
        board.cells[0][0].state = CellState.MOON
        board.cells[1][0].state = CellState.MOON
        board.cells[2][0].state = CellState.MOON
        assert board.check_three_consecutive(2, 0) is False
