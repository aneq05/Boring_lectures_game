from src.board.board_generator import BoardGenerator
from src.cell.cell_setup import CellState
from src.config import BoardSize, Difficulty, GameSettings
from src.core.solver import BoardSolver
from src.core.validator import Validator
from src.utils.move_history import Move, MoveHistory


def test_generated_solution_is_valid():
    settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
    generated = BoardGenerator(settings.size, seed=21).generate(settings.remove_percent)

    assert Validator.is_board_valid(generated.solution)
    assert generated.puzzle.count_empty() > 0


def test_generated_puzzle_has_single_solution_for_small_board():
    settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
    generated = BoardGenerator(settings.size, seed=8).generate(settings.remove_percent)

    assert BoardSolver().count_solutions(generated.puzzle, limit=2) == 1


def test_move_history_undo_redo_cycle():
    history = MoveHistory()
    move = Move(
        row=1,
        col=2,
        previous_state=CellState.EMPTY,
        new_state=CellState.SUN,
    )
    history.record(move)

    undone = history.pop_undo()
    redone = history.pop_redo()

    assert undone == move
    assert redone == move
