# Checklist de release — Starsector FR

## Avant de publier

### mod_info.json
- [ ] ID public = `starsector_lang_pack_fr` (PAS `_dev`)
- [ ] Nom = `Starsector Language Pack - French` (PAS `[DEV]`)
- [ ] Version bumpée (major.minor.patch)
- [ ] gameVersion = version Starsector cible

### Fichiers
- [ ] Tous les fichiers du `replace` sont présents
- [ ] Pas de fichiers dev (.github/, data/test/, .py, tools/, .gitignore)
- [ ] .faction PAS dans le replace (merge auto)
- [ ] JAR compilé Java 17 pour 0.98a+

### Encodage
- [ ] rules.csv en UTF-8
- [ ] skill_data.csv sans mojibake (pas de double encodage Ã©)
- [ ] JSON en UTF-8

### Test en jeu
- [ ] Lancer avec le mod public (pas dev)
- [ ] Station : dialogues FR, accents OK
- [ ] Rencontre de flotte : options FR
- [ ] Bar : textes FR
- [ ] Codex F2 : compétences sans mojibake
- [ ] Missions : briefings FR
- [ ] Pas de crash

### Publication
- [ ] PR dev → main sur privé
- [ ] PR sync → main sur public
- [ ] ZIP créé depuis public/main (git archive)
- [ ] Vérifier contenu ZIP (pas de dev files)
- [ ] Release créée avec notes de version
- [ ] ZIP uploadé sur la release
- [ ] NE PAS supprimer/recréer la release (perte compteur)
