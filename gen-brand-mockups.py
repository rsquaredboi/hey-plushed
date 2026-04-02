#!/usr/bin/env python3
"""Generate 6 brand identity mockups for Plushed using Gemini"""
import urllib.request, json, base64, os, ssl, time

API_KEY = "AIzaSyBexAkFQ4MgjEbJhLKkCHtjmPSMsT4O6oQ"
MODEL = "gemini-2.5-flash-image"
OUT = os.path.expanduser("~/.gstack/projects/Downloads/designs/plushed-brand-20260401")
os.makedirs(OUT, exist_ok=True)
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE

VARIANTS = [
    ("variant-A", "Create a brand identity board mockup for 'Plushed', a premium adult collectible plushie brand. DIRECTION: Soft Luxe. Layout: cream background (#f5f0e8), show the logo 'Plushed' in thin italic serif (Didot-style) in charcoal, a tagline 'soft on the outside' in small caps below, 5 color swatches (cream, charcoal, warm brown, white, sand), a sample product card showing a cute round plushie on cream background, and a mock Instagram post. Aesop packaging vibes. Minimal, grown-up, belongs in a design magazine. Brand board layout with clear sections."),
    ("variant-B", "Create a brand identity board mockup for 'Plushed', a 21+ collectible plushie brand. DIRECTION: Candy Pop Y2K. Layout: light pink background, show the logo 'Plushed' in thick bubbly 3D bubble letters in hot pink and purple, tagline 'so fetch' below, 5 candy color swatches (bubblegum pink, purple, electric blue, blush, deep plum), a product card with glossy styling, and a mock Instagram post. Bratz dolls meets Lisa Frank energy. 2000s nostalgia for adults. Brand board layout."),
    ("variant-C", "Create a brand identity board mockup for 'Plushed', a 21+ plushie brand. DIRECTION: MS Paint Anti-Design. Layout: white background, show the logo 'pLuShEd' in messy hand-drawn marker style with clashing neon colors (magenta, lime green, electric blue, yellow). Deliberately ugly aesthetic like Microsoft Paint 2003. Spray tool textures, pixel art elements. Color swatches are deliberately misaligned. Product card looks like a GeoCities page. Mock social post looks like a MySpace profile. The ugliness IS the design. Internet-ugly-core. Brand board layout."),
    ("variant-D", "Create a brand identity board mockup for 'Plushed', a 21+ collectible plushie brand. DIRECTION: Tokyo Minimal. Layout: pure white background with massive whitespace. Logo 'plushed' in lowercase, lightweight sans-serif (Helvetica-style), tightly kerned, in soft gray. One tiny pastel coral accent color. Muji meets Sonny Angel. Everything is restrained and intentional. 5 swatches: white, light gray, coral, off-white, charcoal. Product card is mostly white space with a small plushie centered. Instagram grid mockup shows clean editorial layout. Japanese design sensibility. Brand board layout."),
    ("variant-E", "Create a brand identity board mockup for 'Plushed', a 21+ collectible plushie brand. DIRECTION: Night Market. Layout: dark background (#0a0a0a). Logo 'plushed' as a neon sign with glowing pink outline letters and cyan secondary glow. Tagline 'open late'. Dark product cards with neon pink borders. Color swatches: hot pink, neon cyan, deep black, midnight blue, white. Instagram story mockup with dark moody neon aesthetic. Tokyo alley at 2am with plush toys in windows. Street food market energy. Brand board layout."),
    ("variant-F", "Create a brand identity board mockup for 'Plushed', a 21+ collectible plushie brand. DIRECTION: Studio Object. Layout: gallery white background. Logo 'PLUSHED' in wide-spaced uppercase geometric sans-serif with a single thin pink line underneath. Museum gift shop energy. Bauhaus influence. 5 swatches: black, hot pink (#ff00d1), white, off-white, light gray. Product displayed as if on a white pedestal/plinth. Instagram grid mockup looks like a gallery exhibition catalog. The plushie is an art object. Brand board layout."),
]

def gen(name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"
    payload = {"contents":[{"parts":[{"text":prompt}]}],"generationConfig":{"responseModalities":["TEXT","IMAGE"],"temperature":1.0}}
    req = urllib.request.Request(url, json.dumps(payload).encode(), headers={"Content-Type":"application/json"})
    try:
        resp = urllib.request.urlopen(req, context=ctx, timeout=120)
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

print(f"Generating {len(VARIANTS)} brand identity mockups...\n")
for i,(n,p) in enumerate(VARIANTS):
    print(f"[{i+1}/{len(VARIANTS)}] {n}...", end="", flush=True)
    gen(n,p)
    if i < len(VARIANTS)-1: time.sleep(12)
print(f"\nDone! Files in {OUT}/")
