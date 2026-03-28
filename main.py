"""
Application entry point.
"""
from __future__ import annotations

import pygame

from src.game_manager import Game
from src.ui.menu import MainMenu


def main():
    pygame.init()

    screen = pygame.display.set_mode((1024, 760))
    pygame.display.set_caption("Let Me Tango - Menu")

    menu = MainMenu(screen)
    settings = menu.run_main_menu()

    if settings:
        game = Game(settings)
        game.run_game()


if __name__ == "__main__":
    main()
