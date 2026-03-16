#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de correction typographique pour les fichiers de traduction.
Corrige automatiquement les espaces autour des ponctuations et guillemets.
"""

import os
import sys
import re
import csv
from pathlib import Path
import chardet
import json

def is_utf8(content):
    """Vérifie si le contenu est encodé en UTF-8."""
    detector = chardet.UniversalDetector()
    for byte in content:
        detector.feed(byte)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding'] == 'utf-8'

def detect_encoding(content):
    """Détermine l'encodage du contenu."""
    detector = chardet.UniversalDetector()
    for byte in content:
        detector.feed(byte)
        if detector.done:
            break
    detector.close()
    return detector.result['encoding']

def fix_typography(text, preserve_tabs=False, preserve_colon_space=False, preserve_comments=False):
    """Corrige les espaces autour des ponctuations.
    
    Args:
        text (str): Texte à corriger
        preserve_tabs (bool): Préserve les tabulations
        preserve_colon_space (bool): Préserve l'espace après les deux points
        preserve_comments (bool): Préserve les commentaires
        
    Returns:
        str: Texte corrigé
    """
    # Ponctuation double (: ; ! ?)
    text = re.sub(r'\s*([;:!?])\s*', r' \1 ', text)
    
    # Points de suspension
    text = re.sub(r'\s*\.\.\.\s*', '... ', text)
    
    # Guillemets
    text = re.sub(r'"\s*([^"]+)\s*"', r' "\1" ', text)
    text = re.sub(r'«\s*([^»]+)\s*»', r' « \1 » ', text)
    
    # Nettoyage des espaces multiples
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    
    # Préserver les tabulations
    if preserve_tabs:
        text = text.replace('    ', '\t')
        
    # Préserver l'espace après les deux points
    if preserve_colon_space:
        text = text.replace(': ', ':')
        
    # Préserver les commentaires
    if preserve_comments:
        lines = text.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('#'):
                lines[i] = line.strip()
        text = '\n'.join(lines)
        
    return text
    
def preserve_comments(text):
    """Préserve les commentaires dans le texte.
    
    Args:
        text (str): Texte avec commentaires
        
    Returns:
        tuple: (texte sans commentaires, liste des commentaires avec leur position)
    """
    # Stocker les commentaires et leur position
    comments = []
    text_without_comments = text
    
    # Trouver tous les commentaires
    comment_pattern = r'#[^\n]*'
    for match in re.finditer(comment_pattern, text):
        start, end = match.span()
        comment = match.group()
        comments.append((start, end, comment))
        
    # Retirer les commentaires du texte
    if comments:
        # Trier les commentaires par position de fin décroissante
        comments.sort(key=lambda x: x[1], reverse=True)
        # Retirer les commentaires un par un
        for start, end, comment in comments:
            text_without_comments = text_without_comments[:start] + ' ' * (end - start) + text_without_comments[end:]
            
    return text_without_comments, comments

def restore_comments(text, comments):
    """Restaure les commentaires dans le texte.
    
    Args:
        text (str): Texte sans commentaires
        comments (list): Liste des commentaires avec leur position
        
    Returns:
        str: Texte avec commentaires restaurés
    """
    # Si pas de commentaires, retourner le texte tel quel
    if not comments:
        return text
        
    # Convertir le texte en liste de caractères pour faciliter les modifications
    text_chars = list(text)
    
    # Trier les commentaires par position de début croissante
    comments.sort(key=lambda x: x[0])
    
    # Restaurer les commentaires un par un
    offset = 0
    for start, end, comment in comments:
        # Ajuster les positions avec l'offset
        adj_start = start + offset
        adj_end = end + offset
        
        # Vérifier si la position est valide
        if adj_start < len(text_chars):
            # Remplacer les espaces par le commentaire
            text_chars[adj_start:adj_end] = list(comment)
            
            # Mettre à jour l'offset
            offset += len(comment) - (end - start)
            
    return ''.join(text_chars)

