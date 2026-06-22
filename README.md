# Divoom Gallery API Wrapper (Python)

Eine einfache, in Python geschriebene API-Schnittstelle, um Pixel Art, Animationen und Metadaten (Trending Artists etc.) aus der Divoom Handy App abzurufen.

Diese API benötigt **keinen** Divoom-Account, um öffentlich verfügbare Daten abzurufen!

## Features

- Suchen nach Stichwörtern in bestimmten Pixel-Größen (z.B. 16x16, 32x32, 64x64).
- Abrufen von "Trending/Hot" Pixel Art Dateien (derzeit stabil für 32x32 auf dem öffentlichen Endpunkt).
- Abrufen der beliebtesten Pixel-Künstler (Hot Experts).
- Direkte Download-Links zu den binären / rohen Dateien oder Animationen.

## Voraussetzungen

- Python 3.x
- Keine zusätzlichen pip-Abhängigkeiten (nutzt `urllib` und Standard-Module).

## Installation

Einfach die Datei `divoom_api.py` in das eigene Projekt kopieren und importieren.

## Benutzung

Hier ist ein einfaches Beispiel, wie man die API verwendet:

```python
from divoom_api import DivoomGalleryAPI
import json

# API instanziieren
api = DivoomGalleryAPI()

# 1. Bilder suchen (Größen: 16, 32, 64, 128)
# Hinweis: Manche Suchanfragen liefern ohne Token keine Ergebnisse oder sind vom Divoom Server gecached
results = api.search_gallery(keyword="mario", size=64, return_cnt=10)
for item in results:
    print("File ID:", item.get("FileId"))
    print("Download URL:", item.get("DownloadUrl"))

# 2. Trending (Heiße) Dateien abrufen
hot_files = api.get_hot_files(size=32, return_cnt=10)
print(f"Gefundene Hot Files: {len(hot_files)}")
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

## Dokumentation der Endpunkte

Intern genutzt:
- `SearchGalleryV2` für die Suche nach Dateien.
- `Hot/GetHotFiles32` für Trends.
- `Cloud/GetHotExpert` für Künstler.
