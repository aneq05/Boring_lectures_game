"""
Grid Renderer - moduł odpowiedzialny za renderowanie siatki planszy
"""
import pygame
from typing import TYPE_CHECKING

from src.utils.colors import UIColors
from src.cell.cell_setup import CellState

if TYPE_CHECKING:
    from src.board.board import Board
    from src.config import GameSettings


class GridRenderer:
    def render_grid(self, screen, board, settings, icon1, icon2):
        """Renderuje całą siatkę planszy."""
        for row in range(board.size):
            for col in range(board.size):
                cell = board.cells[row][col]
                x = settings.grid_offset_x + col * settings.cell_size
                y = settings.grid_offset_y + row * settings.cell_size

                self._render_one_cell(screen, cell, x, y, settings.cell_size, 
                                 icon1, icon2, board.check_three_consecutive(row, col))
    
    def _render_one_cell(self, screen, cell, x, y, cell_size, icon1, icon2, is_valid):
        # Background
        bg_color = UIColors.FIXED_CELL_COLOR.value if cell.is_fixed else UIColors.BACKGROUND.value
        pygame.draw.rect(screen, bg_color, (x, y, cell_size, cell_size))
        
        # Frame
        border_color = UIColors.ERROR_COLOR.value if not is_valid else UIColors.BORDER_COLOR.value
        border_width = 3 if not is_valid else 2
        pygame.draw.rect(screen, border_color, (x, y, cell_size, cell_size), border_width)
        
        # Icons
        icon = icon1 if cell.state == CellState.STATE_A else icon2 if cell.state == CellState.STATE_B else None
        if icon:
            icon_x = x + (cell_size - icon.get_width()) // 2
            icon_y = y + (cell_size - icon.get_height()) // 2
            screen.blit(icon, (icon_x, icon_y))
