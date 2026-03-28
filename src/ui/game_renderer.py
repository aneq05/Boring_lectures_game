"""
Renderer for the gameplay screen.
"""
from __future__ import annotations

import math

import pygame

from src.core.validator import Validator
from src.ui.style import AppStyle
from src.utils.colors import UIColors


class GameRenderer:
    """Draws board, side panel and contextual status for gameplay."""

    def __init__(self, screen: pygame.Surface, settings):
        self.screen = screen
        self.settings = settings
        self.title_font = AppStyle.font(44, bold=True)
        self.heading_font = AppStyle.font(30, bold=True)
        self.body_font = AppStyle.font(25, bold=True)
        self.small_font = AppStyle.font(21)
        self.frame = 0

    def draw(
        self,
        board,
        icons,
        toolbar,
        timer_text: str,
        hints_remaining: int,
        move_count: int,
        selected_cell,
        hovered_cell,
        status_message: str,
        status_kind: str,
        win_popup=None,
        transition_alpha: int = 0,
    ):
        self.frame += 1
        self._draw_background()
        self._draw_header(timer_text, hints_remaining, move_count)
        self._draw_board(board, icons, selected_cell, hovered_cell)
        self._draw_sidebar(board, status_message, status_kind)
        toolbar.draw(self.screen)

        if win_popup:
            win_popup.draw(self.screen)

        if transition_alpha > 0:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((255, 245, 250, transition_alpha))
            self.screen.blit(overlay, (0, 0))

        pygame.display.flip()

    def _draw_background(self):
        AppStyle.draw_vertical_gradient(self.screen, (255, 236, 245), (255, 251, 246))
        w, h = self.screen.get_size()
        t = self.frame / 50.0
        blobs = [
            (int(w * 0.1 + math.sin(t) * 9), int(h * 0.15), 95),
            (int(w * 0.92 + math.sin(t * 0.8) * 8), int(h * 0.22), 85),
            (int(w * 0.84 + math.sin(t * 0.7) * 10), int(h * 0.86), 130),
        ]
        for x, y, radius in blobs:
            pygame.draw.circle(self.screen, (255, 221, 234), (x, y), radius)

    def _draw_header(self, timer_text: str, hints_remaining: int, move_count: int):
        title = self.title_font.render("Let Me Tango", True, AppStyle.TITLE)
        self.screen.blit(title, (40, 24))

        subtitle = self.small_font.render("Fill the board with balanced symbols", True, AppStyle.MUTED)
        self.screen.blit(subtitle, (42, 70))

        chips = [
            (f"Time {timer_text}", self.settings.window_width - 250),
            (f"Moves {move_count}", self.settings.window_width - 430),
            (f"Hints {hints_remaining}", self.settings.window_width - 600),
        ]
        for text_value, x in chips:
            rect = pygame.Rect(x, 24, 152, 44)
            AppStyle.draw_shadowed_rect(
                surface=self.screen,
                rect=rect,
                color=(255, 255, 255),
                border_color=AppStyle.CARD_BORDER,
                radius=20,
                shadow_offset=3,
            )
            text = self.small_font.render(text_value, True, AppStyle.TEXT)
            self.screen.blit(text, text.get_rect(center=rect.center))

    def _draw_board(self, board, icons, selected_cell, hovered_cell):
        grid_rect = pygame.Rect(
            self.settings.grid_offset_x - 16,
            self.settings.grid_offset_y - 16,
            self.settings.size * self.settings.cell_size + 32,
            self.settings.size * self.settings.cell_size + 32,
        )
        AppStyle.draw_shadowed_rect(
            surface=self.screen,
            rect=grid_rect,
            color=UIColors.GRID_BACKGROUND.value,
            border_color=AppStyle.CARD_BORDER,
            radius=26,
            shadow_offset=6,
        )

        errors = {
            (row, col)
            for row, col in board.iter_positions()
            if not Validator.validate_three_consecutive(board, row, col)
        }

        for row in range(board.size):
            for col in range(board.size):
                cell = board.cells[row][col]
                x = self.settings.grid_offset_x + col * self.settings.cell_size
                y = self.settings.grid_offset_y + row * self.settings.cell_size
                rect = pygame.Rect(x, y, self.settings.cell_size, self.settings.cell_size)

                color = UIColors.PANEL_BACKGROUND.value
                if cell.is_fixed:
                    color = UIColors.FIXED_CELL_COLOR.value
                if hovered_cell is cell and not cell.is_fixed:
                    color = UIColors.HOVER_COLOR.value
                if selected_cell is cell:
                    color = UIColors.SELECTED_COLOR.value

                pygame.draw.rect(self.screen, color, rect, border_radius=14)
                border_color = AppStyle.CARD_BORDER
                border_width = 2
                if (row, col) in errors:
                    border_color = UIColors.ERROR_COLOR.value
                    border_width = 3
                pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=14)

                icon = icons.get(cell.state)
                if icon:
                    icon_x = x + (self.settings.cell_size - icon.get_width()) // 2
                    icon_y = y + (self.settings.cell_size - icon.get_height()) // 2
                    self.screen.blit(icon, (icon_x, icon_y))

        for line in range(2, board.size, 2):
            x = self.settings.grid_offset_x + line * self.settings.cell_size
            y = self.settings.grid_offset_y + line * self.settings.cell_size
            pygame.draw.line(
                self.screen,
                (252, 188, 213),
                (x, self.settings.grid_offset_y),
                (x, self.settings.grid_offset_y + board.size * self.settings.cell_size),
                3,
            )
            pygame.draw.line(
                self.screen,
                (252, 188, 213),
                (self.settings.grid_offset_x, y),
                (self.settings.grid_offset_x + board.size * self.settings.cell_size, y),
                3,
            )

    def _draw_sidebar(self, board, status_message: str, status_kind: str):
        panel_rect = pygame.Rect(
            self.settings.sidebar_x,
            self.settings.grid_offset_y,
            self.settings.sidebar_width,
            self.settings.sidebar_height,
        )
        AppStyle.draw_shadowed_rect(
            surface=self.screen,
            rect=panel_rect,
            color=AppStyle.CARD,
            border_color=AppStyle.CARD_BORDER,
            radius=24,
            shadow_offset=6,
        )

        heading = self.heading_font.render("Rules", True, AppStyle.TITLE)
        self.screen.blit(heading, (panel_rect.x + 22, panel_rect.y + 18))

        rules = [
            "1. Every row/column needs",
            "   the same number of both icons.",
            "2. No three identical symbols",
            "   next to each other.",
            "3. Filled rows/columns",
            "   cannot be identical.",
        ]
        y = panel_rect.y + 58
        for line in rules:
            text = self.small_font.render(line, True, AppStyle.MUTED)
            self.screen.blit(text, (panel_rect.x + 22, y))
            y += 23

        status_title = self.heading_font.render("Status", True, AppStyle.TITLE)
        self.screen.blit(status_title, (panel_rect.x + 22, y + 16))

        status_color = AppStyle.TEXT
        if status_kind == "success":
            status_color = AppStyle.SUCCESS
        elif status_kind == "error":
            status_color = AppStyle.DANGER

        wrapped = self._wrap_text(status_message or "Play at your own pace.", 30)
        sy = y + 50
        for line in wrapped[:5]:
            text = self.small_font.render(line, True, status_color)
            self.screen.blit(text, (panel_rect.x + 22, sy))
            sy += 22

        footer = self.body_font.render(f"Empty cells: {board.count_empty()}", True, AppStyle.TEXT)
        self.screen.blit(footer, (panel_rect.x + 22, panel_rect.bottom - 50))

    def _wrap_text(self, text: str, width: int) -> list[str]:
        words = text.split()
        if not words:
            return [""]

        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = f"{current} {word}"
            if len(candidate) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines
