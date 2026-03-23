#!/usr/bin/env python3
"""
Outil 2 : Validation des traductions dans le JSON extrait.

Lit un JSON produit par extract_rules_text.py, valide les traductions
renseignees (text_fr), et produit un rapport.

Garde-fous implementes :
  GF-02  : Variables $xxx preservees, pas d'accents dans les variables
  GF-02c : Detection d'accents dans les noms de variables
  GF-03  : Pas de subprocess, pas de git, pas de os.system
  GF-04  : Detection de traduction mot-a-mot (ratio mots identiques > 50%)
  GF-10  : Rapport de couverture obligatoire
"""

import argparse
import json
import os
import re
import sys

# ---------------------------------------------------------------------------
# Constantes
# ---------------------------------------------------------------------------

# Regex pour detecter les variables $xxx
VARIABLE_RE = re.compile(r'\$[A-Za-z_\u00C0-\u00FF][A-Za-z0-9_.\u00C0-\u00FF]*')

# Regex pour detecter des caracteres accentues dans un nom de variable
ACCENT_RE = re.compile(r'[\u00C0-\u00FF]')

# Seuil de detection mot-a-mot (GF-04)
# Si plus de 50% des mots du texte FR sont identiques au texte EN,
# c'est probablement du mot-a-mot.
WORD_IDENTICAL_THRESHOLD = 0.50

# Apostrophe autorisee : uniquement U+0027 (')
# Interdite : U+2019 (apostrophe typographique)
CURLY_APOSTROPHE = "\u2019"

# Format d'option : [priority:]optionId:Label
OPTION_RE = re.compile(r'^(?:(\d+):)?([^:]+):(.+)$', re.DOTALL)


# ---------------------------------------------------------------------------
# Fonctions de validation
# ---------------------------------------------------------------------------

def extract_variables(text):
    """Extrait les variables $xxx d'un texte."""
    if not text:
        return set()
    return set(VARIABLE_RE.findall(text))


def check_variables_preserved(text_en, text_fr):
    """GF-02 : Verifie que toutes les variables EN sont presentes dans FR.

    Retourne une liste d'erreurs (vide si tout va bien).
    """
    errors = []
    vars_en = extract_variables(text_en)
    vars_fr = extract_variables(text_fr)

    missing = vars_en - vars_fr
    if missing:
        errors.append(
            f"GF-02 : Variables manquantes dans la traduction : {sorted(missing)}"
        )

    added = vars_fr - vars_en
    if added:
        errors.append(
            f"GF-02 : Variables ajoutees dans la traduction : {sorted(added)}"
        )

    return errors


def check_no_accents_in_variables(text_fr):
    """GF-02c : Verifie qu'il n'y a pas d'accents dans les variables.

    Retourne une liste d'erreurs.
    """
    errors = []
    if not text_fr:
        return errors

    for var in VARIABLE_RE.findall(text_fr):
        if ACCENT_RE.search(var):
            errors.append(
                f"GF-02c : Accent detecte dans la variable '{var}'"
            )
    return errors


def check_not_word_for_word(text_en, text_fr):
    """GF-04 : Detection de traduction mot-a-mot.

    Si plus de WORD_IDENTICAL_THRESHOLD des mots sont identiques,
    retourne un avertissement.
    """
    warnings = []
    if not text_en or not text_fr:
        return warnings

    # Normaliser : minuscules, split sur espaces
    words_en = set(text_en.lower().split())
    words_fr = set(text_fr.lower().split())

    if not words_fr:
        return warnings

    # Mots communs (hors variables et mots de moins de 3 lettres)
    common = words_en & words_fr
    # Exclure les variables et mots courts
    common = {w for w in common if not w.startswith("$") and len(w) > 2}
    significant_fr = {w for w in words_fr if not w.startswith("$") and len(w) > 2}

    if not significant_fr:
        return warnings

    ratio = len(common) / len(significant_fr)
    if ratio > WORD_IDENTICAL_THRESHOLD:
        warnings.append(
            f"GF-04 : Possible traduction mot-a-mot "
            f"({len(common)}/{len(significant_fr)} mots identiques, "
            f"ratio={ratio:.0%}). Mots communs : {sorted(list(common)[:10])}"
        )
    return warnings


def check_curly_apostrophes(text_fr):
    """Verifie l'absence d'apostrophes typographiques U+2019."""
    errors = []
    if text_fr and CURLY_APOSTROPHE in text_fr:
        errors.append(
            "Apostrophe typographique U+2019 detectee. "
            "Utiliser uniquement U+0027 (')."
        )
    return errors


def check_option_id_preserved(text_en, text_fr):
    """Verifie que l'option_id n'a pas ete traduit.

    Dans les options, seul le label apres le dernier ':' doit etre traduit.
    L'option_id doit rester identique.
    """
    errors = []
    m_en = OPTION_RE.match(text_en)
    m_fr = OPTION_RE.match(text_fr)

    if m_en and m_fr:
        # Verifier que la priorite est identique
        if m_en.group(1) != m_fr.group(1):
            errors.append(
                f"Option : priorite modifiee "
                f"(EN='{m_en.group(1)}', FR='{m_fr.group(1)}')"
            )
        # Verifier que l'option_id est identique
        if m_en.group(2) != m_fr.group(2):
            errors.append(
                f"Option : option_id modifie "
                f"(EN='{m_en.group(2)}', FR='{m_fr.group(2)}'). "
                f"Seul le label doit etre traduit."
            )
    elif m_en and not m_fr:
        errors.append(
            "Option : format option_id:label perdu dans la traduction."
        )
    return errors


# ---------------------------------------------------------------------------
# Validation d'une entree
# ---------------------------------------------------------------------------

def validate_entry(entry):
    """Valide une entree traduite.

    Retourne un dict avec les cles "errors" et "warnings".
    """
    errors = []
    warnings = []

    text_en = entry.get("text_en", "")
    text_fr = entry.get("text_fr")

    # Pas de traduction : rien a valider
    if text_fr is None or text_fr == "":
        return {"errors": [], "warnings": [], "translated": False}

    # GF-02 : variables preservees
    if entry.get("col") == 5 and entry.get("option_id"):
        # Pour les options, verifier sur le label seulement
        label_en = entry.get("option_label_en", "")
        m_fr = OPTION_RE.match(text_fr)
        label_fr = m_fr.group(3) if m_fr else text_fr
        errors.extend(check_variables_preserved(label_en, label_fr))
    else:
        errors.extend(check_variables_preserved(text_en, text_fr))

    # GF-02c : pas d'accents dans les variables
    errors.extend(check_no_accents_in_variables(text_fr))

    # Apostrophes typographiques
    errors.extend(check_curly_apostrophes(text_fr))

    # Options : verifier que l'option_id est preserve
    if entry.get("col") == 5:
        errors.extend(check_option_id_preserved(text_en, text_fr))

    # GF-04 : detection mot-a-mot
    if entry.get("col") == 4:
        # Seulement pour les textes, pas les options (labels trop courts)
        warnings.extend(check_not_word_for_word(text_en, text_fr))

    return {"errors": errors, "warnings": warnings, "translated": True}


# ---------------------------------------------------------------------------
# Validation du batch complet
# ---------------------------------------------------------------------------

def validate_batch(data):
    """Valide un batch complet de traductions.

    Args:
        data: dict charge depuis le JSON (produit par extract_rules_text.py)

    Returns:
        dict avec :
          - "valid" : True si aucune erreur
          - "entries_report" : liste de rapports par entree
          - "summary" : resume global
    """
    entries = data.get("entries", [])
    entries_report = []
    total_errors = 0
    total_warnings = 0
    translated_count = 0
    untranslated_count = 0

    for i, entry in enumerate(entries):
        result = validate_entry(entry)
        if result["translated"]:
            translated_count += 1
        else:
            untranslated_count += 1

        if result["errors"] or result["warnings"]:
            report = {
                "index": i,
                "row_idx": entry.get("row_idx"),
                "col": entry.get("col"),
                "rule_id": entry.get("rule_id"),
                "errors": result["errors"],
                "warnings": result["warnings"],
            }
            entries_report.append(report)
            total_errors += len(result["errors"])
            total_warnings += len(result["warnings"])

    total = len(entries)
    # GF-10 : rapport de couverture
    coverage = (translated_count / total * 100) if total > 0 else 0.0

    summary = {
        "total_entries": total,
        "translated": translated_count,
        "untranslated": untranslated_count,
        "coverage_pct": round(coverage, 1),
        "total_errors": total_errors,
        "total_warnings": total_warnings,
    }

    return {
        "valid": total_errors == 0,
        "entries_report": entries_report,
        "summary": summary,
    }


# ---------------------------------------------------------------------------
# Point d'entree CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Valide les traductions dans un JSON extrait de rules.csv."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Chemin du fichier JSON d'entree (produit par extract_rules_text.py)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        default=True,
        help="Lancer la validation (defaut: True)",
    )
    parser.add_argument(
        "--report", "-r",
        default=None,
        help="Chemin du rapport JSON de sortie (optionnel)",
    )

    args = parser.parse_args()

    input_path = os.path.abspath(args.input)
    if not os.path.isfile(input_path):
        print(f"ERREUR : fichier JSON introuvable : {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Validation de : {input_path}")
    print(f"Bloc : {data.get('block', '?')}")

    result = validate_batch(data)
    s = result["summary"]

    # Affichage du rapport (GF-10)
    print(f"\n=== RAPPORT DE VALIDATION ===")
    print(f"Entries totales : {s['total_entries']}")
    print(f"Traduites       : {s['translated']}")
    print(f"Non traduites   : {s['untranslated']}")
    print(f"Couverture      : {s['coverage_pct']}%")
    print(f"Erreurs         : {s['total_errors']}")
    print(f"Avertissements  : {s['total_warnings']}")
    print(f"Valide          : {'OUI' if result['valid'] else 'NON'}")

    if result["entries_report"]:
        print(f"\n--- Details ---")
        for report in result["entries_report"]:
            print(f"\nLigne {report['row_idx']}, col {report['col']} "
                  f"(rule: {report['rule_id']}):")
            for err in report["errors"]:
                print(f"  ERREUR : {err}")
            for warn in report["warnings"]:
                print(f"  AVERT  : {warn}")

    # Ecriture du rapport JSON si demande
    if args.report:
        report_path = os.path.abspath(args.report)
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\nRapport ecrit : {report_path}")

    # Code de sortie : 0 si valide, 1 si erreurs
    if not result["valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
