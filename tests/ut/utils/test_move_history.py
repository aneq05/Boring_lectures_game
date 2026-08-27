from src.utils.move_history import Move, MoveHistory
from src.cell.cell_setup import CellState


class TestMove:
    def test_move_creation(self):
        move = Move(row=1, col=2, previous_state=CellState.EMPTY, new_state=CellState.SUN)
        assert move.row == 1
        assert move.col == 2
        assert move.previous_state == CellState.EMPTY
        assert move.new_state == CellState.SUN

    def test_move_equality(self):
        move1 = Move(1, 2, CellState.EMPTY, CellState.SUN)
        move2 = Move(1, 2, CellState.EMPTY, CellState.SUN)
        assert move1 == move2


class TestMoveHistory:
    def test_initialization(self):
        history = MoveHistory()
        assert history.can_undo is False
        assert history.can_redo is False

    def test_record_move(self):
        history = MoveHistory()
        move = Move(0, 0, CellState.EMPTY, CellState.SUN)
        history.record(move)
        assert history.can_undo is True

    def test_undo(self):
        history = MoveHistory()
        move = Move(0, 0, CellState.EMPTY, CellState.SUN)
        history.record(move)
        undone = history.pop_undo()
        assert undone == move
        assert history.can_undo is False

    def test_redo(self):
        history = MoveHistory()
        move = Move(0, 0, CellState.EMPTY, CellState.SUN)
        history.record(move)
        history.pop_undo()
        redone = history.pop_redo()
        assert redone == move

    def test_clear(self):
        history = MoveHistory()
        move = Move(0, 0, CellState.EMPTY, CellState.SUN)
        history.record(move)
        history.clear()
        assert history.can_undo is False
        assert history.can_redo is False

    def test_redo_clears_after_new_move(self):
        history = MoveHistory()
        move1 = Move(0, 0, CellState.EMPTY, CellState.SUN)
        move2 = Move(0, 1, CellState.EMPTY, CellState.MOON)
        history.record(move1)
        history.pop_undo()
        history.record(move2)
        assert history.can_redo is False
