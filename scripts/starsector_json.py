"""
Re-export du module starsector_json depuis scripts.handlers.starsector_json.

Ce shim permet les imports de la forme `from scripts.starsector_json import ...`
qui sont utilisés dans les tests et d'autres modules.
"""

from scripts.handlers.starsector_json import (
    FileType,
    StructureMap,
    StarsectorJsonAnalyzer,
    format_starsector_json,
    parse_starsector_json,
    detect_file_type,
    init_analyzer,
)

__all__ = [
    'FileType',
    'StructureMap',
    'StarsectorJsonAnalyzer',
    'format_starsector_json',
    'parse_starsector_json',
    'detect_file_type',
    'init_analyzer',
]