def get_original_format(file_path):
    """Récupère le format du fichier original.
    
    Args:
        file_path (str): Chemin du fichier à traiter
        
    Returns:
        dict: Informations de format du fichier original
    """
    # Trouver le fichier original correspondant
    original_path = file_path.replace('starsector_lang_pack_fr_private', 'starsector-core')
    if not os.path.exists(original_path):
        return None
        
    try:
        with open(original_path, 'rb') as f:
            content = f.read()
            
        # Détecter l'encodage
        encoding = chardet.detect(content)['encoding']
        if not encoding:
            encoding = 'utf-8'
            
        # Lire le contenu
        text = content.decode(encoding)
        
        # Analyser le format
        format_info = {
            'encoding': encoding,
            'uses_tabs': '\t' in text,
            'indent_size': 0,
            'line_endings': '\r\n' if '\r\n' in text else '\n',
            'has_space_after_colon': ': ' in text,
            'structure': text  # Pour préserver la structure exacte
        }
        
        # Détecter la taille d'indentation
        for line in text.split('\n'):
            if line.startswith(' '):
                spaces = len(line) - len(line.lstrip())
                if spaces > 0:
                    format_info['indent_size'] = spaces
                    break
                    
        return format_info
        
    except Exception as e:
        print(f"Erreur lors de l'analyse du format original : {str(e)}")
        return None

def get_original_file_path(file_path):
    """Trouve le chemin du fichier original correspondant.
    
    Args:
        file_path (str): Chemin du fichier à corriger
        
    Returns:
        str: Chemin du fichier original ou None si non trouvé
    """
    # Chercher dans starsector-core
    core_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(file_path)))), 
                            'starsector-core', 'data', 'strings', os.path.basename(file_path))
    if os.path.exists(core_path):
        return core_path
        
    # Chercher dans original/data/strings/
    original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(file_path))),
                                'original', 'data', 'strings', os.path.basename(file_path))
    if os.path.exists(original_path):
        return original_path
        
    return None

def compare_with_original(text, file_path):
    """Compare le texte avec le fichier original pour préserver le format exact.
    
    Args:
        text (str): Texte à comparer
        file_path (str): Chemin du fichier
        
    Returns:
        str: Texte corrigé selon le format original
    """
    # Trouver le fichier original
    original_path = get_original_file_path(file_path)
    if not original_path:
        print(f"Fichier original non trouvé pour {file_path}")
        return text
        
    try:
        # Lire le fichier original
        with open(original_path, 'r', encoding='utf-8') as f:
            original_text = f.read()
            
        # Analyser la structure
        original_lines = original_text.splitlines()
        text_lines = text.splitlines()
        
        # Vérifier l'indentation
        original_indent = ''
        text_indent = ''
        for line in original_lines:
            if line.strip():
                original_indent = re.match(r'^[\t ]*', line).group()
                break
        for line in text_lines:
            if line.strip():
                text_indent = re.match(r'^[\t ]*', line).group()
                break
                
        # Corriger l'indentation si nécessaire
        if original_indent != text_indent:
            text = text.replace(text_indent, original_indent)
            
        # Vérifier les sauts de ligne
        if '\r\n' in original_text:
            text = text.replace('\n', '\r\n')
            
        # Vérifier les espaces après les deux points
        if ':' in original_text:
            original_has_space = bool(re.search(r':\s', original_text))
            if not original_has_space:
                text = re.sub(r':\s+', ':', text)
                
        # Vérifier les virgules
        if ',' in original_text:
            original_has_space = bool(re.search(r',\s', original_text))
            if not original_has_space:
                text = re.sub(r',\s+', ',', text)
                
        # Vérifier les guillemets
        if '"' in original_text:
            # Préserver le style des guillemets de l'original
            original_quotes = re.findall(r'\\*"', original_text)
            text_quotes = re.findall(r'\\*"', text)
            for i, quote in enumerate(text_quotes):
                if i < len(original_quotes):
                    text = text.replace(quote, original_quotes[i], 1)
                    
        return text
        
    except Exception as e:
        print(f"Erreur lors de la comparaison avec l'original : {str(e)}")
        return text

def preprocess_json(text):
    """Prétraite le texte JSON pour le rendre compatible avec le parser.
    
    Args:
        text (str): Texte JSON à prétraiter
        
    Returns:
        str: Texte prétraité
    """
    # Supprimer les espaces autour des deux points
    text = re.sub(r'\s*:\s*', ':', text)
    
    # Supprimer les espaces après les virgules
    text = re.sub(r',\s+', ',', text)
    
    # Supprimer les espaces en début et fin de ligne
    text = '\n'.join(line.strip() for line in text.splitlines())
    
    return text

