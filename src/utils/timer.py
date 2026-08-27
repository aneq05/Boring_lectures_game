from __future__ import annotations

import time

class GameTimer:
    def __init__(self):
        self._started_at: float | None = None
        self._paused_at: float | None = None
        self._accumulated_pause = 0.0

    def start(self):
        self._started_at = time.perf_counter()
        self._paused_at = None
        self._accumulated_pause = 0.0

    def pause(self):
        if self._started_at is not None and self._paused_at is None:
            self._paused_at = time.perf_counter()

    def resume(self):
        if self._paused_at is not None:
            self._accumulated_pause += time.perf_counter() - self._paused_at
            self._paused_at = None

    def reset(self):
        self._started_at = None
        self._paused_at = None
        self._accumulated_pause = 0.0

    @property
    def elapsed_seconds(self) -> int:
        if self._started_at is None:
            return 0

        current = self._paused_at if self._paused_at is not None else time.perf_counter()
        return max(0, int(current - self._started_at - self._accumulated_pause))

    @property
    def formatted(self) -> str:
        total = self.elapsed_seconds
        minutes, seconds = divmod(total, 60)
        return f"{minutes:02d}:{seconds:02d}"
