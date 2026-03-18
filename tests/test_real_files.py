import json
import logging
import re
import shutil
from pathlib import Path
import pytest
from scripts.handlers.json_handler import JsonHandler

@pytest.fixture
def json_handler():
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)
    return JsonHandler(logger)

def test_multiple_json_types(json_handler, tmp_path):
    """Test la conversion des guillemets sur différents types de fichiers JSON."""
    # Liste des fichiers à tester
    test_files = [
        "strings.json",  # Fichier de traduction
        "config/settings.json",  # Fichier de configuration
        "missions/afistfulofcredits/descriptor.json",  # Fichier de mission
        "campaign/econ/economy.json"  # Fichier d'économie
    ]

    base_dir = Path("d:/Fractal Softworks/Starsector/starsector-core/data")
    if not base_dir.exists():
        pytest.skip(f"Répertoire starsector-core non trouvé : {base_dir}")
    
    for source_file in test_files:
        # Crée un sous-dossier pour chaque type de test
        test_dir = tmp_path / Path(source_file).parent
        test_dir.mkdir(parents=True, exist_ok=True)
        test_file = tmp_path / source_file
        
        # Copie le fichier source
        if (base_dir / source_file).exists():
            shutil.copy2(base_dir / source_file, test_file)
            
            # Lit le contenu original
            with open(test_file, 'r', encoding='utf-8') as f:
                original_content = f.read()
                
            # Vérifie que le fichier a des virgules finales si c'est le cas dans l'original
            has_trailing_commas = bool(re.search(r',(\s*[}\]])', original_content))
            
            # Applique la conversion des guillemets
            assert json_handler.fix_quotes(test_file)
            
            # Lit le résultat
            with open(test_file, 'r', encoding='utf-8') as f:
                result_content = f.read()
            
            # Vérifie que les virgules finales sont préservées si elles existaient
            if has_trailing_commas:
                assert re.search(r',(\s*[}\]])', result_content), \
                    f"Les virgules finales doivent être préservées dans {source_file}"
            
            # Compare la structure (en ignorant les différences de guillemets)
            def normalize_for_comparison(text: str) -> str:
                """Normalise le texte pour la comparaison en préservant la structure."""
                # Remplace tous les types de guillemets par un marqueur unique
                text = re.sub(r'[«»""]', '"', text)
                # Normalise les espaces autour des guillemets
                text = re.sub(r'\s*"\s*', '"', text)
                return text
            
            # Vérifie que la structure est préservée
            normalized_original = normalize_for_comparison(original_content)
            normalized_result = normalize_for_comparison(result_content)
            assert normalized_original == normalized_result, \
                f"La structure du fichier doit être préservée dans {source_file}"
            
            # Vérifie que les guillemets sont correctement convertis
            def check_quotes(text: str):
                """Vérifie que les guillemets sont correctement convertis."""
                # Trouve toutes les chaînes entre guillemets
                strings = re.finditer(r':\s*"([^"\\]*(?:\\.[^"\\]*)*)"', text)
                for match in strings:
                    content = match.group(1)
                    if content:  # Ignore les chaînes vides
                        # Vérifie que les guillemets français sont utilisés et bien espacés
                        quote_pairs = re.finditer(r'«\s*(.*?)\s*»', content)
                        for pair in quote_pairs:
                            quote_content = pair.group(1)
                            # Vérifie les espaces autour des guillemets
                            assert pair.group(0).startswith('« '), \
                                f"Espace manquant après le guillemet ouvrant dans: {pair.group(0)}"
                            assert pair.group(0).endswith(' »'), \
                                f"Espace manquant avant le guillemet fermant dans: {pair.group(0)}"
            
            check_quotes(result_content)

def test_real_file_quotes(json_handler, tmp_path):
    """Test la conversion des guillemets sur un fichier réel."""
    # Copie le fichier de test
    source_file = Path("backups/strings_20250104/strings.json")
    if not source_file.exists():
        pytest.skip(f"Fichier de backup non trouvé : {source_file}")
    test_file = tmp_path / "test_strings.json"
    
    # Copie directe pour préserver le format exact
    shutil.copy2(source_file, test_file)
    
    # Lit le contenu original pour la comparaison
    with open(source_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
        # Vérifie que le fichier original a bien des virgules finales
        assert ',' in original_content and re.search(r',(\s*[}\]])', original_content), \
            "Le fichier original doit avoir des virgules finales"
    
    # Applique la conversion des guillemets
    assert json_handler.fix_quotes(test_file)
    
    # Lit le résultat
    with open(test_file, 'r', encoding='utf-8') as f:
        result_content = f.read()
        
    # Vérifie que les virgules finales sont préservées
    assert ',' in result_content and re.search(r',(\s*[}\]])', result_content), \
        "Les virgules finales doivent être préservées"
    
    # Compare la structure (en ignorant les différences de guillemets)
    def normalize_for_comparison(text: str) -> str:
        """Normalise le texte pour la comparaison en préservant la structure."""
        # Remplace tous les types de guillemets par un marqueur unique
        text = re.sub(r'[«»""]', '"', text)
        # Normalise les espaces autour des guillemets
        text = re.sub(r'\s*"\s*', '"', text)
        return text
    
    # Vérifie que la structure est préservée
    normalized_original = normalize_for_comparison(original_content)
    normalized_result = normalize_for_comparison(result_content)
    assert normalized_original == normalized_result, \
        "La structure du fichier doit être préservée"
    
    # Vérifie que les guillemets sont correctement convertis
    def check_quotes(text: str):
        """Vérifie que les guillemets sont correctement convertis."""
        # Trouve toutes les chaînes entre guillemets
        strings = re.finditer(r':\s*"([^"\\]*(?:\\.[^"\\]*)*)"', text)
        for match in strings:
            content = match.group(1)
            if content:  # Ignore les chaînes vides
                # Vérifie que les guillemets français sont utilisés et bien espacés
                quote_pairs = re.finditer(r'«\s*(.*?)\s*»', content)
                for pair in quote_pairs:
                    quote_content = pair.group(1)
                    # Vérifie les espaces autour des guillemets
                    assert pair.group(0).startswith('« '), \
                        f"Espace manquant après le guillemet ouvrant dans: {pair.group(0)}"
                    assert pair.group(0).endswith(' »'), \
                        f"Espace manquant avant le guillemet fermant dans: {pair.group(0)}"
    
    check_quotes(result_content)
