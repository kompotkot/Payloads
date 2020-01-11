import time
import argparse
from collections import ChainMap


parser = argparse.ArgumentParser(description='Sort files. Example: python SortAndMergeFile.py -i all-dirs.txt all-php.txt -o new.txt -r yes')
parser.add_argument('-i', '--input', nargs='*', help='Input file')
parser.add_argument('-o', '--output', help='Output file')
parser.add_argument('-r', '--order', default='no', help='Sort list, 0 - for first character in word, -1 for last one (default: no)')

args = parser.parse_args()
new_dict = {key: value for key, value in vars(args).items() if value}
settings = ChainMap(new_dict)


def writeAndUpdateFile(fromfile, tofile, order):
    tof = open(tofile, 'w')
    lst = []
    for i in fromfile:
        with open(i) as fp:
            for line in fp:
                if len(line) > 0:       # Filter empty lines
                    lst.append(line.strip().lower())

    lst = set(lst)

    if order == 'yes':
        lst = sorted(lst)

    for i in lst:
        tof.write(i + "\n")

    tof.close()

def w(fromfile, tofile, order):
    tof = open(tofile, 'w')
    lst = []
    for i in fromfile:
        with open(i) as fp:
            for line in fp:
                if len(line) > 0:       # Filter empty lines
                    lst.append(line.strip().lower())

    lst = set(lst)

    if order != 'no':
        lst = sorted(lst, key=lambda x: x[int(order)])

    for i in lst:
        tof.write(i + "\n")

    tof.close()

def main():
    startTime = time.time()
    # writeAndUpdateFile(settings['input'], settings['output'], settings['order'])
    w(settings['input'], settings['output'], settings['order'])
    print(f'Required time: {time.time() - startTime}')

if __name__ == '__main__':
    main()
