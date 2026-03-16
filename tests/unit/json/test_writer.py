"""Tests unitaires pour le module JsonWriter."""

import pytest
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch

from scripts.handlers.json.writer import JsonWriter
from scripts.handlers.json.validator import JsonValidator
from scripts.handlers.json.models import ValidationResult
from scripts.starsector_json import FileType, parse_starsector_json, format_starsector_json


@pytest.fixture
def writer():
    """Fixture pour le JsonWriter."""
    return JsonWriter()

@pytest.fixture
def mock_file(tmp_path):
    """Fixture pour un fichier JSON temporaire."""
    file_path = tmp_path / "test.json"
    content = {
        "strings": {
            "test_id": {
                "text": "Test string with $faction",
                "category": "misc"
            }
        }
    }
    formatted = format_starsector_json(content, FileType.STRINGS)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(formatted)
    return file_path

@pytest.fixture
def mock_tips_content():
    """Fixture pour un contenu tips.json."""
    return [
        {
            "id": "tip1",
            "tip": "Test tip with $market",
            "category": "GENERAL"
        }
    ]

@pytest.fixture
def mock_strings_content():
    """Fixture pour un contenu strings.json."""
    return {
        "strings": {
            "test_id": {
                "text": "Test string with $faction",
                "category": "misc"
            }
        }
    }

@pytest.fixture
def mock_tooltips_content():
    """Fixture pour un contenu tooltips.json."""
    return {
        "codex": {
            "damage_kinetic": {
                "title": "Dégâts Cinétiques",
                "body": "Les dégâts cinétiques sont efficaces contre les boucliers, mais faibles contre l'armure.",
            },
            "damage_energy": {
                "title": "Dégâts Énergétiques",
                "body": "Les dégâts énergétiques sont également efficaces contre les boucliers et l'armure.",
            }
        },
        "warroom": {
            "pause": {
                "title": "Pause",
                "body": "Met le jeu en pause.",
            }
        }
    }

@pytest.fixture
def mock_descriptions_content():
    """Fixture pour un contenu descriptions.json."""
    return [
        {
            "key": "descriptions.csv#('test_item', 'CUSTOM')$text1",
            "original": "Test description with $market reference",
            "translation": "Description de test avec référence $market",
            "stage": 1,
            "context": "Version test"
        },
        {
            "key": "descriptions.csv#('test_weapon', 'WEAPON')$text1",
            "original": "A test weapon description.\nWith multiple lines.",
            "translation": "Une description d'arme de test.\nAvec plusieurs lignes.",
            "stage": 5,
            "context": "Test weapon"
        }
    ]

def test_create_backup(writer, mock_file):
    """Test de la création d'un backup."""
    backup_path = writer.create_backup(mock_file)
    assert backup_path.exists()
    assert backup_path.parent.name == "backups"
    assert mock_file.stem in backup_path.stem

def test_write_json_strings_success(writer, tmp_path):
    """Test d'écriture JSON réussie pour strings.json."""
    file_path = tmp_path / "strings.json"
    content = {
        "strings": {
            "test_id": {
                "text": "Test string with $faction",
                "category": "misc"
            }
        }
    }
    
    result = writer.write_json(content, file_path)
    
    assert result.success
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert parsed["strings"]["test_id"]["text"] == "Test string with $faction"

def test_write_json_tips_success(writer, tmp_path, mock_tips_content):
    """Test d'écriture JSON réussie pour tips.json."""
    file_path = tmp_path / "tips.json"
    
    result = writer.write_json({"tips": mock_tips_content}, file_path)
    
    assert result.success
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert parsed["tips"][0]["tip"] == "Test tip with $market"

def test_write_json_tooltips_success(writer, tmp_path, mock_tooltips_content):
    """Test d'écriture JSON réussie pour tooltips.json."""
    file_path = tmp_path / "tooltips.json"
    
    result = writer.write_json(mock_tooltips_content, file_path)
    
    assert result.success
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert parsed["codex"]["damage_kinetic"]["title"] == "Dégâts Cinétiques"
        assert "efficaces contre les boucliers" in parsed["codex"]["damage_kinetic"]["body"]
        assert parsed["warroom"]["pause"]["title"] == "Pause"

def test_write_json_descriptions_success(writer, tmp_path, mock_descriptions_content):
    """Test d'écriture JSON réussie pour descriptions.json."""
    file_path = tmp_path / "descriptions.json"
    
    result = writer.write_json(mock_descriptions_content, file_path)
    
    assert result.success
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert len(parsed) == 2
        assert parsed[0]["key"] == "descriptions.csv#('test_item', 'CUSTOM')$text1"
        assert parsed[0]["translation"] == "Description de test avec référence $market"
        assert parsed[1]["key"] == "descriptions.csv#('test_weapon', 'WEAPON')$text1"
        assert "plusieurs lignes" in parsed[1]["translation"]

def test_write_json_with_validation_failure(tmp_path):
    """Test d'écriture avec échec de validation."""
    mock_validator = Mock()
    mock_validator.validate_format.return_value = ValidationResult(
        success=False,
        format_type="starsector_json",
        message="Validation failed"
    )
    writer = JsonWriter(validator=mock_validator)
    
    result = writer.write_json({"invalid": "content"}, tmp_path / "test.json")
    
    assert not result.success
    assert "Validation failed" in result.message

def test_update_json_success(writer, mock_file, mock_strings_content):
    """Test de mise à jour JSON réussie."""
    updates = {
        "strings": {
            "new_id": {
                "text": "New string with $faction",
                "category": "misc"
            }
        }
    }
    
    result = writer.update_json(mock_file, updates)
    
    assert result.success
    with open(mock_file, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert "new_id" in parsed["strings"]
        assert parsed["strings"]["new_id"]["text"] == "New string with $faction"

def test_write_json_unicode(writer, tmp_path):
    """Test d'écriture avec caractères Unicode."""
    file_path = tmp_path / "unicode.json"
    content = {
        "strings": {
            "test_id": {
                "text": "Test avec caractères spéciaux : éèàù",
                "category": "misc"
            }
        }
    }
    
    result = writer.write_json(content, file_path)
    
    assert result.success
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        parsed, error = parse_starsector_json(content)
        assert not error
        assert "éèàù" in parsed["strings"]["test_id"]["text"]
