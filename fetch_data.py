#!/usr/bin/env python3
import requests
from pathlib import Path
from xml.etree import ElementTree as ET

PID_SCOPE, PID_IDENT = "knb-lter-nwk", "1"
BASE_META = "https://pasta.lternet.edu/package/eml/{scope}/{ident}"
BASE_DATA = "https://pasta.lternet.edu/package/data/eml/{scope}/{ident}/{rev}/{entity}"

out_dir = Path("raw")
out_dir.mkdir(exist_ok=True)

def latest_revision(scope, ident):
    url = BASE_META.format(scope=scope, ident=ident)
    r = requests.get(url); r.raise_for_status()
    revs = [int(line) for line in r.text.splitlines() if line.isdigit()]
    if not revs:
        raise RuntimeError(f"No revisions at {url}")
    return str(max(revs))

def download_entities(scope, ident, rev):
    meta_url = f"https://pasta.lternet.edu/package/metadata/eml/{scope}/{ident}/{rev}"
    r = requests.get(meta_url); r.raise_for_status()
    root = ET.fromstring(r.content)
    ns = {"d": "eml://ecoinformatics.org/eml-2.1.1"}
    for obj in root.findall(".//d:physical//d:objectName", ns):
        entity = obj.text.strip()
        data_url = BASE_DATA.format(scope=scope, ident=ident, rev=rev, entity=entity)
        dr = requests.get(data_url)
        if dr.ok:
            (out_dir / entity).write_bytes(dr.content)
            print("✓", entity)
        else:
            print("✗ failed", entity)

if __name__ == "__main__":
    rev = latest_revision(PID_SCOPE, PID_IDENT)
    print(f"Using {PID_SCOPE}.{PID_IDENT} → rev {rev}")
    download_entities(PID_SCOPE, PID_IDENT, rev)
