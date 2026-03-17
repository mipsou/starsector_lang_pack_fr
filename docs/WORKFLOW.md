# Workflow de Validation et Publication

## Principe Général

Tout contenu doit suivre le processus suivant :
1. Développement initial dans le dépôt privé
2. Revue et validation dans le dépôt privé
3. Publication dans le dépôt public une fois validé

## Processus Détaillé

### 1. Développement (Dépôt Privé)

- Création dans une branche dédiée
- Documentation dans `/docs`
- Tests dans `/tests`
- Outils dans `/tools`

### 2. Validation (Dépôt Privé)

- Pull Request pour revue
- Tests automatisés
- Revue de code
- Validation de la documentation
- Vérification des standards

### 3. Publication (Dépôt Public)

- Nettoyage des informations sensibles
- Synchronisation du contenu validé
- Mise à jour de la documentation publique
- Tag de version si nécessaire

## Branches

- `main` : Production stable
- `dev` : Développement
- `docs/*` : Documentation
- `feature/*` : Nouvelles fonctionnalités
- `fix/*` : Corrections

## Commandes Git

### Configuration des remotes
```bash
git remote add private git@github.com:mipsou/starsector_lang_pack_fr_private.git
git remote add public git@github.com:mipsou/starsector_lang_pack_fr.git
```

### Workflow typique
```bash
# Développement
git checkout -b feature/nouvelle-fonctionnalite
git commit -m "feat: nouvelle fonctionnalité"
git push private feature/nouvelle-fonctionnalite

# Après validation
git checkout dev
git merge feature/nouvelle-fonctionnalite
git push private dev

# Publication
git push public dev
```

## Checklist de Validation

- [ ] Tests passés
- [ ] Documentation à jour
- [ ] Code revu
- [ ] Pas d'information sensible
- [ ] Standards respectés
- [ ] Traductions validées
