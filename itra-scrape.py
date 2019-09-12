from bs4 import BeautifulSoup
import requests
import re
from collections import namedtuple

class ITRAScraper(object):

    def __init__(self, username, password):
        self.session = requests.Session()

        data = {'login':username, 'pwd':password, 'keepconn':'1'}
        self.session.cookies['langue_affich'] = '_en'
        self.session.cookies['MBLogin'] = username
        self.session.cookies['MBPass'] = password
        r = self.session.post('https://itra.run/', data=data)
        if not r:
            raise ValueError(r.status_code)


    def get_result(self, idedition):
        runner = namedtuple('Runner', ['name', 'time', 'overall_rank', 'sex', 'performance_index', 'nationality'])
        data = {'mode':'getCourse', 'idedition':str(idedition)}
        r = self.session.post('https://itra.run/fiche.php', data=data)
        if not r:
            raise ValueError(r.status_code)

        soup = BeautifulSoup(r.text, features='html.parser')
        result = []
        for row in soup.select('tr.odd, tr.even'):
            result.append(runner(*[data.get_text().strip() for data in row.find_all('td')]))
        return result


    def search_races(self, ddmmyyyy_min, ddmmyyyy_max, keyword):
        data = {'mode':'getres', 'input_cal_rech':keyword, 'dtmin':ddmmyyyy_min, 'dtmax':ddmmyyyy_max}
        r = self.session.post('https://itra.run/results.php', data=data)
        if not r:
            raise ValueError(r.status_code)

        soup = BeautifulSoup(r.text, features='html.parser')
        races = []
        ref = re.compile('^.*getResult\(\'([0-9]+)\'\);.*$')
        for race in soup.select('div.race'):
            name = race.find('h2').get_text().strip()
            idedition = ref.search(race.find('a').attrs['onclick']).group(1)

            where, when = race.find_all('div')[:2]
            where = where.get_text().strip()
            info = when.span.extract().get_text().strip()
            when = when.get_text().strip()
            races.append({'idedition':idedition, 'name':name, 'where':where, 'when':when, 'info':info})
        return races


def test(username, password):
    import sys
    import csv

    itra = ITRAScraper(username, password)

    races = itra.search_races('01/01/2019', '11/09/2019', 'UTMB')
    writer = csv.DictWriter(sys.stdout, fieldnames=races[0].keys())
    for race in races:
        writer.writerow(race)

    return

    result = itra.get_result('39879')
    writer = csv.DictWriter(sys.stdout, fieldnames=result[0]._fields)
    writer.writeheader()
    for runner in result:
        writer.writerow(runner._asdict())


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()
    test(args.username, args.password)

