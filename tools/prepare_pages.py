#!/usr/bin/env python3
"""Prepare a 3DVista local mirror for static hosting.

Reads the user's ~/tour capture and its recursos_recuperados overlay,
normalizes query-string suffixes in downloaded filenames, and assembles
a site/ directory while preserving the relative paths expected by 3DVista.
It does not download files or modify the source tree.
"""
from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

HOST_PREFIX = Path("storage.net-fs.com/hosting/2727323/443")
SKIP_NAMES = {"robots.txt.gz"}
SKIP_PREFIXES = ("resultado", "tour_auditoria")


def normalized_name(name: str) -> str:
    # Some wget/capture workflows preserve ?v=... as literal filename text.
    return name.split("?", 1)[0]


def destination_for(source_root: Path, file_path: Path) -> Path | None:
    rel = file_path.relative_to(source_root)

    # The supplied tour.zip has a top-level tour/ wrapper. Support both that
    # extracted layout and a source directory whose contents are already at
    # the root, without changing the original files.
    if rel.parts and rel.parts[0] == "tour":
        rel = Path(*rel.parts[1:])

    if rel.parts and rel.parts[0] == "recursos_recuperados":
        rel = Path(*rel.parts[1:])
    elif rel.parts[:len(HOST_PREFIX.parts)] == HOST_PREFIX.parts:
        rel = Path(*rel.parts[len(HOST_PREFIX.parts):])
    elif rel.parts and rel.parts[0] in {"lib", "locale"}:
        pass
    elif rel.name in {"script.js", "script_general.js", "index.html"}:
        pass
    else:
        # Ignore audit reports, logs, and unrelated captures.
        return None

    if not rel.parts:
        return None
    clean_parts = [normalized_name(part) for part in rel.parts]
    if any(not part for part in clean_parts):
        return None
    return Path(*clean_parts)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path.home() / "tour")
    parser.add_argument("--output", type=Path, default=Path("site"))
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    output = args.output.expanduser().resolve()
    if not source.is_dir():
        parser.error(f"No existe el directorio fuente: {source}")
    if output == source or source in output.parents:
        parser.error("La carpeta de salida no puede estar dentro del directorio fuente.")

    output.mkdir(parents=True, exist_ok=True)
    copied, skipped = [], []

    for item in sorted(source.rglob("*")):
        if not item.is_file():
            continue
        if item.name in SKIP_NAMES or item.name.startswith(SKIP_PREFIXES):
            skipped.append(str(item.relative_to(source)))
            continue

        rel = destination_for(source, item)
        if rel is None:
            continue

        # The captured original index is the authoritative runtime entry point.
        target = output / rel
        target.parent.mkdir(parents=True, exist_ok=True)

        # Prefer the larger/non-empty file if multiple captures map to one path.
        if target.exists() and target.stat().st_size >= item.stat().st_size:
            continue
        shutil.copy2(item, target)
        copied.append({"source": str(item.relative_to(source)),
                       "destination": str(rel),
                       "bytes": item.stat().st_size})

    (output / ".nojekyll").touch(exist_ok=True)
    report = {
        "source": str(source),
        "output": str(output),
        "files_copied": len(copied),
        "files_skipped": len(skipped),
        "copied": copied,
        "skipped": skipped,
    }
    (output / "prepare-report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "output": str(output),
        "files_copied": len(copied),
        "files_skipped": len(skipped),
        "index_present": (output / "index.html").is_file(),
        "player_present": (output / "lib/tdvplayer.js").is_file(),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
