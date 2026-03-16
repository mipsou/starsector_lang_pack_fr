#!/usr/bin/env python3
import json
import os
import re

def clean_json(content):
    """Nettoie le JSON des commentaires."""
    # Supprimer les commentaires
    content = re.sub(r'^\s*#.*$', '', content, flags=re.MULTILINE)
    # Supprimer les lignes vides
    content = re.sub(r'\n\s*\n', '\n', content)
    # Supprimer les virgules finales
    content = re.sub(r',(\s*[}\]])', r'\1', content)
    return content

def translate_strings():
    """Traduit strings.json en français."""
    # Dictionnaire de traduction
    translations = {
        # FleetInteractionDialog
        "initialWithStationVsLargeFleet": "Le $fleetOrShip de la $faction manœuvre pour rester soutenu par la station, permettant à votre flotte de se désengager. Cependant, vos forces risquent d'être harcelées pendant leur repli.",
        "initialAggressive": "Le $fleetOrShip de la $faction manœuvre pour vous empêcher de vous désengager facilement.",
        "initialDisengage": "Le $fleetOrShip de la $faction tente de se désengager.",
        "initialCareful": "Le $fleetOrShip de la $faction maintient prudemment sa distance, prêt à se désengager en cas d'hostilités.",
        "initialNeutral": "Le $fleetOrShip de la $faction adopte une posture neutre.",
        "initialHoldVsStrongerEnemy": "Le $fleetOrShip de la $faction semble prêt à combattre malgré des forces supérieures, mais ne cherchera probablement pas l'affrontement.",
        
        # Combat
        "retreat": "Retraite",
        "engage": "Engager le combat",
        "pursue": "Poursuivre",
        "hold": "Tenir position",
        "enemyHarass": "Les forces ennemies harcèlent vos vaisseaux pendant leur retraite, causant beaucoup de perturbations, mais ne forcent finalement pas le combat.",
        "enemyUnableToPursue": "Les vaisseaux ennemis sont incapables de poursuivre, permettant à vos forces de se retirer sans autre incident.",
        "enemyDecidesNotToPursue": "Les vaisseaux ennemis ne font aucun mouvement pour poursuivre, permettant à vos forces de se retirer sans autre incident.",
        "enemyPursuit": "La flotte ennemie poursuit vos forces.",
        
        # Interface
        "confirm": "Confirmer",
        "cancel": "Annuler",
        "back": "Retour",
        "next": "Suivant",
        "close": "Fermer",
        "dismiss": "Fermer",
        "approach": "Votre $fleetOrShip approche du point de saut.",
        
        # Messages
        "victory": "Victoire !",
        "defeat": "Défaite...",
        "warning": "Attention !",
        "error": "Erreur",
        "success": "Succès",
        
        # Tooltips
        "tooltipCleanDisengage": "Termine la bataille sans risque d'être harcelé par la flotte adverse.\n\nComme l'ennemi reste maître du champ de bataille, vous ne pourrez pas effectuer d'opérations de récupération.\n\nSi votre flotte n'a pas entrepris d'actions hostiles, le désengagement n'affectera pas votre réputation auprès de la faction adverse.",
        "tooltipHarrassableDisengage": "Termine la bataille sans risque de poursuite. La flotte adverse peut toutefois harceler votre retraite.\n\nComme l'ennemi reste maître du champ de bataille, vous ne pourrez pas effectuer d'opérations de récupération.\n\nSi votre flotte n'a pas entrepris d'actions hostiles, le désengagement n'affectera pas votre réputation auprès de la faction adverse.",
        "tootipAttemptToDisengage": "Tente de battre en retraite. La flotte adverse peut vous poursuivre et forcer le combat, ou vous laisser partir.\n\nComme l'ennemi reste maître du champ de bataille, vous ne pourrez pas effectuer d'opérations de récupération.\n\nSi votre flotte n'a pas entrepris d'actions hostiles, le désengagement - sans endommager les vaisseaux poursuivants - aura le moins d'impact sur votre réputation auprès de la faction adverse.",
        
        # Campaign Help
        "chmNewgame_text": "Bienvenue dans la campagne Starsector !\n\nVous pouvez appuyer sur F5 pour faire une sauvegarde rapide et F9 pour la charger.\n\nÉvitez d'affronter des flottes beaucoup plus grandes que la vôtre, ou celles qui ont des vaisseaux plus imposants, et n'oubliez pas que c'est un travail en cours, donc des bugs peuvent parfois survenir.\n\nBonne chance !",
        "chmNewgame_dismiss": "Fermer",
        "chmNewgameIron_text": "Bienvenue dans la campagne Starsector !\n\nComme vous jouez en mode Iron, vous ne pourrez sauvegarder qu'en quittant le jeu, et vous ne pourrez pas charger une autre partie sans d'abord quitter (et sauvegarder) votre partie actuelle.\n\nÉvitez d'affronter des flottes beaucoup plus grandes que la vôtre, ou celles qui ont des vaisseaux plus imposants, et n'oubliez pas que c'est un travail en cours, donc des bugs peuvent parfois survenir.\n\nBonne chance !",
        "chmNewgameIron_dismiss": "Fermer",
        "chmLootOverCapacity_text": "Attention : vous prenez plus de butin que votre flotte ne peut en transporter.\n\nCela entraînera une augmentation significative de la consommation quotidienne de ravitaillement et une réduction de la vitesse de déplacement.\n\nIl est recommandé soit de prendre moins de butin, soit de vous diriger vers une station proche pour vendre l'excédent.",
        "chmLootOverCapacity_dismiss": "Fermer",
        "chmOverCargoCapacity_text": "Votre flotte transporte plus de cargo que sa capacité ne le permet.\n\nCela entraînera une augmentation significative de la consommation quotidienne de ravitaillement et une réduction de la vitesse de déplacement.\n\nIl est recommandé soit de jeter une partie du cargo maintenant, soit de vous diriger rapidement vers une station pour vendre l'excédent. Vous pouvez jeter du cargo depuis l'écran équipage/cargo.",
        "chmOverCargoCapacity_action": "Ouvrir l'écran équipage/cargo",
        "chmOverCargoCapacity_dismiss": "Fermer",
        "chmAllCritCR_text": "Tous les vaisseaux de votre flotte sont à un niveau de préparation au combat dangereusement bas (moins de 20%).\n\nDéployer ces vaisseaux au combat risque de provoquer des dysfonctionnements critiques - causant des dégâts, désactivant certaines armes et moteurs pendant la bataille, et provoquant d'autres dysfonctionnements critiques pendant le déploiement.\n\nIl est recommandé de laisser votre flotte récupérer avant d'engager le combat. Les vaisseaux regagnent leur préparation au combat avec le temps, et les stations amies offrent un moyen rapide de le faire et d'effectuer des réparations, ainsi que d'embaucher de l'équipage supplémentaire si nécessaire.\n\nVous pouvez vérifier les niveaux de préparation au combat de vos vaisseaux dans l'écran de flotte.",
        "chmAllCritCR_action": "Ouvrir l'écran de flotte",
        "chmAllCritCR_dismiss": "Fermer",
        "chmSupplyUseAfterBattle_text": "La consommation de ravitaillement de votre flotte vient d'augmenter !\n\nLa récupération de la préparation au combat des vaisseaux déployés coûte des ravitaillements, tout comme la réparation des dégâts de bataille.\n\nPour réduire l'utilisation des ravitaillements, les réparations et la récupération de PC des vaisseaux peuvent être suspendues depuis l'écran de flotte.",
        "chmSupplyUseAfterBattle_action": "Ouvrir l'écran de flotte",
        "chmSupplyUseAfterBattle_dismiss": "Fermer",
    }
    
    src = 'original/data/strings/strings.json'
    dst = 'localization/data/strings/strings_fr.json'
    
    # Lire et nettoyer le fichier source
    with open(src, 'r', encoding='utf-8') as f:
        content = f.read()
    content = clean_json(content)
    data = json.loads(content)
    
    # Traduire récursivement
    def translate_dict(d):
        for k, v in d.items():
            if isinstance(v, dict):
                translate_dict(v)
            elif isinstance(v, str):
                if v in translations:
                    d[k] = translations[v]
                elif k in translations:
                    d[k] = translations[k]
    
    # Appliquer les traductions
    translate_dict(data)
    
    # Sauvegarder avec les commentaires originaux
    with open(dst, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("Traduction terminée !")

if __name__ == "__main__":
    translate_strings()
