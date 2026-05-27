package data.scripts;

import com.fs.starfarer.api.BaseModPlugin;
import com.fs.starfarer.api.Global;
import com.fs.starfarer.api.ModSpecAPI;
import com.fs.starfarer.api.campaign.PlanetSpecAPI;
import com.fs.starfarer.api.campaign.SpecialItemSpecAPI;
import com.fs.starfarer.api.campaign.econ.CommoditySpecAPI;
import com.fs.starfarer.api.campaign.econ.SubmarketSpecAPI;
import com.fs.starfarer.api.characters.MarketConditionSpecAPI;
import com.fs.starfarer.api.characters.SkillSpecAPI;
import com.fs.starfarer.api.combat.ShipHullSpecAPI;
import com.fs.starfarer.api.combat.ShipSystemSpecAPI;
import com.fs.starfarer.api.loading.AbilitySpecAPI;
import com.fs.starfarer.api.loading.Description;
import com.fs.starfarer.api.loading.HullModSpecAPI;
import com.fs.starfarer.api.loading.IndustrySpecAPI;
import com.fs.starfarer.api.loading.WeaponSpecAPI;
import org.apache.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;

import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * Plugin principal du mod de traduction FR — v2.0.10.
 *
 * Approche : traduction runtime (pas de replace sur les CSVs specs).
 * Les 5 fichiers specs (ship_data, weapon_data, hull_mods, ship_systems,
 * special_items) sont gardés dans notre mod comme dictionnaires FR et
 * appliqués via l'API publique dans onApplicationLoad().
 *
 * Avantage : les mods de contenu peuvent ajouter leurs entrées sans conflit.
 * Seuls les IDs vanilla présents dans notre dictionnaire sont patchés.
 */
public class FrenchLangModPlugin extends BaseModPlugin {

    private static final Logger log = Global.getLogger(FrenchLangModPlugin.class);
    private static final String PLUGIN_CLASS = "data.scripts.FrenchLangModPlugin";

    @Override
    public void onApplicationLoad() throws Exception {
        log.info("=== French Language Pack v2.0.10 ===");
        log.info("Mode : runtime translation (no replace)");

        String modId = findOurModId();
        if (modId == null) {
            log.error("[FR] Could not find own mod ID — runtime translation skipped");
            return;
        }
        log.info("[FR] Mod ID : " + modId);

        patchShipData(modId);
        patchWeaponData(modId);
        patchHullMods(modId);
        patchShipSystems(modId);
        patchSpecialItems(modId);
        patchMarketConditions(modId);
        patchCommodities(modId);
        patchIndustries(modId);
        patchSkills(modId);
        patchDescriptions(modId);
        patchAbilities(modId);
        patchSubmarkets(modId);
        patchAptitudes(modId);
        patchPlanetSpecs(modId);

        log.info("=== French Language Pack loaded ===");
    }

    @Override
    public void onGameLoad(boolean newGame) {
        Global.getSector().registerPlugin(new FrenchCampaignPlugin());
        log.info("FrenchCampaignPlugin registered");
        Global.getSector().addTransientScript(new FrenchPromptTranslator());
        log.info("FrenchPromptTranslator registered");
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Utility
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Trouve l'ID de notre mod en cherchant le mod dont le plugin class correspond.
     * Fonctionne pour le dev (starsector_lang_pack_fr_dev) et le public
     * (starsector_lang_pack_fr) sans hardcoding.
     */
    private String findOurModId() {
        List<ModSpecAPI> mods = Global.getSettings().getModManager().getEnabledModsCopy();
        for (ModSpecAPI mod : mods) {
            if (PLUGIN_CLASS.equals(mod.getModPluginClassName())) {
                return mod.getId();
            }
        }
        return null;
    }

    /**
     * Charge un CSV depuis notre dossier mod et retourne un dictionnaire
     * indexé par idColumn. Lignes vides et commentaires (# en tête) ignorés.
     */
    private Map<String, JSONObject> loadTranslationMap(String csvPath, String modId, String idColumn) {
        Map<String, JSONObject> dict = new HashMap<String, JSONObject>();
        try {
            JSONArray rows = Global.getSettings().loadCSV(csvPath, modId);
            for (int i = 0; i < rows.length(); i++) {
                JSONObject row = rows.getJSONObject(i);
                String id = row.optString(idColumn, "").trim();
                if (id.isEmpty() || id.startsWith("#")) continue;
                dict.put(id, row);
            }
        } catch (Exception e) {
            log.warn("[FR] Could not load " + csvPath + " : " + e.getMessage());
        }
        return dict;
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Patch methods
    // ─────────────────────────────────────────────────────────────────────────

    private void patchShipData(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/hulls/ship_data.csv", modId, "id");
        log.info("[FR] ship_data dict size : " + dict.size());
        int patched = 0;
        for (ShipHullSpecAPI spec : Global.getSettings().getAllShipHullSpecs()) {
            JSONObject row = dict.get(spec.getHullId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            String designation = row.optString("designation", "").trim();
            if (!name.isEmpty()) spec.setHullName(name);
            if (!designation.isEmpty()) spec.setDesignation(designation);
            patched++;
        }
        log.info("[FR] ship_data patched : " + patched);
    }

    private void patchWeaponData(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/weapons/weapon_data.csv", modId, "id");
        log.info("[FR] weapon_data dict size : " + dict.size());
        int patched = 0;
        for (WeaponSpecAPI spec : Global.getSettings().getAllWeaponSpecs()) {
            JSONObject row = dict.get(spec.getWeaponId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            if (!name.isEmpty()) spec.setWeaponName(name);
            setIfPresent(row, "primaryRoleStr",   v -> spec.setPrimaryRoleStr(v));
            setIfPresent(row, "speedStr",          v -> spec.setSpeedStr(v));
            setIfPresent(row, "trackingStr",       v -> spec.setTrackingStr(v));
            setIfPresent(row, "turnRateStr",       v -> spec.setTurnRateStr(v));
            setIfPresent(row, "accuracyStr",       v -> spec.setAccuracyStr(v));
            setIfPresent(row, "customPrimary",     v -> spec.setCustomPrimary(v));
            setIfPresent(row, "customPrimaryHL",   v -> spec.setCustomPrimaryHL(v));
            setIfPresent(row, "customAncillary",   v -> spec.setCustomAncillary(v));
            setIfPresent(row, "customAncillaryHL", v -> spec.setCustomAncillaryHL(v));
            patched++;
        }
        log.info("[FR] weapon_data patched : " + patched);
    }

    private void patchHullMods(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/hullmods/hull_mods.csv", modId, "id");
        log.info("[FR] hull_mods dict size : " + dict.size());
        int patched = 0;
        for (HullModSpecAPI spec : Global.getSettings().getAllHullModSpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name     = row.optString("name",    "").trim();
            String desc     = row.optString("desc",    "").trim();
            String sModDesc = row.optString("sModDesc", "").trim();
            if (!name.isEmpty())     spec.setDisplayName(name);
            if (!desc.isEmpty())     spec.setDescriptionFormat(desc);
            if (!sModDesc.isEmpty()) spec.setSModEffectFormat(sModDesc);
            patched++;
        }
        log.info("[FR] hull_mods patched : " + patched);
    }

    private void patchShipSystems(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/shipsystems/ship_systems.csv", modId, "id");
        log.info("[FR] ship_systems dict size : " + dict.size());
        int patched = 0;
        for (ShipSystemSpecAPI spec : Global.getSettings().getAllShipSystemSpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            patched++;
        }
        log.info("[FR] ship_systems patched : " + patched);
    }

    private void patchSpecialItems(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/special_items.csv", modId, "id");
        log.info("[FR] special_items dict size : " + dict.size());
        int patched = 0;
        for (SpecialItemSpecAPI spec : Global.getSettings().getAllSpecialItemSpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            String desc = row.optString("desc", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            if (!desc.isEmpty()) spec.setDesc(desc);
            patched++;
        }
        log.info("[FR] special_items patched : " + patched);
    }

    private void patchMarketConditions(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/market_conditions.csv", modId, "id");
        log.info("[FR] market_conditions dict size : " + dict.size());
        int patched = 0;
        for (MarketConditionSpecAPI spec : Global.getSettings().getAllMarketConditionSpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            String desc = row.optString("desc", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            if (!desc.isEmpty()) spec.setDesc(desc);
            patched++;
        }
        log.info("[FR] market_conditions patched : " + patched);
    }

    private void patchCommodities(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/commodities.csv", modId, "id");
        log.info("[FR] commodities dict size : " + dict.size());
        int patched = 0;
        for (CommoditySpecAPI spec : Global.getSettings().getAllCommoditySpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            patched++;
        }
        log.info("[FR] commodities patched : " + patched);
    }

    private void patchIndustries(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/industries.csv", modId, "id");
        log.info("[FR] industries dict size : " + dict.size());
        int patched = 0;
        for (IndustrySpecAPI spec : Global.getSettings().getAllIndustrySpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String name = row.optString("name", "").trim();
            String desc = row.optString("desc", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            if (!desc.isEmpty()) spec.setDesc(desc);
            patched++;
        }
        log.info("[FR] industries patched : " + patched);
    }

    private void patchSkills(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/characters/skills/skill_data.csv", modId, "id");
        log.info("[FR] skill_data dict size : " + dict.size());
        int patched = 0;
        for (String id : Global.getSettings().getSkillIds()) {
            JSONObject row = dict.get(id);
            if (row == null) continue;
            SkillSpecAPI spec = Global.getSettings().getSkillSpec(id);
            if (spec == null) continue;
            String name = row.optString("name", "").trim();
            String desc = row.optString("description", "").trim();
            if (!name.isEmpty()) spec.setName(name);
            if (!desc.isEmpty()) spec.setDescription(desc);
            patched++;
        }
        log.info("[FR] skill_data patched : " + patched);
    }

    private void patchDescriptions(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/strings/descriptions.csv", modId, "id");
        log.info("[FR] descriptions dict size : " + dict.size());
        int patched = 0;
        for (Map.Entry<String, JSONObject> entry : dict.entrySet()) {
            String id = entry.getKey();
            JSONObject row = entry.getValue();
            String typeStr = row.optString("type", "").trim().toUpperCase();
            if (typeStr.isEmpty()) continue;
            Description.Type type;
            try {
                type = Description.Type.valueOf(typeStr);
            } catch (IllegalArgumentException e) {
                log.warn("[FR] Unknown description type '" + typeStr + "' for id '" + id + "'");
                continue;
            }
            Description desc = Global.getSettings().getDescription(id, type);
            if (desc == null) continue;
            setIfPresent(row, "text1", v -> desc.setText1(v));
            setIfPresent(row, "text2", v -> desc.setText2(v));
            setIfPresent(row, "text3", v -> desc.setText3(v));
            setIfPresent(row, "text4", v -> desc.setText4(v));
            setIfPresent(row, "text5", v -> desc.setText5(v));
            patched++;
        }
        log.info("[FR] descriptions patched : " + patched);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Reflection patches (specs without public setters)
    // ─────────────────────────────────────────────────────────────────────────

    private void patchAbilities(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/abilities.csv", modId, "id");
        log.info("[FR] abilities dict size : " + dict.size());
        // Load vanilla English values for desc (no public getDesc() in AbilitySpecAPI)
        Map<String, JSONObject> enDict = loadVanillaCSV("data/campaign/abilities.csv", "id");
        int patched = 0;
        for (Map.Entry<String, JSONObject> entry : dict.entrySet()) {
            String id = entry.getKey();
            JSONObject row = entry.getValue();
            AbilitySpecAPI spec = Global.getSettings().getAbilitySpec(id);
            if (spec == null) continue;
            String frName = row.optString("name", "").trim();
            String frDesc = row.optString("desc", "").trim();
            if (!frName.isEmpty()) {
                setFieldByValue(spec, spec.getName(), frName, "abilityName:" + id);
            }
            if (!frDesc.isEmpty() && enDict.containsKey(id)) {
                String enDesc = enDict.get(id).optString("desc", "").trim();
                if (!enDesc.isEmpty()) {
                    setFieldByValue(spec, enDesc, frDesc, "abilityDesc:" + id);
                }
            }
            patched++;
        }
        log.info("[FR] abilities patched : " + patched);
    }

    private void patchSubmarkets(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap("data/campaign/submarkets.csv", modId, "id");
        log.info("[FR] submarkets dict size : " + dict.size());
        int patched = 0;
        for (SubmarketSpecAPI spec : Global.getSettings().getAllSubmarketSpecs()) {
            JSONObject row = dict.get(spec.getId());
            if (row == null) continue;
            String frName = row.optString("name", "").trim();
            String frDesc = row.optString("desc", "").trim();
            if (!frName.isEmpty()) {
                setFieldByValue(spec, spec.getName(), frName, "submarketName:" + spec.getId());
            }
            if (!frDesc.isEmpty()) {
                setFieldByValue(spec, spec.getDesc(), frDesc, "submarketDesc:" + spec.getId());
            }
            patched++;
        }
        log.info("[FR] submarkets patched : " + patched);
    }

    private void patchAptitudes(String modId) {
        Map<String, JSONObject> dict = loadTranslationMap(
                "data/characters/skills/aptitude_data.csv", modId, "id");
        log.info("[FR] aptitude_data dict size : " + dict.size());
        // Load vanilla English aptitude descriptions (no public getter on SkillSpecAPI)
        Map<String, JSONObject> enDict = loadVanillaCSV("data/characters/skills/aptitude_data.csv", "id");
        Set<String> patchedNames = new HashSet<String>();
        Set<String> patchedDescs = new HashSet<String>();
        int skillsScanned = 0;
        for (String skillId : Global.getSettings().getSkillIds()) {
            SkillSpecAPI skill = Global.getSettings().getSkillSpec(skillId);
            if (skill == null) continue;
            skillsScanned++;
            String aptId = skill.getGoverningAptitudeId();
            JSONObject row = dict.get(aptId);
            if (row == null) continue;
            // Patch aptitude name (readable via interface)
            String enName = skill.getGoverningAptitudeName();
            String frName = row.optString("name", "").trim();
            if (!frName.isEmpty() && enName != null && !patchedNames.contains(aptId)) {
                if (setFieldByValue(skill, enName, frName, "aptitudeName:" + aptId)) {
                    patchedNames.add(aptId);
                }
            }
            // Patch aptitude description (not in SkillSpecAPI interface — use vanilla lookup)
            if (!patchedDescs.contains(aptId) && enDict.containsKey(aptId)) {
                String enDesc = enDict.get(aptId).optString("description", "").trim();
                String frDesc = row.optString("description", "").trim();
                if (!enDesc.isEmpty() && !frDesc.isEmpty()) {
                    if (setFieldByValue(skill, enDesc, frDesc, "aptitudeDesc:" + aptId)) {
                        patchedDescs.add(aptId);
                    }
                }
            }
        }
        log.info("[FR] aptitudes scanned " + skillsScanned + " skills, patched names: "
                + patchedNames.size() + " aptitudes, descs: " + patchedDescs.size());
    }

    private void patchPlanetSpecs(String modId) {
        log.info("[FR] patchPlanetSpecs start");
        JSONObject planetsJson;
        try {
            planetsJson = Global.getSettings().loadJSON("data/config/planets.json", modId);
        } catch (Exception e) {
            log.warn("[FR] Could not load planets.json : " + e.getMessage());
            return;
        }
        int patched = 0;
        for (PlanetSpecAPI spec : Global.getSettings().getAllPlanetSpecs()) {
            String type = spec.getPlanetType();
            if (type == null || !planetsJson.has(type)) continue;
            try {
                JSONObject entry = planetsJson.getJSONObject(type);
                String frName = entry.optString("name", "").trim();
                if (!frName.isEmpty()) {
                    setFieldByValue(spec, spec.getName(), frName, "planetName:" + type);
                    patched++;
                }
            } catch (Exception e) {
                log.warn("[FR] patchPlanetSpecs error on " + type + ": " + e.getMessage());
            }
        }
        log.info("[FR] planetSpecs patched : " + patched);
    }

    // ─────────────────────────────────────────────────────────────────────────
    // Helper
    // ─────────────────────────────────────────────────────────────────────────

    /**
     * Loads a CSV from the vanilla game path (no modId) and returns it indexed by idColumn.
     * Used to obtain English values for specs that have no public getDesc() accessor.
     */
    private Map<String, JSONObject> loadVanillaCSV(String csvPath, String idColumn) {
        Map<String, JSONObject> dict = new HashMap<String, JSONObject>();
        try {
            JSONArray rows = Global.getSettings().loadCSV(csvPath);
            for (int i = 0; i < rows.length(); i++) {
                JSONObject row = rows.getJSONObject(i);
                String id = row.optString(idColumn, "").trim();
                if (id.isEmpty() || id.startsWith("#")) continue;
                dict.put(id, row);
            }
        } catch (Exception e) {
            log.warn("[FR] Could not load vanilla " + csvPath + " : " + e.getMessage());
        }
        return dict;
    }

    /**
     * Finds the first String field (scanning the object's class hierarchy) whose current
     * value equals {@code currentValue} and sets it to {@code newValue}.
     *
     * <p>Uses Java reflection to bypass the absence of public setters in obfuscated specs.
     * The field is located by value (not by name) so it remains functional across Starsector
     * minor patches, as long as the field content is distinct enough.
     *
     * @return true if the field was found and updated, false otherwise.
     */
    private boolean setFieldByValue(Object obj, String currentValue, String newValue, String hint) {
        if (currentValue == null || currentValue.isEmpty()) return false;
        if (newValue == null || newValue.isEmpty()) return false;
        if (currentValue.equals(newValue)) return true; // already correct, nothing to do
        Class<?> cls = obj.getClass();
        while (cls != null && cls != Object.class) {
            for (Field f : cls.getDeclaredFields()) {
                if (f.getType() != String.class) continue;
                try {
                    f.setAccessible(true);
                    Object val = f.get(obj);
                    if (currentValue.equals(val)) {
                        f.set(obj, newValue);
                        log.debug("[FR] Patched field '" + f.getName()
                                + "' on " + cls.getSimpleName() + " [" + hint + "]");
                        return true;
                    }
                } catch (Exception ignored) {
                    // setAccessible may fail for some fields; skip silently
                }
            }
            cls = cls.getSuperclass();
        }
        log.warn("[FR] Field not found [" + hint + "] (searching: '"
                + currentValue.replace("\n", "\\n") + "')");
        return false;
    }

    @FunctionalInterface
    private interface StringSetter {
        void set(String value);
    }

    private void setIfPresent(JSONObject row, String key, StringSetter setter) {
        String v = row.optString(key, "").trim();
        if (!v.isEmpty()) setter.set(v);
    }
}
