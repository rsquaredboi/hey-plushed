#!/usr/bin/env python3
"""Generate 10 identity logos for Hey Plushed theme switcher"""
import urllib.request, json, base64, os, ssl, time

API_KEY = "AIzaSyBexAkFQ4MgjEbJhLKkCHtjmPSMsT4O6oQ"
MODEL = "gemini-2.5-flash-image"
OUT = "/Users/rahul/Downloads/hey-plushed-lite/concepts/identities"
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

# Load Nancy logo for reference on #1
with open("/Users/rahul/Downloads/hey-plushed-lite/nancy-logo-pink.png", "rb") as f:
    nancy_b64 = base64.b64encode(f.read()).decode()

LOGOS = [
    ("01-og-nancy", True,
     "Looking at the attached Nancy logo, create the word 'Plushed' in the EXACT same style — hot pink #ff00d1, same thick bold chunky serif strokes, same playful curves and dramatic flourishes. White background. Just the wordmark 'Plushed', nothing else. Vector flat design."),
    ("02-midnight-neon", False,
     "Create a neon sign style logo for the word 'plushed' in lowercase. The text should look like a glowing neon tube — thin outline strokes with bright pink #ff00d1 glow effect and subtle cyan #00ffcc secondary glow. Black background. Modern nightclub typography. Clean, no icons."),
    ("03-soft-luxe", False,
     "Create an ultra-minimal luxury wordmark for 'Plushed'. Use a thin, elegant serif font (like Didot or Bodoni) in charcoal #2a2a2a on a warm cream #f5f0e8 background. Very thin strokes, high contrast, generous letter-spacing. Think Aesop or Le Labo branding. Quiet luxury. Just the word, no icons."),
    ("04-y2k-candy", False,
     "Create a Y2K/2000s style bubble letter logo for 'Plushed'. Glossy 3D bubble letters in hot pink #ff69b4 with purple #9b59b6 shadows and a slight chrome/metallic sheen. White background. Think early 2000s Bratz dolls or Lisa Frank aesthetic. Bubbly, fun, nostalgic."),
    ("05-brutalist", False,
     "Create a brutalist typography logo. The word 'PLUSHED' in ALL CAPS, extremely bold condensed black sans-serif (like Archivo Black). Pure black text on white background. Raw, aggressive, anti-design. One element in red #ff0000 — either a period after PLUSHED or an underline. Stark, punk energy."),
    ("06-pastel-dream", False,
     "Create a soft kawaii-style wordmark for 'plushed' in lowercase. Rounded, bubbly sans-serif font in pastel pink #FFB5E8. A tiny cute star or sparkle dot over the 'i' — wait no i, put a tiny heart or star above the 'h'. Very soft pastel pink on white background. Gen-Z cute aesthetic."),
    ("07-studio-minimal", False,
     "Create a Swiss/Bauhaus style geometric logo for 'PLUSHED'. Clean geometric sans-serif (like Helvetica or Futura), all uppercase, very precise letter-spacing. Black text on white background. Below the text, a single thin pink #ff00d1 horizontal line. Extremely minimal, gallery/museum aesthetic."),
    ("08-velvet-lounge", False,
     "Create a speakeasy/lounge style logo for 'Plushed'. Combine an elegant script 'P' with serif letters 'lushed'. Gold #d4a574 text on deep purple #2d1b4e background. Art deco influences, thin decorative lines above and below. Intimate, moody, cocktail bar energy."),
    ("09-acid-rave", False,
     "Create a distorted, warped text logo for 'PLUSHED'. The letters should be melting, stretching, or warping — acid/rave graphic design style. Lime green #c8ff00 as primary color with magenta #ff00d1 and cyan #00ffcc accents. Black background. Chaotic, psychedelic, gen-z party energy."),
    ("10-terracotta", False,
     "Create a warm, organic wordmark for 'plushed' in lowercase. Hand-drawn style letterforms with slight imperfections, like a ceramic stamp or woodblock print. Terracotta/rust color #c4704b on a warm cream #faf5ef background. Earthy, grounded, natural. Think ceramics studio branding."),
]

def gen(name, use_nancy, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    parts = []
    if use_nancy:
        parts.append({"inlineData": {"mimeType": "image/png", "data": nancy_b64}})
    parts.append({"text": prompt})
    payload = {"contents": [{"parts": parts}], "generationConfig": {"responseModalities": ["TEXT", "IMAGE"], "temperature": 1.0}}
    req = urllib.request.Request(url, json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=90)
        result = json.loads(resp.read().decode())
        for c in result.get("candidates", []):
            for p in c.get("content", {}).get("parts", []):
                if "inlineData" in p:
                    img = base64.b64decode(p["inlineData"]["data"])
                    path = os.path.join(OUT, f"{name}.png")
                    with open(path, "wb") as f: f.write(img)
                    print(f"  OK ({len(img)//1024}KB)")
                    return True
        print("  No image"); return False
    except Exception as e:
        print(f"  FAIL: {e}"); return False

print(f"Generating {len(LOGOS)} identity logos...\n")
fails = []
for i, (name, use_nancy, prompt) in enumerate(LOGOS):
    print(f"[{i+1}/{len(LOGOS)}] {name}...", end="", flush=True)
    ok = gen(name, use_nancy, prompt)
    if not ok: fails.append(name)
    if i < len(LOGOS) - 1: time.sleep(12)

if fails:
    print(f"\nRetrying {len(fails)} failures...")
    time.sleep(15)
    for name in fails:
        entry = [l for l in LOGOS if l[0] == name][0]
        print(f"  Retry {name}...", end="", flush=True)
        gen(entry[0], entry[1], entry[2])
        time.sleep(15)

print(f"\nDone! Check {OUT}/")
