import unittest
from src import domain

class DomainTest(unittest.TestCase):

    def testDownloadAndSaveStockCurrentData(self):
        print(domain.YEARS_AGO)
        self.assertEqual(10, domain.YEARS_AGO)

if __name__ == "main":
    print("***** hello!")
    unittest.main()
