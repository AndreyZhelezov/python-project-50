import argparse
from gendiff import generate_diff


def main():
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')
    args = parser.parse_args()

    file1_path = args.first_file
    file2_path = args.second_file

    print(generate_diff(file1_path, file2_path))


if __name__ == '__main__':
    main()
