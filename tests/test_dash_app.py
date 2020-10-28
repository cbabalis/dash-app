import unittest
from dash_app import dash_app


class TestDashApp(unittest.TestCase):
    
    def test_read_xlsx(self):
        xlsx_file = '../PROJECT_MATERIAL/nikos_data.xlsx'
        xlsx_contents = dash_app.read_xlsx(xlsx_file)
        assert isinstance(xlsx_contents, dict)


if __name__ == '__main__':
    unittest.main()