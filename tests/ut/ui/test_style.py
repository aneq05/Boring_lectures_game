from src.ui.style import AppStyle


class TestAppStyle:
    def test_color_values(self):
        assert AppStyle.BG_TOP == (255, 235, 244)
        assert AppStyle.BG_BOTTOM == (255, 251, 243)
        assert AppStyle.TITLE == (144, 72, 110)
        assert AppStyle.TEXT == (66, 61, 81)
        assert AppStyle.ACCENT == (255, 132, 164)
