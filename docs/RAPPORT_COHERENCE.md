# Rapport de Cohérence des Traductions

## État au 21/01/2025

### Termes Techniques Récurrents

#### 1. Combat et Mécanique
- **flux** : ✅ Cohérent à travers les fichiers
- **boucliers** : ✅ Cohérent
- **dégâts** : ✅ Cohérent avec accents
- **vaisseau** : ✅ Cohérent

#### 2. Types de Dégâts
- "Dégâts Cinétiques"
- "Dégâts Hautement Explosifs"
- "Dégâts de Fragmentation"
- "Dégâts Énergétiques"

#### 3. Interface
- "état de préparation au combat" : ✅ Cohérent
- "interface de commandement" : ✅ Cohérent

### Problèmes Identifiés

#### 1. Encodage
- ❌ Caractères spéciaux mal encodés dans plusieurs fichiers
- ❌ Présence de "Ã©", "Ã¨", etc.
- ❌ Problèmes particulièrement visibles dans tips.json

#### 2. Incohérences Mineures
- Variations dans la capitalisation
- Espaces avant/après les guillemets
- Ponctuation inconsistante

### Actions Correctives Prioritaires

1. **Encodage**
   - [ ] Convertir tous les fichiers en UTF-8 sans BOM
   - [ ] Vérifier l'encodage après chaque modification
   - [ ] Mettre en place un test automatique d'encodage

2. **Standardisation**
   - [ ] Créer un guide de style pour la capitalisation
   - [ ] Définir les règles pour les espaces typographiques
   - [ ] Harmoniser la ponctuation

3. **Outils**
   - [ ] Développer un script de validation d'encodage
   - [ ] Créer un vérificateur de cohérence
   - [ ] Mettre en place des tests automatisés

### Glossaire des Termes Techniques

| Terme anglais | Traduction française | Contexte d'utilisation |
|--------------|---------------------|----------------------|
| flux | flux | Mécanique de jeu |
| shields | boucliers | Protection des vaisseaux |
| damage | dégâts | Combat |
| ship | vaisseau | Général |
| combat readiness | état de préparation au combat | État des vaisseaux |
| command interface | interface de commandement | Interface utilisateur |

### Notes Techniques
- Tous les fichiers JSON doivent être en UTF-8
- Les variables de jeu ($faction, $fleetOrShip, etc.) doivent rester inchangées
- Les retours à la ligne (\n) doivent être préservés