def normalize_json_content(text):
    """Normalise le contenu JSON pour le parsing.
    
    Args:
        text (str): Texte JSON à normaliser
        
    Returns:
        str: Texte normalisé
    """
    # Prétraiter le texte
    text = preprocess_json(text)
    
    # Sauvegarder les clés non quotées
    unquoted_keys = {}
    def save_unquoted_key(match):
        key = match.group(1)
        placeholder = f"__UNQUOTED_KEY_{len(unquoted_keys)}__"
        unquoted_keys[placeholder] = key
        return f'"{key}":'
    
    # Ajouter des guillemets aux clés non quotées
    text = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*):', save_unquoted_key, text)
    
    # Normaliser les guillemets
    text = text.replace('\\"', '__ESCAPED_QUOTE__')  # Préserver les guillemets déjà échappés
    text = text.replace('"', '\\"')  # Échapper les guillemets non échappés
    text = text.replace('__ESCAPED_QUOTE__', '\\"')  # Restaurer les guillemets déjà échappés
    
    # Normaliser les échappements
    text = re.sub(r'\\\s+', '\\\\', text)  # Corriger les espaces après les backslashes
    text = re.sub(r'\\{3,}', '\\\\', text)  # Réduire les backslashes multiples
    
    # Restaurer les clés non quotées
    for placeholder, key in unquoted_keys.items():
        text = text.replace(f'"{placeholder}":', f'{key}:')
    
    return text

def handle_special_json(text, file_path):
    """Gère les cas spéciaux de fichiers JSON avec une syntaxe non standard.
    
    Args:
        text (str): Texte à traiter
        file_path (str): Chemin du fichier
        
    Returns:
        tuple: (texte normalisé, est_tips_json)
    """
    is_tips_json = False
    
    # Cas spécial pour tips.json : pas de guillemets autour de tips
    if file_path.endswith('tips.json'):
        is_tips_json = True
        # Remplacer tips:[ par "tips":[ pour le parsing
        text = text.replace('tips:[', '"tips":[')
        
    # Cas spécial pour les autres fichiers JSON
    elif file_path.endswith('.json'):
        # Prétraiter le texte
        text = preprocess_json(text)
        
        # Sauvegarder les clés non quotées
        def quote_keys(match):
            return f'"{match.group(1)}":'
            
        # Ajouter des guillemets aux clés non quotées
        text = re.sub(r'([a-zA-Z_][a-zA-Z0-9_]*):', quote_keys, text)
        
    return text, is_tips_json

def fix_json_format(text, file_path):
    """Corrige le format JSON selon les standards Starsector.
    
    Args:
        text (str): Texte à corriger
        file_path (str): Chemin du fichier pour identifier le type
        
    Returns:
        str: Texte corrigé
    """
    # Si ce n'est pas un fichier JSON, retourner le texte tel quel
    if not file_path.endswith('.json'):
        return text
        
    # Si c'est tips.json, ne pas le modifier car il est déjà conforme
    if file_path.endswith('tips.json'):
        return text
        
    # Récupérer le format original
    original_format = get_original_format(file_path)
    if not original_format:
        return text
        
    # Préserver les commentaires
    text_without_comments, comments = preserve_comments(text)
    
    try:
        # Parser le JSON
        data = json.loads(text_without_comments)
        
        # Format standard
        text_without_comments = json.dumps(data, ensure_ascii=False, indent=4)
            
        # Comparer avec l'original pour préserver le format exact
        text_without_comments = compare_with_original(text_without_comments, file_path)
            
    except json.JSONDecodeError as e:
        print(f"Erreur lors du parsing JSON de {file_path}: {str(e)}")
        return text
        
    # Restaurer les commentaires
    text = restore_comments(text_without_comments, comments)
    
    return text

