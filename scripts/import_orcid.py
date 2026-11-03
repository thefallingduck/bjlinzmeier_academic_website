#!/usr/bin/env python3
"""Create publication pages from the works listed on an ORCID record.

ORCID supplies the DOIs; Crossref supplies the metadata. Any DOI that does not
already appear in content/publications/*/index.md gets a new page bundle
(index.md + cite.bib). Standard library only.

Usage:  python3 scripts/import_orcid.py [--dry-run] [--fixtures DIR]
  --fixtures DIR  read orcid.json and crossref/<doi with / as __>.json from DIR
                  instead of the network (used for offline testing).
Writes a summary for the pull request body to scripts/import_report.md.
"""
import argparse, html, json, re, sys, urllib.request
from pathlib import Path

ORCID_ID = "0000-0002-3148-4971"
MY_FAMILY = "linzmeier"          # authors with this surname are written as `me`
CONTACT = "blinzmeier@southalabama.edu"
ROOT = Path(__file__).resolve().parent.parent
PUBS = ROOT / "content" / "publications"
REPORT = ROOT / "scripts" / "import_report.md"

TYPES = {"journal-article": "article-journal", "proceedings-article": "paper-conference",
         "book-chapter": "chapter", "book": "book", "posted-content": "manuscript",
         "dissertation": "thesis", "report": "report", "dataset": "dataset"}
STOP = {"a", "an", "the", "of", "on", "in", "for", "and", "to", "from", "with", "new"}


