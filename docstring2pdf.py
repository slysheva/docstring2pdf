import argparse
import os

import sys
import modules.converter as converter


def get_files_list(file_path):
    if file_path.endswith('.py'):
        return [file_path]
    files_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            if file.endswith('.py'):
                files_list.append(os.path.join(root, file))
    return files_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Converts docstrings to pdf")
    parser.add_argument("-f", "--file", type=str,
                        help="Get docstrings from file or directory")
    parser.add_argument("-o", "--output", type=str,
                        help="""Set path to output file,
                         results/result.pdf default""",
                        default='results/result.pdf')
    parser.add_argument("-a", "--all", action="store_true",
                        help="Output according to __all__")
    parser.add_argument("-p", "--public", action="store_true",
                        help="Output only public interface")
    parser.add_argument("-d", "--docstrings", action="store_true",
                        help="Output only items with docstrings")
    parser.add_argument("-c", "--content", action="store_true",
                        help="Output content table")
    parser.add_argument("-e", "--empty", action="store_true",
                        help="Output empty module")
    args = parser.parse_args()
    files_list = []
    if args.file is None:
        with sys.stdin as f:
            for line in f:
                files_list += get_files_list(line.strip())
    else:
        files_list = get_files_list(args.file)
    result = converter.convert(files_list, args.all,
                               args.public,
                               args.docstrings,
                               args.content,
                               args.empty)
    with open(args.output, 'w') as f:
        print(result, file=f)
