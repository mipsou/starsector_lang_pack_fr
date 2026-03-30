#!/usr/bin/env python3
"""Translate remaining GALLERY batch files EN→FR."""
import json, os, glob

BATCH_DIR = os.path.join(os.path.dirname(__file__), "gallery_batches")

TRANSLATIONS = {
    "hesperus": ("Hesperus", "Des monastères s'accrochaient aux promontoires sublimes qui ceinturaient les provinces volcaniques percées à travers la glace enveloppant le monde. Des pèlerins peu nombreux mais déterminés faisaient le voyage périlleux pour chercher la sagesse de ceux qui avaient renoncé au confort matériel."),
    "hesperus_shrine": ("Sanctuaire d'Hesperus", "Le sol était un champ soudé de plaques blindées patinées en motifs complexes par les atmosphères variées des mondes sur lesquels ces plaques avaient autrefois servi. Des bougies projetaient une lumière vacillante sur un autel simple où reposaient des reliques de l'ère du Domain."),
    "killa_shrine": ("Sanctuaire de Killa", "Il y avait des orbites vides, des cages thoraciques, des fémurs et des colonnes vertébrales encastrés dans des renfoncements, intégrés dans des piliers, couvrant chaque surface. Les os d'anciens fidèles composaient l'architecture même du sanctuaire, un mémorial macabre à la dévotion."),
    "volturn_shrine": ("Sanctuaire de Volturn", "Il était rempli d'armes, d'explosifs, de grenades, de chargeurs cellulaires. Des caisses et des râteliers empilés haut. Le sanctuaire lui-même était installé sous un filet de camouflage, caché des regards indiscrets des autorités."),
    "volturn_shrine_fake": ("Sanctuaire de Volturn, factice", "C'était une triste chose installée au fond d'une arrière-salle, des rangées de bougies disposées autour de la pièce centrale en bois sculptée d'images de saints Luddic. Un leurre pour les inspecteurs, rien de plus."),
    "protest": ("Manifestation", "L'avancée régulière de la gendarmerie brisa la ligne de protestation, les aiguillons de choc montaient et descendaient au rythme de cris étouffés et de hurlements silencieux sur les visages de ceux qui tombaient."),
    "raid_prepare": ("Préparation au Raid", "Chaque escouade se préparait comme pour une chirurgie, calme et précise. L'enfer était prêt à se déverser une fois que les charges de brèche auraient fait exploser les sas."),
    "raid_valuables_result": ("Raid pour Ressources", "Des chocs sourds, presque subsoniques, se faisaient sentir à travers la masse blindée. Des charges de brèche. Quand les marines percèrent enfin les portes blindées, ce qu'ils trouvèrent à l'intérieur valait bien le risque."),
    "raid_disrupt_result": ("Raid de Perturbation", "Le raid pivota sur de simples minutes de chaos. Les communications à travers l'hémisphère crépitaient de parasites ; seuls les relais à faisceau étroit pouvaient percer le brouillage."),
    "raid_covert_result": ("Raid Secret", "Les escouades de marines se retirèrent, laissant derrière elles des cloisons brisées et des alarmes hurlantes parmi les tirs de riposte sporadiques. La MUNISEC était dépassée, au moins temporairement."),
    "fikenhild": ("Fikenhild", "La petite lune océanique de Fikenhild était le centre politique du système, siège du Roi et représentant auprès de la Ligue Persane."),
    "ilm": ("Ilm", "Plus qu'une ville d'entreprise, Ilm était un monde d'entreprise, des plateformes de sécurité orbitales brillant au-dessus jusqu'aux mines téléopérées en dessous."),
    "teahouse": ("Salon de Thé Luddic", "Un brute de la brigade des mœurs toisait tous ceux qui entraient. Ils pouvaient fermer l'endroit à tout moment, mais le salon de thé clandestin fournissait un service que même les autorités appréciaient secrètement."),
    "mazalot": ("Mazalot", "Ils vous guidèrent à travers une ville de briques enduites et de récupération corrodée. De la peinture vive et des jardins luxuriants réussissaient, tout juste, à masquer la désolation sous-jacente."),
    "chalcedon": ("Chalcédoine", "L'architecture chalcédonienne tendait vers le cyclopéisme en surface. En dessous, protégées des tempêtes, se trouvaient les mêmes chambres claustrophobes et les mêmes tunnels étroits que partout ailleurs dans le Secteur."),
    "sentinel": ("Sentinel, la Colonie Perdue", "Il y avait un groupe de structures basses et soignées ; des ouvrages de terre et des panneaux de coque parsemés de verre forgé, hérissés de bouches d'aération. La dernière lueur d'une civilisation qui refusait de s'éteindre."),
    "gate_hauler1": ("Découverte du Transporteur de Portail", "Un Léviathan surgi du temps, familier d'emblée par ses représentations dans le Secteur Persane post-Domain. La forme magistrale du vaisseau portait les cicatrices d'éons de dérive."),
    "gate_hauler2": ("Transporteur de Portail en Vol", "C'étaient les vaisseaux stellaires massifs et automatisés qui transportaient les Portails établissant des connexions quasi-instantanées entre les systèmes stellaires, le réseau qui maintenait le Domain uni."),
    "bombard_prepare": ("Préparation au Bombardement", "\"Si c'est juste suivre les ordres, c'est pas moi qui vais contre la convention. Alors c'est sur le capitaine. Pas vrai ?\""),
    "bombard_tactical_result": ("Bombardement Tactique", "Une éclaboussure d'icônes évidées représentait des cibles mortes sur l'affichage. La dernière, pleine et rouge, cligna pour s'éteindre dans un cercle creux."),
    "bombard_saturation_result": ("Bombardement de Saturation", "Quand Loke vint de l'Abîme /\nLe premier monde, il le brûla /\nLe deuxième, il le prit sans un tir /\nLe troisième — attention, le troisième..."),
    "crew_leaving": ("Équipage Impayé", "\"Le contrat peut aller se faire aspirer par le vide. Pas de crédits, pas d'équipage.\""),
    "nav_buoy": ("Bouée de Navigation", "Une bouée de navigation datant de l'ère du Domain surveillait la topographie locale de l'hyperchamp du système. La télémétrie était d'une grande utilité pour les navigateurs du Secteur."),
    "free_orbit": ("Orbite Libre", "Je lui ai demandé ce qui l'attirait là-bas, encore et encore. Le vieux spacer a mis longtemps avant de répondre.\n\n\"Parce que c'est le seul endroit où personne ne peut me dire quoi faire.\""),
    "sensor_array": ("Réseau de Capteurs", "Le réseau de l'ère du Domain pouvait surveiller passivement un système stellaire entier et disposait d'un émetteur capable de transmission cryptée en temps réel vers les relais de communication voisins."),
    "sensor_array_makeshift": ("Réseau de Capteurs, Improvisé", "Les réseaux de capteurs improvisés construits avec une technologie post-Effondrement surveillaient passivement des systèmes stellaires entiers. Un émetteur embarqué relayait les données vers les relais de communication voisins."),
    "galatia_academy": ("Académie Galatia", "L'Académie Galatia est l'université la plus prestigieuse du Secteur Persane. Le bureau du prévôt dirige l'enseignement et la recherche depuis son campus orbital au-dessus d'Ancyra."),
    "fusion_lamp": ("Lampe à Fusion", "\"Ne soyez pas trop impressionné, marcheur. C'est une pâle imitation du premier jour de Dieu.\""),
    "salvor_ruins": ("Récupérateurs dans les Ruines", "Cela semblait vide au début. Un tombeau colossal, jamais rempli.\n\nUn radar monté sur drone dessina un schéma fantomatique tandis que les projecteurs des combinaisons balayaient les ténèbres, révélant l'ampleur de ce qui avait été laissé derrière."),
    "salvor_explore_hull": ("Exploration d'Épave", "\"On dit qu'un ex-récupérateur est soit vieux soit riche, jamais les deux.\""),
    "dead_zero_g": ("Mort en Apesanteur", "\"C'est trouver les morceaux le pire. Pas tant là dehors, congelés ou grillés, mais ces bouts qui restent collés jusqu'à ce qu'on les gratte de l'intérieur du casque.\""),
    "cache_large": ("Grande Cache", "Une structure immense se dressait, les facettes monolithiques de sa coque marquées par d'innombrables cycles d'érosion spatiale. Les hangars à l'intérieur promettaient des trésors — ou des pièges."),
    "tartessus": ("Tartessus, la Cathédrale de l'Exode Sacré", "Vous vous teniez ensemble enfin sur la place sous l'arche de la Cathédrale de l'Exode Sacré.\n\n\"Et c'est le siège de pas seulement une foi, mais de l'espoir même de la rédemption de l'humanité.\""),
    "cathedral_skyline": ("Cathédrale de l'Exode Sacré", "Parmi les colonnes imposantes étaient fixées des capsules d'atterrissage récupérées des premiers vaisseaux de réfugiés Luddic, désormais intégrées dans la vaste architecture de la cathédrale comme reliques sacrées."),
    "abyssal_light": ("Lumière Abyssale", "Une lumière froide emplissait l'écran de visualisation, tranchante contre les ténèbres absolues de l'abîme hyperspacial. Elle semblait pulser, changeant subtilement d'intensité comme si elle respirait."),
    "abyssal_light2": ("Rencontre avec la Lumière Abyssale", "La lumière froide commença à croître sur l'affichage principal. Une pulsation subtile quémandait l'attention.\n\nUn cri d'alarme, une fusée rouge, puis le silence alors que tous les regards se tournaient vers l'écran."),
    "shrouded_weapon_assembly": ("Assemblage d'Arme Exotique", "Des techniciens en combinaison de protection entretenaient les machines de confinement, enjambant des serpentins de tubes et de fils. Un fatras de composants improvisés entourait le cœur de l'assemblage, une technologie d'origine inconnue."),
    "cargo_pod_drift": ("Capsules de Cargo", "Souvent remplies de marchandises récupérables, voire de cryopods opérationnels, une grappe de capsules de cargo dans l'espace ouvert est une cible tentante pour tout spacer ayant besoin d'un coup de pouce financier."),
    "coronal_tap": ("Siphon Coronal, Intérieur", "Ces mégastructures alimentaient autrefois la puissance industrielle insondable du Domain, plaçant la civilisation humaine bien au-delà de l'échelle de toute civilisation précédente dans l'histoire connue."),
    "coronal_tap2": ("Siphon Coronal, Extérieur", "Ces mégastructures alimentaient autrefois la puissance industrielle insondable du Domain, plaçant la civilisation humaine bien au-delà de l'échelle de toute civilisation précédente dans l'histoire connue."),
    "cryosleeper_interior": ("Cryodormeur", "\"Ceux qui s'éveillent du cryosommeil et qui furent mis en repos à l'époque du Domain sont peut-être les plus perdus de tous. Beaucoup ne s'adaptent jamais au Secteur tel qu'il est devenu.\""),
    "generic_probe": ("Sonde Automatique", "C'était une classe commune de sonde utilisée pour la recherche, l'étude et la surveillance, le type de matériel utilisé par les entreprises civiles autant que par les installations militaires."),
}

batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "gallery_batch_*.json")))
total = 0
for bf in batch_files:
    with open(bf, 'r', encoding='utf-8') as f:
        batch = json.load(f)
    changed = False
    for entry in batch:
        if not entry.get("translated_text") and entry["id"] in TRANSLATIONS:
            entry["translated_title"] = TRANSLATIONS[entry["id"]][0]
            entry["translated_text"] = TRANSLATIONS[entry["id"]][1]
            total += 1
            changed = True
    if changed:
        with open(bf, 'w', encoding='utf-8') as f:
            json.dump(batch, f, ensure_ascii=False, indent=2)
        print(f"  {os.path.basename(bf)}: updated")

print(f"\nTotal newly translated: {total}")
