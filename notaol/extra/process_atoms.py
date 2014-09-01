'''Process penggy source code for atoms.'''
import glob
import re


def main():
    print('import enum')
    print()
    print()
    print('class Atom(enum.Enum):')
    for filename in sorted(glob.glob('include/fdo/atoms/*.h')):
        with open(filename) as in_file:

            pid = None

            for line in in_file:
                words = line.split()

                if len(words) != 3:
                    continue

                if words[0] != '#define':
                    continue

                if words[1].endswith('PID'):
                    pid = words[2]
                    name = words[1].replace('_PID', '')
                    print('    {} = {}'.format(name, pid))
                    continue

                name = words[1].lower()
                value = words[2]
                print('    {} = ({}, {})'.format(name, pid, value))

            print()

    print('----')

    print('class AtomDataType(enum.Enum):')

    for filename in sorted(glob.glob('src/fdo/atoms/*.c')):
        with open(filename) as in_file:

            pid = None

            for line in in_file:
                words = line.split()

                match = re.search(r'(\w{2,}) *, *(\w+)}', line)

                if not match:
                    continue

                name = match.group(1).lower()
                value = match.group(2).replace('},', '')
                print('    {} = DataType.{}'.format(name, value))

if __name__ == '__main__':
    main()
