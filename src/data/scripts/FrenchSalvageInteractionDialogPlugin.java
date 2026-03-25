package data.scripts;

import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.campaign.InteractionDialogAPI;
import com.fs.starfarer.api.campaign.InteractionDialogPlugin;
import com.fs.starfarer.api.campaign.OptionPanelAPI;
import com.fs.starfarer.api.campaign.TextPanelAPI;
import com.fs.starfarer.api.campaign.rules.MemoryAPI;
import com.fs.starfarer.api.combat.EngagementResultAPI;
import com.fs.starfarer.api.impl.campaign.RuleBasedInteractionDialogPluginImpl;
import org.apache.log4j.Logger;

import java.util.HashMap;
import java.util.Map;

/**
 * Wrapper de traduction pour le dialogue de salvage/recuperation.
 *
 * Le salvage utilise le systeme de regles (RuleBasedInteractionDialogPluginImpl).
 * Ce wrapper delegue au plugin vanilla et traduit les textes EN -> FR
 * apres chaque action du joueur.
 *
 * Pattern : Delegation avec interception des options textuelles.
 * Contraintes RSSI : zero java.lang.reflect, gardes null, fallback EN, try/catch.
 *
 * Les 58 strings proviennent de salvage-dialog-fr.csv.
 */
public class FrenchSalvageInteractionDialogPlugin implements InteractionDialogPlugin {

    private static final Logger log = Global.getLogger(FrenchSalvageInteractionDialogPlugin.class);

    /** Plugin vanilla delegue (RuleBasedInteractionDialogPluginImpl) */
    private final InteractionDialogPlugin delegate;

    /** Reference au dialogue pour la traduction post-action */
    private InteractionDialogAPI dialog;

    // ========================================================================
    // Mapping texte EN -> FR : options de dialogue (buttons & labels)
    // Source : salvage-dialog-fr.csv, colonnes type=button/option
    // ========================================================================
    private static final Map<String, String> OPTION_TRANSLATIONS = new HashMap<String, String>();
    static {
        // UI Buttons & Labels
        OPTION_TRANSLATIONS.put("Confirm", "Confirmer");
        OPTION_TRANSLATIONS.put("Abort", "Annuler");
        OPTION_TRANSLATIONS.put("Take All", "Tout prendre");
        OPTION_TRANSLATIONS.put("Confirm & Continue", "Confirmer et continuer");
        OPTION_TRANSLATIONS.put("Continue", "Continuer");
        OPTION_TRANSLATIONS.put("Leave", "Partir");
        OPTION_TRANSLATIONS.put("Cancel", "Annuler");
        OPTION_TRANSLATIONS.put("Go back", "Retour");
        OPTION_TRANSLATIONS.put("Ok", "Ok");

        // Defender Interaction
        OPTION_TRANSLATIONS.put("Engage the automated defenses",
            "Engager les d\u00e9fenses automatis\u00e9es");
        OPTION_TRANSLATIONS.put("Re-engage the automated defenses",
            "R\u00e9-engager les d\u00e9fenses automatis\u00e9es");

        // AI Cores
        OPTION_TRANSLATIONS.put("Select AI cores to turn in",
            "S\u00e9lectionnez les c\u0153urs IA \u00e0 remettre");

        // Fleet Interaction post-combat salvage
        OPTION_TRANSLATIONS.put("Perform a salvage operation, then leave",
            "Effectuer une op\u00e9ration de r\u00e9cup\u00e9ration, puis partir");

        // Salvage confirmation
        OPTION_TRANSLATIONS.put("Proceed with salvage operation?",
            "Proc\u00e9der \u00e0 l'op\u00e9ration de r\u00e9cup\u00e9ration ?");
    }

    // ========================================================================
    // Mapping prompt EN -> FR
    // ========================================================================
    private static final Map<String, String> PROMPT_TRANSLATIONS = new HashMap<String, String>();
    static {
        PROMPT_TRANSLATIONS.put("You decide to...", "Vous d\u00e9cidez de...");
    }

