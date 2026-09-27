#!/usr/bin/env python3
"""Contrôle « zéro vanilla » (P1 : le juridique d'abord, la tech s'adapte).

Le mod ne doit livrer que du texte traduit, jamais de contenu vanilla recopié.
Deux niveaux :

1. Structure (toujours, CI comprise) :
   - data/i18n/*.csv : colonnes limitées à une liste blanche d'affichage ;
   - data/config/planets.json (fusion moteur) : chaque entrée ne porte que "name" ;
   - data/config/custom_entities.json (fusion moteur) : chaque entité ne porte
     que des noms affichés (defaultName, nameInText, shortName, aOrAn, isOrAre),
     feuilles = chaînes ;
   - data/world/factions/*.faction : clés limitées aux libellés affichés
     (noms, articles, grades, postes, noms de flottes), feuilles = chaînes.
2. Contenu (avec --vanilla CHEMIN_STARSECTOR_CORE, en local) :
   - aucune cellule de data/i18n/ identique à la vanilla (échec) ;
   - custom_entities.json : aucun nom identique à la vanilla, aucune entité
     absente de la vanilla (échec) ;
   - libellés .faction identiques à la vanilla signalés (avertissement :
     noms propres non traduits selon le glossaire).

Ne jamais assouplir une règle pour faire passer un fichier : un échec ici
signale une livraison de contenu vanilla, pas un bug du contrôle.

Usage : python tools/check_zero_vanilla.py [--vanilla D:/.../starsector-core]
Code de sortie : 0 si conforme, 1 sinon.
"""
from __future__ import annotations

import csv
import glob
import io
import json
import os
import re
import sys

I18N_COLS = {
    "id", "skinHullId", "type",
    "name", "designation", "desc", "sModDesc", "descriptionPrefix",
    "text1", "text2", "text3", "text4", "text5",
    "description", "author",
    "primaryRoleStr", "speedStr", "trackingStr", "turnRateStr", "accuracyStr",
    "customPrimary", "customPrimaryHL", "customAncillary", "customAncillaryHL",
}
I18N_KEYS = {"id", "skinHullId"}
# Clés composites : un id seul n'est pas unique (descriptions : guardian WEAPON/SHIP…).
I18N_CLE_COMPOSITE = {"descriptions.csv": ("id", "type")}
# Source vanilla de chaque dictionnaire data/i18n/ (contrôle de contenu).
I18N_SOURCE = {
    "ship_data.csv": "data/hulls/ship_data.csv",
    "hull_mods.csv": "data/hullmods/hull_mods.csv",
    "ship_systems.csv": "data/shipsystems/ship_systems.csv",
    "special_items.csv": "data/campaign/special_items.csv",
    "descriptions.csv": "data/strings/descriptions.csv",
    "skill_data.csv": "data/characters/skills/skill_data.csv",
    "weapon_data.csv": "data/weapons/weapon_data.csv",
    "market_conditions.csv": "data/campaign/market_conditions.csv",
    "commodities.csv": "data/campaign/commodities.csv",
    "industries.csv": "data/campaign/industries.csv",
}
FACTION_TOP = {
    "id", "displayName", "displayNameWithArticle", "displayNameLong",
    "displayNameLongWithArticle", "displayNameIsOrAre", "personNamePrefix",
    "personNamePrefixAOrAn", "entityNamePrefix", "ranks", "fleetTypeNames",
}
# custom_entities.json (fusion moteur) : seuls les noms affichés, jamais
# icon/sprite/interactionImage/tags… (les tableaux seraient AJOUTÉS à la vanilla).
ENTITE_CHAMPS = {"defaultName", "nameInText", "shortName", "aOrAn", "isOrAre"}


def lire(chemin: str) -> str:
    brut = open(chemin, "rb").read()
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return brut.decode(enc)
        except UnicodeDecodeError:
            pass
    raise UnicodeDecodeError("?", brut, 0, 1, chemin)


def json_starsector(texte: str):
    """JSON Starsector : commentaires #, clés sans guillemets, virgules finales, .5."""
    sortie, i, n, dans_chaine = [], 0, len(texte), False
    while i < n:
        c = texte[i]
        if dans_chaine:
            sortie.append(c)
            if c == "\\" and i + 1 < n:
                sortie.append(texte[i + 1])
                i += 2
                continue
            if c == '"':
                dans_chaine = False
        elif c == '"':
            dans_chaine = True
            sortie.append(c)
        elif c == "#":
            while i < n and texte[i] != "\n":
                i += 1
            continue
        else:
            sortie.append(c)
        i += 1
    t = "".join(sortie)
    t = re.sub(r",(\s*[}\]])", r"\1", t)
    t = re.sub(r'([{,]\s*)([A-Za-z_][A-Za-z0-9_]*)\s*:', r'\1"\2":', t)
    t = re.sub(r'([:\[,]\s*)(-?)\.(\d)', r"\g<1>\g<2>0.\3", t)
    return json.JSONDecoder().raw_decode(t.strip())[0]


def valeurs_nues(texte: str) -> str:
    """Hors chaînes : met entre guillemets les identifiants nus en valeur
    ([STATIONS]) et retire le suffixe f des flottants (1.1f), pour json_starsector."""
    sortie, i, n, dans_chaine = [], 0, len(texte), False
    while i < n:
        c = texte[i]
        if dans_chaine:
            sortie.append(c)
            if c == "\\" and i + 1 < n:
                sortie.append(texte[i + 1])
                i += 2
                continue
            if c == '"':
                dans_chaine = False
            i += 1
            continue
        if c == '"':
            dans_chaine = True
        elif c == "#":
            while i < n and texte[i] != "\n":
                i += 1
            continue
        else:
            m = re.match(r"[A-Za-z_][A-Za-z0-9_]*", texte[i:i + 200])
            if m:
                mot = m.group(0)
                suite = texte[i + len(mot):].lstrip()[:1]
                if i and (texte[i - 1].isdigit() or texte[i - 1] == ".") and mot == "f":
                    pass
                elif mot in ("true", "false", "null") or suite == ":" or (i and (texte[i - 1].isalnum() or texte[i - 1] == "_")):
                    sortie.append(mot)
                else:
                    sortie.append(f'"{mot}"')
                i += len(mot)
                continue
        sortie.append(c)
        i += 1
    return "".join(sortie)


def lignes_csv(chemin: str) -> tuple[list[str], list[dict]]:
    lecteur = csv.DictReader(io.StringIO(lire(chemin)))
    return list(lecteur.fieldnames or []), list(lecteur)


