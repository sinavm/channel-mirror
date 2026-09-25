#!/usr/bin/env python3
import json, re, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
out = ROOT / "site"
out.mkdir(exist_ok=True)
channels = json.loads((ROOT / "channels.json").read_text())["channels"]
index = ["<!doctype html><meta charset=utf-8><h1>channel-mirror</h1><ul>"]
for name in channels:
    url = f"https://t.me/s/{name}"
    html = ""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "channel-mirror"})
        html = urllib.request.urlopen(req, timeout=20).read().decode("utf-8", "ignore")
    except Exception as e:
        html = f"<p>fetch failed: {e}</p>"
    (out / f"{name}.html").write_text(html)
    index.append(f'<li><a href="{name}.html">{name}</a></li>')
index.append("</ul>")
(out / "index.html").write_text("\n".join(index))
print("mirrored", channels)
