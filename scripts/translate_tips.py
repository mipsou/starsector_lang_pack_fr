#!/usr/bin/env python3
"""
Script de traduction pour le fichier tips.json de Starsector

Ce script traduit les conseils du jeu en français en respectant :
- Le format JSON spécifique de Starsector
- Les règles typographiques françaises
- L'encodage UTF-8 et les sauts de ligne Unix
- Les dispositions de clavier QWERTY/AZERTY/BÉPO

Auteur: Mipsou
Date: 2025-01-22
"""

import json
import sys
import os
from pathlib import Path
import re

# Ajout du répertoire des scripts au PYTHONPATH
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from utils import fix_quotes, format_starsector_json, check_encoding

def fix_quotes(text):
    """Corrige les guillemets et apostrophes dans un texte.
    
    Args:
        text (str): Texte à corriger
        
    Returns:
        str: Texte avec guillemets et apostrophes corrigés
    """
    # Remplacer les guillemets français par des guillemets droits
    text = text.replace('«', '"').replace('»', '"')
    text = text.replace('"', '"').replace('"', '"')
    
    # Remplacer les apostrophes courbes par des apostrophes droites
    text = text.replace(''', "'").replace(''', "'")
    
    # Préserver HARD et SOFT sans échappement
    text = text.replace('\\"HARD\\"', '"HARD"')
    text = text.replace('\\"SOFT\\"', '"SOFT"')
    
    # Supprimer les espaces en trop
    text = ' '.join(text.split())
    
    # Ajouter un point final si nécessaire
    if text and not text.endswith(('.', '?', '!')):
        text += '.'
        
    return text

def merge_tips(tips):
    """Fusionne les tips qui sont coupés.
    
    Args:
        tips (list): Liste des tips à fusionner
        
    Returns:
        list: Liste des tips fusionnés
    """
    merged = []
    i = 0
    while i < len(tips):
        tip = tips[i].strip().strip('"')
        
        # Si le tip actuel se termine par un antislash ou n'a pas de point final
        # et que le prochain tip existe et n'est pas un objet JSON
        if i + 1 < len(tips):
            next_tip = tips[i + 1].strip().strip('"')
            if not tip.endswith('.') and not next_tip.startswith('{'):
                # Vérifier si ce n'est pas un tip déjà complet
                if not (tip.endswith('?') or tip.endswith('!')):
                    tip = f"{tip} {next_tip}"
                    i += 2
                    merged.append(f'"{fix_quotes(tip)}"')
                    continue
                
        if tip.startswith('{'):
            # C'est un objet JSON
            try:
                if match := re.search(r'{\s*"freq"\s*:\s*(\d+)\s*,\s*"tip"\s*:\s*"(.+?)"\s*}', tip):
                    freq = int(match.group(1))
                    tip_text = fix_quotes(match.group(2))
                    merged.append(f'{{"freq": {freq}, "tip": "{tip_text}"}}')
            except Exception as e:
                print(f"Erreur avec l'objet: {tip}")
                print(f"Exception: {e}")
        else:
            merged.append(f'"{fix_quotes(tip)}"')
            
        i += 1
        
    return merged

