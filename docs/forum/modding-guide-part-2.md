# Modding Guide Part 2

A Starsector mod consists of a single folder that contains a directory structure that mimics that of the game. When the game loads the mod, it will pick up files from each mod and will either replace the core game file with the mod's version of it, or merge the two.

Mods can also provide entirely new files (such as graphics for new ships, new sound effects, etc) that the game will load alongside the core assets.

To avoid the risk of the game replacing a core file with one of these due to an unforeseen naming conflict, it's recommended to keep these assets in a folder that's named differently from what the core game uses. For example, ship graphics are usually found under "graphics/ships". A mod might put its ship graphics under "mymod/graphics/ships".

Replace
The following file types are always replaced:

Sound files (e.g, .ogg, .wav)Graphics (.png, .jpg)Scripts (.java)Weapon and projectile specifications (.wpn, .proj)Ship hull and variant specifications (.ship, .variant)Fonts (.fnt)
If multiple mods are enabled and try to replace the same file, the results are undefined (the game may work or crash or anywhere in between), and the mods are considered incompatible. Generally, only total conversions should replace the files specified above.

Merge
Instead of being replaced, some files are merged instead. This is how multiple mods are able to add ships, weapons, missions, etc to the game, without being in conflict. The following file types are merged:

.csv
CSV files (comma-separated-values) are spreadsheets. Incidentally, they can be edited by most spreadsheet software, with the proper settings for reading the file. 

The procedure the game follows when loading a CSV file is as follows:

Load all the rows from the core game version of the fileFor each mod (in unspecified order), read the file row by rowFor each row, check the id column (it's generally clear which column that is for a particular file)
If the id matches an already loaded row, replaced the loaded data with the data from this rowOtherwise, add this row to the loaded rows
If multiple mods attempt to replace the same row from the core game, or just have matching ids for a row in the same file, the mods are incompatible. To avoid these clashes, it's a good idea to have a mod-specific prefix for all new ids.


.json
JSON (JavaScript Object Notation) is a file format used for detailed data specification by most of the game. A lot of these files use different extensions - for example .wpn and .ship - but unless specified here, they replaced rather than merged when loaded.

All .json and .faction files are merged. Other .json files are replaced.

A json file contain a single "json object", which contains key-value pairs. All keys are strings, and values can either be primitives, strings, arrays, or other objects.

When loading a JSON file, the game first loads the core version of the file as the "master version", and then loads versions of the same file from the enabled mods (again, in unspecified order), using them to replace portions of the "master version" and augment it as necessary.

The following rules are followed when loading a mod's version of a core file:

If the key is not present in the master version, add it and everything under itIf the key is present in the master version:If the value is a string or a primitive, replace it with the new valueIf the value is an array and the key does not contain the substring "color", "button", or "music_" in it (not case sensitive), append the values in the array to the master version's arrayIf the value is an array and the key does contain the substring "color", "button", or "music_", replace the array with the new valueIf the value is another object, examine its keys, following the rules aboveIf the file is "data/config/settings.json", there is a set of keys that mods aren't allowed to replace (see file for details).
If multiple mods attempt to replace values for the same keys, the mods are incompatible. However, if multiple mods only add new keys or add new values to an array, they are compatible.

For example, a mod could add a new portrait to the player portrait selection by providing a data/world/factions/player.faction in the mod with the following:
Code: json{
	"portraits":{
		"standard_male":[
			"graphics/portraits/new_portrait.png",
		],
	}
}

Note that that's the entire file. The mod doesn't need to provide the portions of the file that didn't change - indeed, it shouldn't, to minimize the chance of conflict if other mods do need to change them.

Total Conversions
Total conversions often want to replace files that the game would normally merge - for example, to make sure that the only ships and weapons present in the game are just the ones provided by the total conversion. To accomplish this, there is a "replace" field in the mod descriptor (mod_info.json file, an the root of the mod). It is discussed in more detail here.