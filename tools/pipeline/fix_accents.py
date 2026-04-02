#!/usr/bin/env python3
"""
fix_accents.py — Étape QA du pipeline de traduction
Corrige les accents manquants dans rules.csv (colonne texte)
Usage: python fix_accents.py [chemin_vers_rules.csv]
       Par défaut: data/campaign/rules.csv dans le répertoire du script
"""

import re, sys, os

BASE = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "rules.csv")

# Each entry: (compiled_regex, replacement_string, label)
patterns = []

def add(pattern, replacement, label):
    patterns.append((re.compile(pattern), replacement, label))

# ── GROUP A — Common words ──
add(r'\betre\b', 'être', 'etre->être')
add(r'\bEtre\b', 'Être', 'Etre->Être')
add(r'\bete\b', 'été', 'ete->été')
add(r'\bEte\b', 'Été', 'Ete->Été')
add(r'\betait\b', 'était', 'etait->était')
add(r'\bEtait\b', 'Était', 'Etait->Était')
add(r'\betais\b', 'étais', 'etais->étais')
add(r'\betaient\b', 'étaient', 'etaient->étaient')
add(r'\bEtaient\b', 'Étaient', 'Etaient->Étaient')
add(r'\betes\b', 'êtes', 'etes->êtes')
add(r'\bEtes\b', 'Êtes', 'Etes->Êtes')
add(r'\betant\b', 'étant', 'etant->étant')
add(r'\bEtant\b', 'Étant', 'Etant->Étant')
add(r'\bdeja\b', 'déjà', 'deja->déjà')
add(r'\bDeja\b', 'Déjà', 'Deja->Déjà')
add(r'\btres\b', 'très', 'tres->très')
add(r'\bTres\b', 'Très', 'Tres->Très')
add(r'\bdesole\b', 'désolé', 'desole->désolé')
add(r'\bDesolé\b', 'Désolé', 'Desolé->Désolé')
add(r'\bDesole\b', 'Désolé', 'Desole->Désolé')
add(r'\bdesolee\b', 'désolée', 'desolee->désolée')
add(r'\bdesoles\b', 'désolés', 'desoles->désolés')
add(r'\bdesolees\b', 'désolées', 'desolees->désolées')

# ── GROUP B — Words ending in -iere/-ieres ──
for word, accented in [
    ('maniere', 'manière'), ('lumiere', 'lumière'),
    ('derriere', 'derrière'), ('premiere', 'première'),
    ('derniere', 'dernière'), ('entiere', 'entière'),
    ('matiere', 'matière'), ('carriere', 'carrière'),
    ('frontiere', 'frontière'), ('poussiere', 'poussière'),
    ('priere', 'prière'),
]:
    add(r'\b' + word + r'\b', accented, f'{word}->{accented}')
    cap_word = word[0].upper() + word[1:]
    cap_accented = accented[0].upper() + accented[1:]
    add(r'\b' + cap_word + r'\b', cap_accented, f'{cap_word}->{cap_accented}')
    add(r'\b' + word + r's\b', accented + 's', f'{word}s->{accented}s')

# ── GROUP C — Words ending in -eme/-emes ──
for word, accented in [
    ('systeme', 'système'), ('probleme', 'problème'),
]:
    add(r'\b' + word + r'\b', accented, f'{word}->{accented}')
    add(r'\b' + word + r's\b', accented + 's', f'{word}s->{accented}s')
    cap_word = word[0].upper() + word[1:]
    cap_accented = accented[0].upper() + accented[1:]
    add(r'\b' + cap_word + r'\b', cap_accented, f'{cap_word}->{cap_accented}')

# ── GROUP D — Circumflex words ──
add(r'\bcontrole\b', 'contrôle', 'controle->contrôle')
add(r'\bControle\b', 'Contrôle', 'Controle->Contrôle')
add(r'\bcontroles\b', 'contrôles', 'controles->contrôles')
add(r'\bcontroler\b', 'contrôler', 'controler->contrôler')
add(r'\bcontrolee\b', 'contrôlée', 'controlee->contrôlée')
add(r'\bcontrolees\b', 'contrôlées', 'controlees->contrôlées')
add(r'\bcontrolez\b', 'contrôlez', 'controlez->contrôlez')
add(r'\brole\b', 'rôle', 'role->rôle')
add(r'\bRole\b', 'Rôle', 'Role->Rôle')
add(r'\broles\b', 'rôles', 'roles->rôles')
add(r'\bRoles\b', 'Rôles', 'Roles->Rôles')
add(r'\bdiplome\b', 'diplôme', 'diplome->diplôme')
add(r'\bdiplomes\b', 'diplômes', 'diplomes->diplômes')
add(r'\bcote\b', 'côté', 'cote->côté')
add(r'\bCote\b', 'Côté', 'Cote->Côté')
add(r'\bcotes\b', 'côtés', 'cotes->côtés')
add(r'grace a ', 'grâce à ', 'grace a->grâce à')
add(r'Grace a ', 'Grâce à ', 'Grace a->Grâce à')
add(r'grace au', 'grâce au', 'grace au->grâce au')
add(r'Grace au', 'Grâce au', 'Grace au->Grâce au')

