#!/usr/bin/env python3
"""Fix \n count mismatches between batch_X_Y.json (EN) and tr_X_Y.json (FR).

For each text pair where the \n counts differ:
- If FR has MORE \n: remove extra \n by replacing them with spaces,
  keeping only those \n whose relative position best matches the EN \n positions.
- If FR has FEWER \n: insert \n at positions proportional to the EN \n positions.
"""

import json
import os
import glob
import copy


def find_newline_positions(text):
    """Return list of indices where \n occurs."""
    return [i for i, c in enumerate(text) if c == '\n']


def fix_fr_too_many_newlines(en_text, fr_text):
    """FR has more \n than EN. Remove extras, keeping best-matching ones."""
    en_positions = find_newline_positions(en_text)
    fr_positions = find_newline_positions(fr_text)
    en_count = len(en_positions)
    fr_count = len(fr_positions)

    if en_count == 0:
        # EN has no newlines at all - remove ALL \n from FR
        return fr_text.replace('\n\n', ' ').replace('\n', ' ')

    # Convert positions to relative (0..1) within their respective texts
    en_len = len(en_text)
    fr_len = len(fr_text)

    en_rel = [p / en_len for p in en_positions]
    fr_rel = [p / fr_len for p in fr_positions]

    # Greedily select FR \n positions that best match EN \n positions
    # For each EN \n (in order), find the closest unmatched FR \n
    keep_fr_indices = set()
    used_fr = set()

    for en_r in en_rel:
        best_j = None
        best_dist = float('inf')
        for j, fr_r in enumerate(fr_rel):
            if j in used_fr:
                continue
            dist = abs(en_r - fr_r)
            if dist < best_dist:
                best_dist = dist
                best_j = j
        if best_j is not None:
            keep_fr_indices.add(best_j)
            used_fr.add(best_j)

    # Build new FR text, replacing non-kept \n with space
    # But handle \n\n sequences: if both \n in a \n\n pair are removed,
    # replace with single space (not two spaces)
    result = list(fr_text)
    remove_positions = set()
    for j, pos in enumerate(fr_positions):
        if j not in keep_fr_indices:
            remove_positions.add(pos)

    # Replace removed \n with spaces, but avoid double spaces
    # Process from end to start to maintain indices
    for pos in sorted(remove_positions, reverse=True):
        # Check if adjacent char is also a removed \n
        if pos + 1 in remove_positions or (pos > 0 and pos - 1 in remove_positions and result[pos - 1] == ' '):
            # Part of a \n\n sequence being fully removed - replace with nothing
            # (the other \n will become a space)
            result[pos] = ''
        else:
            result[pos] = ' '

    new_text = ''.join(result)
    # Clean up any double spaces that may have been introduced
    while '  ' in new_text:
        new_text = new_text.replace('  ', ' ')

    return new_text


