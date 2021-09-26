import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from main import check_args


class MyTestCase(unittest.TestCase):
    def test_input_1(self):
        self.assertEqual(check_args(["../data/ipv4_data_set.txt", "ipv4"]), True)

    def test_input_2(self):
        self.assertEqual(check_args(["../data/ipv4_data_set.txt", "IPv4"]), True)

    def test_input_3(self):
        self.assertEqual(check_args(["../data/ipv6_data_set.txt", "IPv6"]), True)

    def test_input_4(self):
        self.assertEqual(check_args(["../data/ipv6_data_set_100.txt", "ipv6"]), False)

    def test_input_5(self):
        self.assertEqual(check_args(["../data/ipv6_data_set.txt", "ipv8"]), False)


if __name__ == '__main__':
    unittest.main()