    // ========================================================================
    // Mapping texte panel EN -> FR : phrases longues affichees dans le texte
    // Utilisees pour le remplacement substring dans le contenu affiche.
    // Source : salvage-dialog-fr.csv, colonnes type=text/label/stat
    // ========================================================================
    private static final Map<String, String> TEXT_REPLACEMENTS = new HashMap<String, String>();
    static {
        // Salvage Assessment
        TEXT_REPLACEMENTS.put(
            "You receive a preliminary assessment of a potential salvage operation from the exploration crews.",
            "Vous recevez une \u00e9valuation pr\u00e9liminaire d'une op\u00e9ration de r\u00e9cup\u00e9ration potentielle de la part des \u00e9quipes d'exploration.");
        TEXT_REPLACEMENTS.put("Resource recovery effectiveness:",
            "Efficacit\u00e9 de r\u00e9cup\u00e9ration des ressources :");
        TEXT_REPLACEMENTS.put("Scavenging effectiveness:",
            "Efficacit\u00e9 de fouille :");
        TEXT_REPLACEMENTS.put("Crew & machinery: required (available)",
            "\u00c9quipage et machines : requis (disponible)");
        TEXT_REPLACEMENTS.put("No tariffs", "Aucune taxe");
        TEXT_REPLACEMENTS.put("You pay", "Vous payez");

        // Stat modifiers
        TEXT_REPLACEMENTS.put("Base effectiveness", "Efficacit\u00e9 de base");
        TEXT_REPLACEMENTS.put("Salvaging skill", "Comp\u00e9tence R\u00e9cup\u00e9ration");
        TEXT_REPLACEMENTS.put("Fleetwide salvaging capability",
            "Capacit\u00e9 de r\u00e9cup\u00e9ration de la flotte");
        TEXT_REPLACEMENTS.put("Debris field density", "Densit\u00e9 du champ de d\u00e9bris");
        TEXT_REPLACEMENTS.put("Recent salvage operation",
            "Op\u00e9ration de r\u00e9cup\u00e9ration r\u00e9cente");

        // Titres de panneaux
        TEXT_REPLACEMENTS.put("Salvaged Items", "Objets r\u00e9cup\u00e9r\u00e9s");
        TEXT_REPLACEMENTS.put("Salvage operation", "Op\u00e9ration de r\u00e9cup\u00e9ration");
        TEXT_REPLACEMENTS.put("Current transaction", "Transaction en cours");
        TEXT_REPLACEMENTS.put("Cargo Pods", "Conteneurs de fret");
        TEXT_REPLACEMENTS.put("Spoils", "Butin");
        // "Salvaged" et "Salvage" sont trop courts pour du remplacement global
        // => traites par matchExact dans translatePrompt si besoin

        // Debris Field Description
        TEXT_REPLACEMENTS.put(
            "The field appears stable and will not drift apart any time soon.",
            "Le champ semble stable et ne se dispersera pas de sit\u00f4t.");
        TEXT_REPLACEMENTS.put(
            "The field is unstable, but should not drift apart for ",
            "Le champ est instable mais ne devrait pas se disperser avant ");
        TEXT_REPLACEMENTS.put(
            " Long-range scans indicate it's unlikely anything of much value would be found inside.",
            " Les scans longue port\u00e9e indiquent qu'il est peu probable de trouver quoi que ce soit de valeur \u00e0 l'int\u00e9rieur.");
        TEXT_REPLACEMENTS.put(
            " Long-range scans indicate it's possible something of value could be found inside.",
            " Les scans longue port\u00e9e indiquent qu'il est possible de trouver quelque chose de valeur \u00e0 l'int\u00e9rieur.");
        TEXT_REPLACEMENTS.put(
            " Long-range scans indicate it's likely something of value could be found inside.",
            " Les scans longue port\u00e9e indiquent qu'il est probable de trouver quelque chose de valeur \u00e0 l'int\u00e9rieur.");

        // Risk descriptions
        TEXT_REPLACEMENTS.put(
            "There are indications of some easy pickings to be had, and the risk of an accident during a salvage operation is low.",
            "Des indices montrent qu'il y a des prises faciles \u00e0 port\u00e9e de main, et le risque d'accident lors d'une op\u00e9ration de r\u00e9cup\u00e9ration est faible.");

        // Debris density info
        TEXT_REPLACEMENTS.put(
            "The density of the debris field affects both the amount of resources and the number of rare items found.",
            "La densit\u00e9 du champ de d\u00e9bris affecte \u00e0 la fois la quantit\u00e9 de ressources et le nombre d'objets rares trouv\u00e9s.");
        TEXT_REPLACEMENTS.put(
            "The recovery effectiveness does not affect the chance of finding rare and valuable items.",
            "L'efficacit\u00e9 de r\u00e9cup\u00e9ration n'affecte pas les chances de trouver des objets rares et pr\u00e9cieux.");

        // Accidents
        TEXT_REPLACEMENTS.put(
            "An accident during the operation has resulted in the loss of ",
            "Un accident durant l'op\u00e9ration a entra\u00een\u00e9 la perte de ");
        TEXT_REPLACEMENTS.put(" crew.", " membre(s) d'\u00e9quipage.");
        TEXT_REPLACEMENTS.put(" heavy machinery.", " machine(s) lourde(s).");
        TEXT_REPLACEMENTS.put(" crew and ", " membre(s) d'\u00e9quipage et ");

        // Salvage Results
        TEXT_REPLACEMENTS.put(
            "Operations conclude with nothing of value found.",
            "Les op\u00e9rations se terminent sans rien trouver de valeur.");

        // Ship Recovery
        TEXT_REPLACEMENTS.put(
            "Salvage crews boarding the wreck discover that many essential systems are undamaged and the ship could be restored to basic functionality.",
            "Les \u00e9quipes de r\u00e9cup\u00e9ration montant \u00e0 bord de l'\u00e9pave d\u00e9couvrent que de nombreux syst\u00e8mes essentiels sont intacts et que le vaisseau pourrait \u00eatre remis en \u00e9tat de fonctionnement.");
        TEXT_REPLACEMENTS.put("Closer inspection reveals ",
            "Un examen plus approfondi r\u00e9v\u00e8le ");
        TEXT_REPLACEMENTS.put(" could be restored to basic functionality.",
            " pourrai(en)t \u00eatre remis en \u00e9tat de fonctionnement.");

        // Cargo Manifest
        TEXT_REPLACEMENTS.put("A cargo manifest found by the salvage crews ",
            "Un manifeste de cargaison trouv\u00e9 par les \u00e9quipes de r\u00e9cup\u00e9ration ");
        TEXT_REPLACEMENTS.put(" indicates the presence of a quantity of ",
            " indique la pr\u00e9sence d'une quantit\u00e9 de ");
        TEXT_REPLACEMENTS.put(
            "likely to be found if proper salvage operations are conducted.",
            "susceptible d'\u00eatre trouv\u00e9e si des op\u00e9rations de r\u00e9cup\u00e9ration ad\u00e9quates sont men\u00e9es.");

        // Fleet Bonuses (avec %s pour les valeurs dynamiques)
        TEXT_REPLACEMENTS.put("Your fleet also has a ",
            "Votre flotte b\u00e9n\u00e9ficie \u00e9galement d'un ");
        TEXT_REPLACEMENTS.put(" bonus to the amount of fuel recovered",
            " bonus sur la quantit\u00e9 de carburant r\u00e9cup\u00e9r\u00e9");
        TEXT_REPLACEMENTS.put(" bonus to the number of rare items found",
            " bonus sur le nombre d'objets rares trouv\u00e9s");

        // Tutorial
        TEXT_REPLACEMENTS.put(
            "Scavenging requires Heavy Machinery, but there is some in your cargo holds.",
            "La fouille n\u00e9cessite des Machines lourdes, mais vous en avez dans vos soutes.");

        // Debris Field Tooltip
        TEXT_REPLACEMENTS.put(
            "Scavenging through the debris for anything useful is possible, but can be dangerous for the crew and equipment involved.",
            "Fouiller les d\u00e9bris \u00e0 la recherche de quoi que ce soit d'utile est possible, mais peut \u00eatre dangereux pour l'\u00e9quipage et le mat\u00e9riel impliqu\u00e9s.");

        // Ability name
        TEXT_REPLACEMENTS.put("Scavenging", "Fouille");
    }