def fix_fr_too_few_newlines(en_text, fr_text):
    """FR has fewer \n than EN. Insert \n at proportional positions."""
    en_positions = find_newline_positions(en_text)
    fr_positions = find_newline_positions(fr_text)
    en_count = len(en_positions)
    fr_count = len(fr_positions)

    en_len = len(en_text)
    fr_len = len(fr_text)

    # We need to add (en_count - fr_count) newlines to FR
    # Find EN \n relative positions
    en_rel = [p / en_len for p in en_positions]
    fr_rel = set(p / fr_len for p in fr_positions)

    # For each EN \n position, check if FR already has one nearby
    # If not, insert one at the proportional position
    existing_fr = set(fr_positions)
    new_positions = []

    for en_r in en_rel:
        target_pos = int(en_r * fr_len)
        # Check if FR already has a \n near this position
        has_nearby = False
        for fp in fr_positions:
            if abs(fp / fr_len - en_r) < 0.05:  # within 5% relative distance
                has_nearby = True
                break
        if has_nearby:
            continue

        # Find a good insertion point near target_pos
        # Prefer inserting after a sentence end (. or ") or at a space
        best_pos = target_pos
        search_range = min(50, fr_len // 10)
        best_score = -1

        for offset in range(-search_range, search_range + 1):
            pos = target_pos + offset
            if pos < 1 or pos >= fr_len:
                continue
            char_before = fr_text[pos - 1]
            char_at = fr_text[pos]

            # Score: prefer after sentence-ending punctuation, then after quotes, then spaces
            score = 0
            if char_before in '.!?"':
                score = 3
            elif char_before == ' ':
                score = 1
            elif char_at == ' ':
                score = 1

            # Penalize being far from target
            score -= abs(offset) * 0.01

            if score > best_score:
                best_score = score
                best_pos = pos

        new_positions.append(best_pos)

    if not new_positions:
        return fr_text

    # Insert \n at new positions (process from end to preserve indices)
    result = list(fr_text)
    for pos in sorted(new_positions, reverse=True):
        # Check what EN has at this relative position - is it \n or \n\n?
        en_rel_pos = pos / fr_len
        # Find the matching EN \n
        matching_en_idx = None
        for i, er in enumerate(en_rel):
            if abs(er - en_rel_pos) < 0.1:
                matching_en_idx = en_positions[i]
                break

        # Check if EN has \n\n (double newline = paragraph break)
        if matching_en_idx is not None and matching_en_idx + 1 < en_len and en_text[matching_en_idx + 1] == '\n':
            # Insert \n\n
            # Remove any space at insertion point
            if pos < len(result) and result[pos] == ' ':
                result[pos] = '\n\n'
            else:
                result.insert(pos, '\n\n')
        else:
            # Single \n
            result.insert(pos, '\n')

    return ''.join(result)


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    batch_files = sorted(glob.glob(os.path.join(base_dir, "batch_*_*.json")))

    total_fixed = 0
    fixes = []

    for batch_path in batch_files:
        fname = os.path.basename(batch_path)
        tr_fname = "tr_" + fname[len("batch_"):]
        tr_path = os.path.join(base_dir, tr_fname)

        if not os.path.exists(tr_path):
            continue

        with open(batch_path, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        with open(tr_path, "r", encoding="utf-8") as f:
            fr_data = json.load(f)

        en_dict = {item[0]: item[1] for item in en_data}
        fr_dict = {item[0]: item[1] for item in fr_data}
        modified = False

        for i, item in enumerate(fr_data):
            idx = item[0]
            if idx not in en_dict:
                continue

            en_text = en_dict[idx]
            fr_text = item[1]
            en_count = en_text.count('\n')
            fr_count = fr_text.count('\n')

            if en_count == fr_count:
                continue

            # Fix needed
            if fr_count > en_count:
                new_fr = fix_fr_too_many_newlines(en_text, fr_text)
            else:
                new_fr = fix_fr_too_few_newlines(en_text, fr_text)

            new_count = new_fr.count('\n')
            if new_count != en_count:
                print(f"  WARNING: {tr_fname} idx={idx} fix incomplete: "
                      f"EN={en_count}, was FR={fr_count}, now FR={new_count}")

            fixes.append({
                'file': tr_fname,
                'index': idx,
                'en_newlines': en_count,
                'old_fr_newlines': fr_count,
                'new_fr_newlines': new_count,
                'ok': new_count == en_count,
            })

            fr_data[i][1] = new_fr
            modified = True
            total_fixed += 1

        if modified:
            with open(tr_path, "w", encoding="utf-8") as f:
                json.dump(fr_data, f, ensure_ascii=False, indent=None)

    # Report
    print("=" * 70)
    print(f"FIXES APPLIED: {total_fixed}")
    print("=" * 70)
    ok_count = sum(1 for f in fixes if f['ok'])
    fail_count = sum(1 for f in fixes if not f['ok'])
    print(f"  Successful: {ok_count}")
    print(f"  Incomplete: {fail_count}")
    print()

    for fix in fixes:
        status = "OK" if fix['ok'] else "FAIL"
        print(f"  [{status}] {fix['file']} idx={fix['index']:>5d}  "
              f"EN:\\n={fix['en_newlines']}  FR:{fix['old_fr_newlines']}->{fix['new_fr_newlines']}")

    # Re-run audit
    print()
    print("=" * 70)
    print("RE-AUDIT AFTER FIXES")
    print("=" * 70)
    total_texts = 0
    total_mismatch = 0
    remaining = []

    for batch_path in batch_files:
        fname = os.path.basename(batch_path)
        tr_fname = "tr_" + fname[len("batch_"):]
        tr_path = os.path.join(base_dir, tr_fname)

        if not os.path.exists(tr_path):
            continue

        with open(batch_path, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        with open(tr_path, "r", encoding="utf-8") as f:
            fr_data = json.load(f)

        fr_dict = {item[0]: item[1] for item in fr_data}
        for item in en_data:
            idx = item[0]
            if idx not in fr_dict:
                continue
            total_texts += 1
            en_n = item[1].count('\n')
            fr_n = fr_dict[idx].count('\n')
            if en_n != fr_n:
                total_mismatch += 1
                remaining.append((fname, idx, en_n, fr_n))

    print(f"Total texts: {total_texts}")
    print(f"Remaining mismatches: {total_mismatch}")
    if remaining:
        for r in remaining:
            print(f"  {r[0]} idx={r[1]} EN:{r[2]} FR:{r[3]}")


if __name__ == "__main__":
    main()
