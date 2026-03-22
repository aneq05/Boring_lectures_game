"""
Board module - zarządzanie planszą gry
"""
from typing import Optional, Tuple
from src.cell.cell_setup import Cell, CellState


class Board:
    """
    Klasa reprezentująca planszę gry.

    Attributes:
        size (int): Rozmiar planszy (np. 6 dla planszy 6x6)
        cells (list[list[Cell]]): Dwuwymiarowa lista komórek
    """

    def __init__(self, size: int = 6):
        """
        Inicjalizacja planszy.

        Args:
            size (int): Rozmiar planszy (domyślnie 6)
        """
        self.size = size
        self.cells = [[Cell(r, c) for c in range(size)] for r in range(size)]

    def get_cell(self, row: int, col: int) -> Optional[Cell]:
        """
        Zwraca komórkę na danej pozycji.

        Args:
            row (int): Numer wiersza
            col (int): Numer kolumny

        Returns:
            Optional[Cell]: Komórka lub None jeśli pozycja poza planszą
        """
        if 0 <= row < self.size and 0 <= col < self.size:
            return self.cells[row][col]
        return None

    def get_cell_at_pos(self, mouse_pos: Tuple[int, int], grid_offset_x: int, grid_offset_y: int, cell_size: int) -> Optional[Cell]:
        """
        Zwraca komórkę na podstawie pozycji myszy.

        Args:
            mouse_pos (Tuple[int, int]): Pozycja myszy (x, y)
            grid_offset_x (int): Przesunięcie siatki w osi X
            grid_offset_y (int): Przesunięcie siatki w osi Y
            cell_size (int): Rozmiar pojedynczej komórki

        Returns:
            Optional[Cell]: Komórka lub None jeśli kliknięto poza planszą
        """
        x, y = mouse_pos
        col = (x - grid_offset_x) // cell_size
        row = (y - grid_offset_y) // cell_size
        return self.get_cell(row, col)

    def count_in_row(self, row: int, state: CellState) -> int:
        """
        Liczy symbole danego typu w wierszu.

        Args:
            row (int): Numer wiersza
            state (CellState): Stan komórki do policzenia

        Returns:
            int: Liczba komórek z danym stanem
        """
        return sum(1 for cell in self.cells[row] if cell.state == state)

    def count_in_col(self, col: int, state: CellState) -> int:
        """
        Liczy symbole danego typu w kolumnie.

        Args:
            col (int): Numer kolumny
            state (CellState): Stan komórki do policzenia

        Returns:
            int: Liczba komórek z danym stanem
        """
        return sum(1 for row in self.cells if row[col].state == state)

    def check_three_consecutive(self, row: int, col: int) -> bool:
        """
        Sprawdza czy nie ma 3 takich samych symboli obok siebie.

        Args:
            row (int): Numer wiersza sprawdzanej komórki
            col (int): Numer kolumny sprawdzanej komórki

        Returns:
            bool: True jeśli brak 3 z rzędu, False jeśli są 3 identyczne
        """
        cell = self.get_cell(row, col)
        if not cell or cell.state == CellState.EMPTY:
            return True

        # Sprawdź poziomo
        count = 1
        # W lewo
        for c in range(col - 1, max(-1, col - 3), -1):
            if self.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        # W prawo
        for c in range(col + 1, min(self.size, col + 3)):
            if self.cells[row][c].state == cell.state:
                count += 1
            else:
                break

        if count >= 3:
            return False

        # Sprawdź pionowo
        count = 1
        # W górę
        for r in range(row - 1, max(-1, row - 3), -1):
            if self.cells[r][col].state == cell.state:
                count += 1
            else:
                break
        # W dół
        for r in range(row + 1, min(self.size, row + 3)):
            if self.cells[r][col].state == cell.state:
                count += 1
            else:
                break

        if count >= 3:
            return False

        return True

    def is_complete(self) -> bool:
        """
        Sprawdza czy plansza jest w pełni wypełniona.

        Returns:
            bool: True jeśli wszystkie komórki są wypełnione
        """
        for row in self.cells:
            for cell in row:
                if cell.state == CellState.EMPTY:
                    return False
        return True

    def clear(self):
        """Czyści planszę, resetując wszystkie nie-ustalone komórki do EMPTY."""
        for row in self.cells:
            for cell in row:
                if not cell.is_fixed:
                    cell.state = CellState.EMPTY

    def __repr__(self):
        result = f"Board({self.size}x{self.size}):\n"
        for row in self.cells:
            result += " ".join(
                "A" if c.state == CellState.STATE_A
                else "B" if c.state == CellState.STATE_B
                else "·"
                for c in row
            ) + "\n"
        return result


