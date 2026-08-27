from src.utils.colors import BasicColors, ThemeColors, UIColors


class TestBasicColors:
    def test_white_color(self):
        assert BasicColors.WHITE.value == (255, 255, 255)

    def test_black_color(self):
        assert BasicColors.BLACK.value == (48, 47, 61)

    def test_gray_color(self):
        assert BasicColors.GRAY.value == (176, 175, 190)


class TestThemeColors:
    def test_light_blue_color(self):
        assert ThemeColors.LIGHT_BLUE.value == (212, 236, 255)

    def test_yellow_color(self):
        assert ThemeColors.YELLOW.value == (255, 214, 166)

    def test_red_color(self):
        assert ThemeColors.RED.value == (255, 124, 146)


class TestUIColors:
    def test_background_color(self):
        assert UIColors.BACKGROUND.value == (255, 245, 249)

    def test_text_color_tuple_values(self):
        assert UIColors.TEXT_COLOR.value == (48, 47, 61)
