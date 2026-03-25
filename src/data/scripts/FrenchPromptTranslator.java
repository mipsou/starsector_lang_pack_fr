package data.scripts;

import com.fs.starfarer.api.EveryFrameScript;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.campaign.CampaignUIAPI;
import com.fs.starfarer.api.campaign.InteractionDialogAPI;
import org.apache.log4j.Logger;

import java.util.HashMap;
import java.util.Map;

/**
 * EveryFrameScript qui traduit le prompt "You decide to..." en francais
 * dans TOUS les dialogues de campagne, quel que soit leur source.
 *
 * Contexte du probleme :
 * Le prompt "You decide to..." est hardcode dans CargoPods.java, MarketCMD.java
 * et du code OBF. Le FrenchFleetInteractionDialogPlugin et le
 * FrenchSalvageInteractionDialogPlugin ne couvrent que les dialogues qu'ils
 * wrappent. Les dialogues crees directement par CargoPods/MarketCMD echappent
 * au translatePrompt() car ils ne passent pas par ces wrappers.
 *
 * Solution : un script transient qui tourne a chaque frame et verifie si
 * un dialogue actif a un prompt EN connu, puis le remplace par le FR.
 *
 * Contraintes RSSI :
 * - Zero reflection (java.lang.reflect bloque par le sandbox)
 * - Gardes null sur tous les acces chaines
 * - Try/catch global avec fallback EN (pas de crash)
 * - Log des erreurs pour diagnostic
 *
 * Enregistrement : dans FrenchLangModPlugin.onGameLoad() :
 *   Global.getSector().addTransientScript(new FrenchPromptTranslator());
 *
 * Performance : le script ne fait qu'un getPromptText() + equals() par frame
 * quand un dialogue est ouvert. Cout negligeable.
 */
public class FrenchPromptTranslator implements EveryFrameScript {

    private static final Logger log = Global.getLogger(FrenchPromptTranslator.class);

    /**
     * Mapping des prompts EN -> FR.
     * Extensible : ajouter ici tout prompt hardcode a traduire.
     */
    private static final Map<String, String> PROMPT_TRANSLATIONS = new HashMap<String, String>();
    static {
        PROMPT_TRANSLATIONS.put("You decide to...", "Vous d\u00e9cidez de...");
    }

    /** Dernier prompt traduit — evite les logs repetes */
    private String lastTranslatedPrompt = null;

    /**
     * Ce script ne se termine jamais — il tourne tant que la partie est chargee.
     */
    @Override
    public boolean isDone() {
        return false;
    }

    /**
     * Tourne meme en pause — les dialogues sont interactifs quand le jeu est en pause.
     */
    @Override
    public boolean runWhilePaused() {
        return true;
    }

    /**
     * Verifie a chaque frame si un dialogue actif a un prompt EN a traduire.
     *
     * Chaine d'acces : Global.getSector() -> getCampaignUI() -> getCurrentInteractionDialog()
     * Chaque maillon peut etre null (pas de secteur, pas d'UI, pas de dialogue).
     *
     * @param amount delta temps en secondes (non utilise)
     */
    @Override
    public void advance(float amount) {
        try {
            // Garde null : pas de secteur charge
            if (Global.getSector() == null) return;

            // Garde null : pas d'UI campagne (ecran de chargement, combat)
            CampaignUIAPI campaignUI = Global.getSector().getCampaignUI();
            if (campaignUI == null) return;

            // Garde null : pas de dialogue actif
            InteractionDialogAPI dialog = campaignUI.getCurrentInteractionDialog();
            if (dialog == null) {
                // Reset du tracking quand le dialogue se ferme
                lastTranslatedPrompt = null;
                return;
            }

            // Lire le prompt actuel
            String prompt = dialog.getPromptText();
            if (prompt == null) return;

            // Verifier si ce prompt est dans notre mapping
            String frPrompt = PROMPT_TRANSLATIONS.get(prompt);
            if (frPrompt != null) {
                dialog.setPromptText(frPrompt);

                // Log une seule fois par prompt traduit (evite le spam)
                if (!frPrompt.equals(lastTranslatedPrompt)) {
                    log.info("Prompt traduit: \"" + prompt + "\" -> \"" + frPrompt + "\"");
                    lastTranslatedPrompt = frPrompt;
                }
            }

        } catch (Exception e) {
            // Fallback EN : en cas d'erreur, le prompt reste en anglais
            // On ne crash pas le jeu pour une traduction manquee
            log.error("FrenchPromptTranslator erreur: " + e.getMessage());
        }
    }
}
