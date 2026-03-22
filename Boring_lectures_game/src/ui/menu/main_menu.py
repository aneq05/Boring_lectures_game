"""
Main Menu - orkiestrator menu głównego
"""
import pygame
from typing import Optional

from src.config import GameConfig, GameSettings, Difficulty, BoardSize, Theme
from src.ui.menu.components import Button, Selector, Label, InfoBox
from src.ui.menu.events import MenuEventHandler
from src.ui.menu.renderer import MenuRenderer
from src.utils.colors import ThemeColors, BasicColors


class MainMenu:
    """
    Główna klasa menu - orkiestrator.

    Odpowiedzialność:
    - Koordynacja komponentów UI
    - Zarządzanie stanem wybranych opcji
    - Generowanie GameSettings na podstawie wyborów
    """

    def __init__(self, screen: pygame.Surface):
        """
        Inicjalizacja menu głównego.

        Args:
            screen: Powierzchnia pygame
        """
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False

        # Wybrane opcje
        self.selected_difficulty = GameConfig.DEFAULT_DIFFICULTY
        self.selected_board_size = GameConfig.DEFAULT_BOARD_SIZE
        self.selected_theme = GameConfig.DEFAULT_THEME

        # Moduły
        self.event_handler = MenuEventHandler()
        self.renderer = MenuRenderer(screen)

        # Komponenty UI
        self.components = []
        self._create_ui_components()

    def _create_ui_components(self):
        """Tworzy wszystkie komponenty UI menu."""
        screen_width = self.screen.get_width()

        # Tytuł (przesuń wyżej, zmniejsz rozmiar)
        self.title_label = Label(
            screen_width // 2, 30,
            "Let Me Tango",
            font_size=60,
            color=ThemeColors.BLUE.value,
            centered=True
        )

        # Podtytuł (bliżej tytułu, mniejszy)
        self.subtitle_label = Label(
            screen_width // 2, 85,
            "Logiczna Gra Puzzle",
            font_size=24,
            color=BasicColors.DARK_GRAY.value,
            centered=True
        )

        # Selektor trudności (wyżej, niższy)
        self.difficulty_selector = Selector(
            x=100, y=125, width=400, height=75,
            label="Poziom trudności",
            options=list(Difficulty),
            option_display=lambda d: GameConfig.get_difficulty_name(d),
            initial_index=list(Difficulty).index(self.selected_difficulty),
            on_change=self._on_difficulty_change
        )

        # Selektor rozmiaru (bliżej poprzedniego)
        self.size_selector = Selector(
            x=100, y=215, width=400, height=75,
            label="Rozmiar planszy",
            options=list(BoardSize),
            option_display=lambda s: GameConfig.BOARD_SIZE_SETTINGS[s]["name"],
            initial_index=list(BoardSize).index(self.selected_board_size),
            on_change=self._on_size_change
        )

        # Selektor motywu (bliżej poprzedniego)
        self.theme_selector = Selector(
            x=100, y=305, width=400, height=75,
            label="Motyw",
            options=list(Theme),
            option_display=lambda t: GameConfig.get_theme_name(t),
            initial_index=list(Theme).index(self.selected_theme),
            on_change=self._on_theme_change
        )

        # Info box (wyżej, niższy)
        self.info_box = InfoBox(
            x=100, y=395, width=400, height=110,
            title="Informacje",
            text=self._get_info_text()
        )

        # Przycisk START (dużo wyżej, aby nie nachodzić na instrukcje)
        self.start_button = Button(
            x=screen_width // 2 - 100, y=520,
            width=200, height=60,
            text="START",
            callback=self._start_game,
            color=ThemeColors.GREEN.value,
            hover_color=(150, 255, 150),
            font_size=40
        )

        # Lista komponentów do renderowania i obsługi zdarzeń
        self.components = [
            self.title_label,
            self.subtitle_label,
            self.difficulty_selector,
            self.size_selector,
            self.theme_selector,
            self.info_box,
            self.start_button
        ]

    def _get_info_text(self) -> str:
        """Generuje tekst informacyjny na podstawie wybranych opcji."""
        diff_info = GameConfig.DIFFICULTY_SETTINGS[self.selected_difficulty]
        size_info = GameConfig.BOARD_SIZE_SETTINGS[self.selected_board_size]

        text = f"{diff_info['description']}\n"
        text += f"{size_info['description']}\n"
        text += f"Podpowiedzi: {diff_info['hints_available']}"

        return text

    def _on_difficulty_change(self, difficulty: Difficulty):
        """Callback przy zmianie trudności."""
        self.selected_difficulty = difficulty
        self.info_box.set_content("Informacje", self._get_info_text())

    def _on_size_change(self, board_size: BoardSize):
        """Callback przy zmianie rozmiaru."""
        self.selected_board_size = board_size
        self.info_box.set_content("Informacje", self._get_info_text())

    def _on_theme_change(self, theme: Theme):
        """Callback przy zmianie motywu."""
        self.selected_theme = theme
        self.info_box.set_content("Informacje", self._get_info_text())

    def _start_game(self):
        """Callback dla przycisku START."""
        self.game_started = True
        self.running = False

    def run_main_menu(self) -> Optional[GameSettings]:
        """
        Uruchamia menu i czeka na wybór użytkownika.

        Returns:
            Optional[GameSettings]: Ustawienia gry lub None jeśli wyszedł
        """
        print("🎮 Menu główne uruchomione")
        print("💡 Nawigacja: Strzałki ↑↓ lub Tab - przełączaj | Strzałki ←→ - zmień wartość | Enter/Space - START")

        while self.running:
            # Obsługa zdarzeń (przekaż selektory i przycisk dla nawigacji klawiaturą)
            selectors_list = [self.difficulty_selector, self.size_selector, self.theme_selector]
            action = self.event_handler.handle_events(
                self.components,
                selectors_list,
                self.start_button
            )

            if action['quit']:
                return None

            if action['start_game']:
                self._start_game()

            # Renderowanie
            self.renderer.render(self.components)

            # FPS
            self.clock.tick(60)

        # Zwróć ustawienia jeśli użytkownik kliknął START
        if self.game_started:
            settings = GameSettings(
                difficulty=self.selected_difficulty,
                board_size=self.selected_board_size,
                theme=self.selected_theme
            )
            print(f"✅ Wybrano ustawienia: {settings}")
            return settings

        return None

