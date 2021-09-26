import sys
import os
from subnet_finder import SubnetFinder


def check_args(args: list) -> bool:
    if len(args) != 2:
        print(f"Invalid number of parameters ({len(args)}). Must be main.py file_name ip_type")
        return False

    file_name = args[0]
    if not os.path.isfile(file_name):
        print(f"ERROR: No such file or directory {file_name}")
        return False

    ip_type = args[1]
    if ip_type.lower() not in ("ipv4", "ipv6"):
        print(f"{ip_type} type of ip address does not support. Supported: ipv4, ipv6")
        return False
    return True


def main() -> None:
    if not check_args(sys.argv[1:]):
        exit(1)

    file_name = sys.argv[1]
    ip_type = sys.argv[2].lower()
    subnet_finder = SubnetFinder(file_name, ip_type)
    subnet = subnet_finder.find_subnet()
    if subnet is None:
        exit(1)
    print(f"Result net: {subnet}")


if __name__ == '__main__':
    main()
