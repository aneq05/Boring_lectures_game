from src.config import BoardSize, Difficulty, GameSettings


class TestWinPopup:
    def test_settings_creation(self):
        settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        assert settings is not None
