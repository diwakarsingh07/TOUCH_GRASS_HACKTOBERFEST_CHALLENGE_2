"""
TrailWhisper: Open Naturalist Intelligence & "Touch Grass" Engine
================================================================
Translates acoustic bird identifications into real-world physical observational actions.
Tells the hiker WHERE to look in nature and commands them to put their screen away.
"""

from typing import Dict, Any

FIELD_GUIDE_DATA = {
    "mourning_dove_pigeon": {
        "look_where": "Look low along trail paths, telephone wires, park benches, or ground leaf litter.",
        "visual_clues": "Plump body, soft grayish-brown or iridescent slate plumage, small bobbing head, black wing spots, long pointed tail.",
        "fall_behavior": "Flocking together in autumn fields and ground clearings to gorge on fallen weed seeds, grains, and acorns.",
        "touch_grass_action": "Walk gently. Notice how their wings make a sharp whistling flutter when they launch into flight from the trail."
    },
    "great_horned_owl": {
        "look_where": "Look high up (25–40 feet) near the main trunk of dense pine, spruce, or hemlock trees.",
        "visual_clues": "Large prominent feathered ear-tufts, piercing yellow eyes, mottled gray-brown camouflage against tree bark.",
        "fall_behavior": "Beginning their autumn courtship vocalizations; establishing roosting territories at dusk.",
        "touch_grass_action": "Freeze your footsteps. Do not make sudden movements. Scan the thick silhouette branches against the twilight sky."
    },
    "black_capped_chickadee": {
        "look_where": "Look mid-canopy (10–20 feet up) hopping acrobatically between outer birch and pine twigs.",
        "visual_clues": "Distinctive black cap and bib, stark white cheeks, tiny round body often hanging completely upside-down.",
        "fall_behavior": "Feverishly caching thousands of seeds behind tree bark and in dead leaf clusters for winter survival.",
        "touch_grass_action": "Put your phone in your pocket. Cup your hands behind your ears to pinpoint their fluttering wings above you."
    },
    "red_tailed_hawk": {
        "look_where": "Look at the highest exposed dead snag or utility pole overlooking open meadows and trail clearings.",
        "visual_clues": "Broad rounded wings, pale chest with a speckled belly band, brilliant brick-red tail flashing in the sunlight.",
        "fall_behavior": "Riding autumn thermal air currents while hunting field mice and chipmunks preparing for winter.",
        "touch_grass_action": "Look up at the open sky clearing. Watch for a massive silhouette riding the breeze in wide circular glides."
    },
    "downy_woodpecker": {
        "look_where": "Look 6 to 15 feet up on slender dead branches, hollow limbs, or goldenrod stems.",
        "visual_clues": "Checkered black-and-white wings, bold white back stripe, small chisel bill. Males have a bright red patch on the back of the head.",
        "fall_behavior": "Excavating beetle larvae and fungal galls from autumn-dry deciduous wood.",
        "touch_grass_action": "Follow the mechanical tapping sound with your eyes. Inspect the bark fissures of the nearest oak or maple tree."
    },
    "northern_cardinal": {
        "look_where": "Look in dense tangled understory, briar patches, blackberry brambles, or low dogwood shrubs (3–8 feet off the ground).",
        "visual_clues": "Vivid crimson plumage with a sharp crest and black face mask (males), or warm buff-brown with reddish accents (females).",
        "fall_behavior": "Foraging on fallen autumn seeds, wild dogwood berries, and sumac fruit.",
        "touch_grass_action": "Lower your gaze to the trail brush. Look for an unmistakable burst of brilliant red among the fallen leaves."
    },
    "american_robin": {
        "look_where": "Look down at the moist trail edge, leaf litter, or fruiting mountain ash and cedar trees.",
        "visual_clues": "Warm reddish-orange breast, dark charcoal head and back, yellow bill, alert upright posture on the ground.",
        "fall_behavior": "Switching from worms to autumn wild fruit flocks; gathering in nomadic woodland feeding swarms.",
        "touch_grass_action": "Step quietly. Scan the damp trail shoulder where birds are tossing leaf litter searching for autumn berries."
    },
    "american_crow": {
        "look_where": "Look at the high bare canopy branches or treetops scouting the trail from above.",
        "visual_clues": "Entirely jet-black glossy plumage, heavy stout bill, broad fan-shaped tail in flight.",
        "fall_behavior": "Forming massive communal autumn roosts of hundreds of individuals at dusk.",
        "touch_grass_action": "Look up at the open skyline. Watch for intelligent sentinel scouts alerting the forest of your presence."
    },
    "blue_jay": {
        "look_where": "Look mid-to-high in oak, beech, or acorn trees; flitting actively from branch to branch.",
        "visual_clues": "Vibrant blue crest and back, black necklace collar, bold white wing bars and tail corners.",
        "fall_behavior": "Harvesting and caching acorns in forest moss for winter; imitating raptor screams to clear feeders.",
        "touch_grass_action": "Stop and look 15 feet into the nearest oak. Scan for an electric blue flash among the brown leaves."
    },
    "song_sparrow": {
        "look_where": "Look low in dense marshy shrubs, wild rose tangles, and tall trail grasses (1–5 feet off ground).",
        "visual_clues": "Heavily streaked brown and gray breast with a prominent dark central breast spot, long rounded tail.",
        "fall_behavior": "Foraging on fallen grass seeds and weed grains along trail embankments.",
        "touch_grass_action": "Look down into the tall grasses right by your boots. A tiny sparrow may be foraging under the stalks."
    },
    "woodland_insect": {
        "look_where": "Look closely at sun-warmed tree bark or tall dry prairie grasses.",
        "visual_clues": "Stout green or brown camouflaged bodies resting motionless against warm tree trunks.",
        "fall_behavior": "Final late-season mating chorus before first autumn frost.",
        "touch_grass_action": "Feel the warm sun on your face and listen to the rhythmic pulse of autumn insect life in the canopy."
    },
    "human_speech": {
        "look_where": "Right beside you on the hiking trail!",
        "visual_clues": "Hiker wearing trail runners or backpack, holding a phone or walking with a friend.",
        "fall_behavior": "Chatting about trail landmarks, snacks, or taking phone photos instead of looking up.",
        "touch_grass_action": "Put your phone back in your pocket. Say hello to your trail partner, take a deep breath of pine air, and look up at the trees!"
    },
    "silence_stillness": {
        "look_where": "Everywhere around you across the forest expanse.",
        "visual_clues": "Golden autumn leaves drifting silently to the ground.",
        "fall_behavior": "Forest entering autumn stillness and tranquility.",
        "touch_grass_action": "Cherish this rare silence. Put your phone away, close your eyes, and take three slow, deep breaths."
    },
    "ambient_wind": {
        "look_where": "Look up at the highest treetops swaying against the autumn sky.",
        "visual_clues": "Branches gently bending, showers of red and yellow autumn leaves fluttering down.",
        "fall_behavior": "Autumn cold front winds stripping deciduous leaves to reveal hidden winter nests.",
        "touch_grass_action": "Feel the crisp wind on your cheeks. Pocket your phone and watch the leaves dance in the gusts."
    },
    "rain_stream": {
        "look_where": "Down in the trail ravine, creek bed, or puddles along the path.",
        "visual_clues": "Glistening wet moss, ripples in fresh rainwater pools, clear water coursing over creek stones.",
        "fall_behavior": "Autumn moisture revitalizing woodland mosses, lichens, and fungal mycelium.",
        "touch_grass_action": "Touch the cool wet bark or listen to the stream. Let the screen go black and embrace the wet earth."
    },
    "unknown_nature": {
        "look_where": "Scan 15 to 30 feet into the dense tree canopy in the direction of the sound.",
        "visual_clues": "Watch for sudden flutter of wings or twitch of a branch silhouette.",
        "fall_behavior": "Wild birds feeding actively during daylight hours before winter.",
        "touch_grass_action": "Do not look at your phone to guess. Take 10 quiet steps toward the sound, cup your ears, and look up."
    }
}

