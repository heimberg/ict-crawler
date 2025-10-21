# Claude Skills für ICT Crawler

## VPN ICT Crawler Skill

Dieses Skill ermöglicht es, Modulinformationen von modulbaukasten.ch direkt über Claude abzurufen.

### Verwendung

```
/crawl <modulnummer>
```

Beispiel:
```
/crawl 162
```

### Aktueller Status

**WICHTIG:** Die Authentifizierung bei modulbaukasten.ch funktioniert derzeit nicht. Die auth.php gibt "Access denied" zurück.

Die Skill-Struktur ist vollständig implementiert und wird funktionieren, sobald die Authentifizierung behoben ist.

### Fehlerbehebung

Um das Authentifizierungsproblem zu beheben:

1. Überprüfen Sie die modulbaukasten.ch Website und finden Sie die neue Methode zum Abrufen des Bearer Tokens
2. Aktualisieren Sie die `get_bearer_token()` Funktion in `main.py` entsprechend
3. Testen Sie mit: `python3 -c "from main import get_module_by_number; print(get_module_by_number('162'))"`

### Struktur

- **Skill-Datei:** `.claude/skills/vpn-ict-crawler.md`
- **Command-Datei:** `.claude/commands/crawl.md`
- **Hauptfunktion:** `get_module_by_number()` in `main.py`

### Funktionen

Die `get_module_by_number()` Funktion:
- Durchsucht alle drei Bildungsgänge (INF-PE, ICT, BINF)
- Gibt formatierte Modulinformationen zurück
- Zeigt: Modulnummer, Titel, Bildungsgang, Lernort, Lehrjahr, Modultyp, Kompetenz, PDF-Link
