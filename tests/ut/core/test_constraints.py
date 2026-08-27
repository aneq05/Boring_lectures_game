from src.core.constraints import Constraint, ConstraintType
from src.cell.cell_setup import CellState


class TestConstraint:
    def test_constraint_initialization(self):
        constraint = Constraint((0, 0), (0, 1), ConstraintType.EQUAL)
        assert constraint.cell1 == (0, 0)
        assert constraint.cell2 == (0, 1)
        assert constraint.constraint_type == ConstraintType.EQUAL

    def test_constraint_type_values(self):
        assert ConstraintType.EQUAL.value == "="
        assert ConstraintType.NOT_EQUAL.value == "*"
