# Guide de Contribution - Pack de Traduction Française Starsector

## Table des Matières
1. [Introduction](#introduction)
2. [Prérequis](#prérequis)
3. [Processus](#processus)
4. [Standards](#standards)
5. [Tests](#tests)
6. [Soumission](#soumission)

## Introduction

### Objectifs
- Maintenir une traduction française de qualité
- Assurer la cohérence des textes
- Respecter les règles typographiques
- Faciliter la maintenance

### Types de Contributions
1. Traductions
2. Corrections
3. Documentation
4. Tests
5. Outils

## Prérequis

### Technique
- Python 3.8+
- Git
- Éditeur UTF-8
- pytest

### Linguistique
- Maîtrise du français
- Connaissance de l'anglais
- Règles typographiques
- Terminologie jeu vidéo

### Installation
```bash
git clone https://github.com/mipsou/starsector_lang_pack_fr.git
cd starsector_lang_pack_fr
pip install -r requirements.txt
```

## Processus

### 1. Préparation
```bash
git checkout -b feature/ma-contribution
```

### 2. Validation
```bash
python scripts/validate_translations.py
pytest
```

### 3. Commit
```bash
git add .
git commit -m "type: description"
```

### 4. Pull Request
1. Push sur GitHub
2. Créer la PR
3. Attendre la review
4. Appliquer les retours

## Standards

### Commits
- feat: nouvelle traduction
- fix: correction
- docs: documentation
- test: tests
- tool: outils

### Code
```python
def validate_translation(text):
    """Valide une traduction.
    
    Args:
        text (str): Texte à valider
        
    Returns:
        bool: True si valide
    """
    pass
```

### Documentation
```markdown
# Titre

## Section

Description claire et concise.

### Sous-section

- Point important
- Autre point
```

### Traduction

#### Format
```json
{
  "key": "valeur",
  "_comment": "contexte"
}
```

#### Style
- Voix active
- Temps présent
- 2e personne
- Registre soutenu

## Tests

### Types
1. **Unitaires**
   - Validation fichiers
   - Règles typographiques
   - Encodage

2. **Intégration**
   - Structure complète
   - Cohérence globale
   - Performance

### Exécution
```bash
pytest                      # Tous les tests
pytest test_specific.py     # Test spécifique
pytest -v                   # Mode verbeux
```

### Validation
```bash
python scripts/validate_translations.py
python scripts/update_translations.py --check
```

## Soumission

### Checklist
- [ ] Tests passent
- [ ] Documentation à jour
- [ ] Règles respectées
- [ ] Code commenté
- [ ] PR descriptive

### Process Review
1. Soumission PR
2. Review automatique
3. Review humaine
4. Corrections
5. Merge

### Après Merge
1. Mise à jour locale
2. Nettoyage branches
3. Validation finale

## Ressources

### Documentation
- [Guide Utilisateur](GUIDE_UTILISATEUR.md)
- [Wiki](https://github.com/mipsou/starsector_lang_pack_fr/wiki)
- [API Reference](https://github.com/mipsou/starsector_lang_pack_fr/docs/api)

### Outils
- [validate_translations.py](../scripts/validate_translations.py)
- [update_translations.py](../scripts/update_translations.py)
- [test_integration.py](../scripts/test_integration.py)

### Liens
- [Issues](https://github.com/mipsou/starsector_lang_pack_fr/issues)
- [Pull Requests](https://github.com/mipsou/starsector_lang_pack_fr/pulls)
- [Forum](http://fractalsoftworks.com/forum/)

## Support

### Communauté
- Discord : [Serveur](https://discord.gg/starsector)
- Forum : [Topic](http://fractalsoftworks.com/forum/)
- GitHub : [Discussions](https://github.com/mipsou/starsector_lang_pack_fr/discussions)

### Contact
- Maintainers : [@mipsou](https://github.com/mipsou)
- Email : contact@starsector-fr.com
- Discord : Mipsou#1234
