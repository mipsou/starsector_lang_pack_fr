# Analyse des Logs Starsector

## 1. Séquence de Démarrage

### 1.1 Phase d'Initialisation (0-100ms)
- **0-15ms** : Démarrage launcher et environnement
- **15-20ms** : Configuration et mods
- **80-90ms** : Initialisation graphique OpenGL

### 1.2 Phase de Chargement (32000ms+)
- **32000ms** : Classes Java et scripts
- **32400ms+** : Données de jeu
  - Armes et projectiles
  - Vaisseaux et systèmes
  - Ressources graphiques

## 2. Gestion des Mods

### 2.1 Détection (t+14ms)
- Scan du dossier `mods/`
- Lecture des `mod_info.json`
- Vérification des dépendances

### 2.2 Chargement (t+32362ms)
- Fichiers de traduction
- Ressources graphiques
- Scripts et données

## 3. Système de Traduction

### 3.1 Fichiers Supportés
- **JSON** :
  - ship_names.json
  - strings.json
  - tips.json
- **CSV** :
  - ship_data.csv
  - weapon_data.csv

### 3.2 Séquence de Chargement
1. Détection du mod de traduction
2. Validation des fichiers
3. Application des traductions
4. Vérification de l'encodage

## 4. Analyse des Erreurs

### 4.1 Types de Messages
- **INFO** : Messages standard
- **WARN** : Avertissements non-critiques
- **ERROR** : Erreurs à corriger

### 4.2 Points d'Attention
1. Encodage UTF-8 obligatoire
2. Format JSON spécifique
3. Dépendances entre mods
4. Ordre de chargement

## 5. Performance

### 5.1 Temps de Chargement
- Launcher : 0-15ms
- Configuration : 15-90ms
- Classes : 32000-32400ms
- Données : 32400ms+

### 5.2 Optimisation
1. Préchargement des ressources
2. Cache des traductions
3. Validation anticipée

## 6. Maintenance

### 6.1 Vérifications Régulières
- Logs d'erreur
- Performance de chargement
- Intégrité des fichiers

### 6.2 Actions Correctives
1. Nettoyage des fichiers temporaires
2. Validation des traductions
3. Optimisation des ressources

## 7. Commandes Utiles

### 7.1 Analyse des Logs
```powershell
# Afficher les dernières erreurs
Get-Content 'starsector.log' | Select-String "ERROR"

# Voir le temps de chargement
Get-Content 'starsector.log' | Select-String "Loading time"

# Vérifier les mods chargés
Get-Content 'starsector.log' | Select-String "Loading mod"
```

### 7.2 Maintenance
```powershell
# Nettoyer les fichiers temporaires
Remove-Item '*.temp' -Force

# Vérifier l'encodage
Get-Content '*.json' | Select-Object -First 1
```
