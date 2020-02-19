import sys
import csv
import argparse
import itra_scraper


def main(username, password, idedition, filename, debug):

    if filename == None:
        output = sys.stdout
    else:
        output = open(filename, "w")

    itra = itra_scraper.scraper(username, password, debug=debug)

    rows, columns = itra.get_result(idedition)
    assert(len(rows) > 0)
    writer = csv.writer(output)
    writer.writerow(columns)
    for row in rows:
        writer.writerow(row)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('--output', default=None, help="output csv file name")
    parser.add_argument('--debug', action="store_true")
    parser.add_argument('idedition', help="race idedition")
    args = parser.parse_args()

    main(args.username, args.password, args.idedition, args.output, args.debug)