def get_json(url, accept="application/json"):
    req = urllib.request.Request(url, headers={
        "Accept": accept, "User-Agent": f"bjlinzmeier-site-import (mailto:{CONTACT})"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


def norm(doi):
    d = doi.strip().lower()
    return re.sub(r"^(https?://)?(dx\.)?doi\.org/", "", d)


def orcid_dois(fixtures):
    data = (json.loads((fixtures / "orcid.json").read_text(encoding="utf-8")) if fixtures
            else get_json(f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"))
    dois, nodoi, otypes = {}, [], {}
    for g in data.get("group", []):
        found = None
        for ei in (g.get("external-ids") or {}).get("external-id", []):
            if ei.get("external-id-type") == "doi" and ei.get("external-id-value"):
                found = norm(ei["external-id-value"]); break
        ws = (g.get("work-summary") or [{}])[0]
        title = (((ws.get("title") or {}).get("title")) or {}).get("value", "(untitled)")
        otype = (ws.get("type") or "").lower().replace("_", "-")
        if found: dois[found] = title; otypes[found] = otype
        else: nodoi.append(f"{title}  [ORCID type: {otype or 'unknown'}]")
    return dois, nodoi, otypes


def crossref(doi, fixtures):
    if fixtures:
        p = fixtures / "crossref" / (doi.replace("/", "__") + ".json")
        return json.loads(p.read_text(encoding="utf-8"))["message"]
    return get_json("https://api.crossref.org/works/" + urllib.request.quote(doi, safe="/"))["message"]


def clean(text):
    """Crossref titles/abstracts: keep <sub>/<sup>/<i>, drop other JATS markup."""
    t = re.sub(r"</?jats:(?:title|p|sec)[^>]*>", " ", text or "")
    t = re.sub(r"<(/?)b>", r"<\1i>", t)  # GSA uses bold tags for species names; show as italics
    t = re.sub(r"<jats:(sub|sup|italic)[^>]*>", lambda m: "<i>" if m.group(1) == "italic" else f"<{m.group(1)}>", t)
    t = re.sub(r"</jats:(sub|sup|italic)>", lambda m: "</i>" if m.group(1) == "italic" else f"</{m.group(1)}>", t)
    t = re.sub(r"</?(?!sub|sup|i\b)[a-z][^>]*>", " ", t, flags=re.I)
    t = re.sub(r"^\s*Abstract\s*[:.]?\s*", "", html.unescape(t), flags=re.I)
    return re.sub(r"\s+", " ", t).strip()


def title_of(msg):
    t = clean((msg.get("title") or [""])[0])
    t = re.sub(r"<[^>]+>", "", t)  # list views show titles as plain text, so no tags
    return t.capitalize() if t.isupper() else t


def tkey(t):
    return re.sub(r"[^a-z0-9]", "", clean(t).lower())


def existing_titles():
    out = set()
    for f in PUBS.glob("*/index.md"):
        m = re.search(r"^title:\s*(.+)$", f.read_text(encoding="utf-8"), re.M)
        if m: out.add(tkey(m.group(1).strip().strip("'\"")))
    return out


def existing_dois():
    out = set()
    for f in PUBS.glob("*/index.md"):
        m = re.search(r"^\s*doi:\s*['\"]?([^'\"\s]+)", f.read_text(encoding="utf-8"), re.M)
        if m: out.add(norm(m.group(1)))
    return out


def slug(msg, taken):
    a = (msg.get("author") or [{}])[0]
    fam = re.sub(r"[^a-z]", "", (a.get("family") or MY_FAMILY).lower())
    title = title_of(msg) or "paper"
    words = [w for w in re.findall(r"[a-z]+", title.lower()) if w not in STOP] or ["paper"]
    year = str(date_parts(msg)[0])
    base = f"{fam}-{words[0]}-{year}"; s, n = base, 2
    while s in taken: s, n = f"{base}-{n}", n + 1
    return s


def date_parts(msg):
    for k in ("published", "issued", "published-print", "published-online", "created"):
        dp = (msg.get(k) or {}).get("date-parts", [[None]])[0]
        if dp and dp[0]: return (dp + [1, 1])[:3]
    return [1970, 1, 1]


def q(s):  # JSON strings are valid YAML double-quoted scalars
    return json.dumps(s, ensure_ascii=False)


def bibtex(msg, key):
    au = " and ".join(f"{a.get('family','')}, {a.get('given','')}".strip(", ") for a in msg.get("author", []) if a.get("family") or a.get("given"))
    typ = "article" if msg.get("type") == "journal-article" else "misc"
    f = {"author": au, "title": title_of(msg),
         "journal": (msg.get("container-title") or [""])[0], "year": str(date_parts(msg)[0]),
         "volume": msg.get("volume", ""), "number": msg.get("issue", ""),
         "pages": msg.get("page", ""), "doi": msg.get("DOI", "")}
    body = ",\n".join(f" {k} = {{{v.replace(chr(38), chr(92)+chr(38)) if k != 'doi' else v}}}" for k, v in f.items() if v)
    return f"@{typ}{{{key},\n{body}\n}}\n"


# ORCID labels meeting abstracts imported from Crossref as "conference-paper", so that counts here.
ABSTRACT_ORCID_TYPES = {"conference-abstract", "conference-paper", "conference-poster", "conference-presentation", "lecture-speech"}


def pub_type(msg, otype=""):
    """Conference abstracts get their own type so the site can list them separately."""
    venue = (msg.get("container-title") or [""])[0].lower()
    if otype in ABSTRACT_ORCID_TYPES: return "conference-abstract"
    if "/abs/" in msg.get("DOI", "").lower() or "abstract" in venue:
        return "conference-abstract"
    return TYPES.get(msg.get("type"), "article")


def build_page(msg, otype=""):
    authors, seen = [], set()
    for a in msg.get("author", []):
        if not (a.get("given") or a.get("family")):
            continue  # organisations / affiliations listed as authors
        name = f"{a.get('given','')} {a.get('family','')}".strip()
        who = "me" if (a.get("family") or "").lower() == MY_FAMILY else name
        if who.lower() in seen:
            continue  # Crossref sometimes repeats every author
        seen.add(who.lower()); authors.append(who)
    if not authors: authors = ["me"]
    y, m, d = date_parts(msg)
    venue = (msg.get("container-title") or [""])[0]
    lines = ["---", f"title: {q(title_of(msg))}", "authors:"]
    lines += [f"- {q(a)}" if a != "me" else "- me" for a in authors]
    lines += [f"date: '{y:04d}-{m:02d}-{d:02d}'", "publication_types:",
              f"- {pub_type(msg, otype)}", "publication:", f"  name: {q(venue)}"]
    ab = clean(msg.get("abstract", ""))
    if ab: lines.append(f"abstract: {q(ab)}")
    lines += ["featured: false", "hugoblox:", "  ids:", f"    doi: {msg['DOI']}", "---", ""]
    return "\n".join(lines)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--list", action="store_true", help="print every work ORCID returns, then exit")
    ap.add_argument("--fixtures", type=Path)
    a = ap.parse_args()
    dois, nodoi, otypes = orcid_dois(a.fixtures)
    if a.list:
        print(f"ORCID returned {len(dois) + len(nodoi)} works ({len(dois)} with a DOI)\n")
        for d, t in sorted(dois.items(), key=lambda x: x[1].lower()): print(f"  {otypes.get(d) or '?':<20} {d}  |  {t[:70]}")
        for t in nodoi: print(f"  (no DOI)  |  {t[:90]}")
        return
    have = existing_dois()
    have_titles = existing_titles()
    dupes = []
    taken = {p.name for p in PUBS.iterdir() if p.is_dir()}
    added, review, failed = [], [], []
    for doi, title in sorted(dois.items()):
        if doi in have: continue
        try:
            msg = crossref(doi, a.fixtures)
        except Exception as e:
            failed.append(f"{title} (doi:{doi}): {e}"); continue
        if tkey(title_of(msg)) in have_titles:
            dupes.append(f"{title} (doi:{doi})"); continue
        s = slug(msg, taken); taken.add(s)
        if not a.dry_run:
            d = PUBS / s; d.mkdir(parents=True)
            (d / "index.md").write_text(build_page(msg, otypes.get(doi, "")), encoding="utf-8")
            (d / "cite.bib").write_text(bibtex(msg, s.replace("-", "_")), encoding="utf-8")
        added.append(f"`{s}`: {title} (https://doi.org/{doi})")
        if msg.get("type") == "posted-content":
            review.append(f"`{s}` is a preprint; delete it if the published version is already listed.")
        if not msg.get("abstract"): review.append(f"`{s}` has no abstract from Crossref.")
        if not msg.get("author"): review.append(f"`{s}` has no author list from Crossref, so only you are listed. Add the co-authors.")
        t0 = clean((msg.get("title") or [""])[0])
        if re.sub(r"<[^>]+>", "", t0).isupper(): review.append(f"`{s}` had an ALL-CAPS title; fix capitalization of names and terms.")
    out = ["## Publications imported from ORCID", ""]
    out += [f"- {x}" for x in added] or ["No new works with DOIs found."]
    if review: out += ["", "### Check before merging", ""] + [f"- {x}" for x in review]
    out += ["", "Dates come from Crossref; add a PDF as `<folder>.pdf` only if the publisher allows it."]
    if dupes: out += ["", "### Skipped: title matches a page you already have", ""] + [f"- {x}" for x in dupes]
    if failed: out += ["", "### Crossref lookup failed (will retry next run)", ""] + [f"- {x}" for x in failed]
    if nodoi: out += ["", "### On ORCID without a DOI (add by hand if wanted)", ""] + [f"- {x}" for x in nodoi]
    REPORT.write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    sys.exit(main())
