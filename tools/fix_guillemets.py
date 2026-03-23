#!/usr/bin/env python3
"""
Remplace les guillemets droits "..." par des guillemets français « ... »
dans la colonne text (index 4) de rules.csv, uniquement sur les lignes traduites.

Règles :
- " ouvrant → «\u00a0 (avec espace insécable après)
- " fermant → \u00a0» (avec espace insécable avant)
- Dialogue multi-paragraphe (nombre impair de ") : chaque " ouvrant de paragraphe
  obtient «, le dernier " du texte est fermant et obtient »
"""

import csv
import io
import re

VANILLA_PATH = "D:/Fractal Softworks/Starsector/starsector-core/data/campaign/rules.csv"
MOD_PATH = "data/campaign/rules.csv"
NBSP = "\u00a0"  # espace insécable


def is_opening_quote(text, pos):
    """Détermine si le " à la position pos est un guillemet ouvrant."""
    if pos == 0:
        return True
    # Après un retour à la ligne (début de paragraphe) = ouvrant
    before = text[pos - 1]
    if before == "\n":
        return True
    # Après un espace, une parenthèse ouvrante = ouvrant
    if before in (" ", "\t", "(", "[", "\r"):
        return True
    # Sinon = fermant (après lettre, ponctuation, etc.)
    return False


def replace_quotes_french(text):
    """Remplace les " par « » dans un texte de dialogue.

    Utilise le contexte (position dans le texte) pour déterminer
    si chaque " est ouvrant ou fermant, au lieu d'alterner simplement.
    """
    if '"' not in text:
        return text

    result = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == '"':
            if is_opening_quote(text, i):
                result.append("«" + NBSP)
            else:
                result.append(NBSP + "»")
        else:
            result.append(ch)
        i += 1

    return "".join(result)


def main():
    # Load vanilla texts
    vanilla_texts = {}
    with open(VANILLA_PATH, "r", encoding="cp1252") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) >= 5:
                vanilla_texts[i] = row[4]

    # Read mod CSV
    with open(MOD_PATH, "r", encoding="utf-8") as f:
        raw_content = f.read()

    # Parse with csv module
    rows = []
    reader = csv.reader(io.StringIO(raw_content))
    for row in reader:
        rows.append(row)

    # Apply replacements
    changed = 0
    for i, row in enumerate(rows):
        if len(row) >= 5:
            text = row[4]
            vanilla = vanilla_texts.get(i, "")
            # Only modify translated texts (different from vanilla)
            if text != vanilla and text.strip() and '"' in text:
                new_text = replace_quotes_french(text)
                if new_text != text:
                    row[4] = new_text
                    changed += 1

    print(f"Textes modifiés : {changed}")

    # Write back with same format
    output = io.StringIO()
    writer = csv.writer(output, lineterminator="\r\n")
    for row in rows:
        writer.writerow(row)

    with open(MOD_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(output.getvalue())

    # Verify
    verify_count = 0
    with open(MOD_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) >= 5:
                if "«" in row[4] or "»" in row[4]:
                    verify_count += 1

    print(f"Textes avec « » après correction : {verify_count}")

    # Check no remaining " in translated texts
    remaining = 0
    with open(MOD_PATH, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for i, row in enumerate(reader):
            if len(row) >= 5:
                text = row[4]
                vanilla = vanilla_texts.get(i, "")
                if text != vanilla and text.strip() and '"' in text:
                    remaining += 1

    print(f"Textes traduits avec \" restants : {remaining}")


if __name__ == "__main__":
    main()
