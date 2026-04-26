# Contribuer au pack de langue FR

Merci de votre interet pour ce projet ! Toute aide est la bienvenue.

## Comment contribuer

1. **Fork** le repo et creez une branche depuis `dev`
2. Faites vos modifications
3. Ouvrez une **Pull Request** vers `dev` (jamais vers `main`)

## Regles de traduction

- **Respecter le ton original** du jeu (familier, technique, ironique selon le contexte)
- **Ne pas traduire mot a mot** — privilegier des formulations naturelles en francais
- **Conserver les termes gameplay** tels qu'ils apparaissent en jeu (noms d'armes, de vaisseaux, etc.)
- **Verifier les noms en jeu** dans `weapon_data.csv`, `ship_data.csv`, etc. avant de reformuler une description
- **Ne pas modifier les IDs CSV** (premiere colonne) ni la structure des fichiers

## Validation

- Les contributions passent par le repo prive (dev/QA) avant d'etre poussees vers le public
- Un test en jeu est requis avant merge
- Le CSV doit etre valide (structure, colonnes, guillemets)

## Systeme de confiance contributeur

**Bienvenue !** Ce systeme n'est pas un filtre pour exclure, c'est un **dispositif de securite collective** — il protege la qualite du projet, les joueurs francophones, et te permet de progresser sereinement a ton rythme.

Tout contributeur demarre comme 🆕 **Nouveau** et grandit naturellement avec ses contributions. Les premiers paliers sont rapidement atteignables — quelques PRs propres suffisent pour passer 🌱 **Verifie** puis 🟢 **Confirme**, ce qui couvre deja 90% des besoins de contribution active.

### Niveaux de statut

| Statut | Process applique |
|---|---|
| 🆕 **Nouveau** | Approval CI manuel + review code + test en jeu obligatoire |
| 🌱 **Verifie** | CI auto + review code + test en jeu obligatoire |
| 🟢 **Confirme** | CI auto + review code (test optionnel sur fix triviaux) |
| 🥉 **Regulier** | CI auto + review code (peer-review possible) |
| 🥈 **Referent** | Peer-review entre referents, audit regulier |
| 🥇 **Core** | Tout passe par 4 yeux minimum (jamais solo merge) |

### Comment evoluer

Le statut evolue naturellement avec les contributions :
- Une PR validee propre fait progresser
- Une PR avec ajustements progresse plus lentement
- Une PR rejetee pour qualite fait reculer (reversible avec contribution suivante)
- Le signalement d'un bug critique compte autant qu'une PR
- Un fork dedie a etendre le projet (autre langue, plateforme) compte comme contribution majeure
- Un comportement malveillant entraine un ban immediat

**Pas de course aux points** — l'idee est de grandir ensemble, pas de cumuler.

### Principe zerotrust universel

Quel que soit le statut, **le code review humain reste obligatoire a vie pour tous, mainteneur inclus**. Le statut allege seulement le process administratif (CI auto, peer-review possible), jamais la verification du code. C'est notre garantie de qualite commune.

### Cas particuliers

Les contributeurs connus personnellement par le mainteneur peuvent demarrer a un statut plus eleve que 🆕 Nouveau, mais restent soumis aux memes regles d'evolution.

### Inspirations

Systeme inspire des bonnes pratiques 2026 de la communaute OSS — la confiance est un dispositif de securite collective, jamais un filtre de gatekeeping ([source](https://duckalignment.academy/trust-in-open-source-communities/)).

## Contributeurs

| Pseudo | Contribution | Statut |
|---|---|---|
| [mipsou](https://github.com/mipsou) | Auteur principal | Mainteneur |
| [Dorkamrade](https://github.com/Dorkamrade) | 🌟 Premier contributeur externe — Reformulations descriptions armes (PR #109) | 🆕 Nouveau |
| [Ferno (carlosgmz)](https://github.com/carlosgmz) | Bug CSV abilities (PR #120), cohérence noms abilités tutoriel (PR #122), tip F2 Codex signalé, fork ES en cours | 🟢 Confirmé |
