#!/usr/bin/env python3
"""Generate concept images for Hey Plushed brand concepts"""

import urllib.request
import json
import base64
import os
import ssl
import time

API_KEY = "AIzaSyC9ljCLw5bluNRZK5Jla0ZZmXjc9xFz0t0"
MODEL = "gemini-2.5-flash-image"
OUTPUT_DIR = "/Users/rahul/Downloads/hey-plushed-lite/concepts"

os.makedirs(OUTPUT_DIR, exist_ok=True)

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

STYLE = "Dark moody product photography style, black background, dramatic pink/magenta lighting, luxury brand aesthetic, minimal composition. "

CONCEPTS = [
    ("01-after-dark", STYLE + "A collection of 5 abstract plush toys shaped like suggestive emoji — eggplant, peach, banana, cherry, taco — arranged artfully on black velvet. They look kawaii and innocent but the shapes are unmistakable. Soft pastel colors with pink backlighting. Premium collectible toy brand photography."),
    ("02-walk-of-shame", STYLE + "A cute round plush toy with messy yarn hair, a tiny lipstick smudge on its cheek, one shoe missing, holding a tiny coffee cup accessory. Disheveled but adorable. Morning-after vibes. Kawaii style plush on a nightstand."),
    ("03-couples-magnetic", STYLE + "Two small kawaii plush toys snapping together with magnetic connection — one pink, one blue — their little arms reaching toward each other. Heart shapes where they connect. Romantic but playful. Gift box visible."),
    ("04-hotel-collab", STYLE + "A luxury hotel pillow with crisp white sheets, and a small pink plush toy sitting on the pillow like a chocolate mint. A tiny QR code tag visible on the plush. Boutique hotel aesthetic, warm ambient lighting."),
    ("05-confessional", STYLE + "A wall covered in hundreds of small handwritten cards/notes, backlit with pink neon glow. A single plush toy sitting on a shelf in front of the wall. Anonymous secrets art installation vibe. Dark, moody, intimate."),
    ("06-naughty-nice-flip", STYLE + "A reversible plush toy shown in two states side by side — left side is the 'nice' version (big innocent eyes, smile, halo) and right side is flipped inside-out showing the 'naughty' version (wink, tongue out, tiny devil horns). Same plush, two personalities."),
    ("07-plushed-parlour", STYLE + "A stylish cocktail bar interior with pink neon signage reading 'Plushed'. Behind the bar, shelves display plush toys instead of bottles. Cocktails on the bar have tiny plush toy garnishes. Moody nightlife aesthetic with pink lighting."),
    ("08-monthly-mischief", STYLE + "A premium subscription box being unboxed — matte black box with hot pink tissue paper, a mystery plush toy peeking out, a cocktail recipe card, and a zodiac themed card. Monthly subscription unboxing flat lay."),
    ("09-trophy-shelf", STYLE + "A sleek clear acrylic display shelf with LED backlighting in pink, holding 8-10 different kawaii plush toys arranged like trophies. Bar cart style staging with a cocktail glass nearby. Interior design meets collectibles."),
    ("10-ai-generator", STYLE + "A phone screen showing an AI interface where someone has typed 'make me a gothic plushie that likes coffee' and the screen shows a generated cute gothic plush toy design. The real manufactured version sits next to the phone. Digital to physical concept."),
    ("11-plushed-sloshed", STYLE + "Flat lay photography of a plush toy next to a cocktail recipe card, a small bottle of spirits, and a cocktail glass with a yellow drink. The recipe card has cute illustrated instructions. Branded cocktail pairing concept."),
    ("12-breakup-box", STYLE + "A care package being opened — contains a comfort plush toy, mini wine bottle, chocolate bar, and a card reading 'they didn't deserve you'. Anti-Valentine's gift box. Matte black packaging with hot pink ribbon."),
    ("13-secret-pocket", STYLE + "Close-up of a plush toy with a small hidden zipper being opened, revealing a tiny pocket inside big enough for a ring or note. Product feature detail shot. The zipper pull is heart-shaped."),
    ("14-plushed-radio", STYLE + "A Spotify-style album cover design for 'Plushed Radio' — lo-fi aesthetic with a plush toy wearing tiny headphones, sitting on a windowsill at night with city lights in the background. Warm, cozy, purple-pink tones."),
    ("15-vault-drop", STYLE + "A numbered limited edition plush toy (showing '247/500' on its tag) inside a premium collector's case with a certificate of authenticity. Velvet lined box. Supreme/streetwear drop aesthetic but for plush toys."),
    ("16-zodiac", STYLE + "A circle arrangement of 12 small plush toys, each representing a zodiac sign — the Scorpio one has tiny intense eyes, the Gemini is literally two-headed, the Leo has a tiny mane. Celestial star map background."),
    ("17-pillow-talk", STYLE + "Podcast studio setup with two microphones, but instead of people, two plush toys are 'hosting' — one leaning into the mic, the other laughing. 'Pillow Talk' text overlay. Professional but absurd."),
    ("18-scent-infused", STYLE + "A plush toy next to lavender sprigs, vanilla beans, and eucalyptus leaves — suggesting the scent-infused concept. Apothecary/wellness aesthetic mixed with kawaii. A small spray bottle labeled 'Refill' nearby."),
    ("19-tattoo-collab", STYLE + "A plush toy with intricate tattoo-style patterns on its fabric — traditional tattoo art (roses, daggers, hearts) rendered in cute plush form. Next to it, a temporary tattoo sheet with matching designs."),
    ("20-office-plushie", STYLE + "A desk setup with a small plush toy sitting next to a laptop, wearing tiny glasses. The plush has embroidered text on its belly reading 'per my last email'. Corporate stress ball replacement. Clean desk aesthetic."),
    ("21-nft-physical", STYLE + "Split image concept — left side shows a glowing digital plush toy on a phone screen (NFT/digital collectible), right side shows the real physical plush toy. Digital to physical bridge. Holographic/cyber aesthetic."),
    ("22-hot-takes", STYLE + "Close-up of a plush toy belly with embroidered text reading 'pineapple belongs on pizza'. Other plushies in background with different hot takes visible. Conversation starter collection."),
    ("23-advent-calendar", STYLE + "A premium advent calendar box with 24 small doors, some open revealing tiny mini plush toys inside. Matte black exterior with gold and pink numbering. Luxury Christmas aesthetic but playful."),
    ("24-vending-machine", STYLE + "A hot pink custom vending machine in a dark bar/club setting, filled with different plush toys behind the glass. Neon glow, nightlife setting. Someone's hand reaching for the dispensed plush at the bottom."),
    ("25-animated-series", STYLE + "Character lineup poster showing 6 plush toy characters with distinct personalities — one hungover with coffee, one overdressed for brunch, one doom-scrolling a tiny phone, one doing yoga. Animated series character sheet style."),
]

def generate(name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "temperature": 1.0}
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=120)
        result = json.loads(resp.read().decode("utf-8"))
        for c in result.get("candidates", []):
            for part in c.get("content", {}).get("parts", []):
                if "inlineData" in part:
                    img = base64.b64decode(part["inlineData"]["data"])
                    ext = "png" if "png" in part["inlineData"]["mimeType"] else "jpg"
                    path = os.path.join(OUTPUT_DIR, f"{name}.{ext}")
                    with open(path, "wb") as f:
                        f.write(img)
                    print(f"  OK ({len(img)//1024}KB)")
                    return path
        print("  No image")
        return None
    except Exception as e:
        print(f"  ERROR: {e}")
        return None

if __name__ == "__main__":
    print(f"Generating {len(CONCEPTS)} concept images...\n")
    for i, (name, prompt) in enumerate(CONCEPTS):
        print(f"[{i+1}/{len(CONCEPTS)}] {name}...", end="", flush=True)
        generate(name, prompt)
        if i < len(CONCEPTS) - 1:
            time.sleep(12)
    print("\nDone!")
