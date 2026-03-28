from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.cell.cell_setup import CellState


@dataclass
class ValidationError:
    error_type: str
    message: str
    positions: list[tuple[int, int]]


class Validator:
    @staticmethod
    def validate_three_consecutive(board, row: int, col: int) -> bool:
        cell = board.get_cell(row, col)
        if not cell or cell.state == CellState.EMPTY:
            return True

        count = 1
        for c in range(col - 1, max(-1, col - 3), -1):
            if board.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        for c in range(col + 1, min(board.size, col + 3)):
            if board.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        if count >= 3:
            return False

        count = 1
        for r in range(row - 1, max(-1, row - 3), -1):
            if board.cells[r][col].state == cell.state:
                count += 1
            else:
                break
        for r in range(row + 1, min(board.size, row + 3)):
            if board.cells[r][col].state == cell.state:
                count += 1
            else:
                break

        return count < 3

    @staticmethod
    def validate_count_balance(board, row: Optional[int] = None, col: Optional[int] = None) -> bool:
        rows_to_check = [row] if row is not None else range(board.size)
        cols_to_check = [col] if col is not None else range(board.size)

        for r in rows_to_check:
            sun_count = board.count_in_row(r, CellState.SUN)
            moon_count = board.count_in_row(r, CellState.MOON)
            empty_count = board.count_in_row(r, CellState.EMPTY)
            max_allowed = board.size // 2

            if sun_count > max_allowed or moon_count > max_allowed:
                return False
            if empty_count == 0 and sun_count != moon_count:
                return False

        for c in cols_to_check:
            sun_count = board.count_in_col(c, CellState.SUN)
            moon_count = board.count_in_col(c, CellState.MOON)
            empty_count = board.count_in_col(c, CellState.EMPTY)
            max_allowed = board.size // 2

            if sun_count > max_allowed or moon_count > max_allowed:
                return False
            if empty_count == 0 and sun_count != moon_count:
                return False

        return True

    @staticmethod
    def validate_unique_rows(board) -> bool:
        full_rows: list[tuple[CellState, ...]] = []
        for row_idx in range(board.size):
            row = board.cells[row_idx]
            if all(cell.state != CellState.EMPTY for cell in row):
                row_pattern = tuple(cell.state for cell in row)
                if row_pattern in full_rows:
                    return False
                full_rows.append(row_pattern)
        return True

    @staticmethod
    def validate_unique_cols(board) -> bool:
        full_cols: list[tuple[CellState, ...]] = []
        for col_idx in range(board.size):
            col = [board.cells[row][col_idx] for row in range(board.size)]
            if all(cell.state != CellState.EMPTY for cell in col):
                col_pattern = tuple(cell.state for cell in col)
                if col_pattern in full_cols:
                    return False
                full_cols.append(col_pattern)
        return True

    @staticmethod
    def validate_constraints(board) -> bool:
        # Constraint markers are not implemented yet.
        return True

    @staticmethod
    def is_board_complete(board) -> bool:
        return board.is_complete()

    @staticmethod
    def is_board_valid(board) -> bool:
        for row in range(board.size):
            for col in range(board.size):
                if not Validator.validate_three_consecutive(board, row, col):
                    return False

        if not Validator.validate_count_balance(board):
            return False
        if not Validator.validate_unique_rows(board):
            return False
        if not Validator.validate_unique_cols(board):
            return False
        if not Validator.validate_constraints(board):
            return False

        return True

    @staticmethod
    def get_errors(board) -> list[ValidationError]:
        errors: list[ValidationError] = []

        for row in range(board.size):
            for col in range(board.size):
                if not Validator.validate_three_consecutive(board, row, col):
                    errors.append(
                        ValidationError(
                            "THREE_CONSECUTIVE",
                            f"Three matching symbols in a row near ({row}, {col}).",
                            [(row, col)],
                        )
                    )

        for row in range(board.size):
            sun_count = board.count_in_row(row, CellState.SUN)
            moon_count = board.count_in_row(row, CellState.MOON)
            max_allowed = board.size // 2

            if sun_count > max_allowed:
                errors.append(
                    ValidationError(
                        "TOO_MANY_SUNS_ROW",
                        f"Too many suns in row {row} ({sun_count}/{max_allowed}).",
                        [(row, c) for c in range(board.size) if board.cells[row][c].state == CellState.SUN],
                    )
                )

            if moon_count > max_allowed:
                errors.append(
                    ValidationError(
                        "TOO_MANY_MOONS_ROW",
                        f"Too many moons in row {row} ({moon_count}/{max_allowed}).",
                        [(row, c) for c in range(board.size) if board.cells[row][c].state == CellState.MOON],
                    )
                )

        for col in range(board.size):
            sun_count = board.count_in_col(col, CellState.SUN)
            moon_count = board.count_in_col(col, CellState.MOON)
            max_allowed = board.size // 2

            if sun_count > max_allowed:
                errors.append(
                    ValidationError(
                        "TOO_MANY_SUNS_COL",
                        f"Too many suns in column {col} ({sun_count}/{max_allowed}).",
                        [(r, col) for r in range(board.size) if board.cells[r][col].state == CellState.SUN],
                    )
                )

            if moon_count > max_allowed:
                errors.append(
                    ValidationError(
                        "TOO_MANY_MOONS_COL",
                        f"Too many moons in column {col} ({moon_count}/{max_allowed}).",
                        [(r, col) for r in range(board.size) if board.cells[r][col].state == CellState.MOON],
                    )
                )

        if not Validator.validate_unique_rows(board):
            errors.append(ValidationError("DUPLICATE_ROWS", "Duplicate full rows detected.", []))

        if not Validator.validate_unique_cols(board):
            errors.append(ValidationError("DUPLICATE_COLS", "Duplicate full columns detected.", []))

        return errors

    @staticmethod
    def is_move_valid(board, row: int, col: int, new_state: CellState) -> bool:
        cell = board.get_cell(row, col)
        if not cell or cell.is_fixed:
            return False

        old_state = cell.state
        cell.state = new_state

        is_valid = (
            Validator.validate_three_consecutive(board, row, col)
            and Validator.validate_count_balance(board, row, col)
        )

        cell.state = old_state
        return is_valid
