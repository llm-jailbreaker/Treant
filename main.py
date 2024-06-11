import argparse
from concurrent.futures import ThreadPoolExecutor
from treant.test import integrated_test


def main(args):
    log_file = open(args.log, 'a+')
    with ThreadPoolExecutor(max_workers=args.parallel) as pool:
        integrated_test(args.ipolicy, pool, args.data, log_file, args.result, args.target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="The dataset file (txt). Each line should be the description text of target image.")
    parser.add_argument("--log", default='logs/sample.log', help="Log JSON responses that failed to parse (txt)")
    parser.add_argument("--result", help="The result path (csv file)")
    parser.add_argument('--ipolicy', type=int, default=5, help="policy item count")
    parser.add_argument('--target', type=int, default=0, help="The mode to run, 0: treant, 1: semantic decomposition, 2: drown")
    parser.add_argument('--parallel', type=int, default=4, help="number of threads")
    args = parser.parse_args()
    main(args)
