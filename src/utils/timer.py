"""
Sesyjny timer gry.
"""
from __future__ import annotations

import time


class GameTimer:
    """Mierzy czas aktywnej rozgrywki."""

    def __init__(self):
        self._started_at: float | None = None
        self._paused_at: float | None = None
        self._accumulated_pause = 0.0

    def start(self):
        """Uruchamia timer od zera."""
        self._started_at = time.perf_counter()
        self._paused_at = None
        self._accumulated_pause = 0.0

    def pause(self):
        """Wstrzymuje timer."""
        if self._started_at is not None and self._paused_at is None:
            self._paused_at = time.perf_counter()

    def resume(self):
        """Wznawia timer po pauzie."""
        if self._paused_at is not None:
            self._accumulated_pause += time.perf_counter() - self._paused_at
            self._paused_at = None

    def reset(self):
        """Czyści stan timera."""
        self._started_at = None
        self._paused_at = None
        self._accumulated_pause = 0.0

    @property
    def elapsed_seconds(self) -> int:
        """Zwraca liczbe sekund od startu z uwzglednieniem pauz."""
        if self._started_at is None:
            return 0

        current = self._paused_at if self._paused_at is not None else time.perf_counter()
        return max(0, int(current - self._started_at - self._accumulated_pause))

    @property
    def formatted(self) -> str:
        """Zwraca czas w formacie MM:SS."""
        total = self.elapsed_seconds
        minutes, seconds = divmod(total, 60)
        return f"{minutes:02d}:{seconds:02d}"
