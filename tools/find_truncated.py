#!/usr/bin/env python3
"""Find potentially truncated FR translations by comparing EN/FR text lengths."""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ends_abruptly(en_text, fr_text):
    """Check if FR text ends abruptly compared to EN text."""
    fr_stripped = fr_text.rstrip()
    if not fr_stripped:
        return False
    # Ends with a single letter (likely mid-word truncation)
    if re.search(r'\s[a-zA-ZÀ-ÿ]$', fr_stripped):
        return True
    # EN ends with closing punctuation but FR doesn't
    en_stripped = en_text.rstrip()
    en_has_closing = bool(re.search(r'[.!?"\'\)\]]$', en_stripped))
    fr_has_closing = bool(re.search(r'[.!?"\'\)\]]$', fr_stripped))
    if en_has_closing and not fr_has_closing:
        return True
    return False

results = []

for batch_num in range(1, 7):
    for part_num in range(1, 18):
        batch_file = os.path.join(SCRIPT_DIR, f"batch_{batch_num}_{part_num}.json")
        tr_file = os.path.join(SCRIPT_DIR, f"tr_{batch_num}_{part_num}.json")

        if not os.path.exists(batch_file) or not os.path.exists(tr_file):
            continue

        en_data = load_json(batch_file)
        fr_data = load_json(tr_file)

        # Build index maps
        en_map = {item[0]: item[1] for item in en_data}
        fr_map = {item[0]: item[1] for item in fr_data}

        for idx in en_map:
            if idx not in fr_map:
                continue
            en_text = en_map[idx]
            fr_text = fr_map[idx]
            en_len = len(en_text)
            fr_len = len(fr_text)

            length_suspicious = (en_len > 100 and fr_len < 0.4 * en_len)
            abrupt_end = ends_abruptly(en_text, fr_text) and en_len > 50

            if length_suspicious or abrupt_end:
                reason = []
                if length_suspicious:
                    reason.append(f"SHORT ({fr_len}/{en_len} = {fr_len/en_len:.0%})")
                if abrupt_end:
                    reason.append("ABRUPT_END")

                results.append({
                    "file": f"batch_{batch_num}_{part_num} / tr_{batch_num}_{part_num}",
                    "index": idx,
                    "en_len": en_len,
                    "fr_len": fr_len,
                    "ratio": fr_len / en_len if en_len > 0 else 0,
                    "en_tail": en_text[-50:],
                    "fr_tail": fr_text[-50:],
                    "reason": ", ".join(reason),
                })

print(f"\n{'='*100}")
print(f"TRUNCATION SCAN: {len(results)} suspicious entries found")
print(f"{'='*100}\n")

for r in sorted(results, key=lambda x: x["ratio"]):
    print(f"File: {r['file']}  |  Index: {r['index']}  |  Reason: {r['reason']}")
    print(f"  EN length: {r['en_len']}  |  FR length: {r['fr_len']}  |  Ratio: {r['ratio']:.1%}")
    print(f"  EN tail: ...{r['en_tail']}")
    print(f"  FR tail: ...{r['fr_tail']}")
    print()
