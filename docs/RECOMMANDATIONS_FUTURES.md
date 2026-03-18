# Recommandations pour Futures Versions

## Contexte
Ce document liste les améliorations suggérées pour les prochaines versions du mod, sans impacter les fichiers actuellement en production.

## Général
- Créer une branche de test pour les modifications
- Mettre en place des tests automatisés
- Établir un processus de validation avant publication

## strings.json
- Standardisation des termes militaires
- Cohérence des formulations de combat
- Documentation des variables système

## tooltips.json
### Suggestions pour v2.0
1. **Terminologie**
   - Remplacer "DPS" par "dégâts par seconde"
   - Utiliser "anomalie" au lieu de "bug"
   - Standardiser les termes techniques

2. **Style**
   - Formaliser le ton des messages
   - Uniformiser la longueur des descriptions
   - Améliorer la clarté des instructions

3. **Format**
   - Standardiser la ponctuation
   - Vérifier les sauts de ligne
   - Harmoniser la structure des phrases

### Exemples de Formulations Futures
```diff
# Pour référence uniquement - Ne pas appliquer en production
- "Cette arme est spéciale. En réalité, si vous voyez ceci, c'est probablement un bug."
+ "Cette arme possède des propriétés uniques. Si ce message apparaît, veuillez le signaler comme anomalie."
```

## Processus de Mise à Jour
1. Créer une branche de test
2. Implémenter les changements
3. Tests approfondis
4. Validation communautaire
5. Fusion en production

## Notes
- Conserver la compatibilité avec les versions précédentes
- Documenter tous les changements
- Maintenir des sauvegardes
