package data.scripts;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.Global;
import org.apache.log4j.Logger;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Map;

/**
 * Plugin principal du mod de traduction FR.
 *
 * Patche les strings hardcodes du moteur au demarrage
 * via reflection sur les champs statiques accessibles.
 *
 * Pour les strings dans le code des methodes (addOption, addTitle),
 * un CampaignPlugin separe intercepte les dialogues.
 */
public class FrenchLangModPlugin extends BaseModPlugin {

    private static final Logger log = Global.getLogger(FrenchLangModPlugin.class);

    /** Mapping des tags Intel hardcodes */
    private static final Map<String, String> TAG_TRANSLATIONS = new HashMap<String, String>();
    static {
        TAG_TRANSLATIONS.put("Fleet departures", "Departs de flottes");
        TAG_TRANSLATIONS.put("Hostilities", "Hostilites");
    }

    @Override
    public void onApplicationLoad() throws Exception {
        log.info("=== French Language Pack ===");
        log.info("Patching hardcoded strings...");

        int patched = 0;

        // Patch Tags.INTEL_FLEET_DEPARTURES et Tags.INTEL_HOSTILITIES
        // Ce sont des static final String — modifiables par reflection
        patched += patchStaticField(
            "com.fs.starfarer.api.impl.campaign.ids.Tags",
            "INTEL_FLEET_DEPARTURES",
            "Departs de flottes"
        );
        patched += patchStaticField(
            "com.fs.starfarer.api.impl.campaign.ids.Tags",
            "INTEL_HOSTILITIES",
            "Hostilites"
        );

        log.info("Patched " + patched + " static fields");
        log.info("=== French Language Pack loaded ===");
    }

    @Override
    public void onGameLoad(boolean newGame) {
        // Enregistrer le plugin campagne qui traduit les dialogues
        Global.getSector().registerPlugin(new FrenchCampaignPlugin());
        log.info("FrenchCampaignPlugin registered");
    }

    /**
     * Modifie un champ static final String par reflection.
     * Retourne 1 si reussi, 0 sinon.
     */
    private int patchStaticField(String className, String fieldName, String newValue) {
        try {
            Class<?> clazz = Class.forName(className);
            Field field = clazz.getDeclaredField(fieldName);
            field.setAccessible(true);

            // Retirer le modifier "final" pour permettre l'ecriture
            Field modifiersField = Field.class.getDeclaredField("modifiers");
            modifiersField.setAccessible(true);
            modifiersField.setInt(field, field.getModifiers() & ~java.lang.reflect.Modifier.FINAL);

            String oldValue = (String) field.get(null);
            field.set(null, newValue);
            log.info("  " + className + "." + fieldName + ": \"" + oldValue + "\" -> \"" + newValue + "\"");
            return 1;
        } catch (Exception e) {
            log.error("Failed to patch " + className + "." + fieldName + ": " + e.getMessage());
            return 0;
        }
    }
}