class NaturalistEngine:
    @staticmethod
    def get_field_guidance(classification: Dict[str, Any]) -> Dict[str, Any]:
        """Enriches species classification with physical wilderness field actions."""
        species_id = classification.get("id", "unknown_nature")
        guide = FIELD_GUIDE_DATA.get(species_id, FIELD_GUIDE_DATA["unknown_nature"])

        common_name = classification.get("common_name", "Wilderness Sound")
        look_where = classification.get("look_where") or guide["look_where"]
        visual_clues = classification.get("visual_clues") or guide["visual_clues"]
        fall_behavior = classification.get("fall_behavior") or guide["fall_behavior"]
        touch_grass_action = classification.get("touch_grass_action") or guide["touch_grass_action"]

        # Audio guidance script for earbuds
        if species_id == "human_speech" or classification.get("sound_type") == "human":
            voice_script = "Human speech detected on trail. Put down your phone, look up at the canopy, and enjoy nature."
        elif species_id in ["silence_stillness", "ambient_wind", "rain_stream"]:
            voice_script = f"{common_name} detected. Put your phone in your pocket and touch grass."
        elif not classification.get("identified", True):
            voice_script = "Wilderness sound detected. Take 10 steps toward the canopy, cup your ears, and look up."
        else:
            voice_script = (
                f"Identified: {common_name}. "
                f"{look_where} "
                f"{touch_grass_action} "
                f"Screen is going to sleep. Put your phone away and enjoy the trail."
            )

        return {
            "species": common_name,
            "scientific_name": classification.get("scientific_name", ""),
            "confidence": classification.get("confidence_pct", "90%"),
            "vocalization": classification.get("vocalization", ""),
            "engine": classification.get("engine", "🌲 Offline Bioacoustic Spectral Matcher"),
            "look_where": look_where,
            "visual_clues": visual_clues,
            "fall_behavior": fall_behavior,
            "touch_grass_action": touch_grass_action,
            "earbuds_voice_script": voice_script
        }
