from src.board.board_generator import BoardGenerator
from src.cell.cell_setup import CellState
from src.core.validator import Validator


class TestBoardGenerator:
    def test_initialization(self):
        gen = BoardGenerator(size=6, seed=42)
        assert gen.size == 6

    def test_generate_returns_both_puzzle_and_solution(self):
        gen = BoardGenerator(size=6, seed=42)
        result = gen.generate(remove_ratio=0.4)
        assert result.puzzle is not None
        assert result.solution is not None

    def test_generated_solution_is_valid(self):
        gen = BoardGenerator(size=6, seed=42)
        result = gen.generate(remove_ratio=0.4)
        assert Validator.is_board_valid(result.solution)

    def test_puzzle_has_empty_cells(self):
        gen = BoardGenerator(size=6, seed=42)
        result = gen.generate(remove_ratio=0.4)
        empty_count = sum(1 for row in result.puzzle.cells for cell in row if cell.state == CellState.EMPTY)
        assert empty_count > 0

    def test_puzzle_not_all_empty(self):
        gen = BoardGenerator(size=6, seed=42)
        result = gen.generate(remove_ratio=0.4)
        empty_count = sum(1 for row in result.puzzle.cells for cell in row if cell.state == CellState.EMPTY)
        assert empty_count < 36

    def test_generate_solved_board_is_complete(self):
        gen = BoardGenerator(size=6, seed=42)
        solution = gen.generate_solved_board()
        has_empty = any(cell.state == CellState.EMPTY for row in solution.cells for cell in row)
        assert not has_empty

    def test_puzzle_cells_marked_unfixed_when_empty(self):
        gen = BoardGenerator(size=6, seed=42)
        result = gen.generate(remove_ratio=0.4)
        for row in result.puzzle.cells:
            for cell in row:
                if cell.state == CellState.EMPTY:
                    assert cell.is_fixed == False
