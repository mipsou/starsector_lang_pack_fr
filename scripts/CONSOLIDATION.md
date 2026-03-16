# Plan de Consolidation des Scripts

## Structure Finale (12 fichiers)

### Core (3 fichiers)
1. `rebuild_manager.py` - Gestionnaire principal
   - Point d'entrée unique pour la reconstruction
   - Orchestration des handlers
   - Gestion des erreurs centralisée
   - Migration depuis : rebuild.py, rebuild_manager.py

2. `translation_manager.py` - Gestion des traductions
   - Interface unifiée pour toutes les traductions
   - Support multi-format (JSON, CSV, INI)
   - Préservation des traductions existantes
   - Migration depuis : translate.py, translate_strings.py, translate_tips.py, process_descriptions.py

3. `validation_manager.py` - Validation globale
   - Validation structurelle et linguistique
   - Vérification de cohérence
   - Rapports d'erreurs détaillés
   - Migration depuis : validate_translations.py, validate_french.py, validate_json.py

### Handlers (3 fichiers)
4. `handlers/json_handler.py` - Gestion JSON
   - Format JSON Starsector spécifique
   - Analyse et validation de structure
   - Support des différents types (strings, tips, tooltips)
   - Migration depuis : fix_starsector_json.py, json_utils.py, starsector_json.py

5. `handlers/string_handler.py` - Gestion des chaînes
   - Règles typographiques françaises
   - Normalisation des termes techniques
   - Gestion des variables système
   - Migration depuis : fix_strings.py, format_tips.py, fix_typography.py

6. `handlers/file_handler.py` - Gestion des fichiers
   - Gestion unifiée des encodages
   - Opérations sur les fichiers
   - Validation des chemins
   - Migration depuis : fix_encoding.py, fix_encoding_new.py, analyze_encoding.py

### Utils (3 fichiers)
7. `utils/format_utils.py` - Utilitaires de formatage
   - Fonctions de formatage communes
   - Normalisation des chaînes
   - Règles typographiques
   - Migration depuis : utils.py, fix_typography.py

8. `utils/path_utils.py` - Gestion des chemins
   - Configuration des chemins
   - Validation des accès
   - Gestion des backups
   - Nouveau fichier centralisé

9. `utils/logging_utils.py` - Logging
   - Configuration des logs
   - Niveaux de verbosité
   - Rotation des fichiers
   - Nouveau fichier centralisé

### Tests (3 fichiers)
10. `tests/test_rebuild.py` - Tests de reconstruction
    - Tests unitaires de reconstruction
    - Tests d'intégration
    - Validation de format
    - Migration depuis : test_rebuild.py, test_integration.py

11. `tests/test_translation.py` - Tests de traduction
    - Validation des traductions
    - Tests de cohérence
    - Vérification linguistique
    - Migration depuis : test_fix_translation.py, test_validate_translations.py

12. `tests/test_format.py` - Tests de formatage
    - Tests des formats de fichiers
    - Validation d'encodage
    - Tests typographiques
    - Migration depuis : test_fix_strings.py, autres tests de format

## Plan de Migration

### Phase 1 : Infrastructure (3h)
1. Création de la nouvelle structure de répertoires
2. Mise en place du système de logging
3. Configuration des chemins
4. Tests de base

### Phase 2 : Handlers (3h)
1. Migration du JSON Handler
2. Migration du String Handler
3. Création du File Handler
4. Tests des handlers

### Phase 3 : Managers (2h)
1. Rebuild Manager
2. Translation Manager
3. Validation Manager
4. Tests d'intégration

### Phase 4 : Utils et Tests (1h)
1. Migration des utilitaires
2. Consolidation des tests
3. Documentation
4. Nettoyage final

## Standards de Code

### Documentation
- Docstrings complets pour chaque classe/méthode
- Exemples d'utilisation
- Types annotés (Python type hints)
- Commentaires explicatifs pour la logique complexe

### Tests
- Coverage minimum de 80%
- Tests unitaires pour chaque composant
- Tests d'intégration pour les workflows
- Tests de régression

### Logging
- Niveaux appropriés (DEBUG, INFO, WARNING, ERROR)
- Messages explicites
- Contexte suffisant
- Rotation des logs

### Gestion des Erreurs
- Exceptions personnalisées
- Messages d'erreur clairs
- Stack traces pertinentes
- Récupération gracieuse

## Suivi des Progrès
- [x] Analyse initiale
- [x] Plan de consolidation
- [ ] Phase 1 : Infrastructure
- [ ] Phase 2 : Handlers
- [ ] Phase 3 : Managers
- [ ] Phase 4 : Utils et Tests
