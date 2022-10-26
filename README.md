# Skript zum Abfragen von Modulnamen anhand der Modulnummer
Das Python Skript fragt die Seite [www.modulbaukasten.ch](www.modulbaukasten.ch) nach den im File `modulnummer.txt` aufgeführten Modulnummern ab und speichert die Ergebnisse in der Datei `modulnamen.txt` ab. Die Modulnummern müssen in der Datei `modulnummer.txt` mit einem Zeilenumbruch getrennt sein. 

## Abhängigkeiten
Sämtliche Abhängigkeiten sind in der Datei `requirements.txt` aufgeführt. Diese können mit dem Befehl `pip install -r requirements.txt` installiert werden.

## Token
Um die Abfrage der Modulnamen durchführen zu können, muss ein Bearer Token in einer `.env` Datei hinterlegt werden. Dieses Token muss mittels einer `GET` Abfrage an die Seite [www.modulbaukasten.ch](www.modulbaukasten.ch) ermittelt werden. Das Token wird in der folgenden Form hinterlegt:
```
BEARER_TOKEN = "Bearer xxxxxxxxxxxxx"
```
