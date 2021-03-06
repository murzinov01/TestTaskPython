class SubnetFinder:
    """
    Class that implements finding the minimum subnet algorithm
    """

    def __init__(self, file_name: str, ip_type: str):
        self.ip_type = ip_type
        self.file_name = file_name
        self.data = list()
        self.converted_table_to_dec = self.create_converted_table_to_dec()
        self.converted_table_to_binary = self.create_converted_table_to_binary()

    @staticmethod
    def create_converted_table_to_dec() -> dict:
        """
        Create table to convert from binary symbols (includes hex) to dec
        :return: dict - converted table
        """
        letters = ['a', 'b', 'c', 'd', 'e', 'f']
        convert_table = {str(i): i for i in range(10)}
        convert_table.update({letters[i]: 10 + i for i in range(6)})
        return convert_table

    @staticmethod
    def create_converted_table_to_binary() -> dict:
        """
        Create table to convert from dec digits (0-15) to hex symbols
        :return: dict - converted table
        """
        letters = ['a', 'b', 'c', 'd', 'e', 'f']
        convert_table = {i: str(i) for i in range(10)}
        convert_table.update({10 + i: letters[i] for i in range(6)})
        return convert_table

    @staticmethod
    def _check_ipv4(ip: str) -> bool:
        """
        Check that ipv4 address is valid
        :param ip: - ip address
        :return: True if ip is valid ipv4, False otherwise
        """
        numbers = list(map(int, ip.split('.')))
        if len(numbers) > 4:
            return False

        for number in numbers:
            if number < 0 or number > 255:
                return False
        return True

    @staticmethod
    def _check_ipv6(ip: str) -> bool:
        """
        Check that ipv6 address is valid
        :param ip: - ip address
        :return: True if ip is valid ipv6, False otherwise
        """
        tokens = ip.lower().split(':')
        supported_symbols = ('a', 'b', 'c', 'd', 'e', 'f')
        if len(tokens) > 8:
            return False

        for token in tokens:
            if token == "":
                continue
            for el in token:
                if not el.isalnum() or (el.isalpha() and el not in supported_symbols):
                    return False
        return True

    @staticmethod
    def _find_diff_ip_part(data: list) -> int:
        """
        Find the first different part (octet or hexet) among all the ip addresses in the data
        :param data: list containing ip addresses
        :return: index of the first different part in ip
        """
        for i, octet in enumerate(data[0]):
            for ip in data:
                if ip[i] != octet:
                    return i
        return len(data[0]) - 1

    @staticmethod
    def _dec_to_binary(num: int, digits: int) -> str:
        """
        Convert decimal to binary representation
        :param num: number to convert
        :param digits: the maximum number of bits in the binary representation
        :return: binary representation of the input number
        """
        result = []
        while num != 0:
            result.append(str(num % 2))
            num = int(num / 2)
        result = result[::-1]
        if len(result) < digits:
            result = ['0'] * (digits - len(result)) + result
        return "".join(result)

    @staticmethod
    def _get_binary_num_length(num: str, digits: int) -> int:
        """
        Get actual length of the binary number (without leading zeros)
        :param num: binary num in string
        :param digits: the maximum number of bits in the binary representation
        :return: actual length. Example: 00000101, returns - 3
        """
        prev_zeroes = 0
        for el in num:
            if el == '0':
                prev_zeroes += 1
            else:
                break
        return digits - prev_zeroes

    def _dec_to_hex(self, num: int) -> str:
        """
        Convert decimal number into hex
        :param num: number to convert
        :return: hex representation of the num
        """
        result = []
        while num != 0:
            result.append(self.converted_table_to_binary[num % 16])
            num = int(num / 16)
        if not result:
            return '0'
        else:
            return "".join(result[::-1])

    def _convert_binary_to_dec(self, num: str, base=2) -> int:
        """
        Convert binary number to decimal
        :param num: binary num in string
        :param base: number base (Example: 2, 8, 16)
        :return: decimal number
        """
        result = 0
        num_len = len(num)
        for i in range(num_len - 1, -1, -1):
            result += pow(base, num_len - 1 - i) * self.converted_table_to_dec[num[i]]
        return result

    def print_data(self) -> None:
        """
        prints input data
        :return:
        """
        print("DATA:")
        for ip in self.data:
            print(ip)

    def _ip_to_num_list(self, ip: str) -> list:
        """
        Preprocess the ip in string and convert it to list
        :param ip: ip address
        :return: ip address converted to list
        """
        if self.ip_type == "ipv4":
            return list(map(int, ip.split('.')))
        elif self.ip_type == "ipv6":
            pos = ip.find("::")
            zeroes_to_fill = 7 - (ip.count(":") - 1)
            if pos:
                ip = ip[:pos + 1] + ':'.join(['0'] * zeroes_to_fill) + ip[pos + 1:]
            return [self._convert_binary_to_dec(num, base=16) for num in ip.split(":")]

    def _set_data(self, file_name: str) -> int:
        """
        Read data from the file_name and save it to list
        :param file_name: input file name
        :return: 0 if the data contains the correct addresses, -1 otherwise
        """
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                line = line.lower().rstrip("\n")
                if self.ip_type == "ipv4" and self._check_ipv4(line) or self.ip_type == "ipv6" and self._check_ipv6(line):
                    self.data.append(self._ip_to_num_list(line))
                else:
                    return -1
        return 0

    def _find_subnet_impl(self, _type='ipv4') -> str:
        """
        Implements an algorithm for finding the minimum subnet
        :param _type: ip address type (Supports ipv4 and ipv6)
        :return: subnet and its mask in in a compressed form (/"number of ones in mask")
        """
        bits, parts, digits = 0, 0, 0
        if _type == 'ipv4':
            bits, parts, digits = 8, 4, 8
        elif _type == 'ipv6':
            bits, parts, digits = 16, 8, 16

        min_octet = self._find_diff_ip_part(self.data)
        highest_num = self.data[0][min_octet]
        for i, ip in enumerate(self.data):
            if ip[min_octet] > highest_num:
                highest_num = ip[min_octet]
        highest_num_binary = self._dec_to_binary(highest_num, digits)
        num_length = self._get_binary_num_length(highest_num_binary, digits)

        ones = parts * bits - bits * (parts - min_octet) + (bits - num_length)
        zeroes = parts * bits - ones

        subnet_mask = "1" * ones + "0" * zeroes
        ip = "".join([self._dec_to_binary(self.data[0][i], digits) for i in range(len(self.data[0]))])

        subnet = []
        for el1, el2 in zip(subnet_mask, ip):
            subnet.append(str(int(el1) * int(el2)))
        subnet = "".join(subnet)

        result = []
        for i in range(0, len(subnet), bits):
            number = self._convert_binary_to_dec(subnet[i:i + bits])
            if _type == "ipv6":
                number = self._dec_to_hex(number)
            result.append(str(number))

        subnet = f'{".".join(result)}/{ones}'
        return subnet

    @staticmethod
    def _create_compressed_form(subnet: str) -> str:
        """
        Create compressed form for ipv6 subnets. Remove zeros and replaces them with ::
        :param subnet: ipv6 subnet
        :return: ipv6 subnet in compressed form. Example: ffe0.0.0.0.0.0.0.0/72 -> ffe0::/72
        """
        tokens, ones = subnet.split('/')
        tokens = tokens.split('.')
        result = []
        i = 0
        while i < len(tokens) - 1:
            if tokens[i] == '0' and tokens[i + 1] == '0':
                result.append("::")
                i += 1
                while i != len(tokens) and tokens[i] == '0':
                    i += 1
            else:
                result.append(tokens[i])
                i += 1
        i = 0
        while i < len(result) - 1:
            if result[i] not in (':', '::') and result[i + 1] not in (':', '::'):
                result.insert(i + 1, ':')
                i += 1
            i += 1
        return f"{''.join(result)}/{ones}"

    def find_subnet(self) -> str or None:
        """
        Set data, check it and run an algorithm for finding the minimum subnet
        :return: minimum subnet if data is valid, None otherwise
        """
        if self._set_data(self.file_name) == -1:
            print("Incorrect ips were found in input file")
            return None
        result = self._find_subnet_impl(_type=self.ip_type)
        if self.ip_type == "ipv4":
            return result
        elif self.ip_type == "ipv6":
            return self._create_compressed_form(result)
