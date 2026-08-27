from __future__ import annotations

import pygame


class AppStyle:
    BG_TOP = (255, 235, 244)
    BG_BOTTOM = (255, 251, 243)
    DECORATION = (255, 215, 229)
    CARD = (255, 255, 255)
    CARD_BORDER = (245, 209, 226)
    TITLE = (144, 72, 110)
    TEXT = (66, 61, 81)
    MUTED = (122, 116, 140)
    ACCENT = (255, 132, 164)
    ACCENT_HOVER = (255, 102, 145)
    ACCENT_SOFT = (255, 220, 234)
    SUCCESS = (111, 193, 157)
    DANGER = (241, 112, 136)
    SHADOW = (236, 190, 210)

    @staticmethod
    def font(size: int, bold: bool = False, italic: bool = False) -> pygame.font.Font:
        return pygame.font.SysFont("Segoe UI", size, bold=bold, italic=italic)

    @staticmethod
    def draw_vertical_gradient(
        surface: pygame.Surface,
        top_color: tuple[int, int, int],
        bottom_color: tuple[int, int, int],
    ):
        width, height = surface.get_size()
        for y in range(height):
            t = y / max(1, height - 1)
            color = (
                int(top_color[0] + (bottom_color[0] - top_color[0]) * t),
                int(top_color[1] + (bottom_color[1] - top_color[1]) * t),
                int(top_color[2] + (bottom_color[2] - top_color[2]) * t),
            )
            pygame.draw.line(surface, color, (0, y), (width, y))

    @staticmethod
    def draw_shadowed_rect(
        surface: pygame.Surface,
        rect: pygame.Rect,
        color: tuple[int, int, int],
        border_color: tuple[int, int, int],
        radius: int,
        shadow_offset: int = 5,
    ):
        shadow_rect = rect.move(0, shadow_offset)
        pygame.draw.rect(surface, AppStyle.SHADOW, shadow_rect, border_radius=radius)
        pygame.draw.rect(surface, color, rect, border_radius=radius)
        pygame.draw.rect(surface, border_color, rect, 2, border_radius=radius)
