# itra-scrape
Scraping Tool for ITRA Database

## Search for races
```python ./search_races.py --help```

e.g.
```
$ python ./search_races.py --username YourITRAUserName --password Password 01/01/2020 29/02/2020

idedition,name,where,when,info
49703,Trilhas Ninho Das Águias - 2 Etapa C T M 2020 - 19K Trilhas Ninho Das Águias,Brazil - Rio Grande do Sul,15 February 2020,18.9km 1180M+
61089,Winter Night Trail 2020,Kazakhstan - Almaty,15 February 2020,19.2km 1260M+
54659,Brunello Crossing 2020,Italy - Toscana,16 February 2020,45.3km 1680M+

...

```

## Race Result
```python ./search_results.py --help```

e.g.
```
$ python ./search_results.py 49703

Name / Surname,Time,Overall Rank.,Sex,Nationality
John DOE,04:05:06,1,Man,Brazil

...

```

## Search for runners
```python ./search_runners.py --help```

Not all three search keywords (first name, family name, nationality) have to be given, some can be left blank.
e.g.
```
$ python ./search_runners.py kilian jornet ""

id,data-url,sex,birth_year,name,nationality
run2704,/community/kilian.jornet burgada/2704/9736/,Men,1987,Kilian JORNET,ESP

```
