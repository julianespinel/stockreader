import unittest
from unittest.mock import Mock

from src.stocks import job


class JobTest(unittest.TestCase):

    def setUp(self):
        self.domain_mock = Mock()
        self.scheduler_mock = Mock()
        self.time_series_mock = Mock()
        self.job = job.Job(self.domain_mock, self.scheduler_mock, self.time_series_mock)

    def test_get_number_of_workers_OK_list_less_than_workers_constant(self):
        any_list = [1, 2, 3]
        number_of_workers = self.job.get_number_of_workers(any_list)
        self.assertEqual(len(any_list), number_of_workers)

    def test_get_number_of_workers_OK_list_greater_than_workers_constant(self):
        any_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        number_of_workers = self.job.get_number_of_workers(any_list)
        self.assertEqual(self.job.WORKERS, number_of_workers)
