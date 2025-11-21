"""
Game Manager - główna logika gry i pętla zdarzeń
"""
import pygame
import sys
import os
import logging
from typing import Optional

from src.board.board import Board
from src.board.grind_renderer import GridRenderer
from src.cell.cell_setup import Cell, CellState
from src.config import GameSettings, GameConfig
from src.utils.colors import ThemeColors, BasicColors, UIColors




class Game:
    """
    Główna klasa zarządzająca grą.

    Attributes:
        screen: Powierzchnia pygame do renderowania
        clock: Zegar pygame dla kontroli FPS
        board (Board): Plansza gry
        running (bool): Czy gra jest aktywna
        selected_cell (Optional[Cell]): Aktualnie wybrana komórka
    """

    def __init__(self, settings: GameSettings):
        """
        Inicjalizacja gry.

        Args:
            settings (GameSettings): Ustawienia gry wybrane w menu
            
        Note:
            pygame.init() powinno być wywołane wcześniej w main.py,
            przed utworzeniem instancji Game.
        """
        self.settings = settings
        self.screen = pygame.display.set_mode(
            (self.settings.window_width, self.settings.window_height)
        )
        pygame.display.set_caption("Let Me Tango - Puzzle Game")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        self.board = Board(self.settings.size)
        self.selected_cell: Optional[Cell] = None
        self.running = True

        # Inicjalizacja renderera siatki
        self.grid_renderer = GridRenderer()

        self.load_icons()

        # Przykładowa plansza (tymczasowo - będzie generator)
        self._setup_example_board()

        print(f"🎮 Gra zainicjalizowana z ustawieniami: {self.settings}")

    def load_icons(self):
        """Ładuje ikony według wybranego motywu."""
        theme_info = GameConfig.THEME_SETTINGS[self.settings.theme]
        icon_path = os.path.join("assets", "images", "icons")

        try:
            icon1_path = os.path.join(icon_path, theme_info["icon1"])
            icon2_path = os.path.join(icon_path, theme_info["icon2"])

            self.icon1 = pygame.image.load(icon1_path)
            self.icon2 = pygame.image.load(icon2_path)

            # Scaling the icons
            icon_size = int(self.settings.cell_size * self.settings.icon_scale)
            self.icon1 = pygame.transform.scale(self.icon1, (icon_size, icon_size))
            self.icon2 = pygame.transform.scale(self.icon2, (icon_size, icon_size))

            logging.debug(f"Icons loaded: {theme_info['name']}")

        except Exception as e:
            logging.error(f"Error loading icons: {e}")
            logging.debug(f"  Using the fallback motive: {theme_info['name']}")

            # Creating the fallback of the icons
            icon_size = int(self.settings.cell_size * self.settings.icon_scale)
            self.icon1 = self._create_fallback_icon(icon_size, theme_info["icon1_fallback"])
            self.icon2 = self._create_fallback_icon(icon_size, theme_info["icon2_fallback"])

    def _create_fallback_icon(self, size: int, fallback_type: str) -> pygame.Surface:
        """
        Tworzy zapasową ikonę, jeśli plik obrazu nie może zostać załadowany.
        Używa kolorów zdefiniowanych w colors.py.
        
        Args:
            size: Rozmiar ikony w pikselach
            fallback_type: Typ ikony (np. "yellow_circle", "blue_circle")
            
        Returns:
            pygame.Surface z narysowaną zapasową ikoną
        """
        surface = pygame.Surface((size, size), pygame.SRCALPHA)

        # Mapowanie fallback typów na kolory z colors.py
        fallback_colors = {
            "yellow_circle": ThemeColors.YELLOW.value,
            "blue_circle": ThemeColors.BLUE.value,
            "brown_circle": ThemeColors.BROWN.value,
            "gray_circle": BasicColors.GRAY.value,
            "white_circle": BasicColors.WHITE.value,
            "black_square": BasicColors.BLACK.value,
            "red_circle": ThemeColors.RED.value,
            "orange_circle": ThemeColors.ORANGE.value
        }

        color = fallback_colors.get(fallback_type, BasicColors.GRAY.value)

        if "circle" in fallback_type:
            pygame.draw.circle(surface, color, (size // 2, size // 2), size // 2)
        elif "square" in fallback_type:
            pygame.draw.rect(surface, color, (size // 4, size // 4, size // 2, size // 2))

        return surface

    def _setup_example_board(self):
        """Ustawia przykładową planszę do testowania."""
        # Dodaj kilka stałych komórek jako przykład
        self.board.cells[0][0].state = CellState.STATE_A
        self.board.cells[0][0].is_fixed = True

        self.board.cells[1][1].state = CellState.STATE_B
        self.board.cells[1][1].is_fixed = True

        self.board.cells[2][2].state = CellState.STATE_A
        self.board.cells[2][2].is_fixed = True

        self.board.cells[3][3].state = CellState.STATE_B
        self.board.cells[3][3].is_fixed = True

    def handle_events(self):
        """Obsługuje wszystkie zdarzenia (klawiatura, mysz, etc.)."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Lewy przycisk myszy
                    cell = self.board.get_cell_at_pos(
                        event.pos,
                        self.settings.grid_offset_x,
                        self.settings.grid_offset_y,
                        self.settings.cell_size
                    )
                    if cell:
                        self.selected_cell = cell
                        cell.toggle()

            elif event.type == pygame.KEYDOWN:
                # Skróty klawiszowe
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    # Reset planszy
                    self.board.clear()

    def draw(self):
        """Renderuje wszystkie elementy gry."""
        self.screen.fill(UIColors.BACKGROUND.value)

        # Tytuł
        title = self.font.render("Let Me Tango", True, UIColors.TEXT_COLOR.value)
        title_rect = title.get_rect(center=(self.settings.window_width // 2, 40))
        self.screen.blit(title, title_rect)

        # Instrukcje
        instruction = self.small_font.render(
            "Kliknij komórkę: pusty → A → B → pusty",
            True,
            BasicColors.DARK_GRAY.value
        )
        inst_rect = instruction.get_rect(center=(self.settings.window_width // 2, 80))
        self.screen.blit(instruction, inst_rect)

        # Rysuj siatkę używając GridRenderer
        self.grid_renderer.render_grid(
            screen=self.screen,
            board=self.board,
            settings=self.settings,
            icon1=self.icon1,
            icon2=self.icon2
        )

        # Rysuj zasady na dole
        self._draw_rules()

        pygame.display.flip()

    def _draw_rules(self):
        """Rysuje zasady gry na dole ekranu."""
        info_y = self.settings.grid_offset_y + self.board.size * self.settings.cell_size + 30

        rules = [
            "Zasady:",
            "• Równa liczba symboli A i B w wierszach i kolumnach",
            "• Nie może być 3 takich samych obok siebie",
            "",
            "Skróty: R - reset, ESC - wyjście"
        ]

        for i, rule in enumerate(rules):
            text = self.small_font.render(rule, True, BasicColors.DARK_GRAY.value)
            self.screen.blit(text, (50, info_y + i * 25))

    def run_game(self):
        """Główna pętla gry."""
        print("🎮 Let Me Tango - Gra rozpoczęta!")
        print(f"📋 Rozmiar planszy: {self.board.size}x{self.board.size}")

        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(self.settings.fps)

        print("👋 Gra zakończona!")
        pygame.quit()
        sys.exit()

