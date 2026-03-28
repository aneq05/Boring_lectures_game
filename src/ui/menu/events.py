"""
Menu event handling with keyboard navigation.
"""
from __future__ import annotations

from typing import List

import pygame


class MenuEventHandler:
    """Processes menu events and focus transitions."""

    def __init__(self):
        self.focused_index = 0
        self.max_focusable = 4

    def handle_events(self, components: List, selectors: List, start_button) -> dict:
        self._highlight_focused_element(selectors, start_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"quit": True, "start_game": False}

            if event.type == pygame.KEYDOWN:
                action = self._handle_keyboard(event, selectors, start_button)
                if action:
                    return action

            for component in components:
                if hasattr(component, "handle_event"):
                    component.handle_event(event)

        return {"quit": False, "start_game": False}

    def _handle_keyboard(self, event: pygame.event.Event, selectors: List, start_button) -> dict:
        if event.key == pygame.K_ESCAPE:
            return {"quit": True, "start_game": False}

        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            if self.focused_index == 4:
                return {"quit": False, "start_game": True}

        if event.key in (pygame.K_DOWN, pygame.K_TAB):
            self.focused_index = (self.focused_index + 1) % (self.max_focusable + 1)
            self._highlight_focused_element(selectors, start_button)
            return {"quit": False, "start_game": False}

        if event.key == pygame.K_UP:
            self.focused_index = (self.focused_index - 1) % (self.max_focusable + 1)
            self._highlight_focused_element(selectors, start_button)
            return {"quit": False, "start_game": False}

        if event.key == pygame.K_LEFT and 0 <= self.focused_index < len(selectors):
            selector = selectors[self.focused_index]
            if selector.current_index > 0:
                selector.current_index -= 1
                if selector.on_change:
                    selector.on_change(selector.options[selector.current_index])
            return {"quit": False, "start_game": False}

        if event.key == pygame.K_RIGHT and 0 <= self.focused_index < len(selectors):
            selector = selectors[self.focused_index]
            if selector.current_index < len(selector.options) - 1:
                selector.current_index += 1
                if selector.on_change:
                    selector.on_change(selector.options[selector.current_index])
            return {"quit": False, "start_game": False}

        return {"quit": False, "start_game": False}

    def _highlight_focused_element(self, selectors: List, start_button):
        for selector in selectors:
            if hasattr(selector, "is_focused"):
                selector.is_focused = False
        if hasattr(start_button, "is_focused"):
            start_button.is_focused = False

        if 0 <= self.focused_index < len(selectors):
            if hasattr(selectors[self.focused_index], "is_focused"):
                selectors[self.focused_index].is_focused = True
        elif self.focused_index == 4 and hasattr(start_button, "is_focused"):
            start_button.is_focused = True
