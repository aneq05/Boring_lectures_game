from src.config import BoardSize, Difficulty, GameSettings


class TestGame:
    def test_settings_creation(self):
        settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        assert settings.size == 4
