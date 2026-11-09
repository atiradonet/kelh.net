#!/usr/bin/env python3
"""Keep Subresource Integrity hashes in the HTML in step with the asset files.

Report URI's SRI Validator reports a script or stylesheet tag with no
`integrity` attribute as unprotected, so every /assets/ reference on this site
carries one. The attributes are generated from the files on disk rather than
written by hand, because a stale hash does not fail loudly: the browser simply
refuses to load the subresource, and a stylesheet that silently stops applying
is the kind of breakage nobody notices for a week.

Same-origin subresources need no `crossorigin` attribute -- SRI only requires
CORS when the resource comes from another origin -- so the tags carry
`integrity` alone.

    tools/sri.py --check    verify the committed hashes (CI uses this)
    tools/sri.py --fix      rewrite them from the files on disk

`--check` runs in both deploy workflows, so an asset edit that forgets `--fix`
fails the build instead of shipping a page with dead CSS.
"""

from __future__ import annotations

import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Every page that references a hashed asset. A page added later has to be
# listed here, or its tags go unchecked.
PAGES = ("index.html", "license.html", "security/index.html")

# Opening <link> / <script> tags. The pages are hand-written and well-formed,
# so a tolerant regex is enough here and avoids a dependency on an HTML parser.
TAG = re.compile(r"<(?P<name>link|script)\b(?P<attrs>[^>]*)>", re.IGNORECASE)
REF = re.compile(r'\b(?:href|src)\s*=\s*"(?P<url>/assets/[^"]+)"', re.IGNORECASE)
INTEGRITY = re.compile(r'\s+integrity\s*=\s*"[^"]*"', re.IGNORECASE)


def sri_hash(path: Path) -> str:
    """The sha384-<base64> form browsers expect in an integrity attribute."""
    return "sha384-" + base64.b64encode(hashlib.sha384(path.read_bytes()).digest()).decode()


def rewrite(html: str, problems: list[str], page: str) -> str:
    def fix_tag(match: re.Match[str]) -> str:
        attrs = match.group("attrs")
        ref = REF.search(attrs)
        if ref is None:
            return match.group(0)  # not an asset tag; leave it alone

        asset = ROOT / ref.group("url").lstrip("/")
        if not asset.is_file():
            problems.append(f"{page}: references {ref.group('url')}, which does not exist")
            return match.group(0)

        want = sri_hash(asset)
        had = re.search(r'\bintegrity\s*=\s*"(?P<value>[^"]*)"', attrs, re.IGNORECASE)
        if had is None:
            problems.append(f"{page}: {ref.group('url')} has no integrity attribute")
        elif had.group("value") != want:
            problems.append(
                f"{page}: {ref.group('url')} integrity is stale\n"
                f"      committed {had.group('value')}\n"
                f"      on disk   {want}"
            )
        else:
            return match.group(0)  # already correct

        # Drop any existing integrity attribute, then append the right one.
        # Trailing whitespace is trimmed so a self-closing "/>" stays tidy.
        cleaned = INTEGRITY.sub("", attrs).rstrip()
        return f'<{match.group("name")}{cleaned} integrity="{want}">'

    return TAG.sub(fix_tag, html)


def main(argv: list[str]) -> int:
    if len(argv) != 1 or argv[0] not in {"--check", "--fix"}:
        print(__doc__)
        return 2
    fix = argv[0] == "--fix"

    problems: list[str] = []
    changed: list[str] = []

    for page in PAGES:
        path = ROOT / page
        if not path.is_file():
            problems.append(f"{page}: listed in PAGES but missing from the repository")
            continue
        before = path.read_text(encoding="utf-8")
        after = rewrite(before, problems, page)
        if after != before:
            changed.append(page)
            if fix:
                path.write_text(after, encoding="utf-8")

    if fix:
        if changed:
            print("Updated integrity attributes in:")
            for page in changed:
                print(f"  {page}")
        else:
            print("All integrity attributes already match the assets on disk.")
        # A missing asset is a real error even under --fix.
        hard = [p for p in problems if "does not exist" in p or "missing from" in p]
        for p in hard:
            print(f"error: {p}", file=sys.stderr)
        return 1 if hard else 0

    if problems:
        print("Subresource Integrity check failed:", file=sys.stderr)
        print(file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        print(file=sys.stderr)
        print("Run tools/sri.py --fix and commit the result.", file=sys.stderr)
        return 1

    print(f"Subresource Integrity is current across {len(PAGES)} pages.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
