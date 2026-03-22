"""
Let Me Tango - Główny punkt wejścia do gry.

Ten moduł inicjalizuje pygame i zarządza przepływem między menu a grą.
"""
import pygame
from src.ui.menu import MainMenu
from src.game_manager import Game


def main():
    """
    Główna funkcja uruchamiająca aplikację.
    
    Inicjalizuje pygame (tylko raz!), tworzy menu, a następnie uruchamia grę
    z wybranymi przez użytkownika ustawieniami.
    """
    # Inicjalizacja pygame - TYLKO RAZ na początku aplikacji
    pygame.init()
    
    # Utwórz okno menu
    screen = pygame.display.set_mode((600, 700))
    pygame.display.set_caption("Let Me Tango - Menu")

    menu = MainMenu(screen)
    settings = menu.run_main_menu()

    # Jeśli użytkownik wybrał START (nie ESC)
    if settings:
        # Uruchom grę z wybranymi ustawieniami
        game = Game(settings)
        game.run_game()
    else:
        print("👋 Zamknięto menu bez startu gry")


if __name__ == "__main__":
    main()

