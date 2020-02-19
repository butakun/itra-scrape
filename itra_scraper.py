from bs4 import BeautifulSoup
import requests
import re
import logging
import sys


class ITRAScraper(object):
    def __init__(self, username, password, debug=False):

        self.debug = debug
        self.session = requests.Session()

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)

        data = {"login": username, "pwd": password, "keepconn": "1"}
        self.session.cookies["langue_affich"] = "_en"
        self.session.cookies["MBLogin"] = username
        self.session.cookies["MBPass"] = password
        r = self.session.post("https://itra.run/", data=data)
        r.raise_for_status()

    def get_result(self, idedition):

        data = {"mode": "getCourse", "idedition": str(idedition)}
        r = self.session.post("https://itra.run/fiche.php", data=data)
        r.raise_for_status()

        if self.debug:
            sys.stderr.write(r.text)

        soup = BeautifulSoup(r.text, features="html.parser")

        # column names from table header
        table = soup.find("table", class_="palmares")
        columns = [th.get_text() for th in table.find("thead").find_all("th")]

        rows = []
        for row in soup.select("tr.odd, tr.even"):
            rows.append([data.get_text().strip() for data in row.find_all("td")])

        return rows, columns

    def search_races(self, ddmmyyyy_min, ddmmyyyy_max, keyword=None):

        data = {"mode": "getres", "dtmin": ddmmyyyy_min, "dtmax": ddmmyyyy_max}
        if keyword is not None:
            data["input_cal_rech"] = keyword

        r = self.session.post("https://itra.run/results.php", data=data)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, features="html.parser")
        races = []
        ref = re.compile("^.*getResult\('([0-9]+)'\);.*$")
        for race in soup.select("div.race"):
            name = race.find("h2").get_text().strip()
            idedition = ref.search(race.find("a").attrs["onclick"]).group(1)

            where, when = race.find_all("div")[:2]
            where = where.get_text().strip()
            info = when.span.extract().get_text().strip()
            when = when.get_text().strip()
            races.append(
                {
                    "idedition": idedition,
                    "name": name,
                    "where": where,
                    "when": when,
                    "info": info,
                }
            )
        return races

    def search_runners(self, first_name, family_name, nationality):

        # nationality is a three-leter code, like "FRA", "JPN"
        data = {
            "mode": "search",
            "nat": nationality,
            "nom": family_name,
            "pnom": first_name,
        }

        r = self.session.post("https://itra.run/fiche.php", data=data)
        r.raise_for_status()

        if self.debug:
            sys.stderr.write(r.text)

        pat_tit_1 = re.compile("^(.+), born in (.+)")
        pat_tit_2 = re.compile("^(.+)$")
        pat_nat = re.compile("^\((.+)\)")

        soup = BeautifulSoup(r.text, features="html.parser")
        fcs = soup.find_all("div", class_="fc")
        assert len(fcs) > 0
        rows = []
        for fc in fcs:
            runner = {"id": fc["id"], "data-url": fc["data-url"]}

            tit = fc.find("div", class_="tit").get_text()
            try:
                groups = pat_tit_1.search(tit).groups()
                sex, birth_year = groups[:2]
            except:
                birth_year = "??"
                try:
                    groups = pat_tit_2.search(tit).groups()
                except:
                    sex = "??"

            runner["sex"] = sex
            runner["birth_year"] = birth_year

            info = fc.find("div", class_="info")
            name = info.contents[0]
            nationality = info.find("span").get_text()
            nationality = pat_nat.search(nationality).group(1)
            runner["name"] = name
            runner["nationality"] = nationality
            rows.append(runner)
        return rows


def scraper(username, password, debug):

    return ITRAScraper(username, password, debug)
