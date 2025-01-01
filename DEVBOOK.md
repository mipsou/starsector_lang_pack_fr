# Guide de Développement - Starsector Language Pack FR

## Environnement de Développement

### Structure des Dossiers
starsector_lang_pack_fr/
├── mod_info.json......# Configuration du mod
└── localization/......# Fichiers de localisation
    ├── data/.........# Données du jeu
    │   ├── config/...# Fichiers de configuration
    │   └── strings/..# Fichiers de traduction
    └── graphics/.....# Ressources graphiques
        └── ui/......# Interface utilisateur

### Outils Nécessaires
- Éditeur de texte avec support UTF-8
- Git pour le versioning
- Python pour les scripts d'automatisation
- Starsector pour les tests

## Processus de Développement

### 1. Configuration Initiale
1. Cloner le repository
2. Installer les dépendances Python
3. Configurer l'environnement de développement

### 2. Workflow de Traduction
1. Identifier les fichiers à traduire
2. Créer les fichiers _fr correspondants
3. Traduire le contenu
4. Tester en jeu
5. Valider et commiter

### 3. Tests
- Vérifier l'encodage des fichiers
- Tester les caractères spéciaux
- Vérifier l'intégration en jeu
- Valider les performances

## Standards de Code

### Fichiers de Traduction
- Format CSV :
  ```csv
  id,text
  ship_name,"Nom du vaisseau"
  ```
- Format JSON :
  ```json
  {
    "key": "valeur traduite"
  }
  ```

### Conventions de Nommage
- Fichiers : `nom_original_fr.extension`
- Variables : camelCase
- Constantes : UPPER_CASE

## Git Workflow

### Structure des Branches

### Configuration
- Branche par défaut : `dev`
- Branche de production : `main`

### Workflow
1. Développement sur `dev` (branche par défaut)
2. Création de branches feature/fix depuis `dev`
3. Pull Requests vers `dev`
4. Une fois stable, merge vers `main` via PR

### Protection des Branches

#### `main` (production)
- ✓ Protection maximale
- ✓ Pull requests obligatoires
- ✓ Reviews requises
- ✓ Status checks obligatoires
- ✓ Maintainers en bypass

#### `dev` (développement)
- ✓ Branche par défaut
- ✓ Protection modérée
- ✓ Status checks
- ✓ Up-to-date requis
- ✓ Maintainers en bypass

### Branches
- `main` : Production stable
- `dev` : Développement en cours
- `feature/*` : Nouvelles fonctionnalités
- `fix/*` : Corrections de bugs
- `docs/*` : Documentation

### Process de développement
1. Créer une branche depuis `dev` :
   ```bash
   git checkout -b feature/ma-fonctionnalite dev
   ```

2. Développer et commiter les changements :
   ```bash
   git add .
   git commit -m "feat: description du changement"
   ```

3. Pousser la branche :
   ```bash
   git push origin feature/ma-fonctionnalite
   ```

4. Créer une Pull Request vers `dev`
5. Review et merge dans `dev`
6. Une fois stable, merger `dev` dans `main`

### Conventions de Commit
- `feat:` Nouvelle fonctionnalité
- `fix:` Correction de bug
- `docs:` Documentation
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

### Protection des Branches
- `main` : Push direct interdit, PR requise
- `dev` : Push direct autorisé pour les maintainers

## Rôles et Permissions

### Rôles GitHub
- **Admin** : Accès complet à tous les aspects du projet
- **Maintainer** : Gestion du code et des branches
- **Contributor** : Peut soumettre des PR

### Permissions par Branche

#### Repo Public (starsector_lang_pack_fr)
- `main` :
  - ✓ Protection maximale
  - ✓ PR obligatoire
  - ✓ Review requise
  - ✓ Status checks
  - ✓ Maintainers en bypass

- `dev` :
  - ✓ Protection modérée
  - ✓ Status checks
  - ✓ Up-to-date requis
  - ✓ Maintainers en bypass

#### Repo Privé (starsector_lang_pack_fr_private)
- `main` :
  - ✓ Protection maximale
  - ✓ PR obligatoire
  - ✓ Review requise
  - ✓ Status checks
  - ✓ Maintainers en bypass

- `dev` :
  - ✓ Protection modérée
  - ✓ Status checks
  - ✓ Up-to-date requis
  - ✓ Maintainers en bypass

### Process de Contribution
1. Fork du repo public
2. Créer une branche feature/fix
3. Développer et tester
4. Soumettre une PR vers `dev`
5. Review par un maintainer
6. Merge dans `dev`
7. Une fois stable, merge dans `main`

## Scripts d'Automatisation

### convert_csv_to_json.py
```python
# Convertit les fichiers CSV en JSON
# Usage : python convert_csv_to_json.py input.csv output.json
```

### validate_translations.py
```python
# Vérifie la validité des traductions
# Usage : python validate_translations.py dir_path
```

## Outils de Développement

### Forum Scraper
Un outil pour extraire la documentation du forum officiel.

#### Installation
```bash
cd tools
pip install -r requirements.txt
python forum_scraper.py
```

#### Fonctionnalités
- Extraction automatique des guides officiels
- Conversion en format Markdown
- Sauvegarde locale dans /docs/forum
- Respect des délais entre requêtes
- Nettoyage du HTML en Markdown propre

#### Guides Extraits
- Mod Descriptor (mod_info.json)
- Rule Scripting
- Style Guide
- Publishing Guide
- Eclipse Guide
- Modding Guide Part 2

## Gestion des Ressources

### Fichiers Graphiques
- Formats supportés : PNG, JPG
- Résolution identique aux originaux
- Nommage cohérent avec le jeu

### Fichiers de Configuration
- Toujours en UTF-8
- Structure JSON valide
- Documentation des changements

## Débogage

### Logs
- Activer les logs de développement
- Vérifier starsector.log
- Utiliser les outils de debug du jeu

### Problèmes Courants
1. Encodage incorrect
   - Solution : Vérifier UTF-8 avec/sans BOM
2. Fichiers manquants
   - Solution : Vérifier la structure
3. Erreurs de syntaxe
   - Solution : Valider JSON/CSV

## Optimisation

### Performance
- Minimiser la taille des fichiers
- Éviter les duplications
- Structurer efficacement

### Maintenance
- Documenter les changements
- Suivre les versions du jeu
- Maintenir la cohérence

## Versioning

### Git
- Une branche par fonctionnalité
- Commits atomiques
- Messages descriptifs

### Releases
- Semantic Versioning
- Notes de version détaillées
- Tests complets

## Documentation

### Commentaires
```python
# TODO: Format standard
# FIXME: Pour les bugs
# NOTE: Informations importantes
```

### Markdown
- README.md : Vue d'ensemble
- CDC.md : Spécifications
- CHANGELOG.md : Modifications
- devbook.md : Guide technique

## Ressources

### Liens Utiles
- [Documentation Starsector](http://fractalsoftworks.com/docs)
- [Wiki Modding](http://starsector.wikia.com/wiki/Modding)
- [Forum Officiel](http://fractalsoftworks.com/forum)

### Références
- Mod chinois : Structure et organisation
- Autres mods de traduction
- Documentation officielle

## Ressources Essentielles

### Forums Officiels
- [Forum Modding Starsector](https://fractalsoftworks.com/forum/index.php?board=10.0)
  - Annonces officielles
  - Discussions techniques
  - Support et aide
  - Exemples de mods
  - Meilleures pratiques de la communauté

### Documentation Officielle
- [Guide de Modding Officiel](https://fractalsoftworks.com/forum/index.php?topic=4760.0)
  - **LECTURE OBLIGATOIRE** pour tout développement de mod
  - Couvre les bases et concepts avancés
  - Référence pour la structure des mods
  - Explique le système de chargement des mods

### Points Clés du Guide Officiel
1. **Structure de Base**
   - Dossier du mod dans `Starsector/mods/`
   - `mod_info.json` requis
   - Organisation des ressources

2. **Système de Chargement**
   - Ordre de chargement des mods
   - Gestion des conflits
   - Remplacement de fichiers

3. **Bonnes Pratiques**
   - Tests de compatibilité
   - Gestion des dépendances
   - Documentation du mod

4. **Débogage**
   - Logs du jeu
   - Messages d'erreur communs
   - Solutions aux problèmes fréquents

### Autres Ressources
- Forum Starsector
- Wiki de Modding
- Communauté Discord

## Lectures Obligatoires

### Guides Fondamentaux
1. [Introduction au Modding](https://fractalsoftworks.com/forum/index.php?topic=4760.0)
   - Guide de base pour commencer
   - Structure des mods
   - Concepts fondamentaux

2. [Tutoriel de Modding - Part 1](https://fractalsoftworks.com/forum/index.php?topic=4761.0)
   - Création de votre premier mod
   - Exemples pratiques
   - Bonnes pratiques de base

3. [Modding avec IntelliJ IDEA](https://fractalsoftworks.com/forum/index.php?topic=8355.0)
   - Configuration de l'IDE
   - Outils de développement
   - Débogage avancé

4. [Guide de Style pour les Mods](https://fractalsoftworks.com/forum/index.php?topic=7164.0)
   - Standards de codage
   - Conventions de nommage
   - Meilleures pratiques

5. [Guide de Publication des Mods](https://fractalsoftworks.com/forum/index.php?topic=15244.0)
   - Préparation des releases
   - Documentation requise
   - Processus de publication

6. [Modding avec Eclipse](https://fractalsoftworks.com/forum/index.php?topic=6926.0)
   - Configuration alternative d'IDE
   - Outils spécifiques à Eclipse
   - Workflow de développement

7. [Tutoriel de Modding - Part 2](https://fractalsoftworks.com/forum/index.php?topic=5016.0)
   - Concepts avancés
   - Techniques spécialisées
   - Cas d'utilisation complexes

### Processus d'Apprentissage
1. Lire tous les guides dans l'ordre
2. Prendre des notes sur chaque guide
3. Tester les exemples fournis
4. Consulter régulièrement pour référence

### Points d'Attention Particuliers
- Conventions de nommage
- Structure des fichiers
- Gestion des dépendances
- Tests et validation
- Documentation

## Rapports de Progression

### 30 Décembre 2024 - 01:36
- Configuration initiale du projet
- Mise en place de la structure du mod
- Configuration de git avec branches main/dev
- Documentation des commandes autorisées pour Windsurf
- Préparation de l'environnement pour la lecture des guides officiels

### 30 Décembre 2024 - 01:37
- Tentative de lecture du guide mod_info.json
- Problème : Le forum nécessite une authentification
- Solution à explorer : Trouver une autre méthode pour accéder à la documentation
- Prochaine étape : Vérifier les fichiers locaux pour la documentation

### 30 Décembre 2024 - 01:39
- Début de la lecture systématique des guides
- Lecture du guide mod_info.json
- Extraction des informations essentielles sur la structure des mods
- Documentation des champs requis et optionnels pour mod_info.json

### 30 Décembre 2024 - 01:40
- Lecture du guide sur le Rule Scripting
- Documentation disponible en PDF et RTF :
  - https://s3.amazonaws.com/fractalsoftworks/doc/StarsectorRuleScripting.pdf
  - https://s3.amazonaws.com/fractalsoftworks/doc/StarsectorRuleScripting.rtf
- Note : La documentation des commandes est incomplète, référence au code source pour plus de détails

### 30 Décembre 2024 - 02:21
- Création et implémentation du Forum Scraper
- Installation des dépendances Python
- Extraction réussie des guides du forum
- Documentation stockée dans /docs/forum

### 30 Décembre 2024 - 02:26
- Ajout du téléchargement des documents S3
- Téléchargement réussi de :
  - StarsectorRuleScripting.pdf
  - StarsectorRuleScripting.rtf
- Documents stockés dans /docs/s3

### 30 Décembre 2024 - 02:30
- ✅ Test de lancement du jeu avec le mod activé : Succès
- Confirmation de la compatibilité du mod_info.json
- Prêt pour commencer les traductions

### 30 Décembre 2024 - 02:31
- Conversion du fichier RTF en Markdown
- Création de `rtf_to_md.py` avec les fonctionnalités :
  - Nettoyage et formatage du texte
  - Détection automatique des sections
  - Amélioration du formatage des listes
  - Ajout d'un en-tête avec métadonnées
- Documentation disponible dans `/docs/markdown/StarsectorRuleScripting.md`

### 30 Décembre 2024 - 02:35
- Amélioration du script de conversion RTF vers Markdown :
  - Meilleur formatage des titres (H2 et H3)
  - Variables en code inline avec backticks
  - Formatage des exemples en blocs de code
  - Ajout d'une note de contribution
  - Meilleure gestion des listes
  - Espacement amélioré entre les sections

### 30 Décembre 2024 - 07:35 - 07:49 (14 minutes)
- Correction des badges de progression dans le README
  - Remplacement de progress-bar.dev par shields.io
  - Amélioration du style visuel (flat-square, couleurs)
  - Synchronisation entre les dépôts public et privé
- Temps de développement total : 24h14m

### 30 Décembre 2024 - 07:50 - 08:05 (15 minutes)
- Planification du travail sur les images UI
  - Alignement des commentaires dans la structure
  - Plan de remplacement des images UI
  - Identification des images à traiter par IA
- Temps de développement total : 24h29m

### 30 Décembre 2024 - 08:05 - 08:08 (3 minutes)
- Amélioration de la lisibilité de la structure
  - Utilisation de points pour l'alignement visuel
  - Meilleure représentation des espaces
  - Documentation de la convention
- Temps de développement total : 24h32m

### 30 Décembre 2024 - 08:35 - 08:37 (2 minutes)
- Documentation des bonnes pratiques pour les commandes
  - Ajout de la note sur PowerShell
  - Exemple de gestion des chemins avec espaces
  - Mise en garde sur cmd.exe
- Temps de développement total : 24h34m

### Automatisation des Captures d'Écran

#### Configuration de Chrome Headless
```powershell
# Installation des dépendances
pip install selenium
pip install webdriver_manager

# Script Python pour la capture
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def setup_chrome_headless():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def capture_screenshot(url, output_path):
    driver = setup_chrome_headless()
    driver.get(url)
    driver.save_screenshot(output_path)
    driver.quit()
```

#### Utilisation
```python
# Exemple de capture
capture_screenshot(
    "file:///D:/Fractal%20Softworks/Starsector/mods/starsector_lang_pack_fr/README.md",
    "screenshots/readme.png"
)
```

### 30 Décembre 2024
#### 08:56 - 09:00 (4 minutes)
- Recherche sur Chrome Headless
  - Configuration pour les captures d'écran
  - Script d'automatisation Python
  - Documentation de l'installation
- Temps de développement total : 24h38m

### Automatisation des Captures d'Écran

#### Configuration de Selenium Python
```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--hide-scrollbars")
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_for_element(driver, selector, timeout=10):
    """Attend qu'un élément soit visible"""
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, selector))
    )

def capture_element(driver, element, output_path):
    """Capture un élément spécifique"""
    element.screenshot(output_path)

def capture_full_page(driver, url, output_path):
    """Capture une page entière avec défilement"""
    driver.get(url)
    
    # Obtenir la hauteur totale de la page
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    
    # Attendre le chargement complet
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.execute_script("window.scrollTo(0, 0);")
    
    driver.save_screenshot(output_path)

# Exemple d'utilisation avancée
def process_ui_elements():
    driver = setup_driver()
    try:
        # Charger la page
        driver.get("file:///path/to/ui.html")
        
        # Attendre un élément spécifique
        menu = wait_for_element(driver, "#main-menu")
        
        # Capturer le menu
        capture_element(driver, menu, "menu.png")
        
        # Faire défiler jusqu'à un élément
        footer = driver.find_element(By.CSS_SELECTOR, "footer")
        ActionChains(driver).move_to_element(footer).perform()
        
        # Capturer la page entière
        capture_full_page(driver, driver.current_url, "full_page.png")
        
    finally:
        driver.quit()
```

#### Fonctionnalités Avancées
- Attente des éléments
- Capture d'éléments spécifiques
- Défilement automatique
- Gestion des interactions
- Capture de page complète

### 30 Décembre 2024
#### 09:00 - 09:05 (5 minutes)
- Documentation de Selenium Python
  - Fonctions avancées de capture
  - Gestion des éléments web
  - Exemples d'utilisation
- Temps de développement total : 24h43m

### Authentification et Accès
#### 3. Configuration de l'Accès
```bash
# Nettoyage des configurations précédentes (optionnel)
podman logout registry.redhat.io

# Connexion avec les nouveaux identifiants
podman login registry.redhat.io
# Saisir les informations d'authentification
```

#### 4. Vérification de l'Accès
```bash
# Test de la connexion
podman login --get-login registry.redhat.io

# Test d'accès au registre
podman pull registry.redhat.io/ubi9/ubi-minimal
```

#### 5. Sécurisation
```bash
# Vérification des fichiers d'authentification
ls -la ~/.config/containers/auth.json

# Sauvegarde sécurisée
cp ~/.config/containers/auth.json ~/.config/containers/auth.json.backup
chmod 600 ~/.config/containers/auth.json*
```

#### Notes de Sécurité Importantes
- Protéger les fichiers d'authentification (permissions 600)
- Ne jamais partager les fichiers de configuration
- Utiliser des variables d'environnement pour CI/CD
- Effectuer des sauvegardes sécurisées
- Renouveler régulièrement les identifiants
- Utiliser des droits d'accès minimaux

### 1er Janvier 2025 - 08:48
#### Configuration des Remotes

##### Repo Privé (Source Principale)
```bash
# starsector_lang_pack_fr_private
origin    → github.com:mipsou/starsector_lang_pack_fr_private.git    # Source principale
downstream → github.com:mipsou/starsector_lang_pack_fr.git           # Miroir public
```

##### Repo Public (Miroir)
```bash
# starsector_lang_pack_fr
origin   → github.com:mipsou/starsector_lang_pack_fr.git         # Miroir local
upstream → github.com:mipsou/starsector_lang_pack_fr_private.git # Source principale
```

##### Workflow
1. Développement
   ```bash
   # Dans le repo privé (starsector_lang_pack_fr_private)
   git push origin dev    # Pousse vers le repo privé
   git push downstream dev # Synchronise avec le miroir public
   ```

2. Production
   ```bash
   # Dans le repo privé (starsector_lang_pack_fr_private)
   git push origin main    # Pousse vers le repo privé
   git push downstream main # Synchronise avec le miroir public
   ```

3. Mise à jour du miroir
   ```bash
   # Dans le repo public (starsector_lang_pack_fr)
   git pull upstream dev  # Récupère les changements de dev
   git pull upstream main # Récupère les changements de main
   

```

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   ```

2. Validation
   - Review complète du code
   - Tests de sécurité
   - Vérification des données sensibles

3. Publication
   ```bash
   # Dans le repo public
   git checkout -b release/vX.Y.Z
   # Copier les fichiers nettoyés
   git add .
   git commit -m "release: version X.Y.Z"
   git tag vX.Y.Z
   git push origin main --tags
   ```

##### Sécurité
- ✓ Repos complètement séparés
- ✓ Pas de synchronisation automatique
- ✓ Release manuelle uniquement
- ✓ Validation requise avant publication
- ✓ Nettoyage des données sensibles

### 1er Janvier 2025 - 08:53
#### Séparation des Repositories

##### Repo Privé (Développement)
```bash
# starsector_lang_pack_fr_private
origin → github.com:mipsou/starsector_lang_pack_fr_private.git
```
- Contient tout le code source
- Contient les données sensibles
- Développement actif
- Accès restreint

##### Repo Public (Distribution)
```bash
# starsector_lang_pack_fr
origin → github.com:mipsou/starsector_lang_pack_fr.git
```
- Version publique du mod
- Pas de données sensibles
- Releases uniquement
- Accès public

##### Process de Release
1. Préparation
   ```bash
   # Dans le repo privé
   git checkout -b release/vX.Y.Z
   # Nettoyer les données sensibles
   # Mettre à jour la version
   # Mettre à jour le changelog
   
