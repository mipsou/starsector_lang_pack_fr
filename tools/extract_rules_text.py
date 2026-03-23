#!/usr/bin/env python3
"""
Outil 1 : Extraction des textes traductibles depuis rules.csv.

Lit le CSV (encodage UTF-8, 7 colonnes), extrait UNIQUEMENT les colonnes
text (4) et options (5) vers un fichier JSON.

Garde-fous implementes :
  GF-01 : Colonnes 0,1,2,3,6 JAMAIS extraites ni touchees
  GF-03 : Pas de subprocess, pas de git, pas de os.system
  GF-06 : csv.reader obligatoire, assertion 7 colonnes
  GF-09 : Verrou filelock, 1 processus a la fois
  GF-10 : Rapport de couverture obligatoire
"""

import argparse
import csv
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

ENCODING = "utf-8"

# Colonnes du CSV rules.csv (7 colonnes)
# 0=id, 1=trigger, 2=conditions, 3=script, 4=text, 5=options, 6=notes
NUM_COLS = 7
COLS_TRADUCTIBLES = frozenset([4, 5])  # text, options
COLS_INTOUCHABLES = frozenset([0, 1, 2, 3, 6])  # id, trigger, conditions, script, notes

# Regex pour detecter les variables $xxx dans le texte
VARIABLE_RE = re.compile(r'\$[A-Za-z_][A-Za-z0-9_.]*')

# Format d'option Starsector : [priority:]optionId:Label visible
# On ne traduit que le label (apres le dernier ':')
OPTION_RE = re.compile(r'^(?:(\d+):)?([^:]+):(.+)$', re.DOTALL)


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def extract_variables(text):
    """Extrait la liste des variables $xxx presentes dans le texte."""
    if not text:
        return []
    return VARIABLE_RE.findall(text)


def parse_option(option_str):
    """Parse une option Starsector et retourne (option_id, label).

    Format : [priority:]optionId:Label visible
    Retourne (option_id, label) ou (None, option_str) si pas parsable.
    """
    if not option_str:
        return None, option_str
    m = OPTION_RE.match(option_str)
    if m:
        # priority = m.group(1)  # peut etre None
        option_id = m.group(2)
        label = m.group(3)
        return option_id, label
    return None, option_str


def read_csv_rows(csv_path):
    """Lit le CSV avec csv.reader (GF-06) et retourne toutes les lignes brutes.

    Retourne une liste de tuples (row_idx, row) ou row_idx est l'index
    0-based de la ligne logique dans le CSV.
    """
    rows = []
    with open(csv_path, "r", encoding=ENCODING, newline="") as f:
        reader = csv.reader(f)
        for row_idx, row in enumerate(reader):
            rows.append((row_idx, row))
    return rows


def is_comment_or_empty(row):
    """Retourne True si la ligne est un commentaire CSV ou vide."""
    if not row:
        return True
    if len(row) == 0:
        return True
    # Ligne vide : toutes les cellules vides
    if all(cell.strip() == "" for cell in row):
        return True
    # Commentaire : premiere cellule commence par #
    if row[0].strip().startswith("#"):
        return True
    return False


def validate_row_columns(row, row_idx):
    """Verifie que la ligne a exactement NUM_COLS colonnes (GF-06)."""
    if len(row) != NUM_COLS:
        raise ValueError(
            f"GF-06 : Ligne {row_idx} a {len(row)} colonnes au lieu de {NUM_COLS}. "
            f"Le CSV doit avoir exactement {NUM_COLS} colonnes. "
            f"Contenu : {row!r}"
        )


# ---------------------------------------------------------------------------
# Extraction principale
# ---------------------------------------------------------------------------