def translate_tips(keyboard_layout='azerty', force=True):
    """Traduit le fichier tips.json en respectant les règles typographiques.
    
    Args:
        keyboard_layout (str): Disposition du clavier à utiliser
        force (bool): Force l'écrasement du fichier existant
    """
    try:
        # Chemins des fichiers
        base_dir = Path(SCRIPT_DIR).parent
        tips_file = base_dir / 'data' / 'strings' / 'tips.json'
        
        # Créer le répertoire parent si nécessaire
        tips_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Préparer les tips
        formatted_tips = []
        
        # Ajouter le premier tip avec freq=0
        formatted_tips.append('{"freq":0, "tip":"Vous pouvez modifier la fréquence des conseils en ajoutant un objet json au lieu d\'une chaîne de caractères, comme ceci. Par exemple, ce conseil a une fréquence de 0 et n\'apparaîtra jamais. La valeur de fréquence par défaut est 1."}')
        
        # Ajouter les tips avec HARD et SOFT
        formatted_tips.append('"Baissez vos boucliers pour dissiper le flux \\"HARD\\" généré par les dégâts aux boucliers."')
        formatted_tips.append('"Les boucliers et les armes génèrent tous deux du flux, donc baisser vos boucliers pour encaisser quelques coups sur la coque et l\'armure augmentera votre puissance de feu soutenue. Cela peut être vital, en particulier pour les vaisseaux lourdement blindés."')
        formatted_tips.append('"Les dégâts des armes à faisceau sur les boucliers génèrent un flux \\"SOFT\\" qui peut être dissipé sans baisser les boucliers."')
        
        # Ajouter les autres tips
        formatted_tips.extend([
            '"Appuyez sur TAB pour activer l\'interface de commandement. Utilisez l\'interface de commandement pour donner des ordres à votre flotte."',
            '"Ordonner à un vaisseau d\'en escorter un autre limite la mobilité de l\'escorte. Utilisez cette commande avec précaution."',
            '"Si vos boucliers subissent trop de dégâts, le vaisseau sera en surcharge et les armes et boucliers seront désactivés pendant quelques secondes."',
            '"Les missiles à longue portée (LRM) peuvent toucher des cibles au-delà de la portée visuelle. Appuyez sur Tab pour ouvrir l\'interface de commandement et cibler les vaisseaux éloignés en cliquant dessus puis en sélectionnant \'Définir comme Cible\'."',
            '"Au combat, déplacez la souris pour faire défiler la vue. Appuyez sur \'T\' pour verrouiller votre vue sur votre cible et appuyez à nouveau sur \'T\' pour revenir à la vue normale."',
            '"Appuyez sur le bouton gauche de la souris pour tirer et sur le bouton droit pour utiliser les boucliers. Utilisez ZQSD pour piloter le vaisseau."',
            '"Les dégâts cinétiques sont efficaces contre les boucliers, tandis que les dégâts hautement explosifs sont efficaces contre l\'armure."',
            '"Les dégâts de fragmentation sont faibles contre tout sauf la coque exposée, mais les armes qui en infligent ont tendance à être très efficaces en termes de flux."',
            '"Les armes énergétiques sont également efficaces contre les boucliers et l\'armure, mais ne sont pas aussi bonnes que les types de dégâts plus spécialisés contre l\'un ou l\'autre."',
            '"Un emplacement d\'arme à missiles est polyvalent - il existe des missiles pour pratiquement tous les rôles - mais les lanceurs de missiles ont généralement très peu de munitions."',
            '"Tirer avec des armes ou utiliser les boucliers accumule du flux. Lorsque le niveau de flux est au maximum, vous devrez attendre qu\'il baisse avant de pouvoir tirer à nouveau."',
            '"Les vaisseaux reçoivent un bonus de vitesse maximale lorsque leur niveau de flux est à zéro et qu\'ils ne génèrent pas de flux."',
            '"Lors du réaménagement d\'un vaisseau, maintenez Shift en cliquant sur un emplacement d\'arme pour installer l\'arme précédemment sélectionnée sans ouvrir le menu de sélection d\'armes."',
            '"Lors de la création de groupes d\'armes pour un vaisseau, maintenez Shift en cliquant pour assigner toutes les armes du même type."',
            '"Lors de l\'édition d\'un champ de texte, vous pouvez appuyer sur Shift-Retour arrière pour l\'effacer ou Ctrl-Retour arrière pour supprimer le dernier mot."',
            '"La plupart du commerce sur le marché libre est rendu non rentable par les tarifs. Exploitez les événements en cours et les perturbations pour faire du profit."',
            '"Maintenez Shift en ajoutant ou retirant des évents ou des condensateurs de flux pour le faire plus rapidement."',
            '"Maintenez Shift en utilisant la molette de la souris pour défiler plus rapidement."',
            '"Ctrl-clic pour acheter/vendre un lot. Shift-clic pour prendre les objets un par un. Maintenez Shift et cliquez-glissez pour sélectionner une quantité spécifique."',
            '"Pour faire défiler la carte en combat, faites un clic droit et glissez ou utilisez les touches fléchées."',
            '"Lancer des torpilles à bout portant peut être dangereux pour votre vaisseau."',
            '"Les vaisseaux avec une désignation (D) sont des versions inférieures des coques normales."',
            '"Déployer des vaisseaux en combat réduit leur état de préparation au combat (\\"CR\\"), qui coûte des ressources à récupérer."',
            '"Déployer plus de vaisseaux que nécessaire en combat peut coûter plus de ressources que ce que vous gagnez en combattant."',
            '"Les vaisseaux consomment des ressources pour l\'entretien en fonction de leur statistique ressources/mois et consomment des ressources supplémentaires lors de la récupération du CR ou des réparations."',
            '"Votre flotte peut transporter du cargo, de l\'équipage ou du carburant au-delà de sa capacité maximale au prix d\'une consommation supplémentaire de ressources."',
            '"Vous pouvez obtenir des informations supplémentaires de nombreuses infobulles en appuyant sur F1 pour les développer."',
            '"Plus d\'armes n\'est pas toujours mieux - avoir assez de capacité et de dissipation de flux pour un tir soutenu peut être plus important."',
            '"Réaménager un vaisseau dans l\'espace réduira son état de préparation au combat, particulièrement lors du changement de modifications de coque."',
            '"Les armes qui tirent des projectiles énergétiques ou des projectiles peuvent toucher des cibles au-delà de leur portée maximale, mais n\'infligent que des dégâts de flux doux aux boucliers dans ce cas."',
            '"Vous pouvez créer des groupes de vaisseaux en utilisant Ctrl et les touches numériques et les sélectionner avec les touches numériques. Cela fonctionne à la fois en combat et dans le dialogue de déploiement."',
            '"Les porte-avions arrêteront de lancer des chasseurs de remplacement une fois que leur état de préparation au combat atteint 0%."',
            '"Les porte-avions armés uniquement d\'armes de défense ponctuelle et de missiles tenteront de se tenir à l\'écart des vaisseaux ennemis."',
            '"Appuyez sur \'Z\' pour basculer entre ordonner aux chasseurs d\'un porte-avions d\'attaquer ou de se replier vers le porte-avions."',
            '"Ordonner aux chasseurs de se regrouper fera baisser plus lentement le taux de remplacement du porte-avions et fera en sorte que les escadrilles endommagées tentent de s\'abriter derrière le porte-avions."',
            '"Lorsque vous pilotez un porte-avions, ses chasseurs escorteront un vaisseau allié si le porte-avions le cible et continueront à l\'escorter jusqu\'à ce qu\'ils soient rappelés, même si la cible est effacée."',
            '"Les bombardiers ont un potentiel de dégâts élevé, mais fonctionnent mieux lorsqu\'ils sont combinés avec d\'autres chasseurs, armes et vaisseaux pour s\'assurer qu\'ils peuvent infliger les dégâts."',
            '"Les augmentations en pourcentage sont additives. Les réductions en pourcentage sont généralement multiplicatives."',
            '"Les flottes se déplaçant lentement n\'attirent pas les frappes de tempête dans l\'hyperespace."',
            '"Les armes ont un recul réduit de moitié lorsqu\'elles sont montées dans des emplacements de tourelle."',
            '"Saborder un vaisseau - ou simplement ne pas le récupérer - produira plus de valeur en carburant et en ressources que sa vente."',
            '"Si un système stellaire a peu d\'emplacements stables, vous pouvez en créer un nouveau en interagissant avec l\'étoile."',
            '"Assigner des marines pour attaquer un objectif à faible danger peut créer une diversion et réduire les pertes d\'un raid dangereux plus que de garder ces marines en réserve."',
            '"Le camp avec le plus d\'officiers compétents aux commandes de vaisseaux prêts au combat obtient plus de points de déploiement."',
            '"Les vaisseaux avec des officiers ou des s-mods sont presque toujours récupérables s\'ils sont perdus au combat. Certaines compétences et modifications de coque peuvent également rendre d\'autres vaisseaux toujours récupérables."',
            '"Saborder ou perdre un vaisseau avec des s-mods que vous y avez intégrés accorde assez d\'XP bonus pour récupérer les points d\'histoire dépensés pour la construction des modifications de coque."',
            '"Les courants stellaires sont temporaires et, dans la mémoire récente, synchronisés avec le cycle standard du Domaine. Dans la première moitié du cycle, ils ont tendance à s\'écouler vers l\'est galactique, et dans la seconde moitié, vers l\'ouest."',
            '"Pendant une poursuite, vous pouvez déployer des frégates depuis les flancs en cliquant dessus plusieurs fois pour changer le mode de déploiement."',
            '"Les modifications de coque avec un faible coût en points d\'ordonnance ont tendance à avoir des bonus plus puissants lorsqu\'elles sont intégrées à la coque en utilisant un point d\'histoire. Les modifications plus coûteuses ont tendance à avoir des pénalités."'
        ])
        
        # Sauvegarder
        output = "{\n\ttips:[\n\t\t" + ",\n\t\t".join(formatted_tips) + "\n\t]\n}"
        with open(tips_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(output)
            
        print(f"Formaté {len(formatted_tips)} tips")
        return True
            
    except Exception as e:
        print(f"Erreur lors de la traduction: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python translate_tips.py keyboard_layout")
        print("  keyboard_layout : qwerty, azerty, ou bepo")
        sys.exit(1)
        
    translate_tips(sys.argv[1])
