#!/usr/bin/env python3
"""
Translate rules_src_part1.csv text column (column 5) to French.
Preserves all other columns, handles multiline CSV fields.
"""

import csv
import sys
import os

SRC = os.path.join(os.path.dirname(__file__), '..', 'data', 'campaign', 'rules_src_part1.csv')
DST = os.path.join(os.path.dirname(__file__), '..', 'data', 'campaign', 'rules_part1.csv')

# Translation dictionary: English text -> French text
# Keys are the exact text content of column 5 (text column)
TRANSLATIONS = {
    # === Warning Beacons ===
    "An autonomous warning beacon has been left emitting a distorted wail between official channels. Whatever message it was meant to convey has been corrupted.":
        "Une balise d'alerte autonome emet une plainte deformee entre les canaux officiels. Le message qu'elle etait censee transmettre a ete corrompu.",

    'This autonomous warning beacon emits a looping message.\n\n""DANGER: This star system is known to contain potentially active autonomous weapon systems. Access to this system by unauthorized parties is forbidden by Hegemony Navy diktat 224.34."""':
        'Cette balise d\'alerte autonome emet un message en boucle.\n\n""DANGER : Ce systeme stellaire est connu pour contenir des systemes d\'armement autonomes potentiellement actifs. L\'acces a ce systeme par des parties non autorisees est interdit par le decret 224.34 de la Marine de l\'Hegemonie."""',

    'This autonomous warning beacon emits a looping message.\n\n""This world is corrupted by technological sin and its abomination stands testament to the result of straying from the path of virtue. Trespass is forbidden. Any who scorn this warning shall become both corrupt of body and outlaw by the holy justice enforced by this order of the Knights of Ludd."""':
        'Cette balise d\'alerte autonome emet un message en boucle.\n\n""Ce monde est corrompu par le peche technologique et son abomination temoigne du resultat de ceux qui s\'egarent du chemin de la vertu. Toute intrusion est interdite. Quiconque meprise cet avertissement sera corrompu de corps et hors-la-loi selon la sainte justice appliquee par cet ordre des Chevaliers de Ludd."""',

    # === Gates ===
    "A silent ring of adamantine material, derelict of a former age.\n\nThe Gate is inert.":
        "Un anneau silencieux d'adamantine, vestige d'un age revolu.\n\nLe Portail est inerte.",

    "Before you vast and potent hangs an adamantine ring, derelict of a former age.\n\nYou have scanned this Gate and discovered the rhythm of the secret heart of the thing, hidden in a slip of space. Using the Janus Device to create a bridge to another Gate requires a massive quantity of fuel. The more distant the target, the more fuel is required.\n\nThe Janus Device operates by transferring enormous amounts of peculiarly phased energy via a lead ship's hyperdrive field to stabilize a direct gate-to-gate connection.":
        "Devant vous, vaste et puissant, flotte un anneau d'adamantine, vestige d'un age revolu.\n\nVous avez scanne ce Portail et decouvert le rythme du coeur secret de la chose, cache dans une faille de l'espace. Utiliser le Dispositif de Janus pour creer un pont vers un autre Portail necessite une quantite massive de carburant. Plus la cible est eloignee, plus il faut de carburant.\n\nLe Dispositif de Janus fonctionne en transferant d'enormes quantites d'energie a phase singuliere via le champ d'hyperpropulsion d'un vaisseau amiral pour stabiliser une connexion directe de portail a portail.",

    "Before you vast and potent hangs an adamantine ring, derelict of a former age.\n\nYou have scanned this Gate and discovered the rhythm of the secret heart of the thing, hidden in a slip of space. Using the Janus Device to create a bridge to another Gate requires a massive quantity of fuel. The more distant the target, the more fuel is required.\n\nYou must integrate the Janus Device into your fleet to use the Gate.":
        "Devant vous, vaste et puissant, flotte un anneau d'adamantine, vestige d'un age revolu.\n\nVous avez scanne ce Portail et decouvert le rythme du coeur secret de la chose, cache dans une faille de l'espace. Utiliser le Dispositif de Janus pour creer un pont vers un autre Portail necessite une quantite massive de carburant. Plus la cible est eloignee, plus il faut de carburant.\n\nVous devez integrer le Dispositif de Janus a votre flotte pour utiliser le Portail.",

    "A silent ring of adamantine material, derelict of a former age.\n\nYour sensors officer nods to your cue. Your command interface lights up. 'EXECUTE SCAN' blinks expectantly. The Gate awaits, as cold as a tomb.":
        "Un anneau silencieux d'adamantine, vestige d'un age revolu.\n\nVotre officier de detection hoche la tete a votre signal. Votre interface de commandement s'illumine. 'EXECUTER SCAN' clignote dans l'attente. Le Portail attend, froid comme un tombeau.",

    "A silent ring of adamantine material, derelict of a former age.\n\nYou have scanned this Gate and discovered the rhythm of the secret heart of the thing, hidden in a slip of space.":
        "Un anneau silencieux d'adamantine, vestige d'un age revolu.\n\nVous avez scanne ce Portail et decouvert le rythme du coeur secret de la chose, cache dans une faille de l'espace.",

    "A silent ring of adamantine material, derelict of a former age.\n\nYour sensors officer nods to you; the hyperwave scanner is ready. The words 'EXECUTE SCAN' blink expectantly in your command interface.\n\nYou will need a scan of this Gate to be able to use it, with the Janus Device, as an access or egress point from the Gate network.":
        "Un anneau silencieux d'adamantine, vestige d'un age revolu.\n\nVotre officier de detection vous fait un signe de tete ; le scanneur hyperonde est pret. Les mots 'EXECUTER SCAN' clignotent dans votre interface de commandement.\n\nVous aurez besoin d'un scan de ce Portail pour pouvoir l'utiliser, avec le Dispositif de Janus, comme point d'acces ou de sortie du reseau de Portails.",

    "You order your $shipOrFleet to traverse the dead gateway. Your bridge crew is especially quiet during the passage.\n\nNothing happens.":
        "Vous ordonnez a votre $shipOrFleet de traverser le portail mort. Votre equipage de passerelle est particulierement silencieux pendant la traversee.\n\nRien ne se passe.",

    # Gate scans
    'Your command display is overlaid with a representation of the hyperspace manifold surrounding the Gate. It is calm and cool, devoid of drive-wakes.\n\nAs the scan begins you watch a line of disruption flare between the icon representing your flagship and the icon representing the Gate. Spirals and ripples spill out in non-Newtonian waves, surging from a point at the center of the Gate. No, it\'s not a point - a circle, a sphere, a torus and inverted funnel; then some other form that makes you squeeze your eyes shut. You hear faint music from far away.\n\n""Captain?"" Your sensors officer is looking at you, ""The scan is complete."" You realize it\'s the second time they said this, and you gesture as if you were simply lost in thought.':
        'Votre ecran de commandement se superpose d\'une representation du collecteur hyperspacial entourant le Portail. Il est calme et froid, depourvu de sillages de propulsion.\n\nLorsque le scan commence, vous observez une ligne de perturbation fuser entre l\'icone representant votre vaisseau amiral et celle du Portail. Des spirales et des ondulations se repandent en vagues non newtoniennes, jaillissant d\'un point au centre du Portail. Non, ce n\'est pas un point - un cercle, une sphere, un tore et un entonnoir inverse ; puis une autre forme qui vous force a fermer les yeux. Vous entendez une musique lointaine.\n\n""Capitaine ?"" Votre officier de detection vous regarde. ""Le scan est termine."" Vous realisez que c\'est la deuxieme fois qu\'il le dit, et vous faites un geste comme si vous etiez simplement perdu dans vos pensees.',

    'Your command display shows a representation of the hyperspace manifold. It is calm and cool.\n\nThe scan begins, a line of disruption flaring between your flagship and the Gate. Spirals and ripples spill and surge in non-Newtonian bursts from a point at the center of the Gate. No, not a point - a circle, a sphere, a torus and inverted funnel; then some geometry that does not parse.\n\nYou hear the faint music.\n\n""Captain,"" your sensors officer reports, ""The scan is complete."""':
        'Votre ecran de commandement affiche une representation du collecteur hyperspacial. Il est calme et froid.\n\nLe scan commence, une ligne de perturbation fusant entre votre vaisseau amiral et le Portail. Des spirales et des ondulations deferlent en rafales non newtoniennes depuis un point au centre du Portail. Non, pas un point - un cercle, une sphere, un tore et un entonnoir inverse ; puis une geometrie qui echappe a toute comprehension.\n\nVous entendez la musique lointaine.\n\n""Capitaine,"" rapporte votre officier de detection, ""le scan est termine."""',

    'Your command display shows the hyperspace manifold. It is calm and cool.\n\nThe scanning beam flares in the hyperdimensional display. Spirals and ripples spill in bursts from the Gate, surging into inconceivable geometry. You hear a wisp of faint music.\n\n""Captain,"" your sensors officer reports, ""The scan is complete."""':
        'Votre ecran de commandement affiche le collecteur hyperspacial. Il est calme et froid.\n\nLe faisceau de scan fuse dans l\'affichage hyperdimensionnel. Des spirales et des ondulations deferlent par rafales depuis le Portail, se propageant en geometries inconcevables. Vous percevez un filet de musique lointaine.\n\n""Capitaine,"" rapporte votre officier de detection, ""le scan est termine."""',

    "A surge of energy explodes from the Gate.":
        "Un afflux d'energie explose depuis le Portail.",

    # Gate Hauler Luddic post-scan
    'You personally see off the party of Luddic faithful who maintained vigil from your flagship. Their fleet is returning; their collective devotion uninterrupted.\n\n""Blessings of Ludd upon you, captain,"" says their leader. ""I shall speak well of you to the Prophet Returned.""\n\nYou know to nod in acceptance without raising any theological questions, and give a polite wave as their shuttle leaves the bay.':
        'Vous raccompagnez personnellement le groupe de fideles luddiques qui maintenaient leur vigile depuis votre vaisseau amiral. Leur flotte repart ; leur devotion collective intacte.\n\n""Benedictions de Ludd sur vous, capitaine,"" dit leur chef. ""Je parlerai en votre faveur au Prophete Revenu.""\n\nVous savez hocher la tete en acceptation sans soulever de questions theologiques, et adressez un signe de la main poli tandis que leur navette quitte la soute.',

    # Survey interactions
    "Your $shipOrFleet approaches $entityName.":
        "Votre $shipOrFleet s'approche de $entityName.",

    "You have full survey data for this planet.":
        "Vous disposez de donnees d'exploration completes pour cette planete.",

    "A nearby hostile fleet is tracking your movements, making running a survey operation impossible.":
        "Une flotte hostile a proximite surveille vos mouvements, rendant toute operation d'exploration impossible.",

    "A nearby hostile fleet is tracking your movements, making establishing a colony impossible.":
        "Une flotte hostile a proximite surveille vos mouvements, rendant l'etablissement d'une colonie impossible.",

    "This system is cut off from hyperspace and the jump-points are unstable. The crew, and even officers, are muted; on-edge. You judge it unlikely that any amount of hazard pay could overcome the near-superstitious fear spacers have of being stranded in a system like this.\n\nEstablishing a colony here is not an option.":
        "Ce systeme est coupe de l'hyperespace et les points de saut sont instables. L'equipage, et meme les officiers, sont taciturnes, sur les nerfs. Vous jugez improbable qu'une quelconque prime de risque puisse surmonter la peur quasi superstitieuse qu'ont les spaciens d'etre echoues dans un systeme comme celui-ci.\n\nEtablir une colonie ici n'est pas une option.",

    "Your $shipOrFleet enters low orbit around $entityName.":
        "Votre $shipOrFleet se place en orbite basse autour de $entityName.",

    # Market interactions
    "Your $shipOrFleet transmits identification codes via the transponder and you are soon granted docking clearance.":
        "Votre $shipOrFleet transmet ses codes d'identification via le transpondeur et vous obtenez rapidement une autorisation d'amarrage.",

    "Your $shipOrFleet transmits identification codes via the transponder and you are soon granted a slot in a parking orbit.":
        "Votre $shipOrFleet transmet ses codes d'identification via le transpondeur et vous obtenez rapidement un creneau en orbite de stationnement.",

    "Your $shipOrFleet finishes offloading crew, supplies, and machinery $onOrAt $marketName, and the crew soon busy themselves erecting temporary shelter and basic infrastructure.":
        "Votre $shipOrFleet termine le dechargement de l'equipage, des fournitures et des machines $onOrAt $marketName, et l'equipage s'affaire bientot a eriger des abris temporaires et des infrastructures de base.",

    "You leave the bar and take a shuttle back to your $shipOrFleet.":
        "Vous quittez le bar et prenez une navette pour retourner a votre $shipOrFleet.",

    "$TheFactionLong $factionIsOrAre $relAdjective towards you, and the port authority refuses your request for docking clearance after you identify yourself.\n\nYou might be able to establish contact with underground parties if you come in with the transponder turned off.":
        "$TheFactionLong $factionIsOrAre $relAdjective envers vous, et l'autorite portuaire refuse votre demande d'amarrage apres votre identification.\n\nVous pourriez etablir le contact avec des parties clandestines si vous approchez avec le transpondeur eteint.",

    "Your recent actions around $marketName have generated a lot of local interest, and simply coming in with the transponder off is no longer sufficient to go unnoticed. Judging from the current level of comm chatter and news reports, you estimate it'll take $playerHostileTimeoutStr until the commotion dies down.":
        "Vos actions recentes autour de $marketName ont suscite beaucoup d'interet localement, et approcher simplement avec le transpondeur eteint ne suffit plus pour passer inapercu. A en juger par le niveau actuel des communications et des reportages, vous estimez qu'il faudra $playerHostileTimeoutStr avant que l'agitation ne retombe.",

    "Your recent actions around $marketName have generated a lot of local interest, and engaging in open business is impossible. Judging from the current level of comm chatter and news reports, you estimate it'll take $playerHostileTimeoutStr until the commotion dies down.":
        "Vos actions recentes autour de $marketName ont suscite beaucoup d'interet localement, et faire du commerce ouvertement est impossible. A en juger par le niveau actuel des communications et des reportages, vous estimez qu'il faudra $playerHostileTimeoutStr avant que l'agitation ne retombe.",

    "$TheFactionLong $factionIsOrAre $relAdjective towards you, and the port authority refuses your request for docking clearance after you identify yourself.\n\nThe refusal is rather perfunctory and you get the impression that turning off your transponder to prevent identification might yield better results.":
        "$TheFactionLong $factionIsOrAre $relAdjective envers vous, et l'autorite portuaire refuse votre demande d'amarrage apres votre identification.\n\nLe refus est assez expeditif et vous avez l'impression qu'eteindre votre transpondeur pour empecher l'identification pourrait donner de meilleurs resultats.",

    "Your $shipOrFleet goes into orbit around $marketName, ignoring requests from the $faction port authority to identify yourself.\n\nAt least one $faction patrol is tracking your movements, and no underground parties are willing to run the risk of doing business.":
        "Votre $shipOrFleet se met en orbite autour de $marketName, ignorant les demandes d'identification de l'autorite portuaire $faction.\n\nAu moins une patrouille $faction surveille vos mouvements, et aucun parti clandestin n'est dispose a prendre le risque de faire affaire.",

    "Your $shipOrFleet goes into orbit around $marketName.\n\nAt least one $faction patrol is tracking your movements, and the port authority refuses your request for docking clearance until the matter is resolved.":
        "Votre $shipOrFleet se met en orbite autour de $marketName.\n\nAu moins une patrouille $faction surveille vos mouvements, et l'autorite portuaire refuse votre demande d'amarrage tant que la situation n'est pas resolue.",

    'Your $shipOrFleet goes into orbit around $marketName. The local port authority seems to take no issue with your explanation for why your transponder, regrettably, can\'t be turned on.':
        'Votre $shipOrFleet se met en orbite autour de $marketName. L\'autorite portuaire locale ne semble pas contester votre explication sur la raison pour laquelle votre transpondeur, malheureusement, ne peut pas etre active.',

    "Your $shipOrFleet goes into orbit around $marketName.":
        "Votre $shipOrFleet se met en orbite autour de $marketName.",

    "Your $shipOrFleet goes into orbit around $marketName, ignoring requests from $theFaction port authority to identify yourself.\n\nNo $faction patrols seem to be aware of you just yet, and you have a window of opportunity for doing business with parties untroubled by your lack of docking clearance.":
        "Votre $shipOrFleet se met en orbite autour de $marketName, ignorant les demandes d'identification de l'autorite portuaire de $theFaction.\n\nAucune patrouille $faction ne semble encore avoir conscience de votre presence, et vous avez une fenetre d'opportunite pour faire affaire avec des parties que votre absence d'autorisation d'amarrage ne derange pas.",

    "You establish a linkup with the port authority's cargo management system and browse the inventory.":
        "Vous etablissez une liaison avec le systeme de gestion du fret de l'autorite portuaire et parcourez l'inventaire.",

    "You establish a linkup with the dockyard and see what's available.":
        "Vous etablissez une liaison avec le chantier naval et consultez ce qui est disponible.",

    "You establish a linkup with the dockyard and transmit your $shipOrFleet status.":
        "Vous etablissez une liaison avec le chantier naval et transmettez l'etat de votre $shipOrFleet.",

    "Your $shipOrFleet undergoes full repairs and is restored to maximum combat readiness, at the cost of $global.repairSupplyCost supplies.":
        "Votre $shipOrFleet subit des reparations completes et retrouve sa pleine capacite de combat, au prix de $global.repairSupplyCost fournitures.",

    "You connect to the local comm directory and browse the public and otherwise known listings.":
        "Vous vous connectez au repertoire de communications local et parcourez les annonces publiques et les contacts connus.",

    # Food shortage events
    "Thanks to your efforts, the food shortage is now over before it had a chance to cause much chaos. $marketName's long-term stability is unaffected by the shortage.":
        "Grace a vos efforts, la penurie alimentaire est terminee avant d'avoir pu causer trop de chaos. La stabilite a long terme de $marketName n'est pas affectee par la penurie.",

    "Thanks to your efforts, the food shortage is now over. Its impact on $marketName's stability is reduced.":
        "Grace a vos efforts, la penurie alimentaire est terminee. Son impact sur la stabilite de $marketName est reduit.",

    "Thanks to your illicit efforts, the food shortage is now over. Since much of the food you've delivered went through channels of questionable legality, there's not much hope - or, indeed, desire - for official recognition.":
        "Grace a vos efforts illicites, la penurie alimentaire est terminee. Puisqu'une grande partie de la nourriture que vous avez livree est passee par des canaux de legalite douteuse, il y a peu d'espoir - et, a vrai dire, peu de desir - de reconnaissance officielle.",

    "Thanks in part to your efforts, the recent food shortage is over. Your standing with $theMarketFaction should improve slightly.":
        "En partie grace a vos efforts, la recente penurie alimentaire est terminee. Votre reputation aupres de $theMarketFaction devrait legerement s'ameliorer.",

    "Tapping into the comm network for local news, you learn that there was a recent food shortage. Though the shortage is now over, the local situation is still somewhat destabilized.":
        "En vous connectant au reseau de communications pour les nouvelles locales, vous apprenez qu'il y a eu une recente penurie alimentaire. Bien que la penurie soit terminee, la situation locale reste quelque peu destabilisee.",

    "Tapping into the comm network for local news, you learn that there was a recent and protracted food shortage. Though the shortage is now over, the local situation is still highly destabilized.":
        "En vous connectant au reseau de communications pour les nouvelles locales, vous apprenez qu'il y a eu une recente et prolongee penurie alimentaire. Bien que la penurie soit terminee, la situation locale reste fortement destabilisee.",

    # Greeting lines - generic
    "You try to establish a comm link, but get only static.":
        "Vous tentez d'etablir une liaison comm, mais n'obtenez que des parasites.",

    'You try to establish a comm link, but get only static.':
        'Vous tentez d\'etablir une liaison comm, mais n\'obtenez que des parasites.',

    "You cut the comm link.":
        "Vous coupez la liaison comm.",

    "You cut the comm link after exchanging a few pleasantries.":
        "Vous coupez la liaison comm apres avoir echange quelques politesses.",

    "You cut the comm link after exchanging a few hollow pleasantries.":
        "Vous coupez la liaison comm apres avoir echange quelques politesses creuses.",

    # Transponder conversations
    "You issue an order to activate the transponder and re-open the comm link.":
        "Vous donnez l'ordre d'activer le transpondeur et de rouvrir la liaison comm.",

    "You issue an order to activate the transponder and wait for the cargo scan to finish.":
        "Vous donnez l'ordre d'activer le transpondeur et attendez la fin du scan de cargaison.",

    "You wait for the cargo scan to finish.":
        "Vous attendez la fin du scan de cargaison.",

    # Salvage
    "Your $shipOrFleet approaches $aOrAn $nameInText.":
        "Votre $shipOrFleet s'approche de $aOrAn $nameInText.",

    "Your $shipOrFleet approaches $aOrAn $nameInText left from the initial Domain exploration of the Sector.":
        "Votre $shipOrFleet s'approche de $aOrAn $nameInText laisse par l'exploration initiale du Secteur par le Domaine.",

    "Your $shipOrFleet assumes a stable orbit relative to the debris field.":
        "Votre $shipOrFleet se place en orbite stable par rapport au champ de debris.",

    "A nearby hostile fleet is tracking your movements, making exploration impossible.":
        "Une flotte hostile a proximite surveille vos mouvements, rendant toute exploration impossible.",

    "Your $shipOrFleet finishes its approach to the $nameInText without further incident.":
        "Votre $shipOrFleet termine son approche du $nameInText sans autre incident.",

    # Customs inspection
    "You receive a long-range comm burst from the $faction $otherFleetName directing your $shipOrFleet to come to and prepare for a customs inspection.\n\nThe message contains a standard legal-code attachment detailing the various penalties for evading customs agents, transporting contraband, and other related offenses.\n\nIt's as likely as not that this is nothing more than a legalized shakedown, but it has the weight of $faction authority behind it.":
        "Vous recevez une communication longue portee de la $faction $otherFleetName ordonnant a votre $shipOrFleet de s'arreter et de se preparer a une inspection douaniere.\n\nLe message contient une piece jointe de code juridique standard detaillant les diverses sanctions pour evasion d'agents des douanes, transport de contrebande et autres infractions connexes.\n\nIl y a autant de chances que ce ne soit rien de plus qu'une extorsion legalisee, mais cela a le poids de l'autorite $faction derriere.",

    "The port authority refuses your $shipOrFleet docking clearance until the customs inspection is resolved. Making contact with any underground parties willing to trade is also impossible due to the patrol breathing down your neck.":
        "L'autorite portuaire refuse l'autorisation d'amarrage de votre $shipOrFleet tant que l'inspection douaniere n'est pas resolue. Etablir le contact avec des parties clandestines disposees a commercer est egalement impossible en raison de la patrouille qui vous surveille de pres.",

    "You decline the comms request and continue on your way.":
        "Vous declinez la demande de communication et poursuivez votre route.",

    # Stranded in deep space
    "It can't be denied any longer.\n\nYou're stuck in deep space near an obscure celestial object having foolishly jumped in before ensuring your $shipOrFleet could jump back out.\n\nThe bridge officers are very carefully avoiding an outright panic, assigning makework maintenance duties and shutting down speculation. Still, you can't help but notice questioning glances - spacers will follow almost any order, but this is a serious blunder. \n\nYour navigation officer appears to be having a heated intra-ship comms discussion with your engineering chief. You catch key phrases, \"\"too dangerous\"\", \"\"theoretically impossible\"\", \"\"worked once\"\".":
        "C'est indeniable desormais.\n\nVous etes coince dans l'espace profond pres d'un objet celeste obscur, ayant saute imprudemment avant de vous assurer que votre $shipOrFleet pouvait repartir.\n\nLes officiers de passerelle evitent soigneusement toute panique ouverte, assignant des taches de maintenance pour occuper et coupant court aux speculations. Pourtant, vous ne pouvez ignorer les regards interrogateurs - les spaciens suivent presque n'importe quel ordre, mais c'est une erreur grave.\n\nVotre officier de navigation semble avoir une discussion animee par comm interne avec votre chef ingenieur. Vous saisissez des mots-cles : \"\"trop dangereux\"\", \"\"theoriquement impossible\"\", \"\"a marche une fois\"\".",

    # Decivilized planet
    "Your $shipOrFleet approaches $entityName.\n\n$marketName is in chaos, with what's left of the population scrambling to survive by any means possible. Your sensors pick up some intermittent small-arms fire. The collapse of all authority is complete and irreversible, though a new colony can still be established atop the wreckage of the old.":
        "Votre $shipOrFleet s'approche de $entityName.\n\n$marketName est plongee dans le chaos ; ce qui reste de la population lutte pour survivre par tous les moyens possibles. Vos capteurs detectent des tirs d'armes legeres intermittents. L'effondrement de toute autorite est complet et irreversible, bien qu'une nouvelle colonie puisse encore etre etablie sur les ruines de l'ancienne.",

    # New game creation
    "Your most recent occupation was as...":
        "Votre plus recente occupation etait...",

    "In addition, your fleet includes...":
        "De plus, votre flotte comprend...",

    'Select the campaign difficulty level. ""Easy"" is recommended for a first-time player.':
        'Selectionnez le niveau de difficulte de la campagne. ""Facile"" est recommande pour un premier essai.',

    "You transmit the comms ID and wait for the system to establish a connection.":
        "Vous transmettez l'identifiant comm et attendez que le systeme etablisse la connexion.",

    # Conversations - generic greetings
    'After a short wait, your connection request is accepted.\n\n""Hello. What do you want?""':
        'Apres une breve attente, votre demande de connexion est acceptee.\n\n""Bonjour. Que voulez-vous ?""',

    'After a short wait, your connection request is denied.':
        'Apres une breve attente, votre demande de connexion est refusee.',

    '""Anything else I can do for you?""':
        '""Autre chose que je puisse faire pour vous ?""',

    # NPC comm request
    'As you get near $entityName, you get an incoming comm request.':
        'En approchant de $entityName, vous recevez une demande de communication entrante.',

    # Cargo pods
    "Unfortunately, the pods were wired to explode unless the correct authorization code was given, and the cargo is destroyed in its entirety.":
        "Malheureusement, les capsules etaient piegees pour exploser sans le bon code d'autorisation, et la cargaison est entierement detruite.",

    # Remnant station
    "The grim expanse of the remnant battlestation fills your viewscreen. A bridge officer re-scales the tactical target display so that its entire mass can be seen at once. \n\nA relic from the First AI War, the station nonetheless appears to be fully armed and operational.\n\nThe combat analysis system churns for a few seconds and then beeps angrily instead of producing the usual range of tactical recommendations.":
        "L'etendue sinistre de la station de combat vestige emplit votre ecran. Un officier de passerelle reechelonne l'affichage tactique pour que sa masse entiere soit visible.\n\nRelique de la Premiere Guerre des IA, la station semble neanmoins pleinement armee et operationnelle.\n\nLe systeme d'analyse de combat mouline quelques secondes puis emet un bip furieux au lieu de produire la gamme habituelle de recommandations tactiques.",

    "The grim expanse of the Remnant battlestation fills your viewscreen. A bridge officer re-scales the tactical target display so that its entire mass can be seen at once. \n\nA relic from the First AI War, the station's long arc gapes with empty sockets where weapons platforms and citadels were once present. Despite the obvious damage, the station is armed and operational.\n\nThe combat analysis system churns for a few seconds and then beeps angrily instead of producing the usual range of tactical recommendations.":
        "L'etendue sinistre de la station de combat des Vestiges emplit votre ecran. Un officier de passerelle reechelonne l'affichage tactique pour que sa masse entiere soit visible.\n\nRelique de la Premiere Guerre des IA, le long arc de la station baille de cavites vides ou se trouvaient jadis des plates-formes d'armement et des citadelles. Malgre les dommages evidents, la station est armee et operationnelle.\n\nLe systeme d'analyse de combat mouline quelques secondes puis emet un bip furieux au lieu de produire la gamme habituelle de recommandations tactiques.",

    # Salvage defenders
    "As your $shipOrFleet moves in closer, new energy signatures are detected near the $shortName.":
        "Tandis que votre $shipOrFleet s'approche, de nouvelles signatures energetiques sont detectees pres du $shortName.",

    "As your $shipOrFleet moves in closer, new energy signatures are detected near a larger piece of debris.":
        "Tandis que votre $shipOrFleet s'approche, de nouvelles signatures energetiques sont detectees pres d'un gros debris.",

    "As your $shipOrFleet moves in closer, several energy signatures are detected coming online inside the probe's hold.":
        "Tandis que votre $shipOrFleet s'approche, plusieurs signatures energetiques sont detectees en activation dans la soute de la sonde.",

    "As your $shipOrFleet moves in closer, multiple energy signatures are detected coming online from various points on and within the flayed hull of the survey ship.":
        "Tandis que votre $shipOrFleet s'approche, de multiples signatures energetiques sont detectees en activation depuis divers points sur et dans la coque ecorchee du vaisseau d'exploration.",

    "As your $shipOrFleet moves in closer, numerous strong energy signatures are detected coming online inside the darkened work-bays of the mothership's vast hulk. Your sensors also detect several weapon emplacements powering up on the mothership itself.":
        "Tandis que votre $shipOrFleet s'approche, de nombreuses signatures energetiques puissantes sont detectees en activation dans les hangars obscurs de la vaste carcasse du vaisseau-mere. Vos capteurs detectent egalement plusieurs emplacements d'armes s'activant sur le vaisseau-mere lui-meme.",

    "As your $shipOrFleet moves in closer, numerous strong energy signatures are detected coming online inside the darkened work-bays of the mothership's vast hulk.":
        "Tandis que votre $shipOrFleet s'approche, de nombreuses signatures energetiques puissantes sont detectees en activation dans les hangars obscurs de la vaste carcasse du vaisseau-mere.",

    "As your $shipOrFleet moves in closer, your sensors detect several weapon emplacements powering up in darkened crevasses on the mothership's vast hulk.":
        "Tandis que votre $shipOrFleet s'approche, vos capteurs detectent plusieurs emplacements d'armes s'activant dans les crevasses obscures de la vaste carcasse du vaisseau-mere.",

    # Derelict descriptions
    "Pitted by small impacts, the probe's hull displays iridescence typical of fearsome radiation scarring. Though this probe's manufacture could well date to a thousand cycles ago, some systems are still nominally active.":
        "Criblée d'impacts mineurs, la coque de la sonde affiche l'iridescence typique de terribles cicatrices de radiation. Bien que la fabrication de cette sonde puisse dater d'il y a un millier de cycles, certains systemes sont encore nominalement actifs.",

    "The ancient Domain-era automated survey ship has been ravaged by centuries of exposure to charged particles and high velocity impacts of interstellar dust. Some systems still appear to be nominally active.":
        "L'ancien vaisseau d'exploration automatise de l'ere du Domaine a ete ravage par des siecles d'exposition aux particules chargees et aux impacts a haute vitesse de la poussiere interstellaire. Certains systemes semblent encore nominalement actifs.",

    "The vast bulk of the automated exploration mothership is burned and battered by centuries of service to the Domain, a drifting forgotten hulk, though sensors indicate that some systems are still nominally active.":
        "L'immense masse du vaisseau-mere d'exploration automatise est brulee et cabossee par des siecles de service au Domaine, une epave a la derive et oubliee, bien que les capteurs indiquent que certains systemes sont encore nominalement actifs.",
}

def translate_text(text):
    """Translate text column content. Returns translated text or original if no translation found."""
    if not text or not text.strip():
        return text

    # Try exact match first
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]

    # Try with stripped whitespace
    stripped = text.strip()
    if stripped in TRANSLATIONS:
        return TRANSLATIONS[stripped]

    return text  # Return original if no translation found


def main():
    src_path = os.path.abspath(SRC)
    dst_path = os.path.abspath(DST)

    print(f"Reading: {src_path}")

    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse CSV properly
    reader = csv.reader(content.splitlines(), quotechar='"')
    rows = list(reader)

    print(f"Total rows: {len(rows)}")

    translated_count = 0
    text_count = 0

    output_rows = []
    for i, row in enumerate(rows):
        if i == 0:
            # Header row - copy as-is
            output_rows.append(row)
            continue

        if len(row) >= 5 and row[4].strip():
            text_count += 1
            original = row[4]
            translated = translate_text(original)
            if translated != original:
                translated_count += 1
                row = list(row)
                row[4] = translated

        output_rows.append(row)

    print(f"Rows with text: {text_count}")
    print(f"Rows translated: {translated_count}")

    # Write output
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)

    with open(dst_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in output_rows:
            writer.writerow(row)

    print(f"Written: {dst_path}")


if __name__ == '__main__':
    main()
