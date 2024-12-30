# Guide de Développement - Starsector Language Pack FR

## Environnement de Développement

### Structure des Dossiers
```
starsector_lang_pack_fr/
├── mod_info.json
└── localization/
    ├── data/
    │   ├── config/     # Configurations localisées
    │   └── strings/    # Fichiers de traduction
    └── graphics/
        └── ui/        # Éléments d'interface traduits
```

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

### Problèmes Identifiés
1. Quelques titres de section doivent être mieux formatés
2. Les exemples de code nécessitent un meilleur formatage
3. Les variables sont maintenant en `code` mais certaines peuvent être manquées

### Actions Suivantes
1. Ajouter une table des matières automatique
2. Revoir le formatage des tableaux si présents
3. Ajouter des liens internes pour la navigation

## Plan de Traduction
1. Identifier les fichiers prioritaires à traduire
2. Créer une structure de dossiers miroir pour les traductions
3. Mettre en place un système de suivi de progression
4. Établir un glossaire des termes récurrents

### Méthode de Traduction Proposée
- Traduction par lots thématiques
- Validation des traductions par tests in-game
- Documentation des choix de traduction
- Gestion des versions avec git

### Actions Suivantes
1. Vérifier la qualité de la conversion Markdown
2. Extraire les termes clés pour le glossaire
3. Commencer la traduction de la documentation

### Documentation Technique

#### Structure des Rules
- Fichier : data/campaign/rules.csv
- Contient les règles de comportement du jeu
- Documentation complète dans les fichiers PDF/RTF

### Notes sur mod_info.json
Champs requis :
- id : Identifiant unique du mod
- name : Nom affiché dans le dialogue de sélection
- version : Version du mod (format : "X.Y.Z" ou {major:X, minor:Y, patch:Z})
- description : Description du mod
- gameVersion : Version du jeu compatible

Champs optionnels :
- author : Auteur du mod
- totalConversion : Si true, seul ce mod sera chargé
- utility : Si true, peut être utilisé avec les total conversions
- dependencies : Liste des mods requis
- jars : Liste des fichiers .jar à charger
- modPlugin : Classe principale du mod
- replace : Liste des fichiers à remplacer plutôt que fusionner

### Format des Rapports (Toutes les 5 minutes)
1. Actions effectuées
2. Problèmes rencontrés
3. Solutions appliquées
4. Prochaines étapes

## TODO

### CI/CD
- [ ] Configurer Azure Pipelines
  - [ ] Mettre en place les tests automatiques
  - [ ] Automatiser la conversion PDF/RTF vers Markdown
  - [ ] Configurer le déploiement automatique
  - [ ] Mettre en place les vérifications de qualité du code

## Notes de Développement

### Priorités
1. Stabilité du mod
2. Qualité des traductions
3. Performance
4. Maintenance

### À Faire
- [ ] Automatisation complète
- [ ] Tests unitaires
- [ ] Documentation API
- [ ] Outils de validation

## Chaîne de Chargement du Mod

### Séquence de Chargement
1. **enabled_mods.json** (D:\Fractal Softworks\Starsector\mods\enabled_mods.json)
   - Premier fichier vérifié au démarrage
   - Contient la liste des mods activés
   - Format attendu :
     ```json
     {
       "enabled_mods": [
         "starsector_lang_pack_fr_dev"
       ]
     }
     ```

2. **mod_info.json** (dans chaque dossier de mod)
   - Définit les métadonnées du mod
   - Contrôle les remplacements de fichiers
   - Gère les dépendances

3. **Ressources du Mod**
   - Fichiers de localisation
   - Assets graphiques
   - Configurations

### Points de Vérification
1. enabled_mods.json existe et est valide
2. Le mod est correctement listé
3. mod_info.json est correctement formaté
4. Les chemins de remplacement sont valides

### Erreurs Courantes
1. enabled_mods.json manquant ou mal formaté
2. ID de mod incorrect dans enabled_mods.json
3. Chemins de remplacement invalides

## Configuration de l'Environnement

### Commandes Autorisées
Liste des commandes autorisées pour le développement :

```bash
# Commandes de base
git

# Récupération de la documentation officielle
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=4761.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=8355.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=7164.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=15244.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=6926.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=5016.0"
```

## Configuration Windsurf - Auto-exécution

### Liste Blanche des Commandes
Configuration pour permettre l'auto-exécution par Cascade sans confirmation :

```bash
git
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=4761.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=8355.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=7164.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=15244.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=6926.0"
curl -A "Mozilla/5.0" "https://fractalsoftworks.com/forum/index.php?topic=5016.0"
```

### Configuration
1. Ouvrir Windsurf
2. Aller dans Paramètres
3. Section "Cascade Commands Allow List"
4. Copier-coller chaque commande exactement
5. Ces commandes seront exécutées automatiquement par Cascade

## Retours d'Expérience et Erreurs Connues

### Bonnes Pratiques de Développement
1. **TOUJOURS vérifier avant d'agir** :
   - ✅ Vérifier l'existence des fichiers/dossiers
   - ✅ Contrôler les permissions
   - ✅ Valider les chemins d'accès
   - ❌ Ne jamais supposer qu'un fichier/dossier existe

2. **Commandes et Chemins** :
   - ❌ `starsector.exe` - Ne fonctionne pas (chemin non complet)
   - ✅ `D:\Fractal Softworks\Starsector\starsector.exe` - Correct (chemin complet)
   - ✅ Toujours vérifier l'existence du fichier avant de l'exécuter

### Processus de Vérification
1. Vérifier l'existence des ressources
2. Contrôler les permissions
3. Valider la structure
4. Tester l'exécution

### Documentation des Erreurs
1. Noter immédiatement les erreurs rencontrées
2. Documenter la solution
3. Mettre à jour les bonnes pratiques

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
