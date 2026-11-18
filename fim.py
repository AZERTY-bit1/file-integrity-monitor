#!/usr/bin/env python3
"""File Integrity Monitor (FIM).

Creates a SHA-256 baseline of a folder, then detects files that were
added, modified or deleted since. Useful to spot unexpected changes
(tampering, malware, mistakes) on your own machine.
"""
import argparse
import hashlib
import json
import os
import sys
import time


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def scan(folder: str, exclude=None) -> dict:
    exclude = set(exclude or [])
    result = {}
    for root, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d not in exclude]
        for name in files:
            full = os.path.join(root, name)
            rel = os.path.relpath(full, folder)
            if rel in exclude or name in exclude:
                continue
            try:
                result[rel] = sha256_file(full)
            except (PermissionError, OSError):
                continue
    return result


def compare(baseline: dict, current: dict) -> dict:
    added = sorted(set(current) - set(baseline))
    deleted = sorted(set(baseline) - set(current))
    modified = sorted(p for p in set(baseline) & set(current) if baseline[p] != current[p])
    return {"added": added, "deleted": deleted, "modified": modified}


def cmd_init(args):
    data = {"folder": os.path.abspath(args.folder), "created": time.ctime(),
            "files": scan(args.folder, [os.path.basename(args.baseline)])}
    with open(args.baseline, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[+] Baseline saved: {len(data['files'])} files -> {args.baseline}")


def cmd_check(args):
    with open(args.baseline) as f:
        base = json.load(f)
    current = scan(args.folder, [os.path.basename(args.baseline)])
    diff = compare(base["files"], current)
    total = sum(len(v) for v in diff.values())
    if total == 0:
        print("[OK] No changes detected.")
        return 0
    for kind, sign in (("added", "+"), ("modified", "~"), ("deleted", "-")):
        for p in diff[kind]:
            print(f"[{sign}] {kind.upper():8} {p}")
    print(f"[!] {total} change(s) detected.")
    return 1


def cmd_watch(args):
    print(f"[*] Watching {args.folder} every {args.interval}s (Ctrl+C to stop)")
    with open(args.baseline) as f:
        known = json.load(f)["files"]
    try:
        while True:
            time.sleep(args.interval)
            current = scan(args.folder, [os.path.basename(args.baseline)])
            diff = compare(known, current)
            for kind in ("added", "modified", "deleted"):
                for p in diff[kind]:
                    print(f"{time.strftime('%H:%M:%S')} ALERT {kind}: {p}")
            known = current
    except KeyboardInterrupt:
        print("\n[*] Stopped.")


def main():
    p = argparse.ArgumentParser(description="Simple File Integrity Monitor (SHA-256)")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in (("init", cmd_init), ("check", cmd_check), ("watch", cmd_watch)):
        s = sub.add_parser(name)
        s.add_argument("folder")
        s.add_argument("-b", "--baseline", default="baseline.json")
        if name == "watch":
            s.add_argument("-i", "--interval", type=int, default=10)
        s.set_defaults(func=fn)
    args = p.parse_args()
    sys.exit(args.func(args) or 0)


if __name__ == "__main__":
    main()
