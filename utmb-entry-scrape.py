from bs4 import BeautifulSoup
import requests
import csv


def main():

    session = requests.Session()

    r = session.get("https://utmbmontblanc.com/en/page/108/les-coureurs-2020.html")
    soup = BeautifulSoup(r.text, features="html.parser")

    with open("utmb_2020_lottery.csv", "w") as csvfile:

        field_names = ["race_name", "surname", "first_name", "category", "country", "nationality", "status"]
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()

        for row in soup.find("select").find_all("option"):
            pays = row["value"].strip()
            if pays == "":
                continue

            print(f"scraping {pays}")
            r = session.post("https://utmbmontblanc.com/en/page/108/les-coureurs-2020.html", data={"pays": pays})
            soup = BeautifulSoup(r.text, features="html.parser")

            runners_per_country = 0
            for head in soup.find_all("h2"):
                after_head = head.find_next_sibling()
                if after_head.name != "table":
                    continue
                race_name = head.string
                table = after_head

                first = True
                for row in table.find_all("tr"):
                    if first:
                        first = False
                        continue
                    runner = {"race_name": race_name}
                    runner["surname"] = row.find("td", class_="ins3").contents[1].strip()
                    runner["first_name"] = row.find("td", class_="ins4").string.strip()
                    runner["category"] = row.find("td", class_="ins5").contents[0].strip()
                    runner["country"] = row.find("td", class_="ins7").string.strip()
                    runner["nationality"] = row.find("td", class_="ins8").string.strip()
                    runner["status"] = row.find("td", class_="ins9").string.strip()
                    #print("{race_name}, {surname}, {first_name}, {category}, {country}, {nationality}, {status}".format(**runner))
                    writer.writerow(runner)
                    runners_per_country += 1

            print(f"{pays} had {runners_per_country} entries")


if __name__ == "__main__":
    main()
