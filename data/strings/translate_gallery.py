#!/usr/bin/env python3
"""Translate GALLERY batch files EN→FR."""
import json
import os
import glob

BATCH_DIR = os.path.join(os.path.dirname(__file__), "gallery_batches")

# Translation dictionary: id → (translated_title, translated_text)
TRANSLATIONS = {
    "jump_point_normal": (
        "Point de Saut, vers l'Hyperespace",
        "Il est des lieux où un équilibre se trouve entre la danse des corps célestes, un mélange de qualités ineffables pour tous sauf ceux absolument dévoués à la physique ésotérique.\n\nC'est là que nous perçons le voile vers la grande et tumultueuse mer au-delà des étoiles."
    ),
    "jump_point_hyper": (
        "Point de Saut, depuis l'Hyperespace",
        "Notre contrat est rempli, soutes pleines et parées /\nHourra car nous sautons vers le cœur /\nNous brûlerons vif, longtemps et régulier"
    ),
    "jump_point_wormhole": (
        "Point de Saut, Trou de Ver",
        "S'engouffrer là-dedans sans savoir exactement où l'on va ressortir ?\n\nC'est comme ça qu'on finit en poussière indiscernable du rayonnement cosmique de fond."
    ),
    "city_from_above": (
        "Ville vue d'en Haut",
        "\"Il a risqué tout le système Galatia, des centaines de milliers de citoyens. Ce n'est peut-être qu'un sous-secteur d'un métroplex là en bas,\" il agita vaguement la main en direction de Chicomoztoc. \"Mais,\" sa voix se durcit, \"je ne permettrai aucune 'grande expérience' qui mette ces gens en danger.\""
    ),
    "desert_moons_ruins": (
        "Ruines d'une Lune Désertique",
        "Un ancien vaisseau-spore rencontra Cibola lors d'un âge plus frais et plus humide que son équilibre, le plaçant dans les paramètres de colonisation du vaisseau. Plus tard, les explorateurs du Domain trouvèrent un monde mourant peuplé d'une civilisation petite, arriérée et désespérée s'accrochant à la survie."
    ),
    "quartermaster": (
        "Quartier-maître",
        "\"Vous croyez que les amortisseurs inertiels vous protégeront pendant une manœuvre de combat ? Si ce n'est pas arrimé, c'est un missile prêt à vous transpercer vous et les trois prochains membres d'équipage remontant le puits d'accès. Je veux que cet étalage honteux soit nettoyé avant la fin du quart.\""
    ),
    "comm_relay": (
        "Relais de Communications",
        "Cette plateforme de communication utilisait une technologie perdue de l'ère du Domain mais restait essentielle à la vie civilisée dans le Secteur Persane. Les hyper-ondes à pulsation rapide adaptées à la transmission de données supraluminiques se sont avérées endommager l'ADN, ces relais étaient donc toujours stationnés loin des habitats."
    ),
    "abandoned_station": (
        "Station Abandonnée 1",
        "Le programme de colonisation imposait la construction autour des puits gravitationnels clés d'infrastructures orbitales incluant des docks de réparation, des nanoforges industrielles, des hubs de communication, des dépôts de terraformation, des armureries, des laboratoires de recherche et des habitations pour les cryodormeurs décongelés.\n\nBeaucoup demeure. Plus encore est aussi brisé et mort que les rêves avides du Domain Humain."
    ),
    "abandoned_station2": (
        "Station Abandonnée 2",
        "\"Y'a des fantômes dans les vieilles stations orbitales — riez pas, cul-terreux. C'est vrai. J'les ai vus... ou plutôt moins vus que sentis. Ils ont des signes. De la friture sur les comms quand t'es au fond. Des valves qui se desserrent quand tu regardes pas. Des outils qui sont plus où tu les avais rangés. De grands tombeaux qu'elles sont, et faudrait les laisser dormir dans le froid.\""
    ),
    "abandoned_station3": (
        "Station Abandonnée",
        "La plupart des stations abandonnées ont été pillées depuis longtemps. Ce qui reste, ce sont les fondations dépouillées d'un empire déchu ; des longerons tordus, des plaques anti-gravité fissurées, des machines brisées et des joints usés par les cycles thermiques jusqu'à la ruine."
    ),
    "jangala_station": (
        "Station Jangala",
        "Mégapole orbitale, chantier naval et port ; l'axe de Corvus, grouillant de trafic de vaisseaux. D'anciens portiques de réparation se cachaient entre des hangars industriels corrodés à l'ombre des anneaux de laboratoires et de systèmes de support. Le tout dominé par des quartiers d'habitation et d'affaires toujours croissants couronnés d'une flèche de communication, hérissée d'armes et de réseaux."
    ),
    "industrial_megafacility": (
        "Mégafacilité Industrielle",
        "La fabrication industrielle lourde reposait sur de grandes nanoforges récupérées des ruines du Domain. Cependant, leur qualité de production se dégradait au fil des cycles ; la corruption à l'échelle nanométrique entraînait des défaillances macroscopiques croissantes allant de l'esthétique au structurel."
    ),
    "terran_orbit": (
        "Orbite Terrienne",
        "Les spécifications de la Corporation de Terraformation Eridani-Utopia fournissent la référence « terrienne » la plus largement acceptée pour l'environnement humain prétendument idéal."
    ),
    "pirate_station": (
        "Station Pirate",
        "\"Le chaos ? Non monsieur, c'est de l'honnêteté. Ici, si un homme vous veut mort, vous le verrez dans ses yeux avant qu'il bouge. C'est mieux qu'un ordinateur dans un bureau quelque part qui décide que votre approvisionnement en air ne vaut pas le coût.\""
    ),
    "urban00": (
        "Métroplex 00",
        "Les premiers colons descendus de cryosommeil construisirent des villes pour des millions à partir de plans et de matériaux préparés avec soin, tels qu'ils avaient été conçus il y a des siècles dans un bureau de planification du Domain. Quand les Portes se sont effondrées, les rêves qu'elles représentaient se sont effondrés avec elles."
    ),
    "urban01": (
        "Métroplex 01",
        "Il était une fois un homme qui pensait pouvoir régner sur tout un monde. Il commença par une ville. Puis le monde le brisa."
    ),
    "urban02": (
        "Kay-arco",
        "Les arcos avaient un dicton : « On ne tombe pas si on ne regarde pas en bas. » Évidemment, c'était faux."
    ),
    "urban03": (
        "Cité-Ruche",
        "Les ruches de Chicomoztoc étaient parfois fermées par des émeutes, des protestations ou des insurrections. Mais tant que les grandes Forges continuaient à produire des vaisseaux, des machines et des marchandises, l'Hégémonie n'intervenait que légèrement dans ce grand monde souterrain de l'humanité."
    ),
    "orbital": (
        "Station Orbitale",
        "Les stations orbitales servaient de centres de commandement, de commerce et de culture, suspendues entre les mondes qu'elles desservaient et le vide qu'elles défiaient."
    ),
    "mine": (
        "Mine",
        "L'extraction minière à travers le Secteur alimentait les forges et les chantiers navals, bien que le travail fût dangereux et les conditions souvent inhumaines."
    ),
    "mairaath": (
        "Ruines de Mairaath",
        "La civilisation de Mairaath s'est effondrée bien avant l'arrivée des vaisseaux-spores du Domain. Ce qui reste parle de grandeur et de folie en parts égales."
    ),
    "eochu_bres": (
        "Eochu Bres",
        "Terraformé tardivement lors de la colonisation du Secteur Persane, Eochu Bres est un monde de pics et de fjords fraîchement déchirés par un temps violent et rapidement changeant."
    ),
    "eochu_bres_landing": (
        "Eochu Bres, Atterrissage",
        "Les plateformes d'atterrissage d'Eochu Bres sont battues par les vents et marquées par le givre, mais les lumières des balises de guidage percent obstinément la brume."
    ),
    "survey": (
        "Relevé Planétaire",
        "L'étude systématique des mondes du Secteur était autrefois une priorité du Domain. Aujourd'hui, c'est une entreprise solitaire menée par des spacers aux motivations variées."
    ),
    "luddic_shrine": (
        "Sanctuaire Luddic",
        "Les sanctuaires de Ludd se trouvent partout où les fidèles se rassemblent, des plus simples autels dans des soutes de cargo aux grandes cathédrales orbitales."
    ),
    "orbital_construction": (
        "Construction Orbitale",
        "La construction de structures orbitales est un processus industriel massif nécessitant des nanoforges, des équipages spécialisés et des quantités colossales de matériaux."
    ),
    "dead_gate": (
        "Portail Inactif",
        "Les Portails inactifs dérivent dans le vide, monuments silencieux d'une ère où l'humanité pouvait traverser la galaxie en un instant."
    ),
    "active_gate": (
        "Portail Actif",
        "Un Portail actif pulse d'une énergie que même les meilleurs scientifiques du Secteur ne comprennent qu'imparfaitement. Traverser reste un acte de foi autant que de physique."
    ),
    "eventide": (
        "Eventide",
        "Eventide est un monde de crépuscules perpétuels, son orbite verrouillée par les marées créant une bande habitable entre le jour éternel et la nuit sans fin."
    ),
    "volturn": (
        "Volturn",
        "Les mers de Volturn abritent l'un des écosystèmes xénobiologiques les plus riches du Secteur, dont les fameux homards volturniens tant prisés par l'élite."
    ),
    "space_bar": (
        "Bar de Spacers",
        "Tout port a son bar. C'est là que les contrats se négocient, que les rumeurs circulent et que les fortunes se font et se défont entre deux verres de synthale."
    ),
    "pirate_bar": (
        "Bar Pirate",
        "L'éclairage est sombre, la musique forte et les armes mal dissimulées. Ici, les questions sont indiscrètes et les réponses souvent fatales."
    ),
    "stellar_mirror": (
        "Miroir Stellaire",
        "Une merveille d'ingénierie du Domain, le miroir stellaire concentre et redirige la lumière solaire pour réchauffer des mondes autrement trop froids pour l'habitation humaine."
    ),
    "stellar_shade": (
        "Voile Stellaire",
        "Le pendant du miroir stellaire, le voile bloque une partie du rayonnement solaire pour refroidir des mondes autrement trop chauds, créant des zones habitables là où il n'y en aurait pas."
    ),
    "hegemony_bar": (
        "Bar de Spacers de l'Hégémonie",
        "Une rangée de tireuses ornait le mur sous des bouteilles de chacun des Mondes Centraux — et de quelques autres. Les capitaines marchands se mêlaient aux officiers en permission au bar, servis par du personnel en uniforme. Dans un coin, une bande de cadets de la marine criait et chantait, désespérés de profiter de leur dernier quart de liberté."
    ),
    "sindria": (
        "Sindria",
        "Le joyau du Diktat, Sindria brûle de l'ambition d'Andrada et de la sueur de ses citoyens. Les raffineries de carburant illuminent le ciel nocturne d'une lueur perpétuelle."
    ),
    "bar_diktat": (
        "Bar de Spacers du Diktat Sindrien",
        "L'ordre et la discipline imprègnent même les lieux de détente du Diktat. Les portraits d'Andrada observent depuis chaque mur tandis que les spacers boivent avec une retenue calculée."
    ),
    "tritachyon_bar": (
        "Bar de Spacers Tri-Tachyon",
        "Chrome, verre et lumière froide. Le bar Tri-Tachyon est aussi clinique que l'entreprise elle-même, bien que les conversations murmurées aux tables privées soient tout sauf stériles."
    ),
    "gilead": (
        "Gilead",
        "Gilead est un monde sacré pour l'Église Luddic, un lieu de pèlerinage où les fidèles viennent chercher la rédemption et la guidance spirituelle."
    ),
    "jangala_shrine": (
        "Sanctuaire de Jangala",
        "Un lieu de vénération au cœur de la station, où les fidèles Luddic prient pour la protection divine contre les périls du vide et les abominations de la technologie."
    ),
    "chicomoztoc": (
        "Chicomoztoc",
        "Le cœur industriel de l'Hégémonie, Chicomoztoc est un monde-ruche grouillant de milliards d'âmes, ses forges alimentant les flottes qui maintiennent l'ordre dans le Secteur."
    ),
    "kazeron": (
        "Kazeron",
        "Kazeron est un monde de palais et de politique, où les trois grandes familles-corporations — les Yaribay, les Zal et les Principi — se disputent l'influence et le pouvoir."
    ),
    "sentinel1": (
        "Sentinel, la Colonie Perdue",
        "On ne peut pas dire que la colonie de Sentinel a été un succès. Le monde était marginal, les ressources rares, et l'isolement progressif après l'Effondrement l'a laissée à la dérive."
    ),
    "sentinel2": (
        "Sentinel, la Colonie Retrouvée",
        "On ne peut pas dire qu'elle prospère, mais la colonie de Sentinel a gagné un nouveau sentiment d'espoir et d'énergie après sa réintégration avec l'Hégémonie."
    ),
}

# Process all batch files
batch_files = sorted(glob.glob(os.path.join(BATCH_DIR, "gallery_batch_*.json")))
total = 0
for bf in batch_files:
    with open(bf, 'r', encoding='utf-8') as f:
        batch = json.load(f)

    for entry in batch:
        entry_id = entry["id"]
        if entry_id in TRANSLATIONS:
            entry["translated_title"] = TRANSLATIONS[entry_id][0]
            entry["translated_text"] = TRANSLATIONS[entry_id][1]
            total += 1
        else:
            # Keep original if no translation available
            print(f"  WARNING: No translation for {entry_id}")

    with open(bf, 'w', encoding='utf-8') as f:
        json.dump(batch, f, ensure_ascii=False, indent=2)

    print(f"  {os.path.basename(bf)}: {len(batch)} entries processed")

print(f"\nTotal translated: {total}")
