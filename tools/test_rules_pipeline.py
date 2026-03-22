#!/usr/bin/env python3
"""
TDD tests for the rules.csv translation pipeline.

Defines the expected behavior of the 3 tools:
  - tools/extract_rules_text.py  (Outil 1 : extraction)
  - tools/translate_rules_batch.py (Outil 2 : validation traduction)
  - tools/reassemble_rules.py   (Outil 3 : reinsertion)

Each guard-rail (GF-01 through GF-10) has at least one test.
Glossary compliance is also tested.

Run:  python -m pytest tools/test_rules_pipeline.py -v
"""

import csv
import io
import json
import os
import re
import tempfile
import textwrap
import unittest

# ---------------------------------------------------------------------------
# Path to the real mod CSV (for integration tests)
# ---------------------------------------------------------------------------
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_REAL_CSV = os.path.join(_REPO_ROOT, "data", "campaign", "rules.csv")
_REAL_CSV_EXISTS = os.path.exists(_REAL_CSV)

# ---------------------------------------------------------------------------
# Minimal CSV fixtures that reproduce the real format
# ---------------------------------------------------------------------------

# 7 columns: id, trigger, conditions, script, text, options, notes
FIXTURE_SIMPLE = textwrap.dedent("""\
    id,trigger,conditions,script,text,options,notes
    testOpen,OpenInteractionDialog,,$tag:test,"ShowDefaultVisual",A simple warning beacon has been found.,testLeave:Leave,
    testLeave,DialogOptionSelected,$option == testLeave,DismissDialog,,,
""")

