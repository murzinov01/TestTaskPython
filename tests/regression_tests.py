import unittest
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0], ".."))
from subnet_finder import SubnetFinder


class TestTranslationFunctions(unittest.TestCase):
    # test binary functions
    def test_dec_to_binary_1(self):
        self.assertEqual(SubnetFinder._dec_to_binary(168, 8), "10101000")

    def test_dec_to_binary_2(self):
        self.assertEqual(SubnetFinder._dec_to_binary(0, 8), "00000000")

    def test_dec_to_binary_3(self):
        self.assertEqual(SubnetFinder._dec_to_binary(255, 8), "11111111")

    def test_binary_to_dec_1(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("10101000"), 168)

    def test_binary_to_dec_2(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("00000000"), 0)

    def test_binary_to_dec_3(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("0"), 0)

    def test_binary_to_dec_4(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("11111111"), 255)

    def test_hex_to_dec_1(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("ffe0", _pow=16), 65504)

    def test_hex_to_dec_2(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("0", _pow=16), 0)

    def test_hex_to_dec_3(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._convert_to_dec("f", _pow=16), 15)

    def test_dec_to_hex_1(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._dec_to_hex(65504), "ffe0")

    def test_dec_to_hex_2(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._dec_to_hex(1), "1")

    def test_dec_to_hex_3(self):
        subnet_finder = SubnetFinder("test.txt", "ipv4")
        self.assertEqual(subnet_finder._dec_to_hex(0), "0")

    def test_get_binary_num_length_1(self):
        self.assertEqual(SubnetFinder._get_binary_num_length("00000000", 8), 0)

    def test_get_binary_num_length_2(self):
        self.assertEqual(SubnetFinder._get_binary_num_length("11111111", 8), 8)

    def test_get_binary_num_length_3(self):
        self.assertEqual(SubnetFinder._get_binary_num_length("00000101", 8), 3)

    def test_get_binary_num_length_4(self):
        self.assertEqual(SubnetFinder._get_binary_num_length("00100101", 8), 6)


class TestIpv4Functionality(unittest.TestCase):
    # test check_ipv4()
    def test_check_ipv4_1(self):
        self.assertEqual(SubnetFinder._check_ipv4("192.168.1.2"), True)

    def test_check_ipv4_2(self):
        self.assertEqual(SubnetFinder._check_ipv4("-1.0.0.0"), False)

    def test_check_ipv4_3(self):
        self.assertEqual(SubnetFinder._check_ipv4("300.200.1.0"), False)

    def test_check_ipv4_4(self):
        self.assertEqual(SubnetFinder._check_ipv4("0.0.0.0"), True)

    def test_check_ipv4_5(self):
        self.assertEqual(SubnetFinder._check_ipv4("192.168.1.2.2"), False)


class TestIpv6Functionality(unittest.TestCase):
    # test check_ipv6()
    def test_check_ipv6_1(self):
        self.assertEqual(SubnetFinder._check_ipv6("ffe0::1:0:0:0"), True)

    def test_check_ipv6_2(self):
        self.assertEqual(SubnetFinder._check_ipv6("ffe0::-1:0:0:20"), False)

    def test_check_ipv6_3(self):
        self.assertEqual(SubnetFinder._check_ipv6("0:0:0:0:0:0:0:0"), True)

    def test_check_ipv6_4(self):
        self.assertEqual(SubnetFinder._check_ipv6("2001:DB0:0:123A:0:0:0:30"), True)

    def test_check_ipv6_5(self):
        self.assertEqual(SubnetFinder._check_ipv6("2001:DB0:0:123A:0:0:0:30:1"), False)

    # test create_compressed_form()
    def test_create_compressed_form_1(self):
        self.assertEqual(SubnetFinder._create_compressed_form("ffe0.0.0.0.0.0.0.0/72"), "ffe0::/72")

    def test_create_compressed_form_2(self):
        self.assertEqual(SubnetFinder._create_compressed_form("ffe0.0.0.0.0.0.0.0/20"), "ffe0::/20")

    def test_create_compressed_form_3(self):
        self.assertEqual(SubnetFinder._create_compressed_form("0.0.0.0.0.0.0.0/0"), "::/0")

    def test_create_compressed_form_4(self):
        self.assertEqual(SubnetFinder._create_compressed_form("ffe0.0.0.0.80.0.0.0/128"), "ffe0::80::/128")

    def test_create_compressed_form_5(self):
        self.assertEqual(SubnetFinder._create_compressed_form("45cd.9d44.f7c4.4be.f5cb.0.0.0/88"),
                         "45cd:9d44:f7c4:4be:f5cb::/88")


class TestSubnetFinder(unittest.TestCase):
    DATA_1 = [[192, 168, 1, 2],
              [192, 168, 1, 3],
              [192, 168, 1, 5]]
    DATA_2 = [[192, 168, 1, 0],
              [192, 168, 1, 3],
              [192, 168, 2, 0]]
    DATA_3 = [[192, 168, 1, 0],
              [192, 168, 1, 0],
              [192, 168, 1, 0]]

    # test _find_diff_ip_part()
    def test_find_diff_ip_part_1(self):
        self.assertEqual(SubnetFinder._find_diff_ip_part(self.DATA_1), 3)

    def test_find_diff_ip_part_2(self):
        self.assertEqual(SubnetFinder._find_diff_ip_part(self.DATA_2), 2)

    def test_find_diff_ip_part_3(self):
        self.assertEqual(SubnetFinder._find_diff_ip_part(self.DATA_3), 3)

    # test _find_subnet_ipv4()
    def test_find_subnet_ipv4_1(self):
        subnet_finder = SubnetFinder("../data/ipv4_data_set.txt", "ipv4")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "192.168.1.0/29")

    def test_find_subnet_ipv4_2(self):
        subnet_finder = SubnetFinder("../data/ipv4_data_set_test1.txt", "ipv4")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "0.0.0.0/0")

    def test_find_subnet_ipv4_3(self):
        subnet_finder = SubnetFinder("../data/ipv4_data_set_test2.txt", "ipv4")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "192.168.0.0/20")

    def test_find_subnet_ipv4_4(self):
        subnet_finder = SubnetFinder("../data/ipv4_data_set_test3.txt", "ipv4")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "164.172.80.0/25")

    # test _find_subnet_ipv6()
    def test_find_subnet_ipv6_1(self):
        subnet_finder = SubnetFinder("../data/ipv6_data_set.txt", "ipv6")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "ffe0::/72")

    def test_find_subnet_ipv6_2(self):
        subnet_finder = SubnetFinder("../data/ipv6_data_set_test1.txt", "ipv6")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "ffe0::/20")

    def test_find_subnet_ipv6_3(self):
        subnet_finder = SubnetFinder("../data/ipv6_data_set_test2.txt", "ipv6")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "::/0")

    def test_find_subnet_ipv6_4(self):
        subnet_finder = SubnetFinder("../data/ipv6_data_set_test3.txt", "ipv6")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "ffe0::80::/128")

    def test_find_subnet_ipv6_5(self):
        subnet_finder = SubnetFinder("../data/ipv6_data_set_test4.txt", "ipv6")
        subnet = subnet_finder.find_subnet()
        self.assertEqual(subnet, "45cd:9d44:f7c4:4be:f5cb::/88")


if __name__ == '__main__':
    unittest.main()