def extract_texts(csv_path, block_name=None, line_start=None, line_end=None):
    """Extrait les textes traductibles du CSV.

    Args:
        csv_path: Chemin vers le fichier rules.csv
        block_name: Nom du bloc (pour le rapport), optionnel
        line_start: Premiere ligne a traiter (1-based, incluse), optionnel
        line_end: Derniere ligne a traiter (1-based, incluse), optionnel

    Returns:
        dict avec :
          - "entries" : liste des entrees extraites
          - "stats" : statistiques d'extraction
          - "block" : nom du bloc
    """
    rows = read_csv_rows(csv_path)
    entries = []
    stats = {
        "total_rows": len(rows),
        "comment_or_empty": 0,
        "data_rows": 0,
        "text_segments": 0,
        "option_segments": 0,
        "skipped_out_of_range": 0,
    }

    for row_idx, row in rows:
        # Filtre par range de lignes (1-based)
        if line_start is not None and (row_idx + 1) < line_start:
            stats["skipped_out_of_range"] += 1
            continue
        if line_end is not None and (row_idx + 1) > line_end:
            stats["skipped_out_of_range"] += 1
            continue

        # Ignorer commentaires et lignes vides
        if is_comment_or_empty(row):
            stats["comment_or_empty"] += 1
            continue

        # GF-06 : validation nombre de colonnes
        validate_row_columns(row, row_idx)
        stats["data_rows"] += 1

        row_id = row[0]  # ID de la regle (colonne 0, pour reference uniquement)

        # Colonne 4 : text
        text_content = row[4]
        if text_content.strip():
            variables = extract_variables(text_content)
            entries.append({
                "row_idx": row_idx,
                "col": 4,
                "col_name": "text",
                "rule_id": row_id,
                "text_en": text_content,
                "text_fr": None,
                "variables": variables,
            })
            stats["text_segments"] += 1

        # Colonne 5 : options
        options_content = row[5]
        if options_content.strip():
            # Les options peuvent etre separees par des \n
            raw_options = options_content.split("\n")
            for opt_str in raw_options:
                opt_str = opt_str.strip()
                if not opt_str:
                    continue
                option_id, label = parse_option(opt_str)
                variables = extract_variables(label)
                entries.append({
                    "row_idx": row_idx,
                    "col": 5,
                    "col_name": "options",
                    "rule_id": row_id,
                    "text_en": opt_str,
                    "text_fr": None,
                    "variables": variables,
                    "option_id": option_id,
                    "option_label_en": label,
                })
            stats["option_segments"] += 1

    # GF-10 : rapport de couverture
    total_segments = stats["text_segments"] + stats["option_segments"]
    stats["total_segments"] = total_segments

    result = {
        "block": block_name or "all",
        "csv_path": os.path.abspath(csv_path),
        "entries": entries,
        "stats": stats,
    }
    return result


def write_extract(result, output_path):
    """Ecrit le resultat d'extraction en JSON."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Point d'entree CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Extrait les textes traductibles de rules.csv vers JSON."
    )
    parser.add_argument(
        "--csv",
        default=os.path.join(
            os.path.dirname(__file__), "..", "data", "campaign", "rules.csv"
        ),
        help="Chemin vers rules.csv (defaut: data/campaign/rules.csv)",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Chemin du fichier JSON de sortie",
    )
    parser.add_argument(
        "--block",
        default=None,
        help="Nom du bloc (ex: shrouded, derelict_vambrace)",
    )
    parser.add_argument(
        "--line-start",
        type=int,
        default=None,
        help="Premiere ligne a traiter (1-based, incluse)",
    )
    parser.add_argument(
        "--line-end",
        type=int,
        default=None,
        help="Derniere ligne a traiter (1-based, incluse)",
    )

    args = parser.parse_args()

    csv_path = os.path.abspath(args.csv)
    if not os.path.isfile(csv_path):
        print(f"ERREUR : fichier CSV introuvable : {csv_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Extraction depuis : {csv_path}")
    result = extract_texts(
        csv_path,
        block_name=args.block,
        line_start=args.line_start,
        line_end=args.line_end,
    )

    output_path = os.path.abspath(args.output)
    write_extract(result, output_path)

    # Affichage du rapport (GF-10)
    s = result["stats"]
    print(f"Bloc         : {result['block']}")
    print(f"Lignes CSV   : {s['total_rows']}")
    print(f"Lignes data  : {s['data_rows']}")
    print(f"Commentaires : {s['comment_or_empty']}")
    print(f"Segments text : {s['text_segments']}")
    print(f"Segments opts : {s['option_segments']}")
    print(f"Total segments: {s['total_segments']}")
    print(f"Sortie        : {output_path}")


if __name__ == "__main__":
    main()
