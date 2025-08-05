#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import json

OWNER = "ManiVaultStudio"
REPOS = [
    ("Scatterplot", "View", "master"),
    ("ImageViewerPlugin", "View", "master"),
    ("HeatMap", "View", "master"),
    ("ParallelCoordinatesPlugin", "View", "master"),
    ("SpectralViewPlugin", "View", "main"),
    ("t-SNE-Analysis", "Analysis", "master"),
    ("MeanShiftClustering", "Analysis", "master"),
    ("PcaPlugin", "Analysis", "main"),
    ("SpidrPlugin", "Analysis", "main"),
    ("BinIO", "IO", "master"),
    ("ExtCsvLoader", "IO", "main"),
    ("ImageLoaderPlugin", "IO", "master"),
    ("HDF5Loader", "IO", "master"),
    ("UMAP-Plugin", "Analysis", "main"),
]

CORE_PREFIX = os.environ.get("CORE_PREFIX")
if not CORE_PREFIX:
    sys.exit("ERROR: Please set CORE_PREFIX, e.g. export CORE_PREFIX=release/core_1.3/")

# Derive core version
core_ver = CORE_PREFIX.removeprefix("release/core_").rstrip("/")

# Markdown header
lines = [
    "| Plugin | Type | Compatible Core | Version | Active | Status |",
    "|--------|:----:|:--------:|:----------------:|:------:|:------:|",
]

# Helpers
def fetch_json(url):
    r = requests.get(url, timeout=10)
    return r.json() if r.status_code == 200 else None

for repo, ptype, branch in REPOS:
    # badges
    active = f"![last commit](https://img.shields.io/github/last-commit/{OWNER}/{repo}/{branch})"
    status = f"![ci-build](https://github.com/{OWNER}/{repo}/actions/workflows/build.yml/badge.svg?branch={branch})"

    # Try PluginInfo.json
    info_url = f"https://raw.githubusercontent.com/{OWNER}/{repo}/{branch}/PluginInfo.json"
    info = fetch_json(info_url)

    if info:
        plugin_name = info.get("name", repo)
        core_version = ", ".join(info.get("version", {}).get("core", [])) or core_ver
        plugin_version = info.get("version", {}).get("plugin", "N/A")
    else:
        plugin_name = repo
        core_version = core_ver

        # Fetch branches
        api_url = f"https://api.github.com/repos/{OWNER}/{repo}/branches?per_page=100"
        branches = fetch_json(api_url) or []
        suffixes = [
            b["name"].removeprefix(CORE_PREFIX)
            for b in branches
            if b["name"].startswith(CORE_PREFIX)
        ]
        plugin_version = ", ".join(suffixes) if suffixes else "N/A"

    lines.append(
        f"| [{plugin_name}](https://github.com/{OWNER}/{repo})"
        f" | {ptype} | {core_version} | {plugin_version}"
        f" | {active} | {status} |"
    )

print("\n".join(lines))
