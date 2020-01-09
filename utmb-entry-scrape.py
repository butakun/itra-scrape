from bs4 import BeautifulSoup
import requests


def main():

    session = requests.Session()

    r = session.get("https://utmbmontblanc.com/en/page/108/les-coureurs-2020.html")
    soup = BeautifulSoup(r.text, features="html.parser")

    for row in soup.find("select").select("option"):
        pays = row["value"]
        if pays is None:
            continue

        r = session.post("https://utmbmontblanc.com/en/page/108/les-coureurs-2020.html", data={"pays": pays})
        soup = BeautifulSoup(r.text, features="html.parser")

        for row in soup.select("table"):
            first = True
            for runner in row.select("tr"):
                if first:
                    first = False
                    continue
                status = runner.find("td", class_="ins9").contents
                if status is None:
                    print("empty status?", runner)
                else:
                    print(f"status = {status}")

if __name__ == "__main__":
    main()
