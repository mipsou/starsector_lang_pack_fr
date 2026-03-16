"""
Module de conversion des guillemets pour Starsector.

Fournit une fonction pour convertir les guillemets droits en guillemets français
dans les fichiers JSON de Starsector, en respectant la structure JSON.

Exemple d'utilisation:
    >>> from fix_quotes import convert_quotes_starsector
    >>> texte = '"Texte avec "citation" interne"'
    >>> print(convert_quotes_starsector(texte))
    " Texte avec «\u202Fcitation\u202F» interne "
"""

import re
import regex

# Ensemble des signes de ponctuation concernés
PUNCTUATION_INSIDE = {',', '.'}  # Toujours à l'intérieur
PUNCTUATION_OUTSIDE = {'!', '?', ';'}  # Peuvent être à l'extérieur selon le contexte

def process_quotes(text, level=0):
    """
    Traite récursivement les citations dans le texte.

    Pour le niveau 0 (premier niveau de citation dans le contenu interne),
    on utilise des guillemets doubles typographiques (« … »).
    Pour les niveaux supérieurs (citations imbriquées), on utilise des guillemets simples (‹ … ›).

    La ponctuation est gérée selon les règles typographiques françaises :
    - La virgule et le point sont toujours à l'intérieur des guillemets
    - Le point d'interrogation, d'exclamation et le point-virgule peuvent être à l'extérieur
      avec un espace entre le guillemet fermant et la ponctuation
    """
    # Pattern récursif qui repère une séquence encadrée par des guillemets non échappés.
    pattern = r'"((?:[^"\\]+|\\.|(?R))*)"'
    
    def replacer(match):
        inner = match.group(1)
        # On traite récursivement le contenu pour détecter d'éventuelles citations imbriquées.
        processed_inner = process_quotes(inner, level + 1)
        
        # Gestion de la ponctuation finale
        trailing = ""
        stripped = processed_inner.rstrip()
        if stripped:
            last_char = stripped[-1]
            # Si c'est une ponctuation qui doit être à l'intérieur, on la garde
            if last_char in PUNCTUATION_INSIDE:
                processed_inner = stripped
            # Si c'est une ponctuation qui peut être à l'extérieur, on la déplace
            elif last_char in PUNCTUATION_OUTSIDE:
                trailing = " " + last_char  # Ajout d'un espace avant la ponctuation
                processed_inner = stripped[:-1].rstrip()
        
        # Choix des guillemets en fonction du niveau d'imbrication
        if level == 0:
            # Premier niveau de citation interne → guillemets doubles typographiques
            opening = '«\u202F'
            closing = '\u202F»'
        else:
            # Deuxième niveau (et au-delà) → guillemets simples typographiques
            opening = '‹\u202F'
            closing = '\u202F›'
        
        return opening + processed_inner + closing + trailing

    return regex.sub(pattern, replacer, text)

def convert_quotes_starsector(text):
    """
    Convertit les citations internes d'un texte en respectant les règles suivantes :
      - Les délimiteurs externes (les guillemets encadrant la chaîne complète) restent intacts.
      - Au premier niveau interne, les citations sont encadrées par des guillemets typographiques doubles (« … »).
      - Au second niveau (citations imbriquées), les citations sont encadrées par des guillemets typographiques simples (‹ … ›).
      - La ponctuation finale d'une citation (si présente) est déplacée après le guillemet fermant.
    """
    # Préserver les structures spéciales
    if 'tips:[' in text or text.startswith('{'):
        return text
    
    # Gérer les guillemets échappés
    if '\\' in text:
        # Désescaper les guillemets pour le traitement
        text = text.replace('\\"', '"')
        # Traiter le texte normalement
        return convert_quotes_starsector(text)
    
    # Si la chaîne commence et se termine par un guillemet non échappé,
    # on considère qu'il s'agit des délimiteurs externes à préserver.
    if text.startswith('"') and text.endswith('"'):
        content = text[1:-1]
        processed = process_quotes(content, level=0)
        return '"' + processed + '"'
    else:
        return process_quotes(text, level=0)

def fix_quotes(text: str) -> str:
    """
    Corrige les guillemets dans une chaîne de caractères.
    
    Args:
        text: Texte à corriger
        
    Returns:
        Texte avec guillemets corrigés
    """
    return convert_quotes_starsector(text)

def convert_file_quotes(input_file, output_file=None):
    """
    Convertit les guillemets dans un fichier JSON de Starsector.
    Si output_file n'est pas spécifié, écrase le fichier d'entrée.

    Args:
        input_file (str): Chemin vers le fichier d'entrée
        output_file (str, optional): Chemin vers le fichier de sortie. Si None, écrase le fichier d'entrée.

    Returns:
        bool: True si la conversion a réussi, False sinon
    """
    try:
        # Lecture du fichier ligne par ligne
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Convertir chaque ligne
        converted_lines = []
        for line in lines:
            # Si c'est un commentaire ou une ligne contenant du texte
            if line.lstrip().startswith('#') or '"' in line:
                converted = convert_json_line(line)
                converted_lines.append(converted)
            else:
                converted_lines.append(line)

        # Écrire le résultat
        output_path = output_file if output_file else input_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.writelines(converted_lines)

        return True

    except Exception as e:
        print(f"Erreur lors de la conversion du fichier {input_file}: {str(e)}")
        return False

def convert_json_line(line):
    """
    Convertit une ligne de JSON en préservant la structure.
    
    Args:
        line (str): Ligne à convertir
        
    Returns:
        str: Ligne convertie
    """
    # Si c'est un commentaire, traiter spécialement
    if line.lstrip().startswith('#'):
        # Trouver les chaînes entre guillemets dans le commentaire
        pattern = r'(#[^"]*)?("(?:[^"\\]|\\.)*")'
        parts = re.split(pattern, line)
        
        # Convertir chaque partie
        result = []
        for i, part in enumerate(parts):
            if part:  # Ignorer les parties vides
                if i % 3 == 1:  # Texte avant les guillemets
                    result.append(part)
                elif i % 3 == 2:  # Chaîne entre guillemets
                    # Extraire le contenu sans les guillemets externes
                    content = part[1:-1]
                    # Convertir le contenu
                    converted = convert_quotes_starsector(f'"{content}"')[1:-1]
                    # Remettre les guillemets externes
                    result.append(f'"{converted}"')
                else:  # Texte après les guillemets
                    result.append(part)
        
        return ''.join(result)

    # Si c'est une ligne tips:[, la préserver
    if 'tips:[' in line:
        return line

    # Trouver toutes les chaînes JSON dans la ligne
    pattern = r'("(?:[^"\\]|\\.)*")'
    parts = re.split(pattern, line)
    
    # Convertir uniquement les valeurs, pas les clés
    result = []
    for i, part in enumerate(parts):
        if i % 2 == 1:  # Les parties impaires sont les chaînes trouvées
            # Si c'est une clé (se termine par :)
            if i > 0 and parts[i-1].rstrip().endswith(':'):
                result.append(part)
            # Si c'est une valeur
            else:
                # Extraire le contenu sans les guillemets externes
                content = part[1:-1]
                # Convertir le contenu
                converted = convert_quotes_starsector(f'"{content}"')[1:-1]
                # Remettre les guillemets externes
                result.append(f'"{converted}"')
        else:
            result.append(part)
    
    return ''.join(result)
