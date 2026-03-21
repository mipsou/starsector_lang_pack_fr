package data.scripts;

import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.campaign.InteractionDialogAPI;
import com.fs.starfarer.api.campaign.OptionPanelAPI;
import com.fs.starfarer.api.impl.campaign.FleetInteractionDialogPluginImpl;
import org.apache.log4j.Logger;

import java.util.HashMap;
import java.util.Map;

/**
 * Wrapper autour du dialogue d'interaction de flotte vanilla.
 * Herite de FleetInteractionDialogPluginImpl et traduit les options
 * hardcodees apres que le code vanilla les a ajoutees.
 *
 * Strings cibles (Tier 1 — visibles a chaque rencontre) :
 * - "Open a comm link"
 * - "Cut the comm link"
 * - "Move in to engage"
 * - "Disengage"
 * - "Pursue them"
 * - "Your forces"
 * - "You decide to..."
 * - "Leave"
 * - "Continue"
 */
public class FrenchFleetInteractionDialogPlugin extends FleetInteractionDialogPluginImpl {

    private static final Logger log = Global.getLogger(FrenchFleetInteractionDialogPlugin.class);

    /** Mapping option labels EN -> FR */
    private static final Map<String, String> OPTION_TRANSLATIONS = new HashMap<String, String>();
    static {
        // Tier 1 — dialogue de flotte
        OPTION_TRANSLATIONS.put("Open a comm link", "Ouvrir un canal comm");
        OPTION_TRANSLATIONS.put("Cut the comm link", "Couper la comm");
        OPTION_TRANSLATIONS.put("Move in to engage", "Engager le combat");
        OPTION_TRANSLATIONS.put("Disengage", "Rompre le combat");
        OPTION_TRANSLATIONS.put("Pursue them", "Les poursuivre");
        OPTION_TRANSLATIONS.put("Leave", "Partir");
        OPTION_TRANSLATIONS.put("Continue", "Continuer");
        OPTION_TRANSLATIONS.put("Disengage by executing a series of special maneuvers",
            "Rompre le combat par une serie de manoeuvres speciales");
    }

    /** Mapping prompt text EN -> FR */
    private static final Map<String, String> PROMPT_TRANSLATIONS = new HashMap<String, String>();
    static {
        PROMPT_TRANSLATIONS.put("You decide to...", "Vous decidez de...");
    }

    @Override
    public void init(InteractionDialogAPI dialog) {
        super.init(dialog);
        translateOptions();
        translatePrompt(dialog);
    }

    @Override
    public void optionSelected(String optionText, Object optionData) {
        // Traduire le texte passe a super pour que addOptionSelectedText
        // ecrive le FR dans le panneau narratif
        String translatedText = optionText;
        if (optionText != null && OPTION_TRANSLATIONS.containsKey(optionText)) {
            translatedText = OPTION_TRANSLATIONS.get(optionText);
        }

        // Traduire aussi les options du panneau avant super
        translateOptions();

        super.optionSelected(translatedText, optionData);

        // Apres super, le vanilla reconstruit les options suivantes
        translateOptions();
        translatePrompt(this.dialog);
    }

    /**
     * Traduit toutes les options actuellement affichees.
     * Utilise setOptionText() de l'API OptionPanelAPI.
     */
    private void translateOptions() {
        if (this.options == null) return;

        try {
            // Recuperer la liste des options via l'API
            java.util.List savedOptions = this.options.getSavedOptionList();
            if (savedOptions == null) return;

            // Note : getSavedOptionList retourne des objets internes
            // On ne peut pas iterer dessus facilement en Java 7
            // Approche alternative : tenter setOptionText pour chaque OptionId connu
            for (OptionId optionId : OptionId.values()) {
                if (this.options.hasOption(optionId)) {
                    // On ne connait pas le texte actuel via l'API
                    // Mais on peut tenter de le remplacer par OptionId
                    translateOptionById(optionId);
                }
            }
        } catch (Exception e) {
            log.error("Error translating options: " + e.getMessage());
        }
    }

    /**
     * Traduit une option par son OptionId.
     * Map les OptionId connus vers leur traduction FR.
     */
    private void translateOptionById(OptionId optionId) {
        String frText = null;

        switch (optionId) {
            case OPEN_COMM:
                frText = "Ouvrir un canal comm";
                break;
            case CUT_COMM:
                frText = "Couper la comm";
                break;
            case ENGAGE:
                frText = "Engager le combat";
                break;
            case DISENGAGE:
                frText = "Rompre le combat";
                break;
            case PURSUE:
                frText = "Les poursuivre";
                break;
            case LEAVE:
                frText = "Partir";
                break;
            case CLEAN_DISENGAGE:
                frText = "Rompre le combat par des manoeuvres speciales";
                break;
            case REINIT_CONTINUE:
            case BEGIN_FLEET_ENCOUNTER_2:
                frText = "Continuer";
                break;
            default:
                break;
        }

        if (frText != null) {
            this.options.setOptionText(frText, optionId);
        }
    }

    /**
     * Traduit le prompt text ("You decide to...").
     */
    private void translatePrompt(InteractionDialogAPI dialog) {
        if (dialog == null) return;
        String prompt = dialog.getPromptText();
        if (prompt != null && PROMPT_TRANSLATIONS.containsKey(prompt)) {
            dialog.setPromptText(PROMPT_TRANSLATIONS.get(prompt));
        }
    }
}