def fix_json_escapes(text, file_path):
    """Corrige les séquences d'échappement dans le JSON.
    
    Args:
        text (str): Texte JSON à corriger
        file_path (str): Chemin du fichier pour identifier le type
        
    Returns:
        str: Texte avec échappements corrigés
    """
    # Si ce n'est pas un fichier JSON, retourner le texte tel quel
    if not file_path.endswith('.json'):
        return text
        
    # Préserver les commentaires
    text_without_comments, comments = preserve_comments(text)
    
    try:
        # Gérer les cas spéciaux
        normalized, is_tips_json = handle_special_json(text_without_comments, file_path)
        
        # Normaliser le contenu pour le parsing
        normalized = normalize_json_content(normalized)
        
        # Parser le JSON normalisé
        data = json.loads(normalized)
        
        # Récupérer le format original
        original_format = get_original_format(file_path)
        if original_format:
            original_text = original_format['structure']
            
            # Analyser les échappements dans le fichier original
            escape_pattern = r'\\["\\/bfnrt]'
            original_escapes = set(re.findall(escape_pattern, original_text))
            
            # Appliquer les mêmes types d'échappements
            for escape in original_escapes:
                # Trouver le caractère non échappé correspondant
                char = escape[1]  # Le caractère après le \
                # Échapper toutes les occurrences de ce caractère
                text_without_comments = text_without_comments.replace(char, escape)
                
        # Sérialiser le JSON avec les échappements corrects
        if is_tips_json:
            # Restaurer le format spécial pour tips.json
            text_without_comments = text_without_comments.replace('"tips":[', 'tips:[')
        else:
            # Pour les autres fichiers, utiliser le format standard
            text_without_comments = json.dumps(data, ensure_ascii=False, indent=None)
            
        # Comparer avec l'original pour préserver le format exact
        text_without_comments = compare_with_original(text_without_comments, file_path)
            
    except json.JSONDecodeError as e:
        print(f"Erreur JSON après correction des échappements : {str(e)}")
        return text
        
    # Restaurer les commentaires
    text = restore_comments(text_without_comments, comments)
    
    return text

def fix_file(file_path):
    """Corrige la typographie et le format d'un fichier.
    
    Args:
        file_path (str): Chemin du fichier à corriger
        
    Returns:
        bool: True si la correction a réussi, False sinon
    """
    try:
        # Récupérer le format original
        original_format = get_original_format(file_path)
        if not original_format:
            print(f"Impossible de trouver le fichier original pour {file_path}")
            return False
            
        # Lire le fichier à corriger
        with open(file_path, 'rb') as f:
            content = f.read()
            
        # Utiliser l'encodage du fichier original
        encoding = original_format['encoding']
        if not encoding:
            encoding = 'utf-8'
            
        try:
            # Essayer de décoder avec l'encodage original
            text = content.decode(encoding)
        except UnicodeDecodeError:
            # Si échec, détecter l'encodage actuel
            result = chardet.detect(content)
            source_encoding = result['encoding']
            if not source_encoding:
                source_encoding = 'ascii'
            text = content.decode(source_encoding)
            
        # Préserver les commentaires avant toute modification
        text_with_comments, comments = preserve_comments(text)
        
        # Appliquer le format JSON spécifique à Starsector
        text = fix_json_format(text_with_comments, file_path)
        
        # Corriger les échappements JSON
        text = fix_json_escapes(text, file_path)
        
        # Restaurer les commentaires
        text = restore_comments(text, comments)
        
        # Appliquer les corrections typographiques en préservant le format exact
        text = fix_typography(text, 
                            preserve_tabs=original_format['uses_tabs'],
                            preserve_colon_space=original_format['has_space_after_colon'],
                            preserve_comments=True)
        
        # Convertir en UTF-8 si nécessaire
        if file_path.endswith('.json'):
            # Forcer l'encodage UTF-8 pour les fichiers JSON
            encoding = 'utf-8'
            
        # Sauvegarder avec l'encodage approprié
        with open(file_path, 'wb') as f:
            f.write(text.encode(encoding))
            
        print(f"Corrections appliquées à {file_path} (encodage: {encoding})")
        return True
            
    except Exception as e:
        print(f"Erreur lors de la correction de {file_path}: {str(e)}")
        return False
        
def fix_directory(directory):
    """Corrige la typographie des fichiers dans un répertoire.
    
    Args:
        directory (str): Chemin du répertoire
        
    Returns:
        tuple: (int, int) Nombre de fichiers traités et corrigés
    """
    processed = 0
    fixed = 0
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.json', '.txt', '.csv')):
                file_path = os.path.join(root, file)
                processed += 1
                if fix_file(file_path):
                    fixed += 1
                    
    return processed, fixed
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python fix_typography.py <directory>")
        sys.exit(1)
        
    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Le répertoire {directory} n'existe pas")
        sys.exit(1)
        
    processed, fixed = fix_directory(directory)
    print(f"\nRésumé :")
    print(f"- Fichiers traités : {processed}")
    print(f"- Fichiers corrigés : {fixed}")
