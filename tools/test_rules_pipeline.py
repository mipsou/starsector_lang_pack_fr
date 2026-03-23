#!/usr/bin/env python3
"""
Tests du pipeline rules.csv : extract -> validate -> reassemble.

Couvre les 10 garde-fous GF-01 a GF-10, les regles du glossaire,
et le pipeline complet bout-en-bout.
"""

import csv
import json
import os
import shutil
import tempfile
import unittest

# ---------------------------------------------------------------------------
# Import des modules du pipeline (interfaces reelles)
# ---------------------------------------------------------------------------

sys_path = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, sys_path)

from extract_rules_text import (
    extract_texts,
    extract_variables,
    is_comment_or_empty,
    parse_option,
    read_csv_rows,
    validate_row_columns,
    write_extract,
    ENCODING,
    NUM_COLS,
    COLS_INTOUCHABLES,
    COLS_TRADUCTIBLES,
)
from translate_rules_batch import (
    check_curly_apostrophes,
    check_no_accents_in_variables,
    check_not_word_for_word,
    check_option_id_preserved,
    check_variables_preserved,
    validate_batch,
    validate_entry,
    WORD_IDENTICAL_THRESHOLD,
)
from reassemble_rules import (
    backup_file,
    build_translation_map,
    read_csv_raw,
    reassemble,
    reconstruct_option,
    write_csv,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_csv(rows, path):
    """Ecrit un CSV UTF-8 avec 7 colonnes."""
    with open(path, "w", encoding=ENCODING, newline="") as f:
        writer = csv.writer(f, lineterminator="\r\n")
        for row in rows:
            writer.writerow(row)


def make_json(data, path):
    """Ecrit un fichier JSON UTF-8."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def row7(id_="r1", trigger="", cond="", script="", text="", opts="", notes=""):
    """Construit une ligne CSV a 7 colonnes."""
    return [id_, trigger, cond, script, text, opts, notes]


# ---------------------------------------------------------------------------
# Fixtures CSV
# ---------------------------------------------------------------------------

HEADER = ["id", "trigger", "conditions", "script", "text", "options", "notes"]

SIMPLE_ROWS = [
    HEADER,
    row7("rule1", "DialogOptionSelected", "SomeCondition",
         'FireBest "doStuff"', "Hello $playerName, welcome aboard.",
         "opt1:Continue\nopt2:Leave", "dev note"),
    row7("rule2", "PopulateOptions", "", "",
         "Your $playerFleetOrShip is ready.", "", ""),
]

# Ligne avec variables et option complexe
COMPLEX_ROWS = [
    HEADER,
    row7("shrouded1", "Dialog", "HasTag shrouded",
         'FireAll "checkSubstrate"',
         "The $faction representative says $playerSirOrMadam, the substrate is volatile.",
         "1:shrouded_optA:\"So... what is it?\"\n2:shrouded_optB:\"Is it valuable?\"",
         "shrouded block"),
]


# ===========================================================================
# TESTS
# ===========================================================================


class TestExtractVariables(unittest.TestCase):
    """Tests extract_variables (utilitaire)."""

    def test_basic(self):
        result = extract_variables("Hello $playerName, your $fleet awaits.")
        self.assertIn("$playerName", result)
        self.assertIn("$fleet", result)

    def test_empty(self):
        self.assertEqual(extract_variables(""), [])
        self.assertEqual(extract_variables(None), [])

    def test_no_variables(self):
        self.assertEqual(extract_variables("No variables here."), [])

    def test_dotted_variable(self):
        result = extract_variables("Check $player.canMakeDwellerWeapons flag.")
        self.assertIn("$player.canMakeDwellerWeapons", result)


class TestParseOption(unittest.TestCase):
    """Tests parse_option."""

    def test_simple_option(self):
        opt_id, label = parse_option("opt1:Continue")
        self.assertEqual(opt_id, "opt1")
        self.assertEqual(label, "Continue")

    def test_priority_option(self):
        opt_id, label = parse_option("1:shrouded_optA:\"So... what is it?\"")
        self.assertEqual(opt_id, "shrouded_optA")
        self.assertEqual(label, "\"So... what is it?\"")

    def test_empty_option(self):
        opt_id, label = parse_option("")
        self.assertIsNone(opt_id)

    def test_no_colon(self):
        opt_id, label = parse_option("justtext")
        self.assertIsNone(opt_id)
        self.assertEqual(label, "justtext")


class TestIsCommentOrEmpty(unittest.TestCase):

    def test_comment(self):
        self.assertTrue(is_comment_or_empty(["# this is a comment"]))

    def test_empty_row(self):
        self.assertTrue(is_comment_or_empty([]))
        self.assertTrue(is_comment_or_empty(["", "", ""]))

    def test_data_row(self):
        self.assertFalse(is_comment_or_empty(["rule1", "trigger", "", "", "text", "", ""]))


class TestValidateRowColumns(unittest.TestCase):

    def test_valid_7_cols(self):
        validate_row_columns(["a"] * 7, 0)  # ne doit pas lever

    def test_invalid_col_count(self):
        with self.assertRaises(ValueError) as ctx:
            validate_row_columns(["a"] * 5, 42)
        self.assertIn("GF-06", str(ctx.exception))


# ---------------------------------------------------------------------------
# GF-01 : Colonnes intouchables JAMAIS extraites
# ---------------------------------------------------------------------------

class TestGF01_ColonnesIntouchables(unittest.TestCase):
    """GF-01 : Les colonnes 0,1,2,3,6 ne doivent JAMAIS etre extraites."""

    def test_only_col4_col5_extracted(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                         encoding=ENCODING, newline="",
                                         delete=False) as f:
            writer = csv.writer(f, lineterminator="\r\n")
            for row in SIMPLE_ROWS:
                writer.writerow(row)
            csv_path = f.name

        try:
            result = extract_texts(csv_path)
            for entry in result["entries"]:
                self.assertIn(entry["col"], COLS_TRADUCTIBLES,
                              f"Colonne {entry['col']} extraite, interdit par GF-01")
                self.assertNotIn(entry["col"], COLS_INTOUCHABLES)
        finally:
            os.unlink(csv_path)

    def test_reassemble_preserves_intouchables(self):
        """GF-01 : Apres reinsertion, colonnes 0,1,2,3,6 byte-identiques."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "rules.csv")
            out_path = os.path.join(tmpdir, "rules_out.csv")
            make_csv(SIMPLE_ROWS, csv_path)

            data = {
                "entries": [{
                    "row_idx": 1, "col": 4,
                    "text_en": "Hello $playerName, welcome aboard.",
                    "text_fr": "Bonjour $playerName, bienvenue a bord.",
                }],
            }
            report = reassemble(csv_path, data, output_path=out_path)
            self.assertTrue(report["success"])
            self.assertEqual(report["integrity_errors"], [])

            original = read_csv_raw(csv_path)
            modified = read_csv_raw(out_path)
            for col in COLS_INTOUCHABLES:
                self.assertEqual(original[1][col], modified[1][col],
                                 f"Colonne intouchable {col} modifiee")


# ---------------------------------------------------------------------------
# GF-02 : Variables $xxx preservees
# ---------------------------------------------------------------------------

class TestGF02_VariablesPreservees(unittest.TestCase):

    def test_variables_ok(self):
        errs = check_variables_preserved(
            "Hello $playerName and $faction.",
            "Bonjour $playerName et $faction.",
        )
        self.assertEqual(errs, [])

    def test_variable_missing(self):
        errs = check_variables_preserved(
            "Hello $playerName and $faction.",
            "Bonjour et faction.",
        )
        self.assertTrue(any("GF-02" in e for e in errs))

    def test_variable_added(self):
        errs = check_variables_preserved(
            "Hello $playerName.",
            "Bonjour $playerName et $extra.",
        )
        self.assertTrue(any("GF-02" in e for e in errs))


# ---------------------------------------------------------------------------
# GF-02c : Pas d'accents dans les variables
# ---------------------------------------------------------------------------

class TestGF02c_PasAccentsDansVariables(unittest.TestCase):

    def test_clean_variable(self):
        errs = check_no_accents_in_variables("Le $playerName arrive.")
        self.assertEqual(errs, [])

    def test_accented_variable(self):
        errs = check_no_accents_in_variables("Le $joueurNom\u00e9 arrive.")
        self.assertTrue(any("GF-02c" in e for e in errs))


# ---------------------------------------------------------------------------
# GF-03 : Pas de subprocess, pas de git
# ---------------------------------------------------------------------------

class TestGF03_PasDeSubprocess(unittest.TestCase):
    """GF-03 : Verification statique — aucun import subprocess/os.system."""

    def _check_no_subprocess(self, filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            source = f.read()
        self.assertNotIn("import subprocess", source,
                         f"subprocess detecte dans {filepath}")
        self.assertNotIn("os.system(", source,
                         f"os.system detecte dans {filepath}")
        self.assertNotIn("os.popen(", source,
                         f"os.popen detecte dans {filepath}")

    def test_extract_no_subprocess(self):
        self._check_no_subprocess(os.path.join(sys_path, "extract_rules_text.py"))

    def test_translate_no_subprocess(self):
        self._check_no_subprocess(os.path.join(sys_path, "translate_rules_batch.py"))

    def test_reassemble_no_subprocess(self):
        self._check_no_subprocess(os.path.join(sys_path, "reassemble_rules.py"))


# ---------------------------------------------------------------------------
# GF-04 : Detection traduction mot-a-mot
# ---------------------------------------------------------------------------

class TestGF04_MotAMot(unittest.TestCase):

    def test_mot_a_mot_detecte(self):
        warns = check_not_word_for_word(
            "The ship is ready for combat deployment now.",
            "The ship is ready for combat deployment now.",  # copie brute
        )
        self.assertTrue(any("GF-04" in w for w in warns))

    def test_traduction_naturelle(self):
        warns = check_not_word_for_word(
            "The ship is ready for combat deployment.",
            "Le vaisseau est pret pour le deploiement au combat.",
        )
        self.assertEqual(warns, [])


# ---------------------------------------------------------------------------
# GF-05 : Backup avant ecriture
# ---------------------------------------------------------------------------

class TestGF05_Backup(unittest.TestCase):

    def test_backup_cree(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "rules.csv")
            make_csv(SIMPLE_ROWS, csv_path)

            backup_path = backup_file(csv_path)
            self.assertIsNotNone(backup_path)
            self.assertTrue(os.path.isfile(backup_path))
            self.assertIn("backups", backup_path)

    def test_backup_contenu_identique(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "rules.csv")
            make_csv(SIMPLE_ROWS, csv_path)

            with open(csv_path, "rb") as f:
                original_bytes = f.read()

            backup_path = backup_file(csv_path)
            with open(backup_path, "rb") as f:
                backup_bytes = f.read()

            self.assertEqual(original_bytes, backup_bytes)


# ---------------------------------------------------------------------------
# GF-06 : csv.reader obligatoire, 7 colonnes
# ---------------------------------------------------------------------------

class TestGF06_CsvReader7Colonnes(unittest.TestCase):

    def test_lecture_csv_reader(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                         encoding=ENCODING, newline="",
                                         delete=False) as f:
            writer = csv.writer(f, lineterminator="\r\n")
            for row in SIMPLE_ROWS:
                writer.writerow(row)
            csv_path = f.name

        try:
            rows = read_csv_rows(csv_path)
            # Toutes les lignes data doivent avoir 7 colonnes
            for row_idx, row in rows:
                if not is_comment_or_empty(row):
                    self.assertEqual(len(row), NUM_COLS,
                                     f"Ligne {row_idx} n'a pas {NUM_COLS} colonnes")
        finally:
            os.unlink(csv_path)

    def test_csv_mauvais_nombre_colonnes(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                         encoding=ENCODING, newline="",
                                         delete=False) as f:
            writer = csv.writer(f, lineterminator="\r\n")
            writer.writerow(HEADER)
            writer.writerow(["a", "b", "c"])  # 3 colonnes seulement
            csv_path = f.name

        try:
            with self.assertRaises(ValueError) as ctx:
                extract_texts(csv_path)
            self.assertIn("GF-06", str(ctx.exception))
        finally:
            os.unlink(csv_path)


# ---------------------------------------------------------------------------
# GF-07 : Checklist finale (existence de la fonction)
# ---------------------------------------------------------------------------

class TestGF07_Checklist(unittest.TestCase):

    def test_print_checklist_callable(self):
        from reassemble_rules import print_checklist
        report = {
            "csv_path": "/tmp/test.csv",
            "output_path": "/tmp/test_out.csv",
            "backup_path": "/tmp/backup.bak",
            "dry_run": False,
            "original_row_count": 100,
            "final_row_count": 100,
            "applied_text": 5,
            "applied_options": 3,
            "total_applied": 8,
            "integrity_errors": [],
        }
        # Ne doit pas lever d'exception
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_checklist(report, "test_bloc")
        output = buf.getvalue()
        self.assertIn("CHECKLIST", output)
        self.assertIn("GF-07", output)


# ---------------------------------------------------------------------------
# GF-08 : Template issue (existence de la fonction)
# ---------------------------------------------------------------------------

class TestGF08_TemplateIssue(unittest.TestCase):

    def test_print_issue_template_callable(self):
        from reassemble_rules import print_issue_template
        report = {
            "applied_text": 5,
            "applied_options": 3,
            "total_applied": 8,
            "original_row_count": 100,
        }
        import io
        from contextlib import redirect_stdout
        buf = io.StringIO()
        with redirect_stdout(buf):
            print_issue_template("test_bloc", report)
        output = buf.getvalue()
        self.assertIn("TEMPLATE ISSUE GITHUB", output)
        self.assertIn("GF-08", output)


# ---------------------------------------------------------------------------
# GF-09 : Verrou (pas de test fonctionnel, on verifie que filelock est prevu)
# ---------------------------------------------------------------------------

class TestGF09_Verrou(unittest.TestCase):

    def test_filelock_mentionne_dans_doc(self):
        """GF-09 est documente dans les docstrings des outils."""
        import extract_rules_text
        self.assertIn("GF-09", extract_rules_text.__doc__)


# ---------------------------------------------------------------------------
# GF-10 : Rapport de couverture
# ---------------------------------------------------------------------------

class TestGF10_RapportCouverture(unittest.TestCase):

    def test_extraction_stats(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv",
                                         encoding=ENCODING, newline="",
                                         delete=False) as f:
            writer = csv.writer(f, lineterminator="\r\n")
            for row in SIMPLE_ROWS:
                writer.writerow(row)
            csv_path = f.name

        try:
            result = extract_texts(csv_path)
            stats = result["stats"]
            self.assertIn("total_rows", stats)
            self.assertIn("data_rows", stats)
            self.assertIn("text_segments", stats)
            self.assertIn("option_segments", stats)
            self.assertIn("total_segments", stats)
            self.assertGreater(stats["total_segments"], 0)
        finally:
            os.unlink(csv_path)

    def test_validation_coverage(self):
        data = {
            "entries": [
                {"text_en": "Hello", "text_fr": "Bonjour", "col": 4},
                {"text_en": "World", "text_fr": None, "col": 4},
            ]
        }
        result = validate_batch(data)
        self.assertIn("summary", result)
        self.assertEqual(result["summary"]["translated"], 1)
        self.assertEqual(result["summary"]["untranslated"], 1)
        self.assertEqual(result["summary"]["coverage_pct"], 50.0)

    def test_reassemble_report(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "rules.csv")
            out_path = os.path.join(tmpdir, "rules_out.csv")
            make_csv(SIMPLE_ROWS, csv_path)

            data = {"entries": [
                {"row_idx": 1, "col": 4,
                 "text_en": "Hello $playerName, welcome aboard.",
                 "text_fr": "Bonjour $playerName, bienvenue a bord."}
            ]}
            report = reassemble(csv_path, data, output_path=out_path)
            self.assertIn("applied_text", report)
            self.assertIn("applied_options", report)
            self.assertIn("total_applied", report)
            self.assertEqual(report["applied_text"], 1)


# ---------------------------------------------------------------------------
# Validation des options
# ---------------------------------------------------------------------------

class TestOptionIdPreserved(unittest.TestCase):

    def test_option_id_preserved(self):
        errs = check_option_id_preserved(
            "opt1:Continue",
            "opt1:Continuer",
        )
        self.assertEqual(errs, [])

    def test_option_id_traduit(self):
        errs = check_option_id_preserved(
            "opt1:Continue",
            "opt1_fr:Continuer",
        )
        self.assertTrue(len(errs) > 0)
        self.assertTrue(any("option_id" in e for e in errs))

    def test_option_priority_preserved(self):
        errs = check_option_id_preserved(
            "1:shrouded_optA:\"So... what is it?\"",
            "1:shrouded_optA:\"Alors... qu'est-ce que c'est ?\"",
        )
        self.assertEqual(errs, [])

    def test_option_priority_changed(self):
        errs = check_option_id_preserved(
            "1:shrouded_optA:\"So... what is it?\"",
            "2:shrouded_optA:\"Alors... qu'est-ce que c'est ?\"",
        )
        self.assertTrue(len(errs) > 0)


class TestReconstructOption(unittest.TestCase):

    def test_simple(self):
        result = reconstruct_option("opt1:Continue", "Continuer")
        self.assertEqual(result, "opt1:Continuer")

    def test_with_priority(self):
        result = reconstruct_option(
            "1:shrouded_optA:\"So... what is it?\"",
            "\"Alors... qu'est-ce que c'est ?\"",
        )
        self.assertEqual(result, "1:shrouded_optA:\"Alors... qu'est-ce que c'est ?\"")


# ---------------------------------------------------------------------------
# Apostrophes typographiques
# ---------------------------------------------------------------------------

class TestCurlyApostrophes(unittest.TestCase):

    def test_straight_apostrophe_ok(self):
        errs = check_curly_apostrophes("L'equipe est prete.")
        self.assertEqual(errs, [])

    def test_curly_apostrophe_rejected(self):
        errs = check_curly_apostrophes("L\u2019equipe est prete.")
        self.assertTrue(len(errs) > 0)
        self.assertTrue(any("U+2019" in e for e in errs))


# ---------------------------------------------------------------------------
# Encodage UTF-8
# ---------------------------------------------------------------------------

class TestEncodageUTF8(unittest.TestCase):

    def test_csv_ecrit_utf8(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            rows = [
                HEADER,
                row7("r1", "", "", "", "Les fournitures sont pr\u00eates.", "", ""),
            ]
            make_csv(rows, csv_path)

            # Relire en utf-8 doit fonctionner
            with open(csv_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("fournitures", content)
            self.assertIn("pr\u00eates", content)

    def test_guillemets_francais(self):
        """Les guillemets \u00ab \u00bb (U+00AB, U+00BB) sont dans UTF-8."""
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "test.csv")
            rows = [
                HEADER,
                row7("r1", "", "", "",
                     "Il dit \u00ab Bonjour \u00bb avec conviction.", "", ""),
            ]
            make_csv(rows, csv_path)

            with open(csv_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("\u00ab", content)
            self.assertIn("\u00bb", content)


# ---------------------------------------------------------------------------
# Glossaire — termes obligatoires
# ---------------------------------------------------------------------------

class TestGlossaire(unittest.TestCase):
    """Verifie que le validateur n'interfere pas avec les termes du glossaire."""

    def _validate_single(self, text_en, text_fr, col=4):
        entry = {"text_en": text_en, "text_fr": text_fr, "col": col}
        return validate_entry(entry)

    def test_fournitures_pas_provisions(self):
        """supplies -> fournitures, jamais provisions."""
        r = self._validate_single(
            "You need more supplies.",
            "Vous avez besoin de plus de fournitures.",
        )
        self.assertEqual(r["errors"], [])

    def test_fusiliers_pas_marines(self):
        """marines -> fusiliers, jamais marines."""
        r = self._validate_single(
            "Send the marines to board the ship.",
            "Envoyez les fusiliers aborder le vaisseau.",
        )
        self.assertEqual(r["errors"], [])

    def test_vaisseau_pas_navire(self):
        """ship -> vaisseau, jamais navire."""
        r = self._validate_single(
            "The ship is damaged.",
            "Le vaisseau est endommag\u00e9.",
        )
        self.assertEqual(r["errors"], [])

    def test_variables_preservees_glossaire(self):
        """Les variables restent intactes meme dans un texte traduit glossaire."""
        r = self._validate_single(
            "$playerSirOrMadam, your supplies are running low.",
            "$playerSirOrMadam, vos fournitures s'\u00e9puisent.",
        )
        self.assertEqual(r["errors"], [])

    def test_guillemets_francais_obligatoires(self):
        """Les guillemets \u00ab \u00bb sont utilisables sans erreur UTF-8."""
        text_fr = "Il dit \u00ab Bonjour \u00bb poliment."
        # Doit etre encodable en UTF-8
        encoded = text_fr.encode("utf-8")
        decoded = encoded.decode("utf-8")
        self.assertEqual(decoded, text_fr)

    def test_carburant_pas_combustible(self):
        """fuel -> carburant."""
        r = self._validate_single(
            "You need $fuel units of fuel.",
            "Vous avez besoin de $fuel unit\u00e9s de carburant.",
        )
        self.assertEqual(r["errors"], [])

    def test_porte_nefs(self):
        """carrier -> porte-nefs."""
        r = self._validate_single(
            "The carrier launches its fighters.",
            "Le porte-nefs lance ses chasseurs.",
        )
        self.assertEqual(r["errors"], [])


# ---------------------------------------------------------------------------
# Pipeline bout-en-bout
# ---------------------------------------------------------------------------

class TestPipelineBoutEnBout(unittest.TestCase):
    """Test du pipeline complet : extract -> translate -> validate -> reassemble."""

    def test_pipeline_complet(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Creer le CSV source
            csv_path = os.path.join(tmpdir, "rules.csv")
            json_path = os.path.join(tmpdir, "extract.json")
            out_path = os.path.join(tmpdir, "rules_out.csv")

            rows = [
                HEADER,
                row7("rule1", "DialogOptionSelected", "HasTag test",
                     'FireBest "doSomething"',
                     "$playerSirOrMadam, your fleet requires supplies.",
                     "testOpt1:Continue\ntestOpt2:Leave now",
                     "test note"),
            ]
            make_csv(rows, csv_path)

            # 2. Extraction
            result = extract_texts(csv_path)
            self.assertGreater(len(result["entries"]), 0)
            write_extract(result, json_path)

            # 3. Simuler la traduction (remplir text_fr)
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            for entry in data["entries"]:
                if entry["col"] == 4 and "$playerSirOrMadam" in entry.get("text_en", ""):
                    entry["text_fr"] = (
                        "$playerSirOrMadam, votre flotte a besoin de fournitures."
                    )
                elif entry["col"] == 5:
                    if "testOpt1" in entry.get("text_en", ""):
                        entry["text_fr"] = "testOpt1:Continuer"
                    elif "testOpt2" in entry.get("text_en", ""):
                        entry["text_fr"] = "testOpt2:Partir maintenant"

            # 4. Validation
            validation = validate_batch(data)
            self.assertTrue(validation["valid"],
                            f"Validation echouee: {validation['entries_report']}")
            self.assertEqual(validation["summary"]["total_errors"], 0)

            # 5. Reinsertion
            report = reassemble(csv_path, data, output_path=out_path)
            self.assertTrue(report["success"])
            self.assertEqual(report["integrity_errors"], [])
            self.assertEqual(report["original_row_count"], report["final_row_count"])

            # 6. Verification du CSV final
            final_rows = read_csv_raw(out_path)
            data_row = final_rows[1]

            # Colonnes intouchables preservees
            self.assertEqual(data_row[0], "rule1")
            self.assertEqual(data_row[1], "DialogOptionSelected")
            self.assertEqual(data_row[2], "HasTag test")
            self.assertEqual(data_row[3], 'FireBest "doSomething"')
            self.assertEqual(data_row[6], "test note")

            # Texte traduit
            self.assertIn("fournitures", data_row[4])
            self.assertIn("$playerSirOrMadam", data_row[4])

            # Options traduites, IDs preserves
            self.assertIn("testOpt1:Continuer", data_row[5])
            self.assertIn("testOpt2:Partir maintenant", data_row[5])

    def test_dry_run_ne_modifie_rien(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            csv_path = os.path.join(tmpdir, "rules.csv")
            make_csv(SIMPLE_ROWS, csv_path)

            with open(csv_path, "rb") as f:
                original_bytes = f.read()

            data = {"entries": [
                {"row_idx": 1, "col": 4,
                 "text_en": "Hello $playerName, welcome aboard.",
                 "text_fr": "Bonjour $playerName, bienvenue a bord."}
            ]}
            report = reassemble(csv_path, data, dry_run=True)
            self.assertTrue(report["success"])
            self.assertTrue(report["dry_run"])

            with open(csv_path, "rb") as f:
                after_bytes = f.read()
            self.assertEqual(original_bytes, after_bytes)


class TestBuildTranslationMap(unittest.TestCase):

    def test_text_map(self):
        data = {"entries": [
            {"row_idx": 5, "col": 4, "text_en": "Hello", "text_fr": "Bonjour"},
            {"row_idx": 6, "col": 4, "text_en": "World", "text_fr": None},
        ]}
        text_map, options_map = build_translation_map(data)
        self.assertIn((5, 4), text_map)
        self.assertNotIn((6, 4), text_map)  # text_fr is None

    def test_options_map(self):
        data = {"entries": [
            {"row_idx": 5, "col": 5, "text_en": "opt1:Go",
             "text_fr": "opt1:Aller", "option_id": "opt1"},
            {"row_idx": 5, "col": 5, "text_en": "opt2:Stay",
             "text_fr": "opt2:Rester", "option_id": "opt2"},
        ]}
        text_map, options_map = build_translation_map(data)
        self.assertIn(5, options_map)
        self.assertEqual(len(options_map[5]), 2)


# ---------------------------------------------------------------------------
# Validate entry
# ---------------------------------------------------------------------------

class TestValidateEntry(unittest.TestCase):

    def test_untranslated_entry(self):
        entry = {"text_en": "Hello", "text_fr": None, "col": 4}
        result = validate_entry(entry)
        self.assertFalse(result["translated"])
        self.assertEqual(result["errors"], [])

    def test_valid_translation(self):
        entry = {
            "text_en": "The $fleet is ready.",
            "text_fr": "La $fleet est pr\u00eate.",
            "col": 4,
        }
        result = validate_entry(entry)
        self.assertTrue(result["translated"])
        self.assertEqual(result["errors"], [])

    def test_option_with_preserved_id(self):
        entry = {
            "text_en": "opt1:Continue",
            "text_fr": "opt1:Continuer",
            "col": 5,
            "option_id": "opt1",
            "option_label_en": "Continue",
        }
        result = validate_entry(entry)
        self.assertTrue(result["translated"])
        self.assertEqual(result["errors"], [])


# ===========================================================================

if __name__ == "__main__":
    unittest.main()