    // ========================================================================
    // Constructeur
    // ========================================================================

    /**
     * Cree un wrapper de traduction autour du plugin vanilla.
     *
     * @param delegate le plugin vanilla (RuleBasedInteractionDialogPluginImpl),
     *                 ne doit pas etre null
     */
    public FrenchSalvageInteractionDialogPlugin(InteractionDialogPlugin delegate) {
        if (delegate == null) {
            throw new IllegalArgumentException("Le plugin delegue ne peut pas etre null");
        }
        this.delegate = delegate;
    }

    /**
     * Constructeur par defaut — cree un RuleBasedInteractionDialogPluginImpl
     * comme delegue. Utilise quand le CampaignPlugin doit retourner un plugin
     * directement sans disposer du plugin vanilla.
     */
    public FrenchSalvageInteractionDialogPlugin() {
        this.delegate = new RuleBasedInteractionDialogPluginImpl();
    }

    // ========================================================================
    // InteractionDialogPlugin — delegation integrale + traduction
    // ========================================================================

    @Override
    public void init(InteractionDialogAPI dialog) {
        this.dialog = dialog;
        delegate.init(dialog);
        translateAllOptions();
        translatePrompt();
    }

    @Override
    public void optionSelected(String optionText, Object optionData) {
        // Traduire le texte selectionne pour le log visuel du joueur
        if (this.dialog != null && optionText != null) {
            String frText = OPTION_TRANSLATIONS.get(optionText);
            if (frText != null) {
                try {
                    this.dialog.addOptionSelectedText(frText);
                    delegate.optionSelected(null, optionData);
                } catch (Exception e) {
                    log.error("Erreur traduction optionSelected [" + optionText + "]: " + e.getMessage());
                    // Fallback EN : repasser le texte original au delegate
                    delegate.optionSelected(optionText, optionData);
                }
            } else {
                // Pas de traduction connue : fallback EN
                delegate.optionSelected(optionText, optionData);
            }
        } else {
            delegate.optionSelected(optionText, optionData);
        }

        // Apres delegate — le vanilla reconstruit les options
        translateAllOptions();
        translatePrompt();
    }

