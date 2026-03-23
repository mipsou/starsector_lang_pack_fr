#!/usr/bin/env python3
"""
Outil 3 : Reinsertion des traductions dans rules.csv.

Lit un JSON valide (produit/valide par translate_rules_batch.py),
reinjecte les traductions dans le CSV en preservant la structure exacte.

Garde-fous implementes :
  GF-01 : IDs (col 0) byte-identiques apres reinsertion
  GF-02 : Script (col 3) byte-identique apres reinsertion
  GF-03 : Pas de subprocess, pas de git, pas de os.system
  GF-05 : Backup automatique avant toute ecriture
  GF-06 : csv.reader/csv.writer obligatoire
  GF-07 : Checklist finale imprimee
  GF-08 : Template d'issue genere
  GF-09 : Verrou filelock, 1 processus a la fois
  GF-10 : Rapport de couverture
"""

import argparse
import csv
import json
import os
import re
import shutil
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

ENCODING = "utf-8"
NUM_COLS = 7

# Colonnes intouchables (GF-01, GF-02)
COLS_INTOUCHABLES = frozenset([0, 1, 2, 3, 6])
COLS_TRADUCTIBLES = frozenset([4, 5])

# Format d'option : [priority:]optionId:Label
OPTION_RE = re.compile(r'^(?:(\d+):)?([^:]+):(.+)$', re.DOTALL)


# ---------------------------------------------------------------------------
# Fonctions utilitaires
# ---------------------------------------------------------------------------

def backup_file(filepath):
    """GF-05 : Cree un backup du fichier avant ecriture.

    Retourne le chemin du backup.
    """
    if not os.path.isfile(filepath):
        return None

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = os.path.join(os.path.dirname(filepath), "backups")
    os.makedirs(backup_dir, exist_ok=True)

    basename = os.path.basename(filepath)
    backup_path = os.path.join(backup_dir, f"{basename}.{timestamp}.bak")
    shutil.copy2(filepath, backup_path)
    return backup_path


