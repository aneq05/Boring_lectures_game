"""
Validator - sprawdzanie zasad i poprawności rozwiązań
"""
from typing import List, Tuple, Optional
from src.cell.cell_setup import CellState


class ValidationError:
    """
    Reprezentacja błędu walidacji.

    Attributes:
        error_type (str): Typ błędu
        message (str): Opis błędu
        positions (List[Tuple[int, int]]): Lista pozycji (row, col) z błędem
    """

    def __init__(self, error_type: str, message: str, positions: List[Tuple[int, int]]):
        self.error_type = error_type
        self.message = message
        self.positions = positions

    def __repr__(self):
        return f"ValidationError({self.error_type}: {self.message}, positions={self.positions})"


class Validator:
    """Klasa walidująca zasady gry Tango."""

    @staticmethod
    def validate_three_consecutive(board, row: int, col: int) -> bool:
        """
        Sprawdza czy nie ma 3 takich samych symboli obok siebie.

        Args:
            board: Obiekt Board do sprawdzenia
            row (int): Numer wiersza sprawdzanej komórki
            col (int): Numer kolumny sprawdzanej komórki

        Returns:
            bool: True jeśli brak 3 z rzędu, False jeśli są 3 identyczne
        """
        cell = board.get_cell(row, col)
        if not cell or cell.state == CellState.EMPTY:
            return True

        # Sprawdź poziomo
        count = 1
        # W lewo
        for c in range(col - 1, max(-1, col - 3), -1):
            if board.cells[row][c].state == cell.state:
                count += 1
            else:
                break
        # W prawo
        for c in range(col + 1, min(board.size, col + 3)):
            if board.cells[row][c].state == cell.state:
                count += 1
            else:
                break

        if count >= 3:
            return False

        # Sprawdź pionowo
        count = 1
        # W górę
        for r in range(row - 1, max(-1, row - 3), -1):
            if board.cells[r][col].state == cell.state:
                count += 1
            else:
                break
        # W dół
        for r in range(row + 1, min(board.size, row + 3)):
            if board.cells[r][col].state == cell.state:
                count += 1
            else:
                break

        if count >= 3:
            return False

        return True

    @staticmethod
    def validate_count_balance(board, row: Optional[int] = None, col: Optional[int] = None) -> bool:
        """
        Sprawdza czy liczba słońc i księżyców jest równa w wierszu/kolumnie.
        Jeśli wiersz/kolumna nie jest pełna, sprawdza czy jeszcze możliwe jest wyrównanie.

        Args:
            board: Obiekt Board do sprawdzenia
            row (Optional[int]): Numer wiersza do sprawdzenia (None = wszystkie)
            col (Optional[int]): Numer kolumny do sprawdzenia (None = wszystkie)

        Returns:
            bool: True jeśli balans jest OK lub możliwy, False jeśli naruszony
        """
        rows_to_check = [row] if row is not None else range(board.size)
        cols_to_check = [col] if col is not None else range(board.size)

        # Sprawdź wiersze
        for r in rows_to_check:
            sun_count = board.count_in_row(r, CellState.STATE_A)
            moon_count = board.count_in_row(r, CellState.STATE_B)
            empty_count = board.count_in_row(r, CellState.EMPTY)

            # Maksymalna dozwolona liczba to połowa rozmiaru
            max_allowed = board.size // 2

            # Jeśli któryś symbol przekroczył maksimum
            if sun_count > max_allowed or moon_count > max_allowed:
                return False

            # Jeśli wiersz pełny, muszą być równe
            if empty_count == 0 and sun_count != moon_count:
                return False

        # Sprawdź kolumny
        for c in cols_to_check:
            sun_count = board.count_in_col(c, CellState.STATE_A)
            moon_count = board.count_in_col(c, CellState.STATE_B)
            empty_count = board.count_in_col(c, CellState.EMPTY)

            max_allowed = board.size // 2

            if sun_count > max_allowed or moon_count > max_allowed:
                return False

            if empty_count == 0 and sun_count != moon_count:
                return False

        return True

    @staticmethod
    def validate_unique_rows(board) -> bool:
        """
        Sprawdza czy wszystkie pełne wiersze są unikalne.

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            bool: True jeśli wszystkie pełne wiersze są różne
        """
        full_rows = []

        for row_idx in range(board.size):
            row = board.cells[row_idx]
            # Sprawdź czy wiersz jest pełny
            if all(cell.state != CellState.EMPTY for cell in row):
                row_pattern = tuple(cell.state for cell in row)
                if row_pattern in full_rows:
                    return False  # Znaleziono duplikat
                full_rows.append(row_pattern)

        return True

    @staticmethod
    def validate_unique_cols(board) -> bool:
        """
        Sprawdza czy wszystkie pełne kolumny są unikalne.

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            bool: True jeśli wszystkie pełne kolumny są różne
        """
        full_cols = []

        for col_idx in range(board.size):
            # Zbierz komórki z kolumny
            col = [board.cells[row][col_idx] for row in range(board.size)]
            # Sprawdź czy kolumna jest pełna
            if all(cell.state != CellState.EMPTY for cell in col):
                col_pattern = tuple(cell.state for cell in col)
                if col_pattern in full_cols:
                    return False  # Znaleziono duplikat
                full_cols.append(col_pattern)

        return True

    @staticmethod
    def validate_constraints(board) -> bool:
        """
        Sprawdza ograniczenia = i × (placeholder - będzie rozbudowane).

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            bool: True jeśli wszystkie constraints są spełnione
        """
        # TODO: Implementacja po dodaniu systemu constraints
        # Na razie zwraca True
        return True

    @staticmethod
    def is_board_complete(board) -> bool:
        """
        Sprawdza czy plansza jest w pełni wypełniona.

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            bool: True jeśli wszystkie komórki są wypełnione
        """
        return board.is_complete()

    @staticmethod
    def is_board_valid(board) -> bool:
        """
        Sprawdza wszystkie zasady gry jednocześnie.

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            bool: True jeśli plansza jest poprawna według wszystkich zasad
        """
        # Sprawdź 3 z rzędu dla każdej komórki
        for row in range(board.size):
            for col in range(board.size):
                if not Validator.validate_three_consecutive(board, row, col):
                    return False

        # Sprawdź balans symboli
        if not Validator.validate_count_balance(board):
            return False

        # Sprawdź unikalność wierszy i kolumn (tylko jeśli pełne)
        if not Validator.validate_unique_rows(board):
            return False

        if not Validator.validate_unique_cols(board):
            return False

        # Sprawdź constraints
        if not Validator.validate_constraints(board):
            return False

        return True

    @staticmethod
    def get_errors(board) -> List[ValidationError]:
        """
        Zwraca listę wszystkich błędów na planszy z pozycjami komórek.

        Args:
            board: Obiekt Board do sprawdzenia

        Returns:
            List[ValidationError]: Lista błędów walidacji
        """
        errors = []

        # Sprawdź 3 z rzędu
        for row in range(board.size):
            for col in range(board.size):
                if not Validator.validate_three_consecutive(board, row, col):
                    errors.append(ValidationError(
                        "THREE_CONSECUTIVE",
                        f"Trzy identyczne symbole z rzędu przy pozycji ({row}, {col})",
                        [(row, col)]
                    ))

        # Sprawdź balans w wierszach
        for row in range(board.size):
            sun_count = board.count_in_row(row, CellState.STATE_A)
            moon_count = board.count_in_row(row, CellState.STATE_B)
            max_allowed = board.size // 2

            if sun_count > max_allowed:
                errors.append(ValidationError(
                    "TOO_MANY_SUNS_ROW",
                    f"Za dużo symboli A w wierszu {row} ({sun_count}/{max_allowed})",
                    [(row, c) for c in range(board.size) if board.cells[row][c].state == CellState.STATE_A]
                ))

            if moon_count > max_allowed:
                errors.append(ValidationError(
                    "TOO_MANY_MOONS_ROW",
                    f"Za dużo symboli B w wierszu {row} ({moon_count}/{max_allowed})",
                    [(row, c) for c in range(board.size) if board.cells[row][c].state == CellState.STATE_B]
                ))

        # Sprawdź balans w kolumnach
        for col in range(board.size):
            sun_count = board.count_in_col(col, CellState.STATE_A)
            moon_count = board.count_in_col(col, CellState.STATE_B)
            max_allowed = board.size // 2

            if sun_count > max_allowed:
                errors.append(ValidationError(
                    "TOO_MANY_SUNS_COL",
                    f"Za dużo symboli A w kolumnie {col} ({sun_count}/{max_allowed})",
                    [(r, col) for r in range(board.size) if board.cells[r][col].state == CellState.STATE_A]
                ))

            if moon_count > max_allowed:
                errors.append(ValidationError(
                    "TOO_MANY_MOONS_COL",
                    f"Za dużo symboli B w kolumnie {col} ({moon_count}/{max_allowed})",
                    [(r, col) for r in range(board.size) if board.cells[r][col].state == CellState.STATE_B]
                ))

        # Sprawdź duplikaty wierszy
        if not Validator.validate_unique_rows(board):
            errors.append(ValidationError(
                "DUPLICATE_ROWS",
                "Znaleziono identyczne wiersze",
                []  # TODO: Zwróć konkretne wiersze
            ))

        # Sprawdź duplikaty kolumn
        if not Validator.validate_unique_cols(board):
            errors.append(ValidationError(
                "DUPLICATE_COLS",
                "Znaleziono identyczne kolumny",
                []  # TODO: Zwróć konkretne kolumny
            ))

        return errors

    @staticmethod
    def is_move_valid(board, row: int, col: int, new_state: CellState) -> bool:
        """
        Sprawdza czy ruch jest dozwolony (nie łamie zasad).

        Args:
            board: Obiekt Board
            row (int): Numer wiersza
            col (int): Numer kolumny
            new_state (CellState): Nowy stan do ustawienia

        Returns:
            bool: True jeśli ruch jest dozwolony
        """
        cell = board.get_cell(row, col)
        if not cell or cell.is_fixed:
            return False

        # Zapisz stary stan
        old_state = cell.state

        # Tymczasowo ustaw nowy stan
        cell.state = new_state

        # Sprawdź czy plansza jest nadal poprawna
        is_valid = (
            Validator.validate_three_consecutive(board, row, col) and
            Validator.validate_count_balance(board, row, col)
        )

        # Przywróć stary stan
        cell.state = old_state

        return is_valid

