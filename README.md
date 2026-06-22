# Divoom Gallery API Wrapper (Python)

Eine einfache, in Python geschriebene API-Schnittstelle, um Pixel Art, Animationen und Metadaten (Trending Artists etc.) aus der Divoom Handy App abzurufen.

## WICHTIG: Suchen (Search) benötigt Zugangsdaten

Divoom hat seine Endpunkte teilweise eingeschränkt. Ohne einen Token (Login) liefert die API bei Suchanfragen (z.B. nach bestimmten Spielenamen wie "Minecraft" oder "Landwirtschafts Simulator 25") häufig leere Resultate. Um die vollen Funktionen freizuschalten, unterstützt diese Bibliothek einen Login mit E-Mail und Passwort.

## Features

- **(Authentifiziert)** Suchen nach beliebigen Stichwörtern (Steam-Spiele etc.) in bestimmten Pixel-Größen (16x16, 32x32, 64x64, 128x128).
- Abrufen von "Trending/Hot" Pixel Art Dateien (derzeit stabil für 32x32 auf dem öffentlichen Endpunkt).
- Abrufen der beliebtesten Pixel-Künstler (Hot Experts).
- Direkte Download-Links zu den binären / rohen Dateien oder Animationen.

## Voraussetzungen

- Python 3.x
- Keine zusätzlichen pip-Abhängigkeiten (nutzt `urllib`, `hashlib` und Standard-Module).

## Installation

Einfach die Datei `divoom_api.py` in das eigene Projekt kopieren und importieren.

## Benutzung

Hier ist ein einfaches Beispiel, wie man die API verwendet:

```python
from divoom_api import DivoomGalleryAPI
import json

# API instanziieren
api = DivoomGalleryAPI()

# OPTIONAL ABER EMPFOHLEN: Einloggen für vollumfängliche Suchergebnisse!
# Das Passwort wird sicher lokal in MD5 gehashed und an Divoom gesendet.
api.login("deine_email@beispiel.de", "dein_passwort")

# 1. Bilder suchen (Größen: 16, 32, 64, 128)
# Suchen nach spezifischen Spielen:
results = api.search_gallery(keyword="Landwirtschafts Simulator", size=64, return_cnt=10)
for item in results:
    print("File ID:", item.get("FileId"))
    print("Download URL:", item.get("DownloadUrl"))

# 2. Trending (Heiße) Dateien abrufen
hot_files = api.get_hot_files(size=32, return_cnt=10)
if hot_files:
    print(json.dumps(hot_files[0], indent=2))

# 3. Trending Artists (Experten) abrufen
experts = api.get_hot_experts(return_cnt=5)
for expert in experts:
    print(expert.get("NickName"), "-", expert.get("Level"))
```

## Divoom Bilddateien verarbeiten

Die herunterladbaren Dateien aus `DownloadUrl` haben meistens die Endung `.bin` oder gar keine.
- Bei Animationen handelt es sich oft um umbenannte `.gif` Dateien oder spezielle Divoom-Formate, die mit Header-Bytes (z.B. `11 02` für 32x32 Bilder oder `1A` für Animationen) beginnen.
- Einige Dateien sind leicht AES-verschlüsselt (CBC-Modus). Open-Source-Projekte wie "pixoo_api" bieten Hinweise zum Dekodieren dieser Rohformate, falls Sie die Daten auf eigenen Displays ohne Divoom-Hardware ausgeben wollen.
