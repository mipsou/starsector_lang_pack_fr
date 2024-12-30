import os
import re
from striprtf.striprtf import rtf_to_text

def clean_text(text):
    """Nettoie et formate le texte extrait du RTF."""
    def escape_xml_tags(line):
        """Échappe les balises XML dans le texte normal"""
        if line.strip().startswith('```'):
            return line
        line = re.sub(r'<([^>]+)>', r'`<\1>`', line)
        return line
        
    def clean_special_chars(line):
        """Nettoie les caractères spéciaux"""
        return line.replace('­', '-').replace('`<,', '<').replace(',>`', '>').replace('\x00', '')
        
    # Prétraitement
    lines = text.split('\n')
    formatted_lines = []
    in_code_block = False
    seen_titles = set()  # Pour éviter les titres dupliqués
    
    for i, line in enumerate(lines):
        line = line.rstrip()
        line = clean_special_chars(line)
        
        # Ignorer les lignes vides consécutives et les titres vides
        if not line or line.strip() == '#' or line.strip() == '##':
            continue
            
        # Détecter les titres principaux (en gras dans le RTF)
        if line.startswith('\\b '):
            line = line.replace('\\b ', '').replace('\\b0', '')
            if not any(x in line.lower() for x in ['example:', 'usage:', '```', '###']):
                title = line.strip()
                if title not in seen_titles:  # Éviter les doublons
                    formatted_lines.append(f"\n## {title}\n")
                    seen_titles.add(title)
                continue
                
        # Détecter les sous-sections
        if line.endswith(':') and not line.startswith(('#', '```', '|')):
            title = line[:-1]
            if title not in seen_titles:  # Éviter les doublons
                formatted_lines.append(f"\n### {title}\n")
                seen_titles.add(title)
            continue
            
        # Détecter les blocs de code (indentés dans le RTF)
        if line.startswith('    ') and not in_code_block:
            # Vérifier s'il y a du contenu à mettre dans le bloc de code
            next_lines = [l.strip() for l in lines[i:i+5] if l.strip()]
            if len(next_lines) > 1:  # Au moins 2 lignes de contenu
                formatted_lines.append("\n```")
                in_code_block = True
                formatted_lines.append(line.strip())
            continue
            
        # Fermer le bloc de code
        if in_code_block and not line.startswith('    '):
            formatted_lines.append("```\n")
            in_code_block = False
            
        # Formater les exemples et l'usage
        if line == "Example:":
            formatted_lines.append("\n**Example:**")
            continue
        if line == "Usage:":
            formatted_lines.append("\n**Usage:**")
            continue
            
        # Formater les listes
        if line.lstrip().startswith('• '):
            formatted_lines.append(f"- {line.lstrip()[2:]}")
            continue
            
        # Formater les listes numérotées
        if re.match(r'^\d+\.\s', line):
            formatted_lines.append(line)
            continue
            
        # Échapper les balises XML dans le texte normal
        if not in_code_block:
            line = escape_xml_tags(line)
            
        # Ajouter la ligne si elle n'est pas déjà dans un bloc de code
        if not in_code_block or line.strip():
            formatted_lines.append(line)
    
    # Fermer le dernier bloc de code si nécessaire
    if in_code_block:
        formatted_lines.append("```")
        
    # Nettoyer les sauts de ligne multiples
    text = '\n'.join(formatted_lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    return text

def convert_rtf_to_md(input_file):
    print(f"Conversion de {input_file} en Markdown...")
    
    # Créer le dossier docs/markdown/rtf s'il n'existe pas
    output_dir = os.path.join(os.path.dirname(input_file), "..", "markdown", "rtf")
    os.makedirs(output_dir, exist_ok=True)
    
    # Lire le RTF
    with open(input_file, 'r', encoding='utf-8') as file:
        text = rtf_to_text(file.read())
    
    # Nettoyer et formater le texte
    md_text = clean_text(text)
    
    # Sauvegarder le fichier Markdown
    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + "_rtf.md")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(md_text)
    
    print(f"Conversion terminée. Fichier sauvegardé : {output_file}")

if __name__ == "__main__":
    convert_rtf_to_md("D:\\Fractal Softworks\\Starsector\\mods\\starsector_lang_pack_fr\\docs\\s3\\StarsectorRuleScripting.rtf")