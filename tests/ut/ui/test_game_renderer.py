from src.config import BoardSize, Difficulty, GameSettings


class TestGameRenderer:
    def test_initialization(self):
        settings = GameSettings(board_size=BoardSize.SMALL, difficulty=Difficulty.EASY)
        assert settings is not None
