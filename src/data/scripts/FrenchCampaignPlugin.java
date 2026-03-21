package data.scripts;

import com.fs.starfarer.api.PluginPick;
import com.fs.starfarer.api.campaign.BaseCampaignPlugin;
import com.fs.starfarer.api.campaign.InteractionDialogPlugin;
import com.fs.starfarer.api.campaign.SectorEntityToken;
import com.fs.starfarer.api.campaign.CampaignFleetAPI;
import com.fs.starfarer.api.campaign.CampaignPlugin;

/**
 * Plugin campagne qui intercepte la creation des dialogues
 * pour injecter notre wrapper de traduction.
 *
 * Enregistre via Global.getSector().registerPlugin() dans onGameLoad().
 */
public class FrenchCampaignPlugin extends BaseCampaignPlugin {

    @Override
    public String getId() {
        return "frenchLangPlugin";
    }

    @Override
    public boolean isTransient() {
        return true;
    }

    @Override
    public PluginPick<InteractionDialogPlugin> pickInteractionDialogPlugin(
            SectorEntityToken interactionTarget) {

        // Intercepter les dialogues de flotte
        if (interactionTarget instanceof CampaignFleetAPI) {
            return new PluginPick<InteractionDialogPlugin>(
                new FrenchFleetInteractionDialogPlugin(),
                CampaignPlugin.PickPriority.MOD_GENERAL
            );
        }

        return null; // Laisser le vanilla gerer les autres dialogues
    }
}
