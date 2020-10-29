import unittest
from dash_app import xls_manipulation


class TestXlsManipulation(unittest.TestCase):
    
    def test_read_xlsx(self):
        xlsx_file = '../PROJECT_MATERIAL/nikos_data.xlsx'
        xlsx_contents = xls_manipulation.read_xlsx(xlsx_file)
        assert isinstance(xlsx_contents, dict)


if __name__ == '__main__':
    unittest.main()