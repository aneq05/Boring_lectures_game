"""
Game Manager - glowna logika gry i petla zdarzen.
"""
from __future__ import annotations

import logging
import os
import sys

import pygame

from src.board.board import Board
from src.board.board_generator import BoardGenerator
from src.cell.cell_setup import Cell, CellState
from src.config import GameConfig, GameSettings
from src.core.solver import BoardSolver
from src.core.validator import Validator
from src.ui.game_renderer import GameRenderer
from src.ui.toolbar import Toolbar
from src.ui.win_popup import WinPopup
from src.utils.colors import BasicColors, ThemeColors
from src.utils.move_history import Move, MoveHistory
from src.utils.timer import GameTimer


class Game:
    """Glowna klasa zarzadzajaca rozgrywka."""

    def __init__(self, settings: GameSettings):
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (self.settings.window_width, self.settings.window_height)
        )
        pygame.display.set_caption("Let Me Tango")

        self.clock = pygame.time.Clock()
        self.board: Board | None = None
        self.initial_board: Board | None = None
        self.solution_board: Board | None = None
        self.selected_cell: Cell | None = None
        self.hovered_cell: Cell | None = None
        self.running = True
        self.move_count = 0
        self.hints_used = 0
        self.hints_remaining = self.settings.hints_available
        self.status_message = "Generowanie planszy..."
        self.status_kind = "info"
        self.is_won = False
        self.transition_alpha = 0

        self.timer = GameTimer()
        self.history = MoveHistory()
        self.solver = BoardSolver()
        self.toolbar = Toolbar(self.settings)
        self.renderer = GameRenderer(self.screen, self.settings)
        self.win_popup: WinPopup | None = None

        self.icons: dict[CellState, pygame.Surface] = {}
        self.load_icons()
        self.start_new_game()

    def load_icons(self):
        """Laduje ikony wedlug wybranego motywu."""
        theme_info = GameConfig.THEME_SETTINGS[self.settings.theme]
        icon_path = os.path.join("assets", "images", "icons")

        try:
            icon1_path = os.path.join(icon_path, theme_info["icon1"])
            icon2_path = os.path.join(icon_path, theme_info["icon2"])

            icon1 = pygame.image.load(icon1_path)
            icon2 = pygame.image.load(icon2_path)

            icon_size = int(self.settings.cell_size * self.settings.icon_scale)
            self.icons[CellState.SUN] = pygame.transform.smoothscale(icon1, (icon_size, icon_size))
            self.icons[CellState.MOON] = pygame.transform.smoothscale(icon2, (icon_size, icon_size))
        except Exception as exc:
            logging.error("Error loading icons: %s", exc)
            icon_size = int(self.settings.cell_size * self.settings.icon_scale)
            self.icons[CellState.SUN] = self._create_fallback_icon(icon_size, theme_info["icon1_fallback"])
            self.icons[CellState.MOON] = self._create_fallback_icon(icon_size, theme_info["icon2_fallback"])

    def _create_fallback_icon(self, size: int, fallback_type: str) -> pygame.Surface:
        """Tworzy prosta ikone awaryjna."""
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        fallback_colors = {
            "yellow_circle": ThemeColors.YELLOW.value,
            "blue_circle": ThemeColors.BLUE.value,
            "brown_circle": ThemeColors.BROWN.value,
            "gray_circle": BasicColors.GRAY.value,
            "white_circle": BasicColors.WHITE.value,
            "black_square": BasicColors.BLACK.value,
            "red_circle": ThemeColors.RED.value,
            "orange_circle": ThemeColors.ORANGE.value,
        }
        color = fallback_colors.get(fallback_type, BasicColors.GRAY.value)

        if "circle" in fallback_type:
            pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2 - 2)
        elif "square" in fallback_type:
            pygame.draw.rect(surface, color, (size // 4, size // 4, size // 2, size // 2), border_radius=8)

        return surface

    def start_new_game(self):
        """Tworzy nowy puzzle na podstawie ustawien z menu."""
        generator = BoardGenerator(self.settings.size)
        generated = generator.generate(remove_ratio=self.settings.remove_percent)
        self.board = generated.puzzle
        self.initial_board = generated.puzzle.clone()
        self.solution_board = generated.solution
        self.selected_cell = None
        self.hovered_cell = None
        self.history.clear()
        self.move_count = 0
        self.hints_used = 0
        self.hints_remaining = self.settings.hints_available
        self.is_won = False
        self.win_popup = None
        self.timer.start()
        self._set_status("Nowa plansza gotowa. Powodzenia!", "info")
        self.transition_alpha = 235
        self._sync_toolbar_state()

    def handle_events(self):
        """Obsluguje wszystkie zdarzenia gry."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

            toolbar_action = self.toolbar.handle_event(event)
            if toolbar_action:
                self._handle_toolbar_action(toolbar_action)
                continue

            if event.type == pygame.MOUSEMOTION:
                self.hovered_cell = self.board.get_cell_at_pos(
                    event.pos,
                    self.settings.grid_offset_x,
                    self.settings.grid_offset_y,
                    self.settings.cell_size,
                )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.is_won:
                    continue
                if event.button == 1:
                    self._handle_board_click(event.pos, cycle_forward=True)
                elif event.button == 3:
                    self._handle_board_click(event.pos, cycle_forward=False)

            elif event.type == pygame.KEYDOWN:
                self._handle_keyboard(event)

    def _handle_board_click(self, position: tuple[int, int], cycle_forward: bool):
        cell = self.board.get_cell_at_pos(
            position,
            self.settings.grid_offset_x,
            self.settings.grid_offset_y,
            self.settings.cell_size,
        )
        if not cell:
            return
        self.selected_cell = cell
        if cell.is_fixed:
            self._set_status("To pole jest stale i nie mozna go zmienic.", "error")
            return

        old_state = cell.state
        new_state = self._get_next_state(old_state, cycle_forward)
        if old_state == new_state:
            return

        cell.state = new_state
        self.history.record(Move(cell.row, cell.col, old_state, new_state))
        self.move_count += 1
        self._evaluate_board_after_move()

    def _get_next_state(self, state: CellState, cycle_forward: bool) -> CellState:
        if not cycle_forward:
            return CellState.EMPTY

        sequence = [CellState.EMPTY, CellState.SUN, CellState.MOON]
        index = sequence.index(state)
        return sequence[(index + 1) % len(sequence)]

    def _handle_keyboard(self, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE:
            self.running = False
        elif event.key == pygame.K_r:
            self.reset_board()
        elif event.key == pygame.K_u:
            self.undo()
        elif event.key == pygame.K_y:
            self.redo()
        elif event.key == pygame.K_h:
            self.use_hint()
        elif event.key == pygame.K_c:
            self.check_board()
        elif event.key == pygame.K_n:
            self.start_new_game()

    def _handle_toolbar_action(self, action: str):
        if action == "undo":
            self.undo()
        elif action == "redo":
            self.redo()
        elif action == "hint":
            self.use_hint()
        elif action == "check":
            self.check_board()
        elif action == "reset":
            self.reset_board()
        elif action == "new_game":
            self.start_new_game()

    def undo(self):
        """Cofa ostatni ruch."""
        move = self.history.pop_undo()
        if not move:
            self._set_status("Brak ruchow do cofniecia.", "info")
            return

        cell = self.board.get_cell(move.row, move.col)
        cell.state = move.previous_state
        self.move_count = max(0, self.move_count - 1)
        self.is_won = False
        self.win_popup = None
        self._set_status("Cofnieto ostatni ruch.", "info")
        self._sync_toolbar_state()

    def redo(self):
        """Ponawia cofnięty ruch."""
        move = self.history.pop_redo()
        if not move:
            self._set_status("Brak ruchow do ponowienia.", "info")
            return

        cell = self.board.get_cell(move.row, move.col)
        cell.state = move.new_state
        self.move_count += 1
        self._evaluate_board_after_move()

    def reset_board(self):
        """Przywraca plansze do stanu poczatkowego."""
        self.board.fill_from(self.initial_board)
        self.history.clear()
        self.move_count = 0
        self.hints_used = 0
        self.hints_remaining = self.settings.hints_available
        self.is_won = False
        self.win_popup = None
        self.timer.start()
        self._set_status("Plansza zostala zresetowana.", "info")
        self._sync_toolbar_state()

    def use_hint(self):
        """Uzupelnia jedno pole zgodnie z rozwiazaniem."""
        if self.hints_remaining <= 0:
            self._set_status("Nie masz juz podpowiedzi.", "error")
            return
        hint = self.solver.next_hint(self.board, self.solution_board)
        if not hint:
            self._set_status("Nie ma juz sensownej podpowiedzi do pokazania.", "info")
            return

        cell = self.board.get_cell(hint.row, hint.col)
        previous = cell.state
        cell.state = hint.state
        self.history.record(Move(hint.row, hint.col, previous, hint.state))
        self.move_count += 1
        self.hints_remaining -= 1
        self.hints_used += 1
        self._set_status(f"Podpowiedz: wiersz {hint.row + 1}, kolumna {hint.col + 1}.", "info")
        self._evaluate_board_after_move()

    def check_board(self):
        """Sprawdza aktualny stan planszy."""
        if Validator.is_board_valid(self.board):
            if self.board.is_complete():
                self._handle_win()
            else:
                self._set_status("Plansza jest na razie poprawna. Mozesz grac dalej.", "success")
        else:
            errors = Validator.get_errors(self.board)
            message = errors[0].message if errors else "Plansza lamie jedna z zasad."
            self._set_status(message, "error")
        self._sync_toolbar_state()

    def _evaluate_board_after_move(self):
        if not Validator.is_board_valid(self.board):
            self._set_status("Na planszy pojawil sie konflikt. Sprawdz czerwone pola.", "error")
        else:
            self._set_status("Ruch zapisany.", "info")

        if self.board.is_complete() and Validator.is_board_valid(self.board):
            self._handle_win()

        self._sync_toolbar_state()

    def _handle_win(self):
        if self.is_won:
            return
        self.is_won = True
        self.timer.pause()
        self.win_popup = WinPopup(
            self.screen,
            time_text=self.timer.formatted,
            move_count=self.move_count,
            hints_used=self.hints_used,
        )
        self._set_status("Plansza rozwiazana perfekcyjnie. Gratulacje!", "success")
        self._sync_toolbar_state()

    def _set_status(self, message: str, kind: str):
        self.status_message = message
        self.status_kind = kind

    def _sync_toolbar_state(self):
        self.toolbar.set_button_enabled("undo", self.history.can_undo and not self.is_won)
        self.toolbar.set_button_enabled("redo", self.history.can_redo and not self.is_won)
        self.toolbar.set_button_enabled("hint", self.hints_remaining > 0 and not self.is_won)
        self.toolbar.set_button_enabled("check", not self.is_won)
        self.toolbar.set_button_enabled("reset", not self.is_won)

    def draw(self):
        """Renderuje wszystkie elementy gry."""
        if self.transition_alpha > 0:
            self.transition_alpha = max(0, self.transition_alpha - 14)

        self.renderer.draw(
            board=self.board,
            icons=self.icons,
            toolbar=self.toolbar,
            timer_text=self.timer.formatted,
            hints_remaining=self.hints_remaining,
            move_count=self.move_count,
            selected_cell=self.selected_cell,
            hovered_cell=self.hovered_cell,
            status_message=self.status_message,
            status_kind=self.status_kind,
            win_popup=self.win_popup,
            transition_alpha=self.transition_alpha,
        )

    def run_game(self):
        """Glowna petla gry."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(self.settings.fps)

        pygame.quit()
        sys.exit()