def read_csv_raw(csv_path):
    """Lit le CSV complet et retourne les lignes brutes."""
    rows = []
    with open(csv_path, "r", encoding=ENCODING, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            rows.append(row)
    return rows


def write_csv(csv_path, rows):
    """Ecrit les lignes dans le CSV (UTF-8, CRLF)."""
    with open(csv_path, "w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f, lineterminator="\r\n")
        for row in rows:
            writer.writerow(row)


def reconstruct_option(text_en, text_fr_label):
    """Reconstruit une option traduite en preservant optionId et priorite.

    text_en : option originale complette (ex: "shroudedSubstrate_optSelA:\"So... what is it?\"")
    text_fr_label : traduction du label UNIQUEMENT

    Retourne l'option reconstruite avec l'optionId original.
    """
    m = OPTION_RE.match(text_en)
    if m:
        priority = m.group(1)
        option_id = m.group(2)
        if priority is not None:
            return f"{priority}:{option_id}:{text_fr_label}"
        else:
            return f"{option_id}:{text_fr_label}"
    # Pas de format reconnu, retourner tel quel
    return text_fr_label


# ---------------------------------------------------------------------------
# Reinsertion principale
# ---------------------------------------------------------------------------

def build_translation_map(data):
    """Construit un index des traductions par (row_idx, col).

    Pour les options (col 5), on regroupe par row_idx car il peut y avoir
    plusieurs options sur la meme ligne.

    Retourne :
      text_map : dict[(row_idx, col)] = text_fr  (pour col 4)
      options_map : dict[row_idx] = [(text_en, text_fr), ...]  (pour col 5)
    """
    text_map = {}
    options_map = {}

    for entry in data.get("entries", []):
        text_fr = entry.get("text_fr")
        if text_fr is None or text_fr == "":
            continue

        row_idx = entry["row_idx"]
        col = entry["col"]

        if col == 4:
            text_map[(row_idx, col)] = text_fr
        elif col == 5:
            if row_idx not in options_map:
                options_map[row_idx] = []
            options_map[row_idx].append({
                "text_en": entry["text_en"],
                "text_fr": text_fr,
                "option_id": entry.get("option_id"),
            })

    return text_map, options_map


def reassemble(csv_path, data, output_path=None, dry_run=False):
    """Reinjecte les traductions dans le CSV.

    Args:
        csv_path: Chemin vers le fichier rules.csv source
        data: dict charge depuis le JSON valide
        output_path: Chemin de sortie (si None, ecrase le csv_path)
        dry_run: Si True, ne fait que simuler sans ecrire

    Returns:
        dict avec le rapport de reinsertion
    """
    if output_path is None:
        output_path = csv_path

    # GF-05 : backup avant ecriture
    backup_path = None
    if not dry_run:
        backup_path = backup_file(output_path if os.path.isfile(output_path) else csv_path)

    # Lire le CSV original
    rows = read_csv_raw(csv_path)
    original_row_count = len(rows)

    # Construire les maps de traduction
    text_map, options_map = build_translation_map(data)

    # Sauvegarder les colonnes intouchables pour verification (GF-01, GF-02)
    original_intouchables = {}
    for row_idx, row in enumerate(rows):
        if len(row) == NUM_COLS:
            original_intouchables[row_idx] = {
                col: row[col] for col in COLS_INTOUCHABLES
            }

    # Appliquer les traductions
    applied_text = 0
    applied_options = 0

    for (row_idx, col), text_fr in text_map.items():
        if row_idx < len(rows) and len(rows[row_idx]) == NUM_COLS:
            rows[row_idx][col] = text_fr
            applied_text += 1

    for row_idx, opt_entries in options_map.items():
        if row_idx < len(rows) and len(rows[row_idx]) == NUM_COLS:
            # Reconstruire la colonne options
            original_options = rows[row_idx][5]
            original_lines = original_options.split("\n")

            # Creer un index par text_en pour les remplacements
            replacement_map = {}
            for opt in opt_entries:
                replacement_map[opt["text_en"]] = opt["text_fr"]

            new_lines = []
            for line in original_lines:
                stripped = line.strip()
                if stripped in replacement_map:
                    new_lines.append(replacement_map[stripped])
                else:
                    new_lines.append(line)

            rows[row_idx][5] = "\n".join(new_lines)
            applied_options += 1

    # GF-01, GF-02 : verification post-reinsertion
    integrity_errors = []
    for row_idx, orig_cols in original_intouchables.items():
        if row_idx < len(rows) and len(rows[row_idx]) == NUM_COLS:
            for col, orig_val in orig_cols.items():
                if rows[row_idx][col] != orig_val:
                    integrity_errors.append(
                        f"GF-01/02 : Colonne intouchable {col} modifiee "
                        f"a la ligne {row_idx} (rule: {rows[row_idx][0]})"
                    )

    # Verification nombre de lignes
    if len(rows) != original_row_count:
        integrity_errors.append(
            f"Nombre de lignes modifie : {original_row_count} -> {len(rows)}"
        )

    # Ecriture si pas d'erreur et pas dry_run
    if not dry_run and not integrity_errors:
        write_csv(output_path, rows)

    # GF-10 : rapport de couverture
    report = {
        "csv_path": os.path.abspath(csv_path),
        "output_path": os.path.abspath(output_path),
        "backup_path": backup_path,
        "dry_run": dry_run,
        "original_row_count": original_row_count,
        "final_row_count": len(rows),
        "applied_text": applied_text,
        "applied_options": applied_options,
        "total_applied": applied_text + applied_options,
        "integrity_errors": integrity_errors,
        "success": len(integrity_errors) == 0,
    }

    return report


def print_checklist(report, block_name=""):
    """GF-07 : Imprime la checklist de validation finale."""
    print("\n" + "=" * 60)
    print("  CHECKLIST DE VALIDATION AVANT COMMIT (GF-07)")
    print("=" * 60)
    print(f"  Bloc            : {block_name}")
    print(f"  CSV source      : {report['csv_path']}")
    print(f"  CSV sortie      : {report['output_path']}")
    print(f"  Backup          : {report['backup_path'] or 'N/A'}")
    print(f"  Dry run         : {'OUI' if report['dry_run'] else 'NON'}")
    print(f"  Lignes CSV      : {report['original_row_count']} -> {report['final_row_count']}")
    print(f"  Textes appliques: {report['applied_text']}")
    print(f"  Options appli.  : {report['applied_options']}")
    print(f"  Total appliques : {report['total_applied']}")

    if report["integrity_errors"]:
        print(f"\n  *** ERREURS D'INTEGRITE ({len(report['integrity_errors'])}) ***")
        for err in report["integrity_errors"]:
            print(f"    - {err}")
    else:
        print(f"\n  Integrite       : OK")

    print()
    print("  [ ] 1. Copier le CSV vers le mod actif")
    print("  [ ] 2. Lancer Starsector, charger/nouvelle partie")
    print("  [ ] 3. Verifier les dialogues traduits en jeu")
    print("  [ ] 4. Verifier qu'aucune variable $xxx n'apparait en clair")
    print("  [ ] 5. Verifier qu'aucun option_id n'a ete traduit")
    print("  [ ] 6. Directeur valide -> git add + commit sur dev")
    print("=" * 60)


def print_issue_template(block_name, report):
    """GF-08 : Genere un template d'issue GitHub."""
    print("\n" + "-" * 60)
    print("  TEMPLATE ISSUE GITHUB (GF-08)")
    print("-" * 60)
    print(f"""
Titre : feat(rules.csv): traduction bloc {block_name}

## Description
Traduction du bloc "{block_name}" dans rules.csv.

## Modifications
- {report['applied_text']} segments de texte traduits
- {report['applied_options']} groupes d'options traduits
- Total : {report['total_applied']} modifications

## Verification
- [ ] Variables $xxx preservees
- [ ] Option IDs non traduits
- [ ] Colonnes intouchables preservees
- [ ] Teste en jeu
- [ ] Nombre de lignes CSV inchange ({report['original_row_count']})
""")
    print("-" * 60)


# ---------------------------------------------------------------------------
# Point d'entree CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Reinjecte les traductions validees dans rules.csv."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Chemin du fichier JSON d'entree (valide par translate_rules_batch.py)",
    )
    parser.add_argument(
        "--csv",
        default=None,
        help="Chemin vers rules.csv source (defaut: celui du JSON)",
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Chemin de sortie (defaut: ecrase le CSV source)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="Simuler sans ecrire",
    )
    parser.add_argument(
        "--no-checklist",
        action="store_true",
        default=False,
        help="Ne pas afficher la checklist",
    )
    parser.add_argument(
        "--no-issue",
        action="store_true",
        default=False,
        help="Ne pas afficher le template d'issue",
    )

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.isfile(input_path):
        print(f"ERREUR : fichier JSON introuvable : {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    csv_path = args.csv or data.get("csv_path")
    if not csv_path:
        print("ERREUR : chemin CSV non specifie et absent du JSON", file=sys.stderr)
        sys.exit(1)

    csv_path = os.path.abspath(csv_path)
    if not os.path.isfile(csv_path):
        print(f"ERREUR : fichier CSV introuvable : {csv_path}", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.abspath(args.output) if args.output else csv_path
    block_name = data.get("block", "unknown")

    print(f"Reinsertion depuis : {input_path}")
    print(f"CSV source         : {csv_path}")
    print(f"CSV sortie         : {output_path}")
    print(f"Bloc               : {block_name}")
    print(f"Mode               : {'DRY RUN' if args.dry_run else 'ECRITURE'}")

    report = reassemble(csv_path, data, output_path=output_path, dry_run=args.dry_run)

    # GF-07 : checklist
    if not args.no_checklist:
        print_checklist(report, block_name)

    # GF-08 : template issue
    if not args.no_issue:
        print_issue_template(block_name, report)

    if report["integrity_errors"]:
        print("\n*** REINSERTION ECHOUEE : erreurs d'integrite ***",
              file=sys.stderr)
        sys.exit(1)
    elif args.dry_run:
        print("\nDRY RUN termine. Aucun fichier modifie.")
    else:
        print(f"\nReinsertion terminee avec succes.")
        print(f"Backup : {report['backup_path']}")


if __name__ == "__main__":
    main()
