# Structure du Journal de Développement

## Organisation des Fichiers

### 📁 Structure
1. `DEVBOOK.md`
   - Journal du mois en cours
   - Contient uniquement les entrées du mois actuel
   - Mis à jour quotidiennement

2. Archives Mensuelles
   - Format : `DEVBOOK_YYYY_MM.md`
   - Exemple : `DEVBOOK_2025_01.md`
   - Stockage chronologique des entrées passées

## Format des Entrées

### 📝 Hiérarchie
1. Niveau 1 : `# Guide de Développement - Starsector Language Pack FR`
2. Niveau 2 : `## Journal de Développement - [Mois] [Année]`
3. Niveau 3 : `### YYYY-MM-DD HH:mm : Titre`
4. Niveau 4 : `#### 🛠️ Catégorie`
5. Niveau 5 : Points numérotés

### 🏷️ Catégories et Emojis
- 🛠️ Modifications Techniques
- 🧪 Tests et Validation
- 📝 Documentation
- 🔧 Configuration
- 📦 Dépendances
- 🔒 Sécurité
- 🎨 Interface
- 🔄 Refactorisation
- 📋 Structure
- 🚀 Déploiement

## Structure du Projet

### Répertoires Principaux
- `/data` : Fichiers de données du jeu à traduire
- `/docs` : Documentation du projet
- `/tools` : Outils de validation et d'aide à la traduction
- `/original` : Fichiers sources originaux
- `/backups` : Sauvegardes automatiques
- `/tests` : Tests automatisés
  - `/tests/integration/` : Tests d'intégration
  - `/tests/unit/` : Tests unitaires

### 📄 Formats de Fichiers
1. JSON (Format Starsector)
   - Pas d'espace après les deux points dans les clés
   - Guillemets droits (") uniquement
   - Indentation de 4 espaces
   - Encodage UTF-8 avec sauts de ligne Unix (\n)

2. CSV
   - Encodage UTF-8
   - Séparateur point-virgule
   - Format strict pour les descriptions

### 🔍 Validation
1. Tests Automatisés
   - Tests unitaires pour chaque composant
   - Tests d'intégration pour le système
   - Validation du format JSON
   - Vérification de l'encodage

2. Outils de Validation
   - Détection des caractères de contrôle
   - Validation de la typographie
   - Vérification des chemins
   - Tests de performance

## Processus de Gestion

### 🔄 Archivage Mensuel
1. Fin de mois :
   - Créer `DEVBOOK_YYYY_MM.md`
   - Copier le contenu de `DEVBOOK.md`
   - Vider `DEVBOOK.md`

2. Début de mois :
   - Mettre à jour l'en-tête de `DEVBOOK.md`
   - Commencer les nouvelles entrées

### 📊 Maintenance
1. Vérification quotidienne :
   - Format des entrées
   - Cohérence des emojis
   - Structure hiérarchique

2. Validation mensuelle :
   - Intégrité des archives
   - Liens entre les documents
   - Mise à jour des index