# ── GROUP E — Words ending in -ite/-ité ──
for word, accented in [
    ('securite', 'sécurité'), ('verite', 'vérité'),
    ('societe', 'société'), ('realite', 'réalité'),
    ('capacite', 'capacité'), ('liberte', 'liberté'),
    ('qualite', 'qualité'), ('opportunite', 'opportunité'),
    ('activite', 'activité'), ('volonte', 'volonté'),
    ('beaute', 'beauté'), ('cruaute', 'cruauté'),
]:
    add(r'\b' + word + r'\b', accented, f'{word}->{accented}')
    add(r'\b' + word + r's\b', accented + 's', f'{word}s->{accented}s')
    cap_word = word[0].upper() + word[1:]
    cap_accented = accented[0].upper() + accented[1:]
    add(r'\b' + cap_word + r'\b', cap_accented, f'{cap_word}->{cap_accented}')

add(r'\bnecessite\b', 'nécessité', 'necessite->nécessité')
add(r'\bNecessite\b', 'Nécessité', 'Necessite->Nécessité')
add(r'\bnecessiter\b', 'nécessiter', 'necessiter->nécessiter')
add(r'\bnecessitent\b', 'nécessitent', 'necessitent->nécessitent')
add(r'\bnecessitait\b', 'nécessitait', 'necessitait->nécessitait')

# ── GROUP F — Other common missing accents ──
for word, accented in [
    ('equipe', 'équipe'), ('equipes', 'équipes'),
    ('equipage', 'équipage'), ('equipages', 'équipages'),
    ('energie', 'énergie'), ('energies', 'énergies'),
    ('etoile', 'étoile'), ('etoiles', 'étoiles'),
    ('etat', 'état'), ('etats', 'états'),
    ('evenement', 'événement'), ('evenements', 'événements'),
    ('etranger', 'étranger'), ('etrangere', 'étrangère'),
    ('etrangers', 'étrangers'), ('etrangeres', 'étrangères'),
    ('epave', 'épave'), ('epaves', 'épaves'),
    ('equipement', 'équipement'), ('equipements', 'équipements'),
    ('eleve', 'élevé'), ('echange', 'échange'), ('echanges', 'échanges'),
    ('eviter', 'éviter'), ('ecraser', 'écraser'),
    ('electronique', 'électronique'), ('electroniques', 'électroniques'),
    ('eliminer', 'éliminer'), ('emission', 'émission'), ('emissions', 'émissions'),
]:
    add(r'\b' + word + r'\b', accented, f'{word}->{accented}')
    cap_word = word[0].upper() + word[1:]
    cap_accented = accented[0].upper() + accented[1:]
    add(r'\b' + cap_word + r'\b', cap_accented, f'{cap_word}->{cap_accented}')

# ── Read, process, write ──
def main():
    print(f"Reading {CSV_PATH}...")
    with open(CSV_PATH, 'r', encoding='utf-8', newline='') as f:
        content = f.read()

    original_len = len(content)
    total_replacements = 0
    results = []

    for regex, replacement, label in patterns:
        count = len(regex.findall(content))
        if count > 0:
            content = regex.sub(replacement, content)
            total_replacements += count
            results.append((label, count))

    with open(CSV_PATH, 'w', encoding='utf-8', newline='') as f:
        f.write(content)

    print(f"\n{'='*60}")
    print(f"  ACCENT FIX SUMMARY")
    print(f"{'='*60}")
    print(f"  File: {os.path.basename(CSV_PATH)}")
    print(f"  Total replacements: {total_replacements}")
    print(f"{'='*60}")
    if results:
        print(f"  {'Pattern':<35} {'Count':>6}")
        print(f"  {'-'*35} {'-'*6}")
        for label, count in sorted(results, key=lambda x: -x[1]):
            print(f"  {label:<35} {count:>6}")
    else:
        print("  No replacements needed.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
