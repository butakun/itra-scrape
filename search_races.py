import sys
import csv
import argparse
import itra_scraper


def main(username, password, from_date, to_date, keyword, filename, debug):

    if filename == None:
        output = sys.stdout
    else:
        output = open(filename, "w")

    itra = itra_scraper.scraper(username, password, debug)

    races = itra.search_races(from_date, to_date, keyword)
    assert len(races) > 0
    writer = csv.DictWriter(output, fieldnames=races[0].keys())
    writer.writeheader()
    for race in races:
        writer.writerow(race)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--username")
    parser.add_argument("--password")
    parser.add_argument("--output", default=None, help="output csv file name")
    parser.add_argument("--keyword", default=None, help="keyword for race name")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("from_date", help="DD/MM/YYYY")
    parser.add_argument("to_date", help="DD/MM/YYYY")
    args = parser.parse_args()

    main(
        args.username,
        args.password,
        args.from_date,
        args.to_date,
        args.keyword,
        args.output,
        args.debug,
    )
