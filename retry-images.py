#!/usr/bin/env python3
import urllib.request, json, base64, os, ssl, time

API_KEY = "AIzaSyC9ljCLw5bluNRZK5Jla0ZZmXjc9xFz0t0"
MODEL = "gemini-2.5-flash-image"
OUT = "/Users/rahul/Downloads/hey-plushed-lite/concepts"
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

S = "Dark moody product photography, black background, dramatic pink/magenta lighting, luxury brand aesthetic. "

RETRY = [
    ("05-confessional", S + "A wall covered in hundreds of small handwritten cards and notes, backlit with pink neon glow. A cute round plush toy sitting on a shelf in front. Anonymous secrets art installation. Dark, moody, intimate atmosphere."),
    ("06-naughty-nice-flip", S + "A reversible plush toy shown in two states — left is the nice version with big innocent eyes and halo, right is flipped inside-out showing naughty version with wink and tiny devil horns. Same toy, two sides."),
    ("10-ai-generator", S + "A smartphone screen showing an AI chat interface generating a custom plush toy design. Next to the phone sits the real manufactured plush matching the screen design. Digital meets physical concept."),
    ("15-vault-drop", S + "A numbered limited edition plush toy showing 247 of 500 on its tag, inside a premium velvet-lined collector case with certificate. Streetwear drop aesthetic but for plush toys."),
    ("20-office-plushie", S + "A small plush toy sitting on a clean desk next to a laptop, wearing tiny glasses. Embroidered text on belly reads 'per my last email'. Corporate desk toy. Minimal office aesthetic."),
    ("22-hot-takes", S + "Close-up of cute plush toy belly with embroidered text reading 'pineapple belongs on pizza'. Other plushies in soft focus background with different hot takes. Conversation starter collection."),
    ("23-advent-calendar", S + "A premium advent calendar with 24 small doors, some open revealing tiny mini plush toys. Matte black box with gold and pink numbering. Luxury Christmas aesthetic but playful."),
    ("24-vending-machine", S + "A hot pink custom vending machine filled with different cute plush toys behind glass. Neon glow, dark bar setting. Someone reaching for a dispensed plush at the bottom slot."),
]

def gen(name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"temperature":1.0}}
    req = urllib.request.Request(url, json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=90)
        result = json.loads(resp.read().decode())
        for c in result.get("candidates",[]):
            for p in c.get("content",{}).get("parts",[]):
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    path = os.path.join(OUT, f"{name}.png")
                    with open(path,"wb") as f: f.write(img)
                    print(f"  OK ({len(img)//1024}KB)")
                    return True
        print("  No image"); return False
    except Exception as e:
        print(f"  FAIL: {e}"); return False

for i,(n,p) in enumerate(RETRY):
    print(f"[{i+1}/{len(RETRY)}] {n}...", end="", flush=True)
    gen(n,p)
    if i < len(RETRY)-1: time.sleep(15)
print("\nDone!")