    @Override
    public void optionMousedOver(String optionText, Object optionData) {
        delegate.optionMousedOver(optionText, optionData);
    }

    @Override
    public void advance(float amount) {
        delegate.advance(amount);
        // Traduire en continu — certaines options sont ajoutees de facon asynchrone
        translateAllOptions();
    }

    @Override
    public void backFromEngagement(EngagementResultAPI battleResult) {
        delegate.backFromEngagement(battleResult);
        translateAllOptions();
        translatePrompt();
    }

    @Override
    public Object getContext() {
        return delegate.getContext();
    }

    @Override
    public Map<String, MemoryAPI> getMemoryMap() {
        return delegate.getMemoryMap();
    }

    // ========================================================================
    // Methodes de traduction
    // ========================================================================

    /**
     * Traduit toutes les options visibles dans le panneau d'options.
     *
     * Pour le dialogue rule-based, les optionData sont des String (commande de regle).
     * On ne peut pas connaitre les optionData sans reflect. On traduit donc
     * le texte affiche en interceptant optionSelected() et en utilisant
     * addOptionSelectedText(). Les textes d'options visibles sont remplaces
     * via le texte du bouton quand le rule engine recharge les options.
     *
     * Garde null sur dialog. Try/catch global.
     */
    private void translateAllOptions() {
        if (this.dialog == null) return;
        OptionPanelAPI options = this.dialog.getOptionPanel();
        if (options == null) return;

        try {
            // Pour chaque option connue, on tente le remplacement par optionData string.
            // Dans le rule-based system, beaucoup d'optionData sont des Strings
            // comme "salDefLeave", "salDefEngage", etc.
            // On traduit aussi par les textes exacts connus.
            for (Map.Entry<String, String> entry : OPTION_TRANSLATIONS.entrySet()) {
                try {
                    // Tenter de remplacer si l'option existe avec ce texte comme data
                    if (options.hasOption(entry.getKey())) {
                        options.setOptionText(entry.getValue(), entry.getKey());
                    }
                } catch (Exception e) {
                    // Option pas trouvee — normal, on skip silencieusement
                }
            }
        } catch (Exception e) {
            log.error("Erreur traduction options salvage: " + e.getMessage());
        }
    }

    /**
     * Traduit le prompt text ("You decide to..." -> "Vous decidez de...").
     * Garde null sur dialog. Try/catch.
     */
    private void translatePrompt() {
        if (this.dialog == null) return;
        try {
            String prompt = this.dialog.getPromptText();
            if (prompt != null && PROMPT_TRANSLATIONS.containsKey(prompt)) {
                this.dialog.setPromptText(PROMPT_TRANSLATIONS.get(prompt));
            }
        } catch (Exception e) {
            log.error("Erreur traduction prompt salvage: " + e.getMessage());
        }
    }

    // ========================================================================
    // Utilitaire : traduction de texte par remplacement substring
    // ========================================================================

    /**
     * Applique les remplacements de texte connus sur une chaine.
     * Utilise pour les traductions de phrases longues (assessment, debris, etc.).
     * Fallback EN : retourne le texte original si aucune traduction ne matche.
     *
     * @param text le texte EN a traduire (peut etre null)
     * @return le texte FR ou le texte original si pas de traduction
     */
    public static String translateText(String text) {
        if (text == null) return null;
        String result = text;
        for (Map.Entry<String, String> entry : TEXT_REPLACEMENTS.entrySet()) {
            try {
                if (result.contains(entry.getKey())) {
                    result = result.replace(entry.getKey(), entry.getValue());
                }
            } catch (Exception e) {
                // Erreur de remplacement — on continue avec le texte tel quel
            }
        }
        return result;
    }

    /**
     * Retourne la traduction FR d'un texte d'option, ou null si inconnu.
     * Utilise par d'autres plugins pour traduire des options de salvage.
     *
     * @param enText le texte EN de l'option
     * @return le texte FR ou null
     */
    public static String getOptionTranslation(String enText) {
        if (enText == null) return null;
        return OPTION_TRANSLATIONS.get(enText);
    }
}

