# Eclipse Guide

Download it here.

Overview

This mod provides a simple example of a custom campaign interaction dialog. The code is written so that it avoids using anything that Janino (the compiler used by Starsector) can't handle. So, the source files can be compiled by the game on startup, but the code isn't as clean as it could be.

Key features:
Does not require external compilation or use jar files, everything compiled with JaninoAdds a custom interaction for asteroids - they can be searched for hidden supply cachesKeeps track of asteroids searched and supplies remaining in any found cache using SectorAPI.getPersistentData()Can be added to an existing savegame, can not be removed from one

Files

mod_info.json
Standard mod descriptor. Points to MyModPlugin.java.

data/scripts/AsteriodInteractionDialogPlugin.java
Contains all the code that drives the asteroid interaction dialog.

data/scripts/MyCampaignPlugin.java
Tells the game to use the AsteriodInteractionDialogPlugin for interactions with asteroids.

data/scripts/MyModPlugin.java
Registers MyCampaignPlugin when a savegame is run with this mod for the first time.

(Unlocking this because it seems to make less sense to lock something that's an example rather than actual documentation.)

Sweet. Will this allow, say, to approach an asteroid or planet but instead of an empty dialog panel we would get some sort of mini text quest within that panel that, upon proper choices in that dialog tree would reward me with loot?

Something like this?:

Some signal comes from that asteroid
&gt;approach asteroid carefully
_ignore the asteroid

Scanning the asteroid reveals something on its surface, no life signs
_scan the asteroid (might trigger a trap)
&gt;send a team of marines to examine (might trigger trap, rewards loot)
_shoot it (safe but no loot)

The marines sucessfully retrieve the artifact, upon close inspection a virus took over your ship and kill the crew by asphixiation!
&gt;attempt to retake the ship! (battle)
_attempt to hack the virus and retake control (might infect the fleet)
_run away and save the fleet (safely leave, the ship becomes a hostile-to-all enemy "fleet")

Yeah, you could do something like that. It'd be a little more involved than the example, but not by all that much.

Quote from: frag971 on September 25, 2013, 11:46:05 AMSweet. Will this allow, say, to approach an asteroid or planet but instead of an empty dialog panel 

Do you mean that you've tried the mod and are getting an empty dialog panel when interacting with an asteroid? What you should be getting is 1 line of text ("Your fleet approaches the asteroid."), an image of some wreckage on the right, and two options - "Send down a survey team" and "Leave".

Quote from: Alex on September 25, 2013, 11:51:17 AMDo you mean that you've tried the mod and are getting an empty dialog panel when interacting with an asteroid? What you should be getting is 1 line of text ("Your fleet approaches the asteroid."), an image of some wreckage on the right, and two options - "Send down a survey team" and "Leave".

Works fine for me.

Thanks Alex! You know we love you (I speak for Psyion aswell).

I've finally gotten around to messing with this, and have written a new Asteroid "mining" system that destroys the Asteroid when you're done.

Anyhow, I took a look at the FleetInteractionDialogPluginImpl, because I'm contemplating doing a custom, Janino-friendly version that changes things, but I'm really confused thus far 

I have figured out the basics:

1.  playerFleet and otherFleet are determined at the start of the script via who's talking to whom.
2.  dialog.startBattle(BattleCreationContext) takes us to a Battle.
3.  After a Battle, I presume that backFromEngagement() is called immediately.  I'm not sure how the cases are working there, though.

Stuff I'm confused about:
1.  I'm not sure how we get to the Loot screen, or how the Loot screen is populated with Stuff.

You'll want to look at FleetEncounterContext.java, as it seems to control the loot-related stuff. See the method scrapDisabledShipsAndGenerateLoot.

The first call in backFromEngagement is FleetEncounterContext.processEngagementResults(), which passes off to the FleetEncounterContext.

Sorry I haven't really played round with it that much.

Exactly as Zaphide says - FleetEncounterContext is what you need to look at. 

Note that changing it is tricky as it will require you to change a lot of other scripts in terms of sources/names.

I for one use the copy of that script placed in a data/scripts folder from where it is accessed by IroncladsFleetInteractionDialogue plugin (which is also a modified version of core script).

I recommend using some specialised editor like Intelij IDEA. Its free and provides a lot of help and support. It also fixes errors and misspells

Mod is slightly out of date;

To fix the incompatability:

Add

Code@Override
    public Map&lt;String, MemoryAPI&gt; getMemoryMap() {
        return null;
    }
to the AsteriodInteractionDialogPlugin Class

Method is not used by the mod, so it is safe to just return null.

Thank you for updating that; I was thinking of putting Asteroid-mining back in as a mini-mod.