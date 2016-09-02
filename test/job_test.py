import unittest
from unittest.mock import Mock

from .context import src
from src import job

class JobTest(unittest.TestCase):

    def setUp(self):
        self.domainMock = Mock()
        self.schedulerMock = Mock()
        self.job = job.Job(self.domainMock, self.schedulerMock)

    def testGetNumberOfWorkers_OK_listLessThanWorkersConstant(self):
        anyList = [1, 2, 3]
        numberOfWorkers = self.job.getNumberOfWorkers(anyList)
        self.assertEqual(len(anyList), numberOfWorkers)

    def testGetNumberOfWorkers_OK_listGreaterThanWorkersConstant(self):
        anyList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        numberOfWorkers = self.job.getNumberOfWorkers(anyList)
        self.assertEqual(self.job.WORKERS, numberOfWorkers)