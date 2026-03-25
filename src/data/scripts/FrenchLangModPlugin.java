package data.scripts;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.Global;
import org.apache.log4j.Logger;

/**
 * Plugin principal du mod de traduction FR.
 *
 * Utilise uniquement l'API publique (pas de reflection).
 * Le sandbox Starsector bloque java.lang.reflect.Field.
 *
 * Traduit les dialogues de flotte via un CampaignPlugin
 * qui injecte un wrapper autour de FleetInteractionDialogPluginImpl.
 */
public class FrenchLangModPlugin extends BaseModPlugin {

    private static final Logger log = Global.getLogger(FrenchLangModPlugin.class);

    @Override
    public void onApplicationLoad() throws Exception {
        log.info("=== French Language Pack v1.3.0 ===");
        log.info("Mode : API publique (drop-and-play)");
        log.info("=== French Language Pack loaded ===");
    }

    @Override
    public void onGameLoad(boolean newGame) {
        // Enregistrer le plugin campagne qui traduit les dialogues
        Global.getSector().registerPlugin(new FrenchCampaignPlugin());
        log.info("FrenchCampaignPlugin registered");

        // Enregistrer le script de traduction des prompts (EveryFrameScript)
        Global.getSector().addTransientScript(new FrenchPromptTranslator());
        log.info("FrenchPromptTranslator registered");
    }
}
