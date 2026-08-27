from src.cell.cell_setup import Cell, CellState


class TestCellState:
    def test_cell_state_values(self):
        assert CellState.EMPTY.value == 0
        assert CellState.SUN.value == 1
        assert CellState.MOON.value == 2


class TestCell:
    def test_initialization_defaults(self):
        cell = Cell(row=0, col=1)
        assert cell.row == 0
        assert cell.col == 1
        assert cell.state == CellState.EMPTY
        assert cell.is_fixed == False

    def test_initialization_with_state(self):
        cell = Cell(row=2, col=3, state=CellState.SUN, is_fixed=True)
        assert cell.row == 2
        assert cell.col == 3
        assert cell.state == CellState.SUN
        assert cell.is_fixed == True

    def test_toggle_empty_to_sun(self):
        cell = Cell(0, 0)
        cell.toggle()
        assert cell.state == CellState.SUN

    def test_toggle_sun_to_moon(self):
        cell = Cell(0, 0, state=CellState.SUN)
        cell.toggle()
        assert cell.state == CellState.MOON

    def test_toggle_moon_to_empty(self):
        cell = Cell(0, 0, state=CellState.MOON)
        cell.toggle()
        assert cell.state == CellState.EMPTY

    def test_toggle_fixed_cell_no_change(self):
        cell = Cell(0, 0, state=CellState.SUN, is_fixed=True)
        cell.toggle()
        assert cell.state == CellState.SUN

    def test_set_state(self):
        cell = Cell(0, 0)
        cell.set_state(CellState.MOON)
        assert cell.state == CellState.MOON

    def test_set_state_fixed_cell_no_change(self):
        cell = Cell(0, 0, state=CellState.SUN, is_fixed=True)
        cell.set_state(CellState.MOON)
        assert cell.state == CellState.SUN

    def test_repr(self):
        cell = Cell(0, 1, state=CellState.SUN, is_fixed=True)
        repr_str = repr(cell)
        assert "0" in repr_str
        assert "1" in repr_str
        assert "SUN" in repr_str
