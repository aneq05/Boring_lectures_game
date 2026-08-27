from src.board.board_generator import BoardGenerator
from src.board.board import Board
from src.cell.cell_setup import CellState
from src.config import BoardSize, Difficulty, GameSettings
from src.core.solver import BoardSolver
from src.core.validator import Validator
from src.utils.move_history import Move, MoveHistory


class TestBoardGenerationSystem:
    def test_generated_solution_is_valid(self):
        settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        generated = BoardGenerator(settings.size, seed=21).generate(settings.remove_percent)

        assert Validator.is_board_valid(generated.solution)
        assert generated.puzzle.count_empty() > 0

    def test_generated_puzzle_has_single_solution_for_small_board(self):
        settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        generated = BoardGenerator(settings.size, seed=8).generate(settings.remove_percent)

        assert BoardSolver().count_solutions(generated.puzzle, limit=2) == 1

    def test_puzzle_difficulty_scales_with_empty_cells(self):
        easy_settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        hard_settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.HARD)
        
        easy_gen = BoardGenerator(4, seed=42).generate(easy_settings.remove_percent)
        hard_gen = BoardGenerator(4, seed=42).generate(hard_settings.remove_percent)
        
        easy_empty = sum(1 for row in easy_gen.puzzle.cells for cell in row if cell.state == CellState.EMPTY)
        hard_empty = sum(1 for row in hard_gen.puzzle.cells for cell in row if cell.state == CellState.EMPTY)
        
        assert hard_empty >= easy_empty


class TestGameplayIntegration:
    def test_cell_state_change_with_validation_and_history(self):
        board = Board(4)
        history = MoveHistory()
        
        board.cells[0][0].state = CellState.SUN
        move = Move(row=0, col=0, previous_state=CellState.EMPTY, new_state=CellState.SUN)
        history.record(move)
        
        assert board.cells[0][0].state == CellState.SUN
        assert history.can_undo is True
        assert Validator.validate_three_consecutive(board, 0, 0) is True

    def test_board_constraint_validation_during_gameplay(self):
        board = Board(6)
        
        board.cells[0][0].state = CellState.SUN
        board.cells[0][1].state = CellState.SUN
        board.cells[0][2].state = CellState.SUN
        
        assert Validator.validate_three_consecutive(board, 0, 1) is False

    def test_fixed_cells_cannot_be_changed(self):
        board = Board(6)
        board.cells[0][0].state = CellState.SUN
        board.cells[0][0].is_fixed = True
        
        result = board.set_state(0, 0, CellState.MOON)
        assert result is False
        assert board.cells[0][0].state == CellState.SUN

    def test_undo_redo_restores_previous_state(self):
        board = Board(6)
        history = MoveHistory()
        
        board.cells[0][0].state = CellState.SUN
        move1 = Move(0, 0, CellState.EMPTY, CellState.SUN)
        history.record(move1)
        
        board.cells[0][1].state = CellState.MOON
        move2 = Move(0, 1, CellState.EMPTY, CellState.MOON)
        history.record(move2)
        
        assert history.can_undo is True
        last_move = history.pop_undo()
        assert last_move == move2
        
        assert history.can_redo is True
        redo_move = history.pop_redo()
        assert redo_move == move2


class TestSolverIntegration:
    def test_solver_finds_valid_solution_for_generated_puzzle(self):
        gen = BoardGenerator(4, seed=10).generate(0.40)
        solver = BoardSolver()
        
        solution = solver.solve(gen.puzzle)
        assert solution is not None
        assert Validator.is_board_valid(solution)

    def test_multiple_solution_detection(self):
        gen = BoardGenerator(4, seed=42).generate(0.20)
        solver = BoardSolver()
        
        count = solver.count_solutions(gen.puzzle, limit=3)
        assert count >= 1
