# Publishing Guide

Salvage from various derelicts, planetary ruins, and so on uses a system of "drop groups" to determine what items are generated. The base system is data-driven - that is, the drops are usually configured using entries in csv files - but it's possible to use code to add drops from csv-defined groups to specific entities. It's also possible to generate salvage entirely through code, bypassing drop groups entirely, though this is beyond the scope of this post.

A campaign entity (such as a mining station, a derelict ship, etc) can have two types of drops - "dropValue" and "dropRandom". "dropValue" is used when the goal is to drop roughly a certain amount of credits worth of items. "dropRandom" is used when the goal is to have a chance for some items to drop, but not a guarantee of an approximate value, or in fact anything being dropped at all.

An example of "dropValue" might be "drop 10,000 credits worth of fuel, supplies, metals, and heavy machinery". The actual value will be within 50% of the target amount.

An example of "dropRandom" might be "a 10% chance to drop a ship blueprint with the rare_bp tag".

Drop Groups
A drop group is a set of items from which specific items will be picked. For example, the "basic" drop group might include fuel, supplies, metal, and heavy machinery - so we could then say "drop 10,000 credits worth of items from the 'basic' group". Drop groups can be added to an entity's "dropValue" or "dropRandom" drops.

Drop groups are defined in data/campaign/procgen/drop_groups.csv. This file has the following columns:

commodity
In the simplest case, the id of the commodity being dropped. Can also be a more involved string that includes json and is parsed by the game to figure out exactly what kind of item(s) it refers to. More on this below.

group
The id of the group. All rows with the same id are part of the same group.

freq
The frequency with which this row will be picked from this group, relative to the other rows in this group. For example, if a group has two rows, one with a frequency of 10, and the other with a frequency of 20, it's the same as the items having a frequency of 40 and 80, respectively.

When merging in drop_groups.csv from mods, the game will use both the "commodity" and the "group" columns as the key. Therefore, if a mod needs to remove an item from a group, the way to do that is to add a row identical to the one found in the core drop_groups.csv file, but set its frequency to zero.

The "commodity" column

Commodities
The simplest case is using the id of a commodity from data/campaign/commodities.csv. For example:

food,basic,20

Would add Food to the "basic" group, with a frequency of 20.

nothing
"nothing" (all lowercase) is a reserved keyword. When a row with commodity == nothing is picked, no item will be generated. This should only be used with "dropRandom", since if it was used in a "dropValue" group, a "nothing" result would be ignored and the game would continue to try generating items until the credit value goal was met. For "dropRandom", on the other hand, a "nothing" result would use up a chance to get some kind of drop.

For example:

nothing,extended,100

Would add the chance (with 100 frequency) to get nothing from the "extended" group.

Special items
This column can also be used to specify "special items" (such as blueprints, nanoforges, or modspecs), defined in data/campaign/special_items.csv.

To do this, the value must start with "item_". After that, there are several options. Based on which one is used, each time this row is picked, the game will "resolve" this row into a specific item.

Item id
Something like "item_synchrotron" will just always resolve into the special item with the id "synchrotron".

Tags
We can also omit the id and instead specify that we want an item which has (or does not have) specific tags.

For example:

item_:{tags:[package_bp, !no_drop]}

Means "a special item, with the package_bp tag, and without the no_drop tag". The probability of any specific special item (matching these parameters) being picked is multiplied by the value in its "rarity" column, in special_items.csv. The parameters are separated from the item_ prefix/the optional item id by a colon.

Plugin parameters
Some special items - such as ship blueprints (with the id "ship_bp"), for example - are a base item that can further "resolve" into a range of items depending on the parameters provided. The specifics of the parameters depend on the implementation of the item's plugin, so it's possible for a mod to add an entirely different set of parameters to what will be discussed here.

Plugin parameters are specified after the item id/item_ prefix, and are separated from it by a colon.

For example:
item_ship_bp:{tags:[rare_bp, !no_drop]}

Means "pass in the parameters after the colon to the base 'ship_bp' item and have it interpret them and resolve to a specific item".

It's very important to note that in this case - when an item id is specified after "item_" - the parameters are passed in to the item's plugin. In the previous case, where there is no item id (i.e. "item_:{tags:[package_bp, !no_drop]}"), the parameters are parsed by the core drop algorithm to produce a specific item.

It's also possible to combine the two approaches - i.e. have the core drop algorithm pick a specific item matching the provided tags, and *then* pass in parameters to its plugin to have it resolve into a specific item. This is only necessary if the item is a "base" item and needs to be resolved into something specific. So, for example, a Synchrotron doesn't need any extra parameters, while a "Base Ship Blueprint" item does, so it can become an "Onslaught Ship Blueprint" instead.

To do this, put the plugin parameters into a json object with the key "p", alongside the tags. For example:

item_:{tags:[single_bp], p:{tags:[rare_bp]}}