def feuilles(obj, chemin=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from feuilles(v, f"{chemin}.{k}" if chemin else k)
    else:
        yield chemin, obj


def verifier(racine: str, vanilla: str | None) -> tuple[list[str], list[str]]:
    erreurs, avertissements = [], []

    for chemin in sorted(glob.glob(os.path.join(racine, "data", "i18n", "*.csv"))):
        rel = os.path.relpath(chemin, racine).replace("\\", "/")
        colonnes, lignes = lignes_csv(chemin)
        hors = [c for c in colonnes if c not in I18N_COLS]
        if hors:
            erreurs.append(f"{rel} : colonnes hors liste d'affichage {hors}")
        base = os.path.basename(chemin)
        cles = I18N_CLE_COMPOSITE.get(base)
        if cles is None:
            cle = next((c for c in colonnes if c in I18N_KEYS), None)
            cles = (cle,) if cle else None
        if cles is None or any(c not in colonnes for c in cles):
            erreurs.append(f"{rel} : aucune colonne clé ({sorted(I18N_KEYS)})")
            continue
        if "type" in colonnes and "type" not in cles:
            erreurs.append(f"{rel} : colonne type réservée aux clés composites")
        if not vanilla or rel.endswith("/skins.csv"):
            continue
        source = I18N_SOURCE.get(base)
        if source is None:
            erreurs.append(f"{rel} : fichier i18n sans source vanilla connue (à déclarer ici)")
            continue
        _, van = lignes_csv(os.path.join(vanilla, source))

        def cle_de(r):
            return tuple((r.get(c) or "").strip() for c in cles)

        van = {cle_de(r): r for r in van}
        for r in lignes:
            v = van.get(cle_de(r))
            if v is None:
                continue
            for c in colonnes:
                if c in cles or not (r.get(c) or "").strip():
                    continue
                if (r[c] or "").strip() == (v.get(c) or "").strip():
                    erreurs.append(f"{rel} : {'|'.join(cle_de(r))}.{c} identique à la vanilla")

    skins = os.path.join(racine, "data", "i18n", "skins.csv")
    if vanilla and os.path.exists(skins):
        _, lignes = lignes_csv(skins)
        for r in lignes:
            sid = r["skinHullId"]
            cibles = glob.glob(os.path.join(vanilla, "data", "hulls", "skins", "*.skin"))
            for s in cibles:
                t = lire(s)
                if f'"{sid}"' in t:
                    try:
                        v = json_starsector(t).get("descriptionPrefix", "")
                    except ValueError:
                        v = None
                    if v is not None and v.strip() == (r.get("descriptionPrefix") or "").strip():
                        erreurs.append(f"data/i18n/skins.csv : {sid}.descriptionPrefix identique à la vanilla")
                    break

    planetes = os.path.join(racine, "data", "config", "planets.json")
    if os.path.exists(planetes):
        pl = json_starsector(lire(planetes))
        van = json_starsector(lire(os.path.join(vanilla, "data", "config", "planets.json"))) if vanilla else {}
        for k, v in pl.items():
            if not isinstance(v, dict) or set(v) != {"name"}:
                erreurs.append(f"data/config/planets.json : {k} porte autre chose que \"name\" ({sorted(v) if isinstance(v, dict) else type(v).__name__})")
            elif k in van and v["name"].strip() == str(van[k].get("name", "")).strip():
                erreurs.append(f"data/config/planets.json : {k}.name identique à la vanilla")

    entites = os.path.join(racine, "data", "config", "custom_entities.json")
    if os.path.exists(entites):
        rel = "data/config/custom_entities.json"
        try:
            ce = json_starsector(valeurs_nues(lire(entites)))
        except ValueError as e:
            ce = None
            erreurs.append(f"{rel} : illisible ({e})")
        van = json_starsector(valeurs_nues(lire(os.path.join(vanilla, rel)))) if vanilla else {}
        for k, v in (ce or {}).items():
            if not isinstance(v, dict) or not v:
                erreurs.append(f"{rel} : {k} n'est pas un objet de noms non vide")
                continue
            hors = sorted(set(v) - ENTITE_CHAMPS)
            if hors:
                erreurs.append(f"{rel} : {k} porte des champs hors noms affichés {hors}")
            for champ, val in v.items():
                if not isinstance(val, str):
                    erreurs.append(f"{rel} : {k}.{champ} n'est pas une chaîne ({type(val).__name__})")
            if vanilla:
                if k not in van:
                    erreurs.append(f"{rel} : {k} absente de la vanilla (entité incomplète créée)")
                    continue
                for champ, val in v.items():
                    if champ in ENTITE_CHAMPS and isinstance(val, str) and val.strip() == str(van[k].get(champ, "")).strip():
                        erreurs.append(f"{rel} : {k}.{champ} identique à la vanilla")

    for chemin in sorted(glob.glob(os.path.join(racine, "data", "world", "factions", "*.faction"))):
        rel = os.path.relpath(chemin, racine).replace("\\", "/")
        try:
            f = json_starsector(lire(chemin))
        except ValueError as e:
            erreurs.append(f"{rel} : illisible ({e})")
            continue
        hors = sorted(set(f) - FACTION_TOP)
        if hors:
            erreurs.append(f"{rel} : clés hors libellés affichés {hors}")
        for k in ("ranks",):
            for sous, bloc in (f.get(k) or {}).items():
                if sous not in ("ranks", "posts") or not isinstance(bloc, dict):
                    erreurs.append(f"{rel} : ranks.{sous} inattendu")
                    continue
                for rang, val in bloc.items():
                    if not isinstance(val, dict) or set(val) != {"name"}:
                        erreurs.append(f"{rel} : ranks.{sous}.{rang} porte autre chose que \"name\"")
        for nom, val in (f.get("fleetTypeNames") or {}).items():
            if not isinstance(val, str):
                erreurs.append(f"{rel} : fleetTypeNames.{nom} n'est pas une chaîne")
        for cle, val in feuilles(f):
            if cle != "id" and not isinstance(val, str):
                erreurs.append(f"{rel} : {cle} n'est pas une chaîne ({type(val).__name__})")
        if vanilla:
            vp = os.path.join(vanilla, os.path.relpath(chemin, racine))
            if os.path.exists(vp):
                try:
                    vf = dict(feuilles(json_starsector(lire(vp))))
                except ValueError:
                    vf = {}
                identiques = [c for c, v in feuilles(f) if c != "id" and vf.get(c) == v]
                if identiques:
                    avertissements.append(f"{rel} : {len(identiques)} libellé(s) identique(s) à la vanilla {identiques[:4]}")
    return erreurs, avertissements


def main() -> int:
    args = sys.argv[1:]
    vanilla = None
    if "--vanilla" in args:
        vanilla = args[args.index("--vanilla") + 1]
    racine = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    erreurs, avertissements = verifier(racine, vanilla)
    for a in avertissements:
        print(f"⚠️  {a}")
    for e in erreurs:
        print(f"❌ {e}")
    if erreurs:
        print(f"\nÉCHEC zéro vanilla : {len(erreurs)} écart(s).")
        return 1
    print(f"✅ Zéro vanilla : conforme ({'structure + contenu' if vanilla else 'structure'}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
