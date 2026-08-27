from src.config import Difficulty, BoardSize, Theme, GameSettings


class TestGameSettings:
    def test_initialization_defaults(self):
        settings = GameSettings()
        assert settings.difficulty == Difficulty.MEDIUM
        assert settings.board_size == BoardSize.MEDIUM
        assert settings.theme == Theme.SUN_MOON

    def test_size_computed_from_board_size(self):
        settings = GameSettings(board_size=BoardSize.SMALL)
        assert settings.size == 4
        
        settings = GameSettings(board_size=BoardSize.LARGE)
        assert settings.size == 8

    def test_remove_percent_computed_from_difficulty(self):
        easy = GameSettings(difficulty=Difficulty.EASY)
        assert easy.remove_percent == 0.40
        
        expert = GameSettings(difficulty=Difficulty.EXPERT)
        assert expert.remove_percent == 0.75

    def test_hints_available_from_difficulty(self):
        easy = GameSettings(difficulty=Difficulty.EASY)
        assert easy.hints_available == 5
        
        expert = GameSettings(difficulty=Difficulty.EXPERT)
        assert expert.hints_available == 1

    def test_cell_size_from_board_size(self):
        small = GameSettings(board_size=BoardSize.SMALL)
        assert small.cell_size == 100
        
        xlarge = GameSettings(board_size=BoardSize.XLARGE)
        assert xlarge.cell_size == 50

    def test_window_dimensions(self):
        settings = GameSettings()
        assert settings.window_width == 1024
        assert settings.window_height == 760
        assert settings.fps == 60

    def test_grid_offsets_computed(self):
        settings = GameSettings(board_size=BoardSize.SMALL)
        assert settings.grid_offset_x == 48
        assert settings.grid_offset_y == 130
        assert settings.sidebar_x > 0
        assert settings.sidebar_width > 0