The above will first pick a special item with a  "single_bp" tag - which will be a  ship, weapon, or fighter blueprint - and then pass in the bolded parameters to resolve the pick to a specific item. This is only possible because all three plugins for items having the "single_bp" tag - ShipBlueprintItemPlugin, WeaponBlueprintItemPlugin, and FighterBlueprintItemPlugin - expect their parameters in the same format, and can interpret them in the same way. In this case, we'll end up with a ship, weapon, or fighter blueprint, where the actual item - the ship, the weapon, or the fighter - has a "rare_bp" tag.

If, for example, a mod added another special item with the "single_bp" tag, and it did not handle parameters in this format, that could cause problems. For example, that item's plugin might just crash trying to parse unexpected parameters.

Ship weapons
Ship weapons can also be specified. While they are not "special items", they are handled in a similar way. Instead of an "item_" prefix, they use a "wpn_" prefix.

Weapon id
As with special items, you can specify the weapon id directly. For example "wpn_vulcan" will always resolve into the Vulcan Cannon

Tags and other parameters

You can specify weapon size, weapon type, and tags.

wpn_:{weaponSize:SMALL, weaponType:BALLISTIC, tags:[rare_bp]}

The above will resolve into a small ballistic weapon with the "rare_bp" tag. If there is no matching weapon, then this row will resolve into "nothing" instead.

Adding drop groups to entities using the entity spreadsheet
For drop groups to be used, they need to be added to an entity's dropValue or dropRandom drop group sets.

For standard salvage entities - the ones defined in data/campaign/procgen/salvage_entity_gen_data.csv - this can be done using the "drop_value" and "drop_random" columns in that spreadsheet.

drop_value
For drop_value, it's a comma-separated list of &lt;group id&gt;:&lt;credit value&gt;. For example:

basic:5000,
machinery:4000

Means 5000 (+-50%) credits worth from the "basic" group, and 4000 (+-50%) from the "machinery" group. 

For special items only, at least one item will be added even if its value exceeds the specified drop value.

drop_random
For drop_random, the syntax is slightly more involved, though it's still a comma separated list.

Example 1:

ai_cores3:5

Means "5 chances to drop something from the 'ai_cores3' group.


Example 2:

extended:5x3000,

Means "5 chances to drop something from the 'extended' group, and each time the choice is made, drop 3000 (+-50%) credits worth of that item".

If the value is specified, and a single item exceeds the value, then the item may turn into "nothing" with a probability based on the ratio of the item's value and the drop value. For example, if there's a 10,000 credit item in the the "extended" group, and the target drop value was 3000, there would be a 30% chance to drop the item and a 70% chance to drop nothing instead.

Adding drop groups using code


Code: javaSectorEntityToken entity = ...;

/* Adding to dropRandom: a custom drop group (not defined in the csv) */
DropData d = new DropData();
d.chances = 5;
d.addCustom("item_:{tags:[single_bp], p:{tags:[rare_bp]}}", 1f);
d.addCustom("item_industry_bp:planetaryshield", 1f);
entity.addDropRandom(d);

/* Adding 1000 chances at "ai_cores3" to dropRandom */
d = new DropData();
d.chances = 1000;
d.group = "ai_cores3";
entity.addDropRandom(d);

/* A custom group with a 50% chance to drop a Synchrotron */
d = new DropData();
d.chances = 100;
d.addCustom("item_synchrotron", 1f);
d.addNothing(1f);
entity.addDropRandom(d);

/* 5000 to 15000 worth of food and organics */
/* A 2-1 ratio of units of food to units of organics */
d = new DropData();
d.value = 10000;
d.addCommodity(Commodities.FOOD, 10f);
d.addCommodity(Commodities.ORGANICS, 5f);
entity.addDropValue(d);


Feedback/questions welcome!

Thanks for posting this! It's very welcome information on something that I personally didn't understand very well, if at all. I've gone ahead and transcribed this post to the wiki.

Nice! Glad this is helpful.

Very useful!  This is something I've wondered about for quite some time now, but hadn't gotten around to asking about

Pending additions in next release:

freq for "nothing" can be specified as a percentage and will remain stable if items are added/remove to/from the group
dropRandom: can specify e.g. &lt;group&gt;:1-4x1000 to roll 1 to 4 times in a group (the x1000 is optional)

Quotefreq
The frequency with which this row will be picked from this group, relative to the other rows in this group. For example, if a group has two rows, one with a frequency of 10, and the other with a frequency of 20, it's the same as the items having a frequency of 40 and 80, respectively.

When merging in drop_groups.csv from mods, the game will use both the "commodity" and the "group" columns as the key. Therefore, if a mod needs to remove an item from a group, the way to do that is to add a row identical to the one found in the core drop_groups.csv file, but set its frequency to zero.

Can I use decimals in this frequency? I'm having a hard time replicating the frequency when I put in decimals like 0.1

I believe so.