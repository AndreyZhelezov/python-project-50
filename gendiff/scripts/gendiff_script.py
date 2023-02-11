import argparse
from gendiff import generate_diff


def main():
    output_formats = ['stylish', 'plain', 'json']
    parser = argparse.ArgumentParser(
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format',
                        help=f'set format of output. Formats: [{"|".join(output_formats)}]',
                        default='stylish')
    args = parser.parse_args()
    if args.format not in output_formats:
        print(f'Format "{args.format}" is not available!')
        parser.print_help()
        exit(1)

    file1_path = args.first_file
    file2_path = args.second_file

    print(generate_diff(file1_path, file2_path, args.format))


if __name__ == '__main__':
    main()
