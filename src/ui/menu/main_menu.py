"""
Main menu orchestration.
"""
from __future__ import annotations

from typing import Optional

import pygame

from src.config import BoardSize, Difficulty, GameConfig, GameSettings, Theme
from src.ui.menu.components import Button, InfoBox, Label, Selector
from src.ui.menu.events import MenuEventHandler
from src.ui.menu.renderer import MenuRenderer
from src.ui.style import AppStyle


class MainMenu:
    """Coordinates menu components and selected game options."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False

        self.selected_difficulty = GameConfig.DEFAULT_DIFFICULTY
        self.selected_board_size = GameConfig.DEFAULT_BOARD_SIZE
        self.selected_theme = GameConfig.DEFAULT_THEME

        self.event_handler = MenuEventHandler()
        self.renderer = MenuRenderer(screen)
        self.components = []
        self._create_ui_components()

    def _create_ui_components(self):
        screen_width = self.screen.get_width()
        card_center_x = screen_width // 2
        card_left = card_center_x - 230
        width = 460

        self.title_label = Label(
            card_center_x,
            86,
            "Let Me Tango",
            font_size=70,
            color=AppStyle.TITLE,
            centered=True,
            bold=True,
        )

        self.subtitle_label = Label(
            card_center_x,
            128,
            "A cozy logic puzzle",
            font_size=30,
            color=AppStyle.MUTED,
            centered=True,
        )

        self.difficulty_selector = Selector(
            x=card_left,
            y=170,
            width=width,
            height=92,
            label="Difficulty",
            options=list(Difficulty),
            option_display=lambda d: GameConfig.get_difficulty_name(d),
            initial_index=list(Difficulty).index(self.selected_difficulty),
            on_change=self._on_difficulty_change,
        )

        self.size_selector = Selector(
            x=card_left,
            y=276,
            width=width,
            height=92,
            label="Board size",
            options=list(BoardSize),
            option_display=lambda s: GameConfig.BOARD_SIZE_SETTINGS[s]["name"],
            initial_index=list(BoardSize).index(self.selected_board_size),
            on_change=self._on_size_change,
        )

        self.theme_selector = Selector(
            x=card_left,
            y=382,
            width=width,
            height=92,
            label="Theme",
            options=list(Theme),
            option_display=lambda t: GameConfig.get_theme_name(t),
            initial_index=list(Theme).index(self.selected_theme),
            on_change=self._on_theme_change,
        )

        self.info_box = InfoBox(
            x=card_left,
            y=492,
            width=width,
            height=118,
            title="Session info",
            text=self._get_info_text(),
        )

        self.start_button = Button(
            x=card_center_x - 120,
            y=632,
            width=240,
            height=66,
            text="Start game",
            callback=self._start_game,
            color=AppStyle.ACCENT,
            hover_color=AppStyle.ACCENT_HOVER,
            font_size=40,
        )

        self.components = [
            self.title_label,
            self.subtitle_label,
            self.difficulty_selector,
            self.size_selector,
            self.theme_selector,
            self.info_box,
            self.start_button,
        ]

    def _get_info_text(self) -> str:
        diff_info = GameConfig.DIFFICULTY_SETTINGS[self.selected_difficulty]
        size_info = GameConfig.BOARD_SIZE_SETTINGS[self.selected_board_size]
        return (
            f"{diff_info['description']}\n"
            f"{size_info['description']}\n"
            f"Hints available: {diff_info['hints_available']}"
        )

    def _on_difficulty_change(self, difficulty: Difficulty):
        self.selected_difficulty = difficulty
        self.info_box.set_content("Session info", self._get_info_text())

    def _on_size_change(self, board_size: BoardSize):
        self.selected_board_size = board_size
        self.info_box.set_content("Session info", self._get_info_text())

    def _on_theme_change(self, theme: Theme):
        self.selected_theme = theme
        self.info_box.set_content("Session info", self._get_info_text())

    def _start_game(self):
        self.game_started = True
        self.running = False

    def run_main_menu(self) -> Optional[GameSettings]:
        while self.running:
            selectors_list = [self.difficulty_selector, self.size_selector, self.theme_selector]
            action = self.event_handler.handle_events(self.components, selectors_list, self.start_button)

            if action["quit"]:
                return None
            if action["start_game"]:
                self._start_game()

            self.renderer.render(self.components)
            self.clock.tick(60)

        if self.game_started:
            self.renderer.play_exit_transition(self.components)
            return GameSettings(
                difficulty=self.selected_difficulty,
                board_size=self.selected_board_size,
                theme=self.selected_theme,
            )

        return None
