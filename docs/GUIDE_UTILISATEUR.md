# Guide Utilisateur - Pack de Traduction Française Starsector

## Table des Matières
1. [Installation](#installation)
2. [Configuration](#configuration)
3. [Utilisation](#utilisation)
4. [Validation](#validation)
5. [Dépannage](#dépannage)
6. [FAQ](#faq)

## Installation

### Prérequis
- Starsector version 0.97a-RC11 ou supérieure
- 50 Mo d'espace disque libre
- Encodage système en UTF-8

### Étapes d'Installation
1. Téléchargez la dernière version du pack
2. Extrayez l'archive dans le dossier `mods`
3. Vérifiez la structure suivante :
   ```
   mods/
   └── starsector_lang_pack_fr/
       ├── mod_info.json
       └── localization/
           └── data/
               ├── strings/
               └── missions/
   ```
4. Lancez le launcher Starsector
5. Activez le mod "French Language Pack"

## Configuration

### Options Disponibles
- **Typographie** : Stricte/Souple
- **Validation** : Automatique/Manuelle
- **Backup** : Activé/Désactivé

### Fichier de Configuration
```json
{
  "typography": "strict",
  "validation": "auto",
  "backup": true
}
```

## Utilisation

### Structure des Fichiers
- `strings/` : Textes d'interface
- `missions/` : Textes de missions
- `descriptions/` : Descriptions d'items

### Format des Fichiers
1. **Missions**
   ```
   Lieu : [lieu]
   Date : [date]
   Objectifs : [objectifs]
   Description : [description]
   ```

2. **Strings**
   ```json
   {
     "key": "valeur",
     "section": {
       "subkey": "valeur"
     }
   }
   ```

### Règles Typographiques
- Espaces avant : `;:!?»`
- Espaces après : `«`
- Guillemets : `« »`
- Points de suspension : `…`

## Validation

### Outils de Validation
1. **validate_translations.py**
   - Vérifie la structure
   - Valide l'encodage
   - Contrôle la typographie

2. **update_translations.py**
   - Met à jour les traductions
   - Crée les backups
   - Maintient la cohérence

### Messages d'Erreur Courants
| Message | Cause | Solution |
|---------|-------|----------|
| "Encodage incorrect" | Fichier non UTF-8 | Réencodez en UTF-8 |
| "Structure invalide" | Format incorrect | Vérifiez le format |
| "Erreur typographique" | Règle non respectée | Corrigez la typographie |

## Dépannage

### Problèmes Courants
1. **Texte non traduit**
   - Vérifiez l'activation du mod
   - Contrôlez le fichier de traduction
   - Validez l'encodage

2. **Caractères corrompus**
   - Vérifiez l'encodage UTF-8
   - Réinstallez le pack
   - Restaurez depuis le backup

3. **Erreurs de validation**
   - Lisez le message d'erreur
   - Corrigez selon les règles
   - Revalidez le fichier

### Logs et Diagnostics
- `validate_translations.log`
- `update_translations.log`
- `error_report.txt`

## FAQ

### Questions Générales
Q: Le mod est-il compatible avec d'autres mods ?
R: Oui, il ne modifie que les fichiers de traduction.

Q: Puis-je contribuer aux traductions ?
R: Oui, consultez le guide de contribution.

### Questions Techniques
Q: Comment changer l'encodage d'un fichier ?
R: Utilisez un éditeur comme Notepad++ et "Enregistrer sous" en UTF-8.

Q: Les backups prennent-ils beaucoup d'espace ?
R: Non, environ 1 Mo par version.

### Support
- Forum : [Topic Starsector](http://fractalsoftworks.com/forum/)
- GitHub : [Issues](https://github.com/mipsou/starsector_lang_pack_fr/issues)
- Discord : [Serveur Communautaire](https://discord.gg/starsector)
