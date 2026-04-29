"""
build_lexicon.py  —  Philolog Lexicon Processor
================================================
Steps:
  1. SECURITY SCAN  — strip SQL injections, script tags from reference file
  2. PARSE TBESG    — extract tab-delimited data rows (start with G####)
  3. FILTER         — keep only Strong's IDs present in our lexicon
  4. UTF-8 VERIFY   — decode/re-encode strictly as UTF-8
  5. ENRICH         — fill missing Greek lemmas, glosses, LSJ notes
  6. DEDUPLICATE    — merge contexts for identical Greek lemmas
  7. OUTPUT         — lexicon_MASTER.json  +  lexicon.json (clean)
"""

import json, re
from pathlib import Path

BASE       = Path(__file__).parent
INPUT      = BASE / "texts" / "lexicon.json"
REF_FILE   = BASE / "reference_data.txt"
MASTER_OUT = BASE / "texts" / "lexicon_MASTER.json"
PROD_OUT   = BASE / "texts" / "lexicon.json"

GREEK_RE = re.compile(r'[\u0370-\u03FF\u1F00-\u1FFF]')

LSJ_CORRECTIONS = {
    "bloodguilt":      ("blood",
                        "LSJ primary: haima = blood. Liturgical context: guilt of bloodshed."),
    "loving-kindness": ("mercy, pity",
                        "LSJ: eleos = mercy, pity. Liturgical use: God's steadfast covenant love."),
    "O Lord":          ("lord, master",
                        "Vocative form Kyrie; LSJ primary of Kyrios = having power, lord."),
    "Theotokos":       ("God-bearer, Mother of God",
                        "Liturgical title; compound theos + tokos (birth). Not in classical LSJ."),
    "gladsome light":  ("joyful, glad",
                        "LSJ: hilaros = cheerful, glad. Liturgical phrase Phos hilaron = Gladsome Light."),
}

MANUAL_FIXES = {
    "theh-OS":    dict(lemma="\u0398\u03b5\u03cc\u03c2",   gloss="god, God",       strongs="G2316", partOfSpeech="noun",
                       liturgical_note="LSJ: theos = god. Used as proper name of God in LXX/NT."),
    "KEE-ree-eh": dict(lemma="\u039a\u03cd\u03c1\u03b9\u03bf\u03c2", gloss="lord, master", strongs="G2962", partOfSpeech="noun",
                       liturgical_note="Vocative Kyrie — the standard liturgical address O Lord."),
    "meh":        dict(lemma="\u1f10\u03b3\u03ce",   gloss="I, me",          strongs="G1473", partOfSpeech="pronoun",
                       liturgical_note="Accusative me; appears as me in liturgical translation."),
    "soo":        dict(lemma="\u03c3\u03cd",    gloss="you (singular)", strongs="G4771", partOfSpeech="pronoun",
                       liturgical_note="Genitive sou; appears as your in liturgical translation."),
}

SQL_RE    = re.compile(r'\b(DROP\s+TABLE|INSERT\s+INTO|DELETE\s+FROM|UPDATE\s+SET|ALTER\s+TABLE|CREATE\s+TABLE|TRUNCATE|EXEC\s*\(|xp_cmdshell)\b', re.IGNORECASE)
SCRIPT_RE = re.compile(r'<\s*script[\s>]|javascript\s*:', re.IGNORECASE)
ROW_RE    = re.compile(r'^G\d{4,5}\b')

def security_scan(lines):
    clean, injections = [], []
    for i, line in enumerate(lines, 1):
        if SQL_RE.search(line):
            injections.append((i, "SQL", line[:120]))
            continue
        if SCRIPT_RE.search(line):
            injections.append((i, "SCRIPT", line[:120]))
            continue
        clean.append(line)
    return clean, injections

def parse_tbesg(lines):
    db = {}
    for line in lines:
        line = line.rstrip('\n')
        if not ROW_RE.match(line):
            continue
        parts = line.split('\t')
        if len(parts) < 7:
            continue
        sid   = parts[0].strip()
        greek = parts[3].strip()
        trans = parts[4].strip()
        short = parts[6].strip()
        full  = parts[7].strip() if len(parts) > 7 else ""
        base_sid = re.match(r'(G\d{4,5})', sid)
        if not base_sid:
            continue
        sid = base_sid.group(1)
        full_clean = re.sub(r'<[^>]+>', '', full)
        full_clean = re.sub(r'\s+', ' ', full_clean).strip()
        if sid not in db:
            db[sid] = {"lemma": greek, "translit": trans, "gloss": short, "definition": full_clean}
    return db

def collect_our_strongs(lexicon):
    ids = set()
    for e in lexicon:
        sid = e.get("strongs", "")
        if sid:
            ids.add(sid)
    for fix in MANUAL_FIXES.values():
        ids.add(fix["strongs"])
    return ids

def is_greek(text):
    return bool(GREEK_RE.search(text or ""))

def clean_str(text):
    return re.sub(r'[.,;]+$', '', (text or "").strip())

def pos_norm(pos):
    return (pos or "").lower().strip()

def apply_lsj(entry):
    g = clean_str(entry.get("gloss") or entry.get("definition") or "")
    if g in LSJ_CORRECTIONS:
        lsj_gloss, note = LSJ_CORRECTIONS[g]
        entry["gloss"] = lsj_gloss
        entry.setdefault("liturgical_note", note)
    return entry

def process(lexicon, tbesg_db):
    lemma_map = {}
    for raw in lexicon:
        e = dict(raw)
        phonetic = (e.get("phonetic") or "").strip()
        sid = e.get("strongs", "")
        if not is_greek(e.get("lemma", "")):
            fix = MANUAL_FIXES.get(phonetic)
            if fix:
                e.update(fix)
                e["audit_note"] = "Lemma replaced: was English — fixed via phonetic map"
            elif sid and sid in tbesg_db:
                truth = tbesg_db[sid]
                if is_greek(truth["lemma"]):
                    e["lemma"] = truth["lemma"]
                    e.setdefault("gloss", clean_str(truth["gloss"]))
                    e["audit_note"] = f"Lemma fixed via TBESG {sid}"
                else:
                    e["audit_note"] = f"WARNING: TBESG {sid} also lacks Greek lemma"
            else:
                e["audit_note"] = "WARNING: Could not resolve Greek lemma"
        if not is_greek(e.get("lemma", "")):
            print(f"  SKIP: {repr(e.get('lemma'))}")
            continue
        if not e.get("gloss"):
            if sid and sid in tbesg_db:
                e["gloss"] = clean_str(tbesg_db[sid]["gloss"] or tbesg_db[sid]["definition"])
            else:
                e["gloss"] = clean_str(e.get("definition", ""))
        if not e.get("phonetic") and sid and sid in tbesg_db:
            e["phonetic"] = tbesg_db[sid]["translit"]
        if sid and sid in tbesg_db:
            e["tbesg_definition"] = tbesg_db[sid]["definition"]
        e["partOfSpeech"] = pos_norm(e.get("partOfSpeech"))
        e = apply_lsj(e)
        greek_lemma = e["lemma"].replace("\u00b7", "").strip()
        if greek_lemma not in lemma_map:
            lemma_map[greek_lemma] = e
            lemma_map[greek_lemma]["contexts"] = list(e.get("contexts") or [])
        else:
            existing = set(lemma_map[greek_lemma]["contexts"])
            incoming = set(e.get("contexts") or [])
            lemma_map[greek_lemma]["contexts"] = sorted(existing | incoming)
            if not lemma_map[greek_lemma].get("gloss") and e.get("gloss"):
                lemma_map[greek_lemma]["gloss"] = e["gloss"]
            if e.get("audit_note"):
                prev = lemma_map[greek_lemma].get("audit_note", "")
                if e["audit_note"] not in prev:
                    lemma_map[greek_lemma]["audit_note"] = (prev + "; " + e["audit_note"]).strip("; ")
    return sorted(lemma_map.values(), key=lambda x: x["lemma"])

def make_master(processed):
    out = []
    for e in processed:
        out.append({
            "lemma":            e.get("lemma"),
            "phonetic":         e.get("phonetic", ""),
            "gloss":            e.get("gloss", ""),
            "partOfSpeech":     e.get("partOfSpeech", ""),
            "strongs":          e.get("strongs", ""),
            "strongs_translit": e.get("strongs_translit", ""),
            "tbesg_definition": e.get("tbesg_definition", ""),
            "definition":       e.get("definition", ""),
            "liturgical_note":  e.get("liturgical_note", ""),
            "audit_note":       e.get("audit_note", ""),
            "contexts":         e.get("contexts", []),
            "frequency":        e.get("frequency", 0),
            "roots":            e.get("roots", ""),
            "related":          e.get("related", ""),
            "derivation":       e.get("derivation", ""),
        })
    return out

def make_production(processed):
    out = []
    for e in processed:
        entry = {
            "lemma":        e.get("lemma"),
            "phonetic":     e.get("phonetic", ""),
            "gloss":        e.get("gloss", ""),
            "partOfSpeech": e.get("partOfSpeech", ""),
            "contexts":     e.get("contexts", []),
        }
        if e.get("liturgical_note"):
            entry["liturgical_note"] = e["liturgical_note"]
        out.append(entry)
    return out

def main():
    print(f"Loading {INPUT.name} ...")
    lexicon = json.loads(INPUT.read_bytes().decode("utf-8"))
    print(f"  {len(lexicon)} raw entries")
    our_strongs = collect_our_strongs(lexicon)
    print(f"  {len(our_strongs)} unique Strong's IDs in our data")

    print(f"\nReading {REF_FILE.name} ...")
    raw_bytes = REF_FILE.read_bytes()
    try:
        raw_bytes.decode("utf-8")
        print("  UTF-8 verification: PASS")
    except UnicodeDecodeError as err:
        print(f"  UTF-8 WARNING — bad bytes at pos {err.start}; replacing")
    text  = raw_bytes.decode("utf-8", errors="replace")
    lines = text.splitlines()
    print(f"  {len(lines)} lines total")

    clean_lines, injections = security_scan(lines)
    if injections:
        print(f"  SECURITY: {len(injections)} suspicious lines removed")
        for lineno, kind, snippet in injections:
            print(f"    Line {lineno} [{kind}]: {snippet!r}")
    else:
        print("  Security scan: PASS — no injections found")

    tbesg_db = parse_tbesg(clean_lines)
    print(f"  Parsed {len(tbesg_db)} TBESG entries")
    filtered_db = {k: v for k, v in tbesg_db.items() if k in our_strongs}
    print(f"  Filtered to {len(filtered_db)} entries matching our lexicon")

    print("\nProcessing lexicon entries...")
    processed = process(lexicon, filtered_db)
    print(f"  {len(processed)} deduplicated Greek entries")

    master = make_master(processed)
    MASTER_OUT.write_text(json.dumps(master, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n  Written: {MASTER_OUT.name}")

    production = make_production(processed)
    prod_json = json.dumps(production, ensure_ascii=False, indent=2)
    prod_json.encode("utf-8").decode("utf-8")  # final UTF-8 round-trip check
    PROD_OUT.write_text(prod_json, encoding="utf-8")
    print(f"  Written: {PROD_OUT.name}")

    warnings  = [e for e in master if "WARNING" in (e.get("audit_note") or "")]
    fixes     = [e for e in master if "fixed" in (e.get("audit_note") or "").lower() or "replaced" in (e.get("audit_note") or "").lower()]
    lsj_edits = [e for e in master if e.get("liturgical_note")]
    no_gloss  = [e for e in production if not e.get("gloss")]

    print("\n── Summary ─────────────────────────────────────────────────────")
    print(f"  Raw input entries:         {len(lexicon)}")
    print(f"  Output entries (deduped):  {len(production)}")
    print(f"  Lemmas fixed (non-Greek):  {len(fixes)}")
    print(f"  LSJ gloss corrections:     {len(lsj_edits)}")
    print(f"  Entries still no gloss:    {len(no_gloss)}")
    print(f"  Audit warnings:            {len(warnings)}")
    if warnings:
        print("\n  Warnings:")
        for e in warnings:
            print(f"    - {e['lemma']!r}: {e['audit_note']}")
    if no_gloss:
        print("\n  Still missing gloss:")
        for e in no_gloss:
            print(f"    - {e['lemma']!r}")
    if lsj_edits:
        print("\n  LSJ-corrected entries:")
        for e in lsj_edits:
            print(f"    - {e['lemma']} -> {e['gloss']!r}")
    print("\nDone.")

if __name__ == "__main__":
    main()
