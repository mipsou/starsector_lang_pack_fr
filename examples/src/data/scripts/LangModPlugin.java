package data.scripts;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.EveryFrameScript;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.campaign.InteractionDialogAPI;

/**
 * Minimal language mod plugin — example translating ONE hardcoded Java string.
 *
 * How it works:
 *   Starsector hardcodes "You decide to..." in dialog prompts (not externalized in CSV/JSON).
 *   An EveryFrameScript watches the active dialog and swaps the prompt text with our translation.
 *
 * To adapt for another language:
 *   1. Change the translation string below.
 *   2. Rename this class (e.g. SpanishLangModPlugin) and keep only ONE plugin per mod.
 *   3. Compile to a JAR, reference it in mod_info.json via "jars": ["jars/yourlang.jar"].
 *
 * Constraints:
 *   - No reflection (Starsector sandbox blocks java.lang.reflect).
 *   - Null-guard every API access — no crashes during loading/combat screens.
 */
public class LangModPlugin extends BaseModPlugin {

    // Your translation here — replace with your target language
    private static final String TARGET = "You decide to...";
    private static final String REPLACEMENT = "Vous décidez de...";

    @Override
    public void onGameLoad(boolean newGame) {
        Global.getSector().addTransientScript(new PromptTranslator());
    }

    /** Runs every frame, replaces the hardcoded prompt when it appears. */
    static class PromptTranslator implements EveryFrameScript {
        public boolean isDone() { return false; }
        public boolean runWhilePaused() { return true; }

        public void advance(float amount) {
            try {
                if (Global.getSector() == null) return;
                if (Global.getSector().getCampaignUI() == null) return;

                InteractionDialogAPI dialog = Global.getSector().getCampaignUI().getCurrentInteractionDialog();
                if (dialog == null) return;

                if (TARGET.equals(dialog.getPromptText())) {
                    dialog.setPromptText(REPLACEMENT);
                }
            } catch (Exception e) {
                // Fallback EN if anything goes wrong — never crash the game
            }
        }
    }
}
