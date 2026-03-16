"""
Classes de données pour la gestion des fichiers JSON.

Ce module contient toutes les classes de données utilisées par les différents
composants du gestionnaire JSON (validator, converter, writer).
"""

from dataclasses import dataclass, field
from typing import Set, List, Dict, Any, Optional
from pathlib import Path


@dataclass
class ValidationResult:
    """Résultat de validation d'un fichier JSON."""
    success: bool
    format_type: str
    message: str = ""
    backup_path: Optional[Path] = None


@dataclass
class ComparisonResult:
    """Résultat de comparaison entre deux structures JSON."""
    valid_structure: bool
    identical: bool
    differences: List[str]


@dataclass
class VariableValidation:
    """Résultat de validation des variables système."""
    success: bool
    variables: Set[str]
    invalid_vars: Set[str]


@dataclass
class JsonFormat:
    """Définition d'un format JSON spécifique."""
    name: str
    required_fields: Set[str]
    optional_fields: Set[str] = field(default_factory=set)
    array_fields: Set[str] = field(default_factory=set)
    nested_fields: Dict[str, 'JsonFormat'] = field(default_factory=dict)


# Formats JSON connus
TIPS_FORMAT = JsonFormat(
    name="tips",
    required_fields={"title", "text"},
    optional_fields={"tags"}
)

TOOLTIPS_FORMAT = JsonFormat(
    name="tooltips",
    required_fields={"id", "text"},
    optional_fields={"context"}
)

STRINGS_FORMAT = JsonFormat(
    name="strings",
    required_fields={"id", "text"},
    optional_fields={"description", "notes"}
)

# Variables système connues
SYSTEM_VARIABLES = {
    "$faction", "$fleetOrShip", "$playerName",
    "$shipName", "$systemName", "$planetName",
    "$location", "$market", "$commodityName",
    "$manOrWoman", "$hisOrHer", "$heOrShe"
}
