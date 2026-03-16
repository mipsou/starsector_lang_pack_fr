"""Tests d'intégration pour le workflow JSON complet."""

import pytest
from pathlib import Path
import shutil

from scripts.handlers.json.writer import JsonWriter
from scripts.handlers.json.validator import JsonValidator, FileType
from scripts.starsector_json import format_starsector_json, parse_starsector_json

@pytest.fixture
def test_data_dir(tmp_path):
    """Crée un répertoire de test avec des fichiers JSON."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    return data_dir

@pytest.fixture
def mock_strings_file(test_data_dir):
    """Crée un fichier strings.json de test."""
    content = {
        "strings": {
            "test_id": {
                "text": "Test avec $faction",
                "category": "misc"
            }
        }
    }
    file_path = test_data_dir / "strings.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_starsector_json(content, FileType.STRINGS))
    return file_path

@pytest.fixture
def mock_tips_file(test_data_dir):
    """Crée un fichier tips.json de test."""
    content = {
        "tips": [
            {
                "id": "tip1",
                "tip": "Conseil avec $market",
                "category": "GENERAL"
            }
        ]
    }
    file_path = test_data_dir / "tips.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_starsector_json(content, FileType.TIPS))
    return file_path

@pytest.fixture
def mock_tooltips_file(test_data_dir):
    """Crée un fichier tooltips.json de test."""
    content = {
        "codex": {
            "damage_test": {
                "title": "Test Dégâts",
                "body": "Description avec $damage",
            }
        },
        "warroom": {
            "test_command": {
                "title": "Commande Test",
                "body": "Description avec $flux",
            }
        }
    }
    file_path = test_data_dir / "tooltips.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_starsector_json(content, FileType.TOOLTIPS))
    return file_path

@pytest.fixture
def mock_descriptions_file(test_data_dir):
    """Crée un fichier descriptions.json de test."""
    content = [
        {
            "key": "descriptions.csv#('test_weapon', 'WEAPON')$text1",
            "original": "Test weapon description with $damage",
            "translation": "Description d'arme test avec $damage",
            "stage": 1,
            "context": "Test context"
        }
    ]
    file_path = test_data_dir / "descriptions.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(format_starsector_json(content, FileType.DESCRIPTIONS))
    return file_path

def test_workflow_strings(mock_strings_file):
    """Test le workflow complet pour strings.json."""
    # 1. Backup
    writer = JsonWriter()
    backup = writer.create_backup(mock_strings_file)
    assert backup.exists()

    # 2. Modification
    updates = {
        "strings": {
            "new_id": {
                "text": "Nouveau test avec $faction",
                "category": "misc"
            }
        }
    }
    result = writer.write_json(updates, mock_strings_file, FileType.STRINGS)
    assert result.success

    # 3. Validation
    with open(mock_strings_file, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert "new_id" in parsed["strings"]
        assert "$faction" in parsed["strings"]["new_id"]["text"]

def test_workflow_tooltips(mock_tooltips_file):
    """Test le workflow complet pour tooltips.json."""
    # 1. Backup
    writer = JsonWriter()
    backup = writer.create_backup(mock_tooltips_file)
    assert backup.exists()

    # 2. Modification
    with open(mock_tooltips_file, "r", encoding="utf-8") as f:
        content = f.read()
        current_content, _ = parse_starsector_json(content)
    
    current_content["codex"]["new_damage"] = {
        "title": "Nouveau Test",
        "body": "Description avec $damage et $flux",
    }
    
    result = writer.write_json(current_content, mock_tooltips_file, FileType.TOOLTIPS)
    assert result.success

    # 3. Validation
    with open(mock_tooltips_file, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert "new_damage" in parsed["codex"]
        assert "$damage" in parsed["codex"]["new_damage"]["body"]
        assert "$flux" in parsed["codex"]["new_damage"]["body"]

def test_workflow_descriptions(mock_descriptions_file):
    """Test le workflow complet pour descriptions.json."""
    # 1. Backup
    writer = JsonWriter()
    backup = writer.create_backup(mock_descriptions_file)
    assert backup.exists()

    # 2. Modification
    with open(mock_descriptions_file, "r", encoding="utf-8") as f:
        content = f.read()
        current_content, _ = parse_starsector_json(content)
    
    current_content.append({
        "key": "descriptions.csv#('new_weapon', 'WEAPON')$text1",
        "original": "New weapon description with $damage",
        "translation": "Nouvelle description d'arme avec $damage",
        "stage": 1,
        "context": "New test context"
    })
    
    result = writer.write_json(current_content, mock_descriptions_file, FileType.DESCRIPTIONS)
    assert result.success

    # 3. Validation
    with open(mock_descriptions_file, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert len(parsed) == 2  # Original + nouveau
        assert any(item["key"] == "descriptions.csv#('new_weapon', 'WEAPON')$text1" for item in parsed)

def test_cross_format_variables():
    """Test la cohérence des variables système entre les formats."""
    validator = JsonValidator()
    
    # Test des variables communes
    variables = {
        "$faction": [FileType.STRINGS, FileType.TOOLTIPS, FileType.DESCRIPTIONS],
        "$market": [FileType.STRINGS, FileType.TIPS, FileType.DESCRIPTIONS],
        "$damage": [FileType.TOOLTIPS, FileType.DESCRIPTIONS],
        "$flux": [FileType.TOOLTIPS, FileType.DESCRIPTIONS]
    }
    
    for var, formats in variables.items():
        for fmt in formats:
            # Crée un contenu de test avec la variable
            if fmt == FileType.DESCRIPTIONS:
                test_content = [{
                    "key": "test_key",
                    "original": f"Test with {var}",
                    "translation": f"Test avec {var}",
                    "stage": 1,
                    "context": "Test"
                }]
            elif fmt == FileType.STRINGS:
                test_content = {
                    "strings": {
                        "test_id": {
                            "text": f"Test avec {var}",
                            "category": "misc"
                        }
                    }
                }
            elif fmt == FileType.TIPS:
                test_content = {
                    "tips": [
                        {
                            "id": "test_tip",
                            "tip": f"Test avec {var}",
                            "category": "GENERAL"
                        }
                    ]
                }
            else:  # TOOLTIPS
                test_content = {
                    "codex": {
                        "test_tooltip": {
                            "title": "Test",
                            "body": f"Test avec {var}"
                        }
                    }
                }
            
            formatted = format_starsector_json(test_content, fmt)
            parsed, error = parse_starsector_json(formatted)
            assert not error
            assert validator.validate_format(parsed, fmt).success

def test_compare_with_originals():
    """Test la compatibilité avec les fichiers originaux en anglais.

    Vérifie que les fichiers originaux peuvent être parsés par notre parser
    et que le round-trip (parse -> format -> reparse) est stable.

    NOTE: La validation de format (validate_format) n'est pas appliquée aux
    fichiers originaux car leur structure (Starsector natif) diffère du format
    attendu par nos validateurs internes (conçus pour les fichiers de traduction).
    """
    original_dir = Path("original/data/strings")

    files_to_test = ["strings.json", "tips.json", "tooltips.json"]

    for filename in files_to_test:
        file_path = original_dir / filename
        if file_path.exists():
            print(f"\nTest de {filename}...")

            # Lecture du fichier original
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse du format Starsector
            parsed, error = parse_starsector_json(content)
            assert not error, f"Erreur de parsing pour {filename}: {error}"
            assert parsed, f"Contenu vide après parsing pour {filename}"

            # Test de round-trip : format -> reparse
            formatted = format_starsector_json(parsed)
            reparsed, error = parse_starsector_json(formatted)
            assert not error, f"Erreur de reparse pour {filename}: {error}"
            assert reparsed == parsed, f"Différence après reformatage pour {filename}"

            print(f"{filename} parsé et round-trip validé avec succès")
        else:
            pytest.skip(f"Fichier original {filename} non trouvé dans {file_path}")
