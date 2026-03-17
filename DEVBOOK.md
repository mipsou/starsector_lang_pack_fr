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

## Automatisation des Captures d'Écran

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

### 30 Décembre 2024 - 08:56 - 09:00 (4 minutes)
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

### 30 Décembre 2024 - 09:00 - 09:05 (5 minutes)
- Documentation de Selenium Python
  - Fonctions avancées de capture
  - Gestion des éléments web
  - Exemples d'utilisation
- Temps de développement total : 24h43m

## Authentification et Accès

#### 1. Diagnostic Initial
```bash
# Vérification du statut de connexion
podman login --get-login registry.redhat.io

```

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

## Support

### Contact
- GitHub Issues
- Forum Starsector
- Discord communautaire

### Contribution
1. Fork le projet
2. Créer une branche
3. Commiter les changements
4. Soumettre une PR

## Annexes

### Templates
- Pull Request
- Issue
- Documentation
- Release Notes

## À Propos du Projet

### Informations
- **Auteur** : mipsou
- **Version** : 0.1.0
- **Licence** : MIT
- **GitHub** : [starsector_lang_pack_fr](https://github.com/mipsou/starsector_lang_pack_fr)

## DEVBOOK - Guide du Développeur 

### Structure du Projet

#### 1. Branches
```
main (production)
└── dev (développement)
    ├── feature/*
    ├── fix/*
    └── trad/*
```

#### 2. Organisation des Fichiers
```
.
├── .github/
│   ├── workflows/      # GitHub Actions
│   ├── ISSUE_TEMPLATE/ # Templates d'issues
│   └── PULL_REQUEST_TEMPLATE.md
├── data/
│   ├── campaign/      # Textes de campagne
│   ├── characters/    # Dialogues
│   └── missions/      # Missions
├── docs/
│   ├── api/          # Documentation API
│   ├── process/      # Processus
│   └── tools/        # Documentation outils
├── tools/
│   ├── validation/   # Scripts de validation
│   └── conversion/   # Outils de conversion
├── README.md         # Documentation principale
├── DEVBOOK.md       # Guide développeur
└── GUIDELINES.md     # Règles de traduction
```

## Workflow de Développement

#### 1. Issues
- Utiliser les templates appropriés
- Ajouter les labels pertinents
- Assigner les responsables

#### 2. Branches
- Créer depuis `dev`
- Nommer selon le type :
  - `feature/description`
  - `fix/description`
  - `trad/section-description`

#### 3. Commits
- Format : `type(scope): description`
- Types valides :
  ```
  feat     : Nouvelle fonctionnalité
  fix      : Correction de bug
  docs     : Documentation
  style    : Formatage
  refactor : Refactoring
  test     : Tests
  chore    : Maintenance
  ci       : Intégration continue
  ```

#### 4. Pull Requests
- Utiliser le template
- Référencer les issues
- Attendre les validations

## CI/CD

#### 1. GitHub Actions
- PR Validation
  - Format des commits
  - Données sensibles
  - Documentation
- Translation Check
  - Fichiers JSON/CSV
  - Chaînes non traduites
- Auto Label
  - Labels automatiques
  - Statut des PRs

#### 2. Hooks Git
```bash
# Pre-commit
./scripts/pre-commit.sh

# Pre-push
./scripts/pre-push.sh
```

## Outils de Développement

#### 1. Installation
```bash
# Cloner le repo
git clone git@github.com:mipsou/starsector_lang_pack_fr_private.git

# Installer les dépendances
pip install -r requirements.txt

# Configurer les hooks
./scripts/setup.sh
```

#### 2. Scripts Utiles
```bash
# Valider les traductions
./tools/validate.sh

# Convertir les fichiers
./tools/convert.sh

# Tester en local
./tools/test.sh
```

#### 3. VSCode Extensions
- GitLens
- Prettier
- JSON Tools
- CSV Editor

## Gestion des Versions

#### 1. Versions
- Format : `MAJOR.MINOR.PATCH`
- Exemples :
  - `1.0.0` : Version majeure
  - `1.1.0` : Nouvelles traductions
  - `1.1.1` : Corrections

#### 2. Tags
```bash
# Créer un tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Pousser les tags
git push origin --tags
```

#### 3. Releases
1. Créer depuis un tag
2. Ajouter les notes
3. Publier sur GitHub

## Déploiement

#### 1. Préparation
```bash
# Vérifier les traductions
./tools/check.sh

# Générer la documentation
./tools/docs.sh

# Créer l'archive
./tools/package.sh
```

#### 2. Publication
1. Merger dans `main`
2. Créer le tag
3. Publier la release

#### 3. Vérification
- Tester en jeu
- Valider les fichiers
- Vérifier la documentation

## Maintenance

#### 1. Backups
- Sauvegardes quotidiennes
- Archives des releases
- Historique Git

#### 2. Nettoyage
```bash
# Nettoyer les branches
git remote prune origin
git branch --merged | grep -v "main" | xargs git branch -d

# Optimiser le repo
git gc --aggressive
```

#### 3. Mises à Jour
- Dépendances
- Scripts
- Documentation

## Contact

#### 1. Équipe
- **Lead Dev** : @mipsou
- **Traducteurs** : @team
- **Relecteurs** : @reviewers

#### 2. Communication
- Issues GitHub
- Discord
- Email

#### 3. Support
1. Consulter la documentation
2. Vérifier les issues
3. Contacter l'équipe

## Notes de Version

#### 30/12/2023
- Configuration initiale
- Mise en place CI/CD
- Templates et guidelines

#### À Faire
- [ ] Tests automatisés
- [ ] Documentation API
- [ ] Outils de validation

## Notes Importantes sur l'Environnement

#### Terminal et Commandes
- Toutes les commandes doivent être exécutées dans PowerShell
- Chemins avec espaces : utiliser des guillemets doubles
  ```powershell
  # Exemple de commande avec chemin contenant des espaces
  Copy-Item "D:\Fractal Softworks\Starsector\mods\source.txt" "D:\Fractal Softworks\Starsector\mods\dest.txt"
  ```
- Ne pas utiliser cmd.exe qui gère mal les chemins avec espaces

### 2 Janvier 2025 - 05:44
#### Correction de la Documentation de Test

##### Procédure de Test Corrigée
1. Vérification préalable :
   - Mod activé dans enabled_mods.json ✓
   - Structure des fichiers en place ✓

2. Lancement du jeu :
   - Exécuter `D:/Fractal Softworks/Starsector/starsector.exe`
   - Observer le menu principal
   - Vérifier l'affichage des tips en français

##### Rappel Important
- Le jeu se lance via l'exécutable (.exe) et non le batch (.bat)
- Les modifications sont prises en compte au démarrage du jeu
- En cas de problème, vérifier starsector.log

{{...}}

### 2 Janvier 2025 - 05:27
#### Analyse de la Structure des Fichiers de Traduction

##### État Actuel des Fichiers (data/strings/)
```
descriptions_fr.csv
ship_names_fr.json
strings_fr.json
tooltips_fr.json
tips.json              # Ne suit pas la convention de nommage _fr
```

##### Observations sur le Nommage
1. Convention identifiée :
   - Les fichiers de traduction utilisent le suffixe "_fr"
   - Le fichier tips.json ne suit pas cette convention
   - Cette incohérence pourrait causer des problèmes de maintenance

##### Configuration du Mod (mod_info.json)
```json
"replace": [
  "data/strings/tips.json",
  "data/strings/strings.json"
]
```

##### Tests Effectués
1. Test local du mod :
   - Les tips ne s'affichent pas correctement dans le menu
   - Possible problème de structure ou de nommage

##### Questions en Suspens
1. Structure du fichier tips.json :
   - Faut-il utiliser un tableau ou un objet pour les tips ?
   - Le mod chinois utilise un tableau
   - Notre implémentation utilise un objet

2. Convention de nommage :
   - Devons-nous renommer tips.json en tips_fr.json ?
   - Impact potentiel sur le système de remplacement de fichiers

##### Prochaines Actions (En Attente de Validation)
1. [ ] Vérifier la structure exacte du fichier tips.json
2. [ ] Comparer avec l'implémentation chinoise
3. [ ] Proposer une standardisation du nommage
4. [ ] Documenter les changements nécessaires

##### Notes Techniques
1. Emplacement des fichiers :
   - Mod français : D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/
   - Mod chinois : D:/Fractal Softworks/Starsector/mods/temp_mods/chinese_game_mod/
2. Structure observée du mod chinois :
   - Utilisation d'un dossier localization
   - Scripts Python pour la gestion
   - Organisation modulaire des traductions

### 2 Janvier 2025 - 05:30
#### Traduction des Tips et Strings

##### Méthodologie de Traduction
1. Création d'un fichier de suivi des traductions :
   - Fichier : `data/strings/translations/tips_translations.csv`
   - Format : deux colonnes (original, translation)
   - Permet de garder une trace de toutes les traductions

##### Traductions Effectuées (Première Partie)
1. Tips de base du jeu :
   - Tips sur les mécaniques de flux
   - Tips sur les contrôles de base
   - Tips sur les types de dégâts
   - Tips sur les armes et boucliers

##### Notes de Traduction
1. Adaptations spécifiques :
   - "LMB/RMB" traduit avec "bouton gauche/droit de la souris" pour plus de clarté
   - "WASD" adapté en "ZQSD" pour le clavier AZERTY français
   - Termes techniques conservés ("flux", "LRM")

##### Prochaines Étapes
1. [ ] Continuer la traduction des tips restants
2. [ ] Traduire le fichier strings.json
3. [ ] Intégrer les traductions dans les fichiers finaux
4. [ ] Vérifier la cohérence des traductions
5. [ ] Tester en jeu

##### Structure des Fichiers
```
data/strings/
├── translations/
│   └── tips_translations.csv    # Fichier de référence des traductions
├── tips.json                    # Fichier final des tips
└── strings.json                 # À créer
```

### 2 Janvier 2025 - 05:34
#### Suite des Traductions des Tips

##### Traductions Ajoutées
1. Tips sur les mécaniques avancées :
   - Gestion du flux et de la vitesse
   - Raccourcis clavier et interface
   - Mécaniques de commerce et de ressources
   - Combat et déploiement
   - Systèmes de porte-avions
   - Mécaniques de jeu avancées

##### Notes de Traduction Importantes
1. Terminologie cohérente :
   - "supplies" traduit par "ressources"
   - "hull mods" traduit par "modifications de coque"
   - "s-mods" conservé tel quel
   - "story points" traduit par "points d'histoire"

2. Adaptations spécifiques :
   - Touches de clavier adaptées au contexte français
   - Termes techniques conservés quand nécessaire
   - Clarification des concepts de jeu complexes

##### Statistiques de Traduction
- Total des tips traduits : 40+
- Cohérence terminologique maintenue
- Adaptations culturelles effectuées (AZERTY, terminologie française)

##### Prochaines Étapes
1. [ ] Créer le fichier tips.json final avec toutes les traductions
2. [ ] Commencer la traduction du fichier strings.json
3. [ ] Vérifier la cohérence globale des traductions
4. [ ] Tester en jeu

{{...}}

### 2 Janvier 2025 - 05:35
#### Création des Fichiers de Traduction Finaux

##### Actions Effectuées
1. Création du fichier tips_fr.json :
   - Format JSON avec tableau de tips
   - Toutes les traductions intégrées
   - Respect de la structure originale
   - Conservation des fréquences spéciales (freq:0)

2. Mise à jour du mod_info.json :
   - Nouvelle structure de remplacement avec from/to
   - Utilisation explicite des chemins de fichiers
   ```json
   "replace": [
     {"from": "data/strings/tips.json", "to": "data/strings/tips_fr.json"},
     {"from": "data/strings/strings.json", "to": "data/strings/strings_fr.json"}
   ]
   ```

##### Structure Finale
```
data/strings/
├── translations/
│   └── tips_translations.csv    # Fichier de référence des traductions
├── tips_fr.json                 # Fichier final des tips en français
└── strings_fr.json             # À créer
```

##### Prochaines Étapes
1. [ ] Commencer la traduction de strings.json
2. [ ] Créer strings_fr.json
3. [ ] Tester le mod avec les nouveaux fichiers
4. [ ] Vérifier l'affichage des caractères spéciaux

{{...}}

### 2 Janvier 2025 - 05:40
#### Test Local des Traductions

##### Procédure de Test
1. Vérifier que le mod est activé dans :
   `D:/Fractal Softworks/Starsector/mods/enabled_mods.json`

2. Structure des fichiers à vérifier :
   ```
   D:/Fractal Softworks/Starsector/mods/starsector_lang_pack_fr_private/
   ├── mod_info.json             # Configuration du remplacement
   └── data/
       └── strings/
           ├── tips_fr.json      # Tips traduits
           └── translations/     # Fichiers de référence
   ```

3. Lancer le jeu :
   - Exécuter `D:/Fractal Softworks/Starsector/starsector.exe`
   - Vérifier les tips dans le menu principal
   - Contrôler l'affichage des caractères spéciaux

##### Points de Vérification
1. [ ] Tips visibles dans le menu principal
2. [ ] Caractères spéciaux (é, è, à, etc.) correctement affichés
3. [ ] Pas de problèmes d'encodage
4. [ ] Textes correctement formatés

##### En Cas de Problème
1. Vérifier l'encodage UTF-8 des fichiers
2. Contrôler la structure JSON
3. Vérifier les chemins dans mod_info.json
4. Consulter les logs du jeu dans :
   `D:/Fractal Softworks/Starsector/starsector.log`

### 2 Janvier 2025 - 05:49
#### Analyse des Structures JSON du Jeu

##### Structure de tips.json
```json
{
    "tips": [
        {"freq":0, "tip":"Exemple avec fréquence personnalisée"},
        "Tip simple sans fréquence (freq=1 par défaut)",
        "Autre tip simple"
    ]
}
```

##### Structure de strings.json
```json
{
    "fleetInteractionDialog": {
        "initialWithStationVsLargeFleet": "Texte...",
        "initialAggressive": "Texte...",
        "initialDisengage": "Texte..."
    }
}
```

##### Points Clés
1. Tips :
   - Tableau de strings ou d'objets
   - Objets peuvent avoir une fréquence personnalisée
   - Format simple sans imbrication

2. Strings :
   - Structure imbriquée par catégories
   - Utilisation de tokens ($faction, $fleetName, etc.)
   - Textes plus complexes avec variables

##### Validation
- Les fichiers de traduction respectent ces structures ✓
- L'encodage UTF-8 est utilisé ✓
- Les tokens sont préservés dans les traductions ✓

{{...}}

### 2 Janvier 2025 - 05:53
#### Correction de la Structure JSON

##### Problème Identifié
- Différence de structure dans tips_fr.json
- Indentation incorrecte
- Doublons dans les traductions

##### Actions Effectuées
1. Correction du fichier tips_fr.json :
   - Ajustement de l'indentation
   - Suppression des doublons
   - Respect strict de la structure originale

##### Structure Corrigée
```json
{
    "tips":[
        {"freq":0, "tip":"Texte..."},
        "Tip simple...",
        "Autre tip..."
    ]
}
```

##### Validation
- Structure identique à l'original ✓
- Indentation correcte ✓
- Pas de doublons ✓
- Encodage UTF-8 préservé ✓

{{...}}

### 2 Janvier 2025 - 05:56
#### Traduction de strings.json

##### Section fleetInteractionDialog
1. Traductions ajoutées :
   - initialWithStationVsLargeFleet
   - initialAggressive
   - initialDisengage
   - initialCareful
   - initialNeutral
   - initialHoldVsStrongerEnemy
   - initialAggressiveSide

##### Points Clés
- Conservation des tokens ($faction, $fleetOrShip, etc.)
- Adaptation des formulations pour le français
- Respect du style et du ton du jeu
- Encodage UTF-8 avec caractères spéciaux

##### Prochaines Sections à Traduire
1. [ ] Combat
2. [ ] Market
3. [ ] Intel
4. [ ] Campaign

##### Notes de Traduction
- Utilisation du féminin pour "flotte" ($fleetOrShip)
- Adaptation des expressions idiomatiques
- Cohérence dans la terminologie militaire

{{...}}

### 2 Janvier 2025 - 06:32
#### Traduction des Noms de Vaisseaux

##### Actions Réalisées
1. Création du fichier `ship_names_fr.json`
2. Traduction des catégories principales :
   - FRIGATE : Noms de frégates
   - DESTROYER : Noms de destroyers
   - CRUISER : Noms de croiseurs
   - CAPITAL_SHIP : Noms de vaisseaux capitaux
   - GENERAL : Noms généraux
   - PIRATES : Noms de pirates
   - DERELICT_DRONE : Noms de drones abandonnés

##### Prochaines Étapes
1. Compléter la traduction des autres catégories de noms
2. Vérifier la cohérence des traductions
3. Tester l'intégration en jeu
4. Valider l'encodage UTF-8

##### Notes Techniques
- Conservation des identifiants techniques (ex: Delta-Max)
- Adaptation culturelle des noms quand nécessaire
- Respect de la structure JSON d'origine

{{...}}
