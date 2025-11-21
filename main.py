"""
Let Me Tango - Główny punkt wejścia do gry.

Ten moduł inicjalizuje pygame i zarządza przepływem między menu a grą.
"""
import pygame
from src.ui.menu import MainMenu
from src.game_manager import Game


def main():
    pygame.init()

    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Let Me Tango - Menu")

    menu = MainMenu(screen)
    settings = menu.run_main_menu()

    if settings:
        game = Game(settings)
        game.run_game()
    else:
        print("👋 Zamknięto menu bez startu gry")


if __name__ == "__main__":
    main()

