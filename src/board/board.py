"""
Board module - zarzadzanie plansza gry.
"""
from __future__ import annotations

from typing import Optional, Tuple

from src.cell.cell_setup import Cell, CellState


class Board:
    """
    Klasa reprezentujaca plansze gry.

    Attributes:
        size: Rozmiar planszy.
        cells: Dwuwymiarowa lista komorek.
    """

    def __init__(self, size: int = 6):
        self.size = size
        self.cells = [[Cell(r, c) for c in range(size)] for r in range(size)]

    def clone(self) -> "Board":
        """Tworzy pelna kopie planszy."""
        board = Board(self.size)
        for row in range(self.size):
            for col in range(self.size):
                source = self.cells[row][col]
                board.cells[row][col] = Cell(
                    row=row,
                    col=col,
                    state=source.state,
                    is_fixed=source.is_fixed,
                )
        return board

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """Zwraca komorke na danej pozycji albo None."""
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.cells[row][col]
        return None

    def get_cell_at_pos(
        self,
        mouse_pos: Tuple[int, int],
        grid_offset_x: int,
        grid_offset_y: int,
        cell_size: int,
    ) -> Optional[Cell]:
        """Zwraca komorke na podstawie pozycji kursora."""
        x, y = mouse_pos
        col = (x - grid_offset_x) // cell_size
        row = (y - grid_offset_y) // cell_size
        return self.get_cell(row, col)

    def set_state(self, row: int, col: int, state: CellState, fixed: Optional[bool] = None) -> bool:
        """Ustawia stan komorki i opcjonalnie znacznik fixed."""
        cell = self.get_cell(row, col)
        if not cell:
            return False

        if fixed is not None:
            cell.is_fixed = fixed

        if cell.is_fixed and fixed is None:
            return False

        cell.state = state
        return True

    def get_row_states(self, row: int) -> list[CellState]:
        """Zwraca stany komorek w wierszu."""
        return [cell.state for cell in self.cells[row]]

    def get_col_states(self, col: int) -> list[CellState]:
        """Zwraca stany komorek w kolumnie."""
        return [self.cells[row][col].state for row in range(self.size)]

    def count_in_row(self, row: int, state: CellState) -> int:
        """Liczy symbole danego typu w wierszu."""
        return sum(1 for cell in self.cells[row] if cell.state == state)

    def count_in_col(self, col: int, state: CellState) -> int:
        """Liczy symbole danego typu w kolumnie."""
        return sum(1 for row in self.cells if row[col].state == state)

    def check_three_consecutive(self, row: int, col: int) -> bool:
        """Sprawdza czy nie ma trzech takich samych symboli obok siebie."""
        cell = self.get_cell(row, col)
        if not cell or cell.state == CellState.EMPTY:
            return True

        count = 1
        for c in range(col - 1, max(-1, col - 3), -1):
            if self.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        for c in range(col + 1, min(self.size, col + 3)):
            if self.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        if count >= 3:
            return False

        count = 1
        for r in range(row - 1, max(-1, row - 3), -1):
            if self.cells[r][col].state == cell.state:
                count += 1
            else:
                break
        for r in range(row + 1, min(self.size, row + 3)):
            if self.cells[r][col].state == cell.state:
                count += 1
            else:
                break

        return count < 3

    def is_complete(self) -> bool:
        """Sprawdza czy plansza jest w pelni wypelniona."""
        for row in self.cells:
            for cell in row:
                if cell.state == CellState.EMPTY:
                    return False
        return True

    def clear(self):
        """Resetuje wszystkie nieustalone pola do EMPTY."""
        for row in self.cells:
            for cell in row:
                if not cell.is_fixed:
                    cell.state = CellState.EMPTY

    def fill_from(self, other: "Board", preserve_fixed: bool = False):
        """Kopiuje zawartosc z innej planszy."""
        for row in range(self.size):
            for col in range(self.size):
                other_cell = other.cells[row][col]
                self.cells[row][col].state = other_cell.state
                if not preserve_fixed:
                    self.cells[row][col].is_fixed = other_cell.is_fixed

    def iter_positions(self):
        """Generator wszystkich pozycji na planszy."""
        for row in range(self.size):
            for col in range(self.size):
                yield row, col

    def count_empty(self) -> int:
        """Zlicza puste komorki."""
        return sum(
            1
            for row, col in self.iter_positions()
            if self.cells[row][col].state == CellState.EMPTY
        )

    def __repr__(self):
        result = f"Board({self.size}x{self.size}):\n"
        for row in self.cells:
            result += " ".join(
                "S" if c.state == CellState.SUN
                else "M" if c.state == CellState.MOON
                else "."
                for c in row
            ) + "\n"
        return result
