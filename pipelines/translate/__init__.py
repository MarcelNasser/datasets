import csv
import os

_path = os.path.join(os.path.dirname(__file__), ".")

_iso639 = csv.DictReader(open(os.path.join(_path, "iso639.csv")))

SUPPORTED_LANG = {x['Code']:x['Lang'] for x in _iso639}
