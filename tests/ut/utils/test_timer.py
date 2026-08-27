import time
from src.utils.timer import GameTimer


class TestGameTimer:
    def test_initialization(self):
        timer = GameTimer()
        assert timer.elapsed_seconds == 0

    def test_start_and_elapsed(self):
        timer = GameTimer()
        timer.start()
        time.sleep(0.05)
        assert timer.elapsed_seconds >= 0

    def test_pause(self):
        timer = GameTimer()
        timer.start()
        time.sleep(0.02)
        timer.pause()
        paused_time = timer.elapsed_seconds
        time.sleep(0.02)
        assert timer.elapsed_seconds == paused_time

    def test_reset(self):
        timer = GameTimer()
        timer.start()
        time.sleep(0.05)
        timer.reset()
        assert timer.elapsed_seconds == 0

    def test_formatted(self):
        timer = GameTimer()
        timer.start()
        time.sleep(0.05)
        formatted = timer.formatted
        assert ":" in formatted
        parts = formatted.split(":")
        assert len(parts) == 2
        assert parts[0].isdigit()
        assert parts[1].isdigit()
