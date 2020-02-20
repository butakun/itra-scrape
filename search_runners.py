import sys
import csv
import argparse
import itra_scraper


def main(username, password, first_name, family_name, nationality, filename, debug):

    if filename == None:
        output = sys.stdout
    else:
        output = open(filename, "w")

    itra = itra_scraper.scraper(username, password, debug)

    runners = itra.search_runners(first_name, family_name, nationality)
    assert len(runners) > 0

    writer = csv.DictWriter(output, fieldnames=runners[0].keys())
    writer.writeheader()
    for runner in runners:
        writer.writerow(runner)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username")
    parser.add_argument("-p", "--password")
    parser.add_argument("-o", "--output", default=None, help="output csv file name")
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("first_name")
    parser.add_argument("family_name")
    parser.add_argument("nationality")
    args = parser.parse_args()

    main(
        args.username,
        args.password,
        args.first_name,
        args.family_name,
        args.nationality,
        args.output,
        args.debug,
    )
