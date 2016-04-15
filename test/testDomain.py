import unittest
from unittest.mock import MagicMock
from src.domain import Domain

class DomainTest(unittest.TestCase):

    def setUp(self):
        self.mongoMock = MagicMock()
        self.downloadMock = MagicMock()
        self.domain = Domain(self.mongoMock, self.downloadMock)

    def testDownloadAndSaveStockCurrentData(self):
        print(self.domain.YEARS_AGO)
        self.assertEqual(10, self.domain.YEARS_AGO)

if __name__ == "main":
    print("***** hello!")
    unittest.main()