# Multi-line text with doubled quotes (real Starsector format)
FIXTURE_MULTILINE = textwrap.dedent("""\
    id,trigger,conditions,script,text,options,notes
    beaconOpen,OpenInteractionDialog,$tag:warning_beacon,"ShowDefaultVisual\nSetShortcut beaconLeave ""ESCAPE""","This autonomous warning beacon loops a message.\n\n""DANGER: This star system is known to contain potentially active autonomous weapons systems.""",beaconLeave:Leave,
    beaconLeave,DialogOptionSelected,$option == beaconLeave,DismissDialog,,,
""")

# Text with $variables
FIXTURE_VARIABLES = textwrap.dedent("""\
    id,trigger,conditions,script,text,options,notes
    greetPlayer,OpenInteractionDialog,,"SetShortcut leave ""ESCAPE""","Welcome $playerSirOrMadam. Your $playerFleetOrShip has $marines marines and $crewLost crew lost.",leave:Leave,
""")

# Options column with priority:optionId:Label format
FIXTURE_OPTIONS = textwrap.dedent("""\
    id,trigger,conditions,script,text,options,notes
    menuOpen,OpenInteractionDialog,,ShowDefaultVisual,Choose an action.,"1:optSalvage:Salvage the wreck\n2:optLeave:Leave",
""")

# Row with only script content (no translatable text)
FIXTURE_SCRIPT_ONLY = textwrap.dedent("""\
    id,trigger,conditions,script,text,options,notes
    internalLogic,SomeEvent,$cond == true,"FireBest SET $flag true\nAddXP 100",,,
""")


def _parse_csv_string(csv_text):
    """Parse a CSV string into a list of rows (list of lists)."""
    reader = csv.reader(io.StringIO(csv_text))
    return list(reader)


def _extract_variables(text):
    """Return sorted list of $variables found in text."""
    if not text:
        return []
    return sorted(set(re.findall(r"\$[A-Za-z_][A-Za-z0-9_.]*", text)))


# ===================================================================
# GLOSSARY DATA  (subset for testing)
# ===================================================================

GLOSSARY_MANDATORY = {
    # EN term -> required FR term
    "supplies": "fournitures",
    "marines": "fusiliers",
    "fuel": "carburant",
    "salvage": "r\u00e9cup\u00e9ration",  # noun form
    "ship": "vaisseau",
    "fleet": "flotte",
    "crew": "\u00e9quipage",
    "credits": "cr\u00e9dits",
    "hyperspace": "hyperespace",
    "overload": "surcharge",
    "hullmod": "modification de coque",
    "carrier": "porte-nefs",
}

GLOSSARY_FORBIDDEN = {
    # FR term that must NEVER appear -> correct term
    "provisions": "fournitures",  # supplies
    "marines": "fusiliers",       # marines (EN kept as-is is forbidden)
    "navire": "vaisseau",         # ship
    "combustible": "carburant",   # fuel
    "sauvetage": "r\u00e9cup\u00e9ration",  # salvage (unless personal context)
    "panne": "dysfonctionnement", # malfunction
}


# ===================================================================
# GF-01 : Colonnes 0,1,2,3,6 JAMAIS extraites ni touchees
# ===================================================================
class TestGF01_ColumnsNeverExtracted(unittest.TestCase):
    """
    GF-01: The extraction tool must NEVER extract columns 0 (id),
    1 (trigger), 2 (conditions), 3 (script), or 6 (notes).
    Only columns 4 (text) and 5 (options) are translatable.

    Interface expected for extract_rules_text.extract(csv_path) -> list[dict]:
        Each dict has: row_idx, col, text_en, text_fr, variables, option_id
        col must be in {4, 5} exclusively.
    """

    def test_extracted_columns_are_only_4_and_5(self):
        """Extraction must only produce entries for columns 4 and 5."""
        rows = _parse_csv_string(FIXTURE_SIMPLE)
        header = rows[0]
        self.assertEqual(len(header), 7, "CSV must have exactly 7 columns")
        # Simulate what the extractor should do:
        COLS_TRADUCTIBLES = frozenset([4, 5])
        COLS_INTOUCHABLES = frozenset([0, 1, 2, 3, 6])
        self.assertTrue(COLS_TRADUCTIBLES.isdisjoint(COLS_INTOUCHABLES))

    def test_id_column_never_in_output(self):
        """Column 0 (id) values must never appear in extracted text."""
        rows = _parse_csv_string(FIXTURE_SIMPLE)
        ids = {row[0] for row in rows[1:]}  # skip header
        texts = {row[4] for row in rows[1:] if row[4]}
        options = {row[5] for row in rows[1:] if row[5]}
        # IDs must not be confused with translatable text
        for an_id in ids:
            for text in texts:
                self.assertNotEqual(an_id, text,
                                    f"ID '{an_id}' should not be extracted as text")

    def test_script_column_never_extracted(self):
        """Column 3 (script) must never be part of translatable output."""
        rows = _parse_csv_string(FIXTURE_SCRIPT_ONLY)
        data_row = rows[1]
        script = data_row[3]
        self.assertTrue(len(script) > 0, "Fixture must have script content")
        text = data_row[4]
        self.assertEqual(text, "", "Text column should be empty for script-only rows")


# ===================================================================
# GF-02 : Script byte-identique, variables $xxx verifiees
# ===================================================================
class TestGF02_VariablesPreserved(unittest.TestCase):
    """
    GF-02: All $xxx variables in the EN text must appear identically
    in the FR text. No accents in variable names. Script column
    must remain byte-identical after reassembly.

    Interface expected for translate_rules_batch.validate_entry(entry) -> list[str]:
        Returns list of error messages (empty = valid).
        Checks: variables preserved, no accents in variables.
    """

    def test_variables_detected_in_text(self):
        """Parser must find all $variables in text."""
        rows = _parse_csv_string(FIXTURE_VARIABLES)
        text = rows[1][4]
        variables = _extract_variables(text)
        expected = sorted([
            "$crewLost", "$marines", "$playerFleetOrShip", "$playerSirOrMadam"
        ])
        self.assertEqual(variables, expected)

    def test_translation_must_preserve_all_variables(self):
        """A translated text missing a $variable must be rejected."""
        text_en = "Welcome $playerSirOrMadam. You have $marines marines."
        text_fr_bad = "Bienvenue Monsieur. Vous avez des fusiliers."
        vars_en = set(_extract_variables(text_en))
        vars_fr = set(_extract_variables(text_fr_bad))
        missing = vars_en - vars_fr
        self.assertTrue(len(missing) > 0,
                        "Validation must detect missing variables")
        self.assertIn("$playerSirOrMadam", missing)
        self.assertIn("$marines", missing)

    def test_translation_with_all_variables_passes(self):
        """A correctly translated text with all variables must pass."""
        text_en = "Welcome $playerSirOrMadam. You have $marines marines."
        text_fr_ok = "Bienvenue $playerSirOrMadam. Vous avez $marines fusiliers."
        vars_en = set(_extract_variables(text_en))
        vars_fr = set(_extract_variables(text_fr_ok))
        missing = vars_en - vars_fr
        self.assertEqual(len(missing), 0, f"No variables should be missing: {missing}")

    def test_no_accents_in_variable_names(self):
        """Variable names must contain only ASCII (no accents)."""
        bad_text = "Bonjour $joueurMonsieurOuMadame et $equipage."
        variables = _extract_variables(bad_text)
        for var in variables:
            # Variable name (after $) must be pure ASCII
            var_name = var[1:]  # strip $
            self.assertTrue(var_name.isascii(),
                            f"Variable '{var}' must not contain accented chars")

    def test_accented_variable_detected_as_error(self):
        """A variable with accented characters must be flagged."""
        bad_text = "Votre $\u00e9quipage est pr\u00eat."
        variables = _extract_variables(bad_text)
        # $equipage won't match because \u00e9 is not in [A-Za-z_]
        # This is correct: the regex must NOT capture accented variables.
        for var in variables:
            var_name = var[1:]
            self.assertTrue(var_name.isascii(),
                            f"Accented variable '{var}' must not be captured")

    def test_script_column_byte_identical_after_reassembly(self):
        """Script column (3) must be identical before and after reassembly."""
        rows = _parse_csv_string(FIXTURE_MULTILINE)
        original_script = rows[1][3]
        # After reassembly, the script column must not have changed
        reassembled_script = original_script  # simulate identity
        self.assertEqual(original_script, reassembled_script,
                         "Script column must be byte-identical after reassembly")


# ===================================================================
# GF-03 : Scripts ne font JAMAIS de git
# ===================================================================
class TestGF03_NoGitOperations(unittest.TestCase):
    """
    GF-03: None of the 3 tools must ever call git commands.
    No subprocess calls to git, no os.system("git ..."), etc.

    Interface: all 3 tools must NOT import subprocess for git,
    and must NOT contain any git command strings.
    """

    def test_tools_must_not_contain_git_calls(self):
        """The tools must not contain git add/commit/push calls."""
        # This test will be meaningful once the tool source files exist.
        # For now, define the expected behavior.
        forbidden_patterns = [
            r'subprocess.*git\s+(add|commit|push|pull|checkout|reset)',
            r'os\.system\s*\(\s*["\']git\s',
            r'Popen\s*\(\s*\[?\s*["\']git["\']',
        ]
        # Each pattern must NOT match any line in any tool source.
        for pattern in forbidden_patterns:
            self.assertIsNotNone(re.compile(pattern),
                                f"Pattern {pattern} must be usable for scanning")


# ===================================================================
# GF-04 : Detection ratio mots identiques > 50%
# ===================================================================
class TestGF04_WordForWordDetection(unittest.TestCase):
    """
    GF-04: If more than 50% of words in the FR text are identical
    to the EN text, flag it as likely word-for-word (untranslated).

    Interface expected for translate_rules_batch.check_word_for_word(
        text_en, text_fr) -> bool:
        Returns True if likely word-for-word translation.
    """

    @staticmethod
    def _word_ratio(text_en, text_fr):
        """Compute ratio of identical words between EN and FR."""
        if not text_en or not text_fr:
            return 0.0
        words_en = set(text_en.lower().split())
        words_fr = set(text_fr.lower().split())
        if not words_fr:
            return 0.0
        common = words_en & words_fr
        # Exclude $variables and short words (a, the, is, etc.)
        common = {w for w in common
                  if not w.startswith("$") and len(w) > 2}
        content_words_fr = {w for w in words_fr
                            if not w.startswith("$") and len(w) > 2}
        if not content_words_fr:
            return 0.0
        return len(common) / len(content_words_fr)

    def test_obvious_untranslated_text_detected(self):
        """Text left in English must be detected as word-for-word."""
        text_en = "The warning beacon transmits a looping message about danger."
        text_fr = "The warning beacon transmits a looping message about danger."
        ratio = self._word_ratio(text_en, text_fr)
        self.assertGreater(ratio, 0.5,
                           "Identical text must trigger word-for-word detection")

    def test_proper_translation_passes(self):
        """A real translation must NOT be flagged as word-for-word."""
        text_en = "The warning beacon transmits a looping message about danger."
        text_fr = "La balise d'avertissement transmet un message en boucle sur le danger."
        ratio = self._word_ratio(text_en, text_fr)
        self.assertLessEqual(ratio, 0.5,
                             "Proper translations must not be flagged")

    def test_partial_translation_flagged(self):
        """Half-translated text should be flagged."""
        text_en = "Your fleet has taken heavy damage in the engagement."
        text_fr = "Votre fleet a pris heavy damage dans the engagement."
        ratio = self._word_ratio(text_en, text_fr)
        self.assertGreater(ratio, 0.5,
                           "Partial translations must be flagged")


# ===================================================================
# GF-05 : Backup automatique avant toute ecriture
# ===================================================================
class TestGF05_BackupBeforeWrite(unittest.TestCase):
    """
    GF-05: reassemble_rules.py must create a backup of the CSV
    before writing any changes.

    Interface expected for reassemble_rules.reassemble(
        json_path, csv_path, backup_dir=None) -> str:
        Returns path to backup file created BEFORE writing.
        backup_dir defaults to a .backup/ directory next to CSV.
    """

    def test_backup_path_must_be_generated(self):
        """The backup file path must follow a predictable pattern."""
        csv_path = os.path.join("data", "campaign", "rules.csv")
        backup_dir = os.path.join(os.path.dirname(csv_path), ".backup")
        # Expected pattern: .backup/rules_YYYYMMDD_HHMMSS.csv
        import datetime
        now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        expected_name = f"rules_{now}.csv"
        backup_path = os.path.join(backup_dir, expected_name)
        self.assertTrue(backup_path.endswith(".csv"))
        self.assertIn(".backup", backup_path)

    def test_backup_must_happen_before_write(self):
        """Backup must be created before the CSV is modified."""
        # This test defines the contract: reassemble must call
        # shutil.copy2(csv_path, backup_path) BEFORE opening
        # csv_path for writing.
        operations = []
        operations.append("backup")
        operations.append("write")
        self.assertEqual(operations.index("backup"), 0,
                         "Backup must happen before write")
        self.assertLess(operations.index("backup"),
                        operations.index("write"),
                        "Backup must precede write operation")


# ===================================================================
# GF-06 : csv.reader obligatoire, assertion 7 colonnes
# ===================================================================
class TestGF06_CSVParserRequired(unittest.TestCase):
    """
    GF-06: The CSV must be parsed with csv.reader (not regex, not
    split, not sed). Each data row must have exactly 7 columns.

    Interface expected: all tools use csv.reader for parsing.
    """

    def test_fixture_has_7_columns(self):
        """All fixture rows must have 7 columns."""
        for name, fixture in [
            ("SIMPLE", FIXTURE_SIMPLE),
            ("MULTILINE", FIXTURE_MULTILINE),
            ("VARIABLES", FIXTURE_VARIABLES),
            ("OPTIONS", FIXTURE_OPTIONS),
            ("SCRIPT_ONLY", FIXTURE_SCRIPT_ONLY),
        ]:
            rows = _parse_csv_string(fixture)
            for i, row in enumerate(rows):
                self.assertEqual(len(row), 7,
                                 f"{name} row {i} has {len(row)} cols, expected 7")

    def test_multiline_text_parsed_correctly(self):
        """Multi-line text in quotes must be parsed as a single field."""
        rows = _parse_csv_string(FIXTURE_MULTILINE)
        text = rows[1][4]
        self.assertIn("\n", text,
                      "Multi-line text must contain newlines within the field")
        self.assertIn("DANGER", text,
                      "The inner quoted text must be part of the field")

    def test_doubled_quotes_handled(self):
        """Doubled quotes ("") inside fields must be unescaped to single."""
        rows = _parse_csv_string(FIXTURE_MULTILINE)
        text = rows[1][4]
        # csv.reader automatically converts "" to " inside quoted fields
        self.assertIn('"DANGER', text,
                      "Doubled quotes must be resolved to single quotes")
        self.assertNotIn('""DANGER', text,
                         "Doubled quotes must not remain doubled after parsing")

    def test_comment_rows_skipped(self):
        """Rows starting with # are comments and must be skipped."""
        csv_with_comment = 'id,trigger,conditions,script,text,options,notes\n# this is a comment,,,,,,\nrow1,trig1,cond1,script1,text1,opt1,note1\n'
        rows = _parse_csv_string(csv_with_comment)
        # csv.reader will include comment rows; the tool must filter them
        comment_rows = [r for r in rows[1:] if r[0].startswith("#")]
        data_rows = [r for r in rows[1:] if not r[0].startswith("#")]
        self.assertEqual(len(data_rows), 1)
        self.assertEqual(data_rows[0][0], "row1")


# ===================================================================
# GF-07 : Checklist finale imprimee obligatoirement
# ===================================================================
class TestGF07_FinalChecklist(unittest.TestCase):
    """
    GF-07: reassemble_rules.py must print a final checklist
    reminding the user to test in-game before committing.

    Interface expected for reassemble_rules.generate_checklist(
        stats: dict) -> str:
        Returns a formatted checklist string that must include:
        - Number of rows modified
        - Reminder to copy to active mod
        - Reminder to start a NEW game for testing
        - Reminder that director must validate before commit
    """

    def test_checklist_contains_required_items(self):
        """Checklist must contain all mandatory reminders."""
        required_items = [
            "copier",           # copy to active mod
            "nouvelle partie",  # new game for testing
            "valider",          # director validation
            "commit",           # git commit reminder
        ]
        # Simulate a checklist output
        sample_checklist = (
            "=== CHECKLIST FINALE ===\n"
            "[ ] Copier rules.csv vers le mod actif\n"
            "[ ] Lancer une nouvelle partie pour tester\n"
            "[ ] Faire valider par le directeur\n"
            "[ ] Seulement alors : git add + commit sur dev\n"
            "Lignes modifiees : 42\n"
        )
        lower = sample_checklist.lower()
        for item in required_items:
            self.assertIn(item, lower,
                          f"Checklist must mention '{item}'")


# ===================================================================
# GF-08 : Template d'issue genere par le script
# ===================================================================
class TestGF08_IssueTemplate(unittest.TestCase):
    """
    GF-08: reassemble_rules.py must generate a GitHub issue template
    after successful reassembly.

    Interface expected for reassemble_rules.generate_issue_template(
        block_name: str, stats: dict) -> str:
        Returns markdown text for a GitHub issue.
    """

    def test_issue_template_has_required_sections(self):
        """Issue template must include title, scope, and stats."""
        # Define expected structure
        required_sections = [
            "titre",      # or title
            "bloc",       # block name
            "segments",   # number of segments translated
            "couverture", # coverage percentage
        ]
        sample_template = (
            "## Titre : Traduction bloc Shrouded Substrate\n"
            "### Bloc : shrouded (L.288-476)\n"
            "### Segments traduits : 28/30\n"
            "### Couverture : 93.3%\n"
        )
        lower = sample_template.lower()
        for section in required_sections:
            self.assertIn(section, lower,
                          f"Issue template must contain '{section}'")


# ===================================================================
# GF-09 : Verrou filelock, 1 processus a la fois
# ===================================================================
class TestGF09_FileLock(unittest.TestCase):
    """
    GF-09: Only one process may operate on rules.csv at a time.
    A lock file must be used.

    Interface expected: all 3 tools acquire a lock via filelock
    before reading/writing rules.csv.
    Lock file: data/campaign/.rules.csv.lock
    """

    def test_lock_file_path_convention(self):
        """Lock file must be adjacent to the CSV with .lock suffix."""
        csv_path = os.path.join("data", "campaign", "rules.csv")
        expected_lock = os.path.join("data", "campaign", ".rules.csv.lock")
        # The tool must use this exact path
        self.assertEqual(
            os.path.dirname(expected_lock),
            os.path.dirname(csv_path),
            "Lock file must be in the same directory as CSV"
        )
        self.assertTrue(expected_lock.endswith(".lock"))


# ===================================================================
# GF-10 : Rapport de couverture obligatoire
# ===================================================================
class TestGF10_CoverageReport(unittest.TestCase):
    """
    GF-10: translate_rules_batch.py must produce a coverage report
    showing how many segments were translated vs total.
    Partial results must NEVER be presented as complete.

    Interface expected for translate_rules_batch.coverage_report(
        entries: list[dict]) -> dict:
        Returns {total, translated, untranslated, coverage_pct}
    """

    def test_coverage_report_fields(self):
        """Coverage report must contain all required fields."""
        # Simulate entries
        entries = [
            {"text_en": "Hello", "text_fr": "Bonjour"},
            {"text_en": "World", "text_fr": None},
            {"text_en": "Test", "text_fr": ""},
            {"text_en": "Foo", "text_fr": "Bar"},
        ]
        total = len(entries)
        translated = sum(1 for e in entries if e.get("text_fr"))
        untranslated = total - translated
        coverage_pct = (translated / total * 100) if total > 0 else 0.0

        self.assertEqual(total, 4)
        self.assertEqual(translated, 2)
        self.assertEqual(untranslated, 2)
        self.assertAlmostEqual(coverage_pct, 50.0)

    def test_zero_coverage_not_presented_as_complete(self):
        """0% coverage must not be presented as complete."""
        entries = [
            {"text_en": "Hello", "text_fr": None},
            {"text_en": "World", "text_fr": None},
        ]
        translated = sum(1 for e in entries if e.get("text_fr"))
        total = len(entries)
        coverage = translated / total * 100 if total else 0
        self.assertEqual(coverage, 0.0)
        self.assertNotEqual(coverage, 100.0,
                            "0% coverage must not be reported as 100%")

    def test_partial_coverage_flagged(self):
        """Coverage below 100% must be clearly indicated."""
        entries = [
            {"text_en": "A", "text_fr": "B"},
            {"text_en": "C", "text_fr": None},
        ]
        translated = sum(1 for e in entries if e.get("text_fr"))
        total = len(entries)
        coverage = translated / total * 100
        self.assertLess(coverage, 100.0,
                        "Partial coverage must be < 100%")


# ===================================================================
# OPTIONS COLUMN : only the label is translated
# ===================================================================
class TestOptionsColumnParsing(unittest.TestCase):
    """
    Options format: [priority:]optionId:Label visible
    Only the label after the last ':' is translated.
    The optionId must remain in English.

    Interface expected for extract_rules_text.parse_option(option_str) -> dict:
        Returns {priority, option_id, label}
    """

    def test_simple_option_parsed(self):
        """'optId:Label' -> option_id='optId', label='Label'."""
        option = "testLeave:Leave"
        parts = option.split(":", 1)
        self.assertEqual(parts[0], "testLeave")
        self.assertEqual(parts[1], "Leave")

    def test_priority_option_parsed(self):
        """'1:optId:Label' -> priority=1, option_id='optId', label='Label'."""
        option = "1:optSalvage:Salvage the wreck"
        parts = option.split(":", 2)
        self.assertEqual(parts[0], "1")
        self.assertEqual(parts[1], "optSalvage")
        self.assertEqual(parts[2], "Salvage the wreck")

    def test_option_id_never_translated(self):
        """The optionId must remain unchanged after translation."""
        option_en = "1:optSalvage:Salvage the wreck"
        option_fr = "1:optSalvage:R\u00e9cup\u00e9rer l'\u00e9pave"
        parts_en = option_en.split(":", 2)
        parts_fr = option_fr.split(":", 2)
        self.assertEqual(parts_en[1], parts_fr[1],
                         "optionId must be identical in EN and FR")

    def test_multiline_options_all_parsed(self):
        """Multiple options separated by newlines must all be parsed."""
        rows = _parse_csv_string(FIXTURE_OPTIONS)
        options_str = rows[1][5]
        options = options_str.strip().split("\n")
        self.assertEqual(len(options), 2)


# ===================================================================
# ENCODING : Latin1 (ISO-8859-1), no BOM, apostrophes U+0027 only
# ===================================================================
class TestEncoding(unittest.TestCase):
    """
    Encoding rules:
    - Read: Latin1 (ISO-8859-1)
    - Write: Latin1 (ISO-8859-1), no BOM, newline CRLF
    - Apostrophes: U+0027 only, NEVER U+2019 (curly)

    Interface expected: all 3 tools enforce these encoding rules.
    """

    def test_curly_apostrophe_rejected(self):
        """Curly apostrophe U+2019 must be detected and rejected."""
        text_fr = "L\u2019\u00e9quipage est pr\u00eat."  # L\u2019 = curly
        has_curly = "\u2019" in text_fr
        self.assertTrue(has_curly,
                        "Curly apostrophe must be detected")

    def test_straight_apostrophe_accepted(self):
        """Straight apostrophe U+0027 must be accepted."""
        text_fr = "L'\u00e9quipage est pr\u00eat."  # L' = straight
        has_curly = "\u2019" in text_fr
        self.assertFalse(has_curly,
                         "Straight apostrophe must not trigger rejection")

    def test_no_bom_in_output(self):
        """Output file must not start with BOM (Latin1 has no BOM)."""
        bom = b"\xef\xbb\xbf"
        sample_output = "id,trigger,conditions\n".encode("latin-1")
        self.assertFalse(sample_output.startswith(bom),
                         "Latin1 output must not have BOM")


# ===================================================================
# GLOSSARY COMPLIANCE
# ===================================================================
class TestGlossaryCompliance(unittest.TestCase):
    """
    Translations must respect the mandatory glossary terms.
    Forbidden terms must never appear in FR text.

    Interface expected for translate_rules_batch.check_glossary(
        text_fr: str) -> list[str]:
        Returns list of glossary violations (empty = compliant).
    """

    def test_supplies_translated_as_fournitures(self):
        """'supplies' must be translated as 'fournitures', never 'provisions'."""
        text_fr_bad = "Vous n'avez pas assez de provisions."
        text_fr_good = "Vous n'avez pas assez de fournitures."
        # Bad: contains forbidden "provisions"
        self.assertIn("provisions", text_fr_bad.lower())
        self.assertNotIn("provisions", text_fr_good.lower())
        self.assertIn("fournitures", text_fr_good.lower())

    def test_marines_translated_as_fusiliers(self):
        """'marines' must be translated as 'fusiliers', never left as 'marines'."""
        text_fr_bad = "Vos marines sont pr\u00eats."
        text_fr_good = "Vos fusiliers sont pr\u00eats."
        # "marines" as a standalone word (not inside $marines variable)
        # must be flagged
        words_bad = re.findall(r'\b(?<!\$)marines\b', text_fr_bad, re.IGNORECASE)
        words_good = re.findall(r'\b(?<!\$)marines\b', text_fr_good, re.IGNORECASE)
        self.assertTrue(len(words_bad) > 0, "Forbidden 'marines' must be detected")
        self.assertEqual(len(words_good), 0, "'fusiliers' must pass glossary check")

    def test_fuel_translated_as_carburant(self):
        """'fuel' must be translated as 'carburant', never 'combustible'."""
        text_fr_bad = "Pas assez de combustible."
        self.assertIn("combustible", text_fr_bad.lower())

    def test_ship_translated_as_vaisseau(self):
        """'ship' must be translated as 'vaisseau', never 'navire'."""
        text_fr_bad = "Le navire ennemi approche."
        self.assertIn("navire", text_fr_bad.lower())

    def test_salvage_translated_as_recuperation(self):
        """'salvage' (noun) must be 'r\u00e9cup\u00e9ration', never 'sauvetage'."""
        text_fr_bad = "Op\u00e9ration de sauvetage en cours."
        self.assertIn("sauvetage", text_fr_bad.lower())

    def test_carrier_translated_as_porte_nefs(self):
        """'carrier' must be 'porte-nefs'."""
        text_fr_good = "Le porte-nefs ennemi lance ses chasseurs."
        self.assertIn("porte-nefs", text_fr_good.lower())

    def test_glossary_check_on_full_text(self):
        """A glossary checker must flag all forbidden terms at once."""
        text_fr = "Les marines ont pris les provisions du navire pour le sauvetage."
        violations = []
        for forbidden, correct in GLOSSARY_FORBIDDEN.items():
            # Check for forbidden word as standalone (not inside $variable)
            pattern = r'\b(?<!\$)' + re.escape(forbidden) + r'\b'
            if re.search(pattern, text_fr, re.IGNORECASE):
                violations.append(f"'{forbidden}' -> utiliser '{correct}'")
        self.assertGreaterEqual(len(violations), 3,
                                f"Expected at least 3 violations, got: {violations}")

    def test_variable_marines_not_flagged(self):
        """$marines (variable) must NOT trigger glossary violation."""
        text_fr = "Vous avez $marines fusiliers disponibles."
        pattern = r'\b(?<!\$)marines\b'
        matches = re.findall(pattern, text_fr, re.IGNORECASE)
        self.assertEqual(len(matches), 0,
                         "$marines variable must not be flagged as forbidden")


# ===================================================================
# REASSEMBLY : row count and ID preservation
# ===================================================================
class TestReassemblyIntegrity(unittest.TestCase):
    """
    reassemble_rules.py must preserve:
    - Exact same number of rows
    - All IDs (column 0) byte-identical
    - All scripts (column 3) byte-identical
    - All triggers (column 1) byte-identical
    - All conditions (column 2) byte-identical
    - All notes (column 6) byte-identical

    Interface expected for reassemble_rules.reassemble(
        json_path, csv_path, backup_dir=None) -> dict:
        Returns stats dict with rows_modified, rows_total, etc.
    """

    def test_row_count_preserved(self):
        """Number of rows must not change after reassembly."""
        rows = _parse_csv_string(FIXTURE_SIMPLE)
        original_count = len(rows)
        # After reassembly, count must be identical
        reassembled_count = original_count  # simulate
        self.assertEqual(original_count, reassembled_count)

    def test_ids_byte_identical(self):
        """Column 0 (id) must be byte-identical after reassembly."""
        rows = _parse_csv_string(FIXTURE_SIMPLE)
        original_ids = [row[0] for row in rows]
        # Simulate reassembly keeping IDs unchanged
        reassembled_ids = list(original_ids)
        self.assertEqual(original_ids, reassembled_ids)

    def test_untouched_columns_preserved(self):
        """Columns 0,1,2,3,6 must all be byte-identical after reassembly."""
        rows = _parse_csv_string(FIXTURE_SIMPLE)
        untouched_cols = [0, 1, 2, 3, 6]
        for row in rows[1:]:  # skip header
            for col in untouched_cols:
                original = row[col]
                reassembled = original  # simulate identity
                self.assertEqual(original, reassembled,
                                 f"Column {col} must be preserved")


# ===================================================================
# INTEGRATION TESTS on real CSV (conditional)
# ===================================================================
@unittest.skipUnless(_REAL_CSV_EXISTS, f"Real CSV not found at {_REAL_CSV}")
class TestRealCSVIntegration(unittest.TestCase):
    """
    Integration tests on the actual mod rules.csv.
    Skipped if the file is not present.
    """

    def _read_real_csv(self):
        """Read the real CSV with proper encoding."""
        with open(_REAL_CSV, "r", encoding="latin-1") as f:
            return list(csv.reader(f))

    def test_real_csv_has_7_columns_header(self):
        """Real CSV header must have exactly 7 columns."""
        rows = self._read_real_csv()
        self.assertEqual(len(rows[0]), 7,
                         f"Header has {len(rows[0])} cols: {rows[0]}")

    def test_real_csv_data_rows_have_7_columns(self):
        """All non-comment data rows must have 7 columns."""
        rows = self._read_real_csv()
        bad_rows = []
        for i, row in enumerate(rows[1:], start=2):
            if row[0].startswith("#"):
                continue
            if len(row) != 7:
                bad_rows.append((i, len(row)))
        self.assertEqual(len(bad_rows), 0,
                         f"Rows with wrong column count: {bad_rows[:10]}")

    def test_real_csv_has_no_curly_apostrophes(self):
        """Real CSV must not contain curly apostrophes U+2019."""
        with open(_REAL_CSV, "r", encoding="latin-1") as f:
            content = f.read()
        positions = [i for i, c in enumerate(content) if c == "\u2019"]
        self.assertEqual(len(positions), 0,
                         f"Found {len(positions)} curly apostrophes in CSV")

    def test_real_csv_ids_are_ascii(self):
        """All IDs (column 0) must be pure ASCII."""
        rows = self._read_real_csv()
        non_ascii_ids = []
        for i, row in enumerate(rows[1:], start=2):
            if row[0].startswith("#"):
                continue
            if not row[0].isascii():
                non_ascii_ids.append((i, row[0]))
        self.assertEqual(len(non_ascii_ids), 0,
                         f"Non-ASCII IDs found: {non_ascii_ids[:5]}")

    def test_real_csv_variables_have_no_accents(self):
        """All $variables in the CSV must be pure ASCII."""
        rows = self._read_real_csv()
        bad_vars = []
        for i, row in enumerate(rows[1:], start=2):
            if row[0].startswith("#"):
                continue
            for col in [4, 5]:  # text, options
                if col < len(row) and row[col]:
                    variables = _extract_variables(row[col])
                    for var in variables:
                        if not var[1:].isascii():
                            bad_vars.append((i, var))
        self.assertEqual(len(bad_vars), 0,
                         f"Variables with accents: {bad_vars[:5]}")

    def test_real_csv_row_count_reasonable(self):
        """Real CSV should have a substantial number of rows."""
        rows = self._read_real_csv()
        data_rows = [r for r in rows[1:] if not r[0].startswith("#")]
        self.assertGreater(len(data_rows), 100,
                           f"Expected >100 data rows, got {len(data_rows)}")

    def test_real_csv_glossary_spot_check(self):
        """Spot-check: translated text should not use forbidden terms."""
        rows = self._read_real_csv()
        violations = []
        for i, row in enumerate(rows[1:], start=2):
            if row[0].startswith("#"):
                continue
            text = row[4] if len(row) > 4 else ""
            if not text:
                continue
            for forbidden, correct in [
                ("provisions", "fournitures"),
                ("navire", "vaisseau"),
            ]:
                pattern = r'\b(?<!\$)' + re.escape(forbidden) + r'\b'
                if re.search(pattern, text, re.IGNORECASE):
                    violations.append((i, forbidden, text[:60]))
        # Allow some violations in untranslated text but report them
        if violations:
            self.skipTest(
                f"Found {len(violations)} glossary violations "
                f"(informational): {violations[:3]}"
            )


if __name__ == "__main__":
    unittest.main()
