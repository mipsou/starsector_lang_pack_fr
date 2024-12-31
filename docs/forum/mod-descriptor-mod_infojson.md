# Mod Descriptor (mod_info.json)

mod_info.json, found in the root directory of a mod, contains metadata describing the mod, as well as some directives for how the contents of the mod should be treated.

The following fields in this file are recognized by the game:
"id":"samples_mymod1",Required.

Unique identifier for this mod. Should be something very unlikely to be used by another mod.

"name":"My Mod Name",Required.

Name of the mod, displayed in the mod selection dialog.

"author":"Alex",Optional.

Mod's author.

"totalConversion":"true",Optional, defaults to "false".

Whether the mod is a total conversion. Setting this flag to true indicates that if the game loads this mod, it should not load any other mods (except for utility mods) at the same time. The game will also skip loading ship variants that refer to hull ids that no longer exist (i.e. if the TC replaces ship_data.csv with a new ship set).

"utility":"true",Optional, defaults to "false".

Whether the mod is a utility. Utility mods can be used alongside total conversions. Note: it's the responsibility of the utility mod's creator to ensure that it's actually able to do so.

"version":"0.3.2.1",Version of this mod; required. Can also be specified as: "version":{"major":3, "minor":2, "patch":1}A major version mismatch between the mod and another mod that depends on that version of it means the mod that depends on it can not be enabled. A minor/patch mismatch results in a warning.

"dependencies":[
    {"id":"lw_lazylib", "name":"LazyLib", "version":{"major":2, "minor":4e}},
]Which mods this mod requires to run. Version can also be specified as a single string. "patch" and "minor" are optional, both here and in other places a version is specified. A major mismatch with a dependency means this mod can't be enabled. A minor/patch mismatch results in a warning. If the version of the dependency is omitted, any version will do. A missing dependency means this mod can't be enabled.

"requiredMemoryMB":1024,Optional. If this mod substantially increases the memory required by the game, it should be set to some amount; used by the automatic memory allocation function of the launcher. Generally speaking, major faction mods should set it to 50-100mb; the rule of thumb is that if you're not sure, don't set this value. Major content-scale-affecting mods such as Nexerlin should probably set this value based on the top end of the requirements their mod can reach.Deprecated, since the automatic memory allocation function does not work.


"description":"My mod description",Required.

Description of the mod, displayed in the mod selection dialog.

"gameVersion":"0.9.1a-RC8",Required. Can also be specified as: "gameVersion":{"major":9, "minor":1, "patch":8}A major version mismatch between the mod and the running version of the game means that mod can't be enabled. A minor/patch mismatch results in a warning.

"replace":["data/missions/mission_list.csv"],Optional.

Certain files - such as the mission list, weapon/ship data, sounds, etc - are merged as they're loaded. For example, the core game has a set of missions, and two other mods add a few missions each. The game will merge these files together prior to loading the merged files. This allows multiple mods to coexist, but sometimes - especially for total conversions - this is not desirable.

Adding a file to the "replace" list will ensure that the mod's copy of the file will be used as-is, instead of being merged with the core file. In the above example, the mod is saying that the missions specified in its mission_list.csv should be the only ones loaded, instead of being added to the core set of missions.

Graphics, sound, and .java files are automatically replaced and don't need to be specified here.

Mods that aren't total conversions probably shouldn't use this parameter, as they're unlikely to be compatible with other mods as a result.

"jars":["one.jar","jars/two.jar"],Optional.

The specified jar files will be loaded by the game on startup, and will be accessible from scripts, or anywhere where a class is referred to by name. For example, the "statsScript" field of a ship system definition, or an entry in generators.csv can both refer to a class found in one of the jar files.

Note: if a class is found both in a jar file and as a .java file (in the same package), the one from the jar will be used.


Sample mod_info.json
Code{
  "id":"samples_mymod1",
  "name":"My Mod Name",
  "author":"Alex",
  "totalConversion":"false",
  "utility":"false",
  "version":"0.01",
  "description":"My mod description",
  "gameVersion":"0.53.1a",
  "replace":["data/missions/mission_list.csv"],
  "jars":["one.jar","jars/two.jar"],
}

"modPlugin":"data.scripts.MyModPlugin",Optional.

The specified class must implement the com.fs.starfarer.api.ModPlugin interface. A new instance of it will be created and appropriate methods will be called when various lifecycle events occur, such as when the game application has finished loading. See com/fs/starfarer/api/ModPlugin.java in starfarer.api.zip for details.

Updated OP for 0.95a.