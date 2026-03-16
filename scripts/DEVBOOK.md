# Journal de Développement - Restructuration des Scripts

## 31/01/2025 - Plan de Restructuration

### Nouvelle Architecture

1. Core Components:
   - `rebuild_manager.py` : Gestionnaire principal de reconstruction
   - `format_spec.py` : Spécifications de format pour chaque type de fichier
   - `file_type.py` : Énumération des types de fichiers supportés

2. Handlers:
   - `json_handler.py` : Gestion spécifique des fichiers JSON
   - `csv_handler.py` : Gestion spécifique des fichiers CSV
   - `ini_handler.py` : Gestion spécifique des fichiers INI

3. Utils:
   - `format_utils.py` : Utilitaires de formatage (guillemets, espaces, etc.)
   - `path_utils.py` : Gestion des chemins et fichiers
   - `logging_utils.py` : Configuration des logs

4. Tests:
   - `test_rebuild.py` : Tests de reconstruction
   - `test_format.py` : Tests de formatage
   - `test_handlers.py` : Tests des handlers spécifiques

### Prochaines Étapes

1. Phase 1 - Mise en place de la structure
   - [x] Création du RebuildManager de base
   - [x] Implémentation du format JSON Starsector
   - [ ] Séparation des handlers par type de fichier
   - [ ] Création des utilitaires communs

2. Phase 2 - Migration des fonctionnalités
   - [ ] Migration des scripts existants vers la nouvelle structure
   - [ ] Adaptation des tests unitaires
   - [ ] Documentation des nouvelles interfaces

3. Phase 3 - Historique et Traductions
   - [ ] Conception du système d'historique des traductions
   - [ ] Implémentation de la sauvegarde/restauration
   - [ ] Tests de préservation des traductions

### Standards de Code

1. Format JSON Starsector:
   - Tabulation pour l'indentation
   - Pas d'espace après les deux points
   - Guillemets droits (")
   - Encodage UTF-8
   - Sauts de ligne Unix (\n)

2. Gestion des Erreurs:
   - Logging détaillé
   - Messages d'erreur explicites
   - Validation des entrées/sorties

3. Tests:
   - Tests unitaires pour chaque composant
   - Tests d'intégration pour les workflows complets
   - Validation du format Starsector

### Analyse de find_control_chars_binary

### Fonction actuelle
- Localisation : `utils.py`
- But : Détection des caractères de contrôle dans les fichiers
- Appelée par : `normalize_json_structure` pour :
  - Analyse initiale des fichiers
  - Diagnostic en cas d'erreur

### Format des logs
- Nom : `[nom_fichier].control_chars.log`
- Emplacement : Même dossier que le fichier analysé
- Contenu :
  1. En-tête avec le nom du fichier
  2. Position des caractères de contrôle (ligne, colonne)
  3. Contexte en hexadécimal et ASCII

### Points à vérifier
1. La fonction est-elle correctement appelée ?
2. Les logs sont-ils générés au bon endroit ?
3. Le format des logs est-il utile pour le diagnostic ?
4. La détection fonctionne-t-elle correctement ?

### Tests à effectuer
1. Test via normalize_json_structure
2. Vérification des logs générés
3. Validation du format des logs
4. Test avec différents types de fichiers

### Résultats des tests
[À remplir après les tests]

### Plan de Tests - find_control_chars_binary

### Tests Unitaires
1. **Test de Base**
   ```python
   def test_find_control_chars_basic():
       """Vérifie la détection basique des caractères de contrôle."""
       # Créer un fichier de test avec des caractères de contrôle connus
       # Vérifier que la fonction les détecte correctement
       # Vérifier le format du log généré
   ```

2. **Test des Chemins**
   ```python
   def test_find_control_chars_paths():
       """Vérifie la gestion des chemins de fichiers."""
       # Test avec chemin absolu
       # Test avec chemin relatif
       # Test avec caractères spéciaux dans le chemin
   ```

3. **Test d'Encodage**
   ```python
   def test_find_control_chars_encoding():
       """Vérifie la gestion des différents encodages."""
       # Test avec fichier UTF-8
       # Test avec caractères non-ASCII
   ```

4. **Test des Erreurs**
   ```python
   def test_find_control_chars_errors():
       """Vérifie la gestion des erreurs."""
       # Test avec fichier inexistant
       # Test avec fichier non lisible
       # Test avec fichier vide
   ```

### Tests d'Intégration
1. **Test avec normalize_json_structure**
   ```python
   def test_integration_normalize_json():
       """Vérifie l'intégration avec normalize_json_structure."""
       # Test du flux complet de normalisation
       # Vérifier les appels à find_control_chars_binary
       # Valider les logs générés
   ```

2. **Test de Migration**
   ```python
   def test_migration_compatibility():
       """Vérifie la compatibilité pendant la migration."""
       # Test des anciens chemins de logs
       # Test des nouveaux chemins de logs
       # Vérifier que les deux fonctionnent
   ```

### Fixtures Nécessaires
1. **Fichiers de Test**
   - fichier_normal.json (sans caractères de contrôle)
   - fichier_control.json (avec caractères de contrôle)
   - fichier_special.json (cas particuliers)

2. **Environnement de Test**
   - Dossier temporaire pour les logs
   - Backup des fichiers originaux
   - Configuration de test isolée

### Fixtures de Test Créées

#### 1. fichier_normal.json
- Fichier JSON valide sans caractères de contrôle
- Structure simple avec champs basiques
- Encodage UTF-8 standard

#### 2. fichier_control.json
- Contient des caractères de contrôle spécifiques :
  - \t (tabulation)
  - \n (nouvelle ligne)
  - \r\n (retour chariot)
  - \b (backspace)
  - \f (form feed)
- Utilisé pour tester la détection

#### 3. fichier_special.json
- Caractères spéciaux et non-ASCII en UTF-8
- Émojis (🚀✨🌟)
- Caractères accentués (éèêë)
- Caractères japonais (特殊テスト)

#### 4. fichier_vide.json
- Fichier totalement vide
- Utilisé pour tester la gestion des erreurs
- Cas limite important

#### 5. fichier_invalide.json
- Format Starsector non respecté :
  - Espace après les deux points (interdit)
  - Guillemets français (« ») au lieu de droits (")
  - Mauvaise indentation (doit être 4 espaces)
  - Apostrophe droite (') au lieu de courbe
  - Sauts de ligne Windows (\r\n) au lieu d'Unix (\n)
- Test des règles spécifiques au format Starsector

#### Notes d'Implémentation
- Tous les fichiers sont placés dans `tests/fixtures/`
- Encodage strictement en UTF-8
- Format JSON spécifique à Starsector :
  - Pas d'espace après les deux points
  - Guillemets droits uniquement
  - Indentation de 4 espaces exactement
  - Sauts de ligne style Unix
- Cas de test adaptés aux spécificités du jeu

### Validation des Logs
- Vérifier le format des logs
- Valider les informations de position
- Contrôler l'affichage du contexte
- Vérifier l'encodage des logs

### Métriques de Couverture
- Couverture de code > 90%
- Tous les chemins d'erreur testés
- Tous les formats de fichiers testés
- Tous les cas d'encodage testés

### Notes Importantes

- Ne pas modifier les fichiers originaux
- Préserver la structure exacte des fichiers
- Documenter tous les changements de format
- Maintenir la compatibilité avec les versions précédentes

### Problèmes Identifiés

### Conflit de Module utils
- **Date** : 2025-02-01
- **Statut** : ⚠️ SUSPECT
- **Description** : Conflit entre le fichier `utils.py` et le dossier `utils/`
  - Le fichier contient des fonctions importantes comme `find_control_chars_binary`
  - Le dossier `utils/` semble être un package Python
  - Les imports échouent à cause de cette ambiguïté
- **Impact** :
  - Les fonctions ne peuvent pas être importées correctement
  - Risque de comportement imprévisible
  - Bloque les tests des fonctionnalités
- **À investiguer** :
  1. Structure actuelle du package utils/
  2. Dépendances entre utils.py et utils/
  3. Historique des modifications
- **Note** : Ne pas modifier la structure avant une analyse complète

### Plan de Résolution - Conflit Module utils

### État Actuel
- Ancien système : `utils.py` (monolithique)
- Nouveau système : package `utils/` avec sous-modules spécialisés
  - format_utils.py
  - logging_utils.py
  - path_utils.py

### Risques Identifiés
1. Perte de fonctionnalités pendant la migration
2. Rupture des imports existants
3. Régression dans les scripts qui utilisent utils.py
4. Conflit de noms entre ancien et nouveau système

### Plan de Migration
1. **Phase 1 : Préparation**
   - ✓ Documenter la structure actuelle
   - ✓ Identifier les fonctions à migrer
   - □ Créer une liste de dépendances
   - □ Sauvegarder l'état actuel

2. **Phase 2 : Migration Progressive**
   - □ Migrer fonction par fonction :
     - □ Copier dans le nouveau module approprié
     - □ Tester la nouvelle implémentation
     - □ Maintenir l'ancienne version
   - □ Mettre à jour les imports dans utils/__init__.py
   - □ Créer des alias pour la compatibilité

3. **Phase 3 : Tests et Validation**
   - □ Tests unitaires pour chaque fonction migrée
   - □ Tests d'intégration
   - □ Validation des chemins de migration
   - □ Vérification des logs et diagnostics

4. **Phase 4 : Transition**
   - □ Déprécier progressivement utils.py
   - □ Mettre à jour la documentation
   - □ Former les utilisateurs aux nouveaux imports
   - □ Période de support double (ancien/nouveau)

### Points de Contrôle
- Chaque fonction migrée doit être testée individuellement
- Maintenir une liste des fonctions migrées/à migrer
- Documenter les changements d'API
- Conserver les tests de régression

### Règles de Migration
1. Ne pas supprimer de code sans validation
2. Toujours avoir une version fonctionnelle
3. Documenter chaque changement
4. Tester avant/après chaque migration
5. Prévoir un plan de rollback

### Notes Importantes
- La migration doit être transparente pour les utilisateurs
- Prévoir des messages de dépréciation clairs
- Maintenir la compatibilité ascendante
- Documenter les nouvelles pratiques recommandées

### Analyse des Dépendances - find_control_chars_binary

### Fonction Analysée
```python
def find_control_chars_binary(file_path)
```

### Dépendances
1. **Imports Système**
   - sys (pour stdout)
   - codecs (pour l'encodage)
   - Path (de pathlib)

2. **Dépendances Internes**
   - Appelée par normalize_json_structure :
     - Pour l'analyse initiale
     - Pour le diagnostic d'erreur
   - Pas d'autres dépendances internes

3. **Fichiers Générés**
   - [nom_fichier].control_chars.log
   - Créé dans le même dossier que le fichier analysé

4. **Points d'Intégration**
   - Entrée : Chemin du fichier à analyser
   - Sortie : Fichier log et affichage console
   - Utilisé comme outil de diagnostic

### Migration Proposée
1. **Destination** : utils/logging_utils.py
   - Cohérent avec la nouvelle structure
   - Regroupe les fonctions de diagnostic

2. **Modifications Nécessaires**
   - Déplacer la fonction
   - Adapter les imports
   - Centraliser les logs dans un dossier dédié
   - Maintenir la compatibilité avec normalize_json_structure

3. **Tests Requis**
   - Test unitaire de la fonction
   - Test d'intégration avec normalize_json_structure
   - Validation des logs générés

### Notes
- Fonction de diagnostic pure (pas de modification de fichiers)
- Peut être migrée sans risque majeur
- Garder une trace des anciens emplacements de logs

### Prochain Sprint

1. Créer les nouveaux fichiers de base:
   - Handlers séparés pour JSON/CSV/INI
   - Utilitaires de formatage
   - Tests unitaires

2. Migrer progressivement les fonctionnalités:
   - Un type de fichier à la fois
   - Tests complets avant/après
   - Documentation à jour

3. Préparer le système d'historique:
   - Conception de la structure de données
   - Format de sauvegarde
   - Mécanisme de restauration

### 2025-02-01 20:39 : Analyse de la documentation existante

#### 📚 Structure documentaire
1. Documentation des tests :
   - `scripts/tests/` : Structure de base en place
   - `fixtures/` : Jeu de données de test
   - Tests unitaires, intégration et performance

2. Documentation technique :
   - `FORMATS_JSON.md` : Spécifications des formats
   - `MEMOIRE_TECHNIQUE.md` : Architecture globale
   - `REFERENCE_ENCODAGE.md` : Standards d'encodage

3. Documentation de développement :
   - `scripts/DEVBOOK.md` : Journal spécifique aux scripts
   - `scripts/CONSOLIDATION.md` : Plan de restructuration
   - `docs/DEVBOOK_*.md` : Archives mensuelles

#### 🔄 Plan de consolidation révisé
1. Utiliser l'existant :
   - Conserver la structure `scripts/tests/`
   - Maintenir les fixtures actuelles
   - Suivre les standards documentés

2. Améliorations ciblées :
   - Organiser les tests par type
   - Enrichir les fixtures
   - Documenter les nouveaux tests

3. Documentation :
   - Mettre à jour `scripts/DEVBOOK.md`
   - Enrichir `CONSOLIDATION.md`
   - Maintenir les standards existants
