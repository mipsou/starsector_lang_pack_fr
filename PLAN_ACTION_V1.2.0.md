# Plan d'Action Détaillé pour le Livrable v1.2.0 (Traduction `strings.json` et `descriptions.csv`)

1.  **Objectif Principal** : Produire la version 1.2.0 du pack de traduction français pour Starsector, incluant la traduction complète et validée des fichiers `strings.json` et `descriptions.csv`.

2.  **Fichiers Clés** :
    *   Fichier de traduction `strings.json` à compléter/valider : `starsector_lang_pack_fr_private/localization/data/strings/strings.json`
    *   Fichier original `strings.json` de référence : `starsector_lang_pack_fr_private/original/data/strings/strings.json`
    *   Fichier de traduction `descriptions.csv` à traduire : `starsector_lang_pack_fr_private/localization/data/strings/descriptions.csv` (actuellement en anglais)
    *   Fichier original `descriptions.csv` de référence : `starsector_lang_pack_fr_private/original/data/strings/descriptions.csv`
    *   Documentation de référence :
        *   `MEMOIRE_TECHNIQUE.md`
        *   `FORMATS_JSON.md` (pour `strings.json`)
        *   `DEVBOOK.md`
        *   `README.md` (à mettre à jour pour la v1.2.0)
        *   `mod_info.json` (à mettre à jour pour la v1.2.0)

3.  **Phases du Projet** :

    *   **Phase 1: Travaux sur `strings.json` (À réaliser par le mode "Code")**
        1.  **Finalisation de la Traduction** :
            *   Lire `starsector_lang_pack_fr_private/localization/data/strings/strings.json` et `starsector_lang_pack_fr_private/original/data/strings/strings.json`.
            *   Identifier et traduire toutes les chaînes restantes en anglais.
            *   Réviser les traductions existantes si nécessaire pour la cohérence et la qualité.
        2.  **Validation et Formatage** :
            *   Appliquer les règles de typographie française.
            *   Formater le JSON selon les standards Starsector.
            *   Assurer l'encodage UTF-8 sans BOM.

    *   **Phase 2: Travaux sur `descriptions.csv` (À réaliser par le mode "Code")**
        1.  **Traduction Intégrale** :
            *   Lire `starsector_lang_pack_fr_private/localization/data/strings/descriptions.csv` (actuellement en anglais) et `starsector_lang_pack_fr_private/original/data/strings/descriptions.csv`.
            *   Traduire toutes les descriptions de la colonne `text1` (et autres colonnes pertinentes si elles contiennent du texte à traduire) en français. Le format CSV doit être préservé (séparateur virgule, guillemets si nécessaire).
        2.  **Validation et Formatage** :
            *   Appliquer les règles de typographie française.
            *   Assurer l'encodage UTF-8 sans BOM.
            *   Valider la structure CSV (nombre de colonnes, etc.).

    *   **Phase 3: Préparation du livrable (Pack v1.2.0) (À réaliser par le mode "Code" ou "Architecte" après validation des Phases 1 & 2)**
        1.  **Mise à jour de `mod_info.json`** :
            *   Version : "1.2.0".
            *   Description : Indiquer l'ajout des traductions de `strings.json` et `descriptions.csv`.
        2.  **Mise à jour de `README.md`** :
            *   Fonctionnalités : Inclure `strings.json` et `descriptions.csv`.
            *   Notes de Version : Pour la v1.2.0.
            *   Prochaines Versions : v1.3.0 (missions).
        3.  **Nettoyage et Packaging** :
            *   Créer l'archive ZIP `starsector_lang_pack_fr-1.2.0.zip`.
        4.  **Documentation des Travaux** :
            *   Ajouter une entrée dans `DEVBOOK.md` pour la v1.2.0.

4.  **Diagramme Mermaid du Plan** :
    ```mermaid
    graph TD
        subgraph Phase 1 - strings.json (Mode Code)
            P1_A[Lire strings.json (FR existant) et strings.json (Original)] --> P1_B{Identifier/Réviser chaînes};
            P1_B --> P1_C[Traduire/Compléter chaînes en Français];
            P1_C --> P1_D[Valider/Formater strings.json];
            P1_D --> P1_E{strings.json OK?};
        end

        subgraph Phase 2 - descriptions.csv (Mode Code)
            P2_A[Lire descriptions.csv (FR existant - anglais) et descriptions.csv (Original)] --> P2_B[Traduire intégralement descriptions.csv];
            P2_B --> P2_C[Valider/Formater descriptions.csv];
            P2_C --> P2_D{descriptions.csv OK?};
        end

        subgraph Phase 3 - Préparation Livrable v1.2.0 (Mode Code/Architecte)
            P3_A[Mettre à jour mod_info.json (v1.2.0)];
            P3_B[Mettre à jour README.md (v1.2.0)];
            P3_C[Créer archive ZIP du mod (v1.2.0)];
            P3_D[Documenter dans DEVBOOK.md (v1.2.0)];
            P3_E[Livrable: Pack v1.2.0 Prêt];
        end

        P1_E -- Oui --> P2_A;
        P1_E -- Non --> P1_C;
        P2_D -- Oui --> P3_A;
        P2_D -- Non --> P2_B;