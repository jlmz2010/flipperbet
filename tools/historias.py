"""Genera las historias de WhatsApp e Instagram (1080x1920) de FlipperBet.
Uso: python3 tools/historias.py --semana 5 --partidos 14
Requiere: pip install cairosvg (las fuentes vienen en tools/fonts)."""
import os, sys, shutil, subprocess, argparse
ap = argparse.ArgumentParser(); ap.add_argument("--semana", type=int, required=True); ap.add_argument("--partidos", type=int, required=True)
ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "historias"))
args = ap.parse_args(); SEMANA, PARTIDOS = args.semana, args.partidos
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
fdir = os.path.expanduser("~/.fonts"); os.makedirs(fdir, exist_ok=True)
for f in os.listdir(FONTS): shutil.copy(os.path.join(FONTS, f), fdir)
subprocess.run(["fc-cache", "-f"], check=False)
import cairosvg


DEEP = "#073a54"; OCEAN = "#0b5e86"; SKY = "#3fa3d4"
GOLD = "#d4a534"; GOLD_L = "#f0c75a"; GOLD_D = "#8f6b15"; WHITE = "#f3f8fb"

def ball(a=150, b=92):
    k = 1.33
    return (f"M{-a},0 C{-a*0.5},{-b*k} {a*0.5},{-b*k} {a},0 "
            f"C{a*0.5},{b*k} {-a*0.5},{b*k} {-a},0 Z")

def mark(cx, cy, s=1.0, arcs=True):
    """Coin-ball mark centered at cx,cy; nominal size ~ 380px wide at s=1."""
    laces = "".join(
        f'<line x1="{x}" y1="-16" x2="{x}" y2="16" stroke="{WHITE}" stroke-width="9" stroke-linecap="round"/>'
        for x in (-36, -12, 12, 36))
    arc_svg = ""
    if arcs:
        arc_svg = (
            f'<path d="M-190,150 C-150,40 -60,-70 60,-150" fill="none" stroke="{SKY}" stroke-width="14" stroke-linecap="round" opacity=".9"/>'
            f'<path d="M-150,185 C-105,90 -30,5 70,-60" fill="none" stroke="{GOLD}" stroke-width="9" stroke-linecap="round" opacity=".55"/>'
        )
    return f'''<g transform="translate({cx},{cy}) scale({s})">
  {arc_svg}
  <g transform="rotate(-32)">
    <path d="{ball()}" transform="translate(9,15)" fill="{GOLD_D}"/>
    <path d="{ball()}" fill="url(#gold)"/>
    <path d="{ball(126, 74)}" fill="none" stroke="{GOLD_D}" stroke-width="5" opacity=".7"/>
    <line x1="-62" y1="0" x2="62" y2="0" stroke="{WHITE}" stroke-width="10" stroke-linecap="round"/>
    {laces}
    <path d="M-104,-44 C-70,-72 -20,-84 30,-80" fill="none" stroke="#fff6d6" stroke-width="8" stroke-linecap="round" opacity=".6"/>
  </g>
</g>'''

DEFS = f'''<defs>
  <linearGradient id="gold" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="{GOLD_L}"/><stop offset=".55" stop-color="{GOLD}"/><stop offset="1" stop-color="#b8871f"/>
  </linearGradient>
  <pattern id="yards" width="64" height="10" patternUnits="userSpaceOnUse">
    <rect width="3" height="10" fill="#ffffff" opacity=".06"/>
  </pattern>
</defs>'''

def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{DEFS}{body}</svg>'


WORD = 'font-family="Barlow Condensed" font-weight="800"'

from PIL import ImageFont
BC800 = os.path.join(FONTS, "BarlowCondensed_800ExtraBold.ttf")
def two_tone(x, y, size, a, b, ca, cb, anchor="middle", ls=2):
    f = ImageFont.truetype(BC800, size)
    wa = f.getlength(a) + ls*len(a); wb = f.getlength(b) + ls*len(b)
    x0 = x - (wa+wb)/2 if anchor == "middle" else x
    return (f'<text x="{x0:.1f}" y="{y}" {WORD} font-size="{size}" letter-spacing="{ls}" fill="{ca}">{a}</text>'
            f'<text x="{x0+wa:.1f}" y="{y}" {WORD} font-size="{size}" letter-spacing="{ls}" fill="{cb}">{b}</text>')



def story(ig):
    link_block = (
        # Instagram: links in text aren't clickable, so leave room for the link sticker
        f'<text x="540" y="1470" text-anchor="middle" font-family="Libre Franklin" font-weight="700" font-size="46" fill="{WHITE}">Toca el link</text>'
        f'<path d="M540,1500 L540,1580 M505,1548 L540,1583 L575,1548" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        if ig else
        f'<text x="540" y="1470" text-anchor="middle" font-family="Libre Franklin" font-weight="600" font-size="40" fill="#a9c9da">Entra aquí:</text>'
        f'<rect x="90" y="1505" width="900" height="120" rx="14" fill="{GOLD}"/>'
        f'<text x="540" y="1583" text-anchor="middle" font-family="Libre Franklin" font-weight="800" font-size="46" fill="#1c1405">jlmz2010.github.io/flipperbet</text>'
    )
    body = (
        f'<rect width="1080" height="1920" fill="{DEEP}"/><rect width="1080" height="1920" fill="url(#yards)"/>'
        + mark(540, 330, 0.9) +
        two_tone(540, 590, 120, "Flipper", "Bet", GOLD, WHITE) +
        f'<text x="540" y="650" text-anchor="middle" font-family="Libre Franklin" font-weight="600" font-size="32" letter-spacing="8" fill="{SKY}">NFL EN ESPAÑOL</text>' +
        two_tone(540, 930, 250, "SEMANA ", str(SEMANA), WHITE, GOLD, ls=0) +
        f'<text x="540" y="1060" text-anchor="middle" font-family="Libre Franklin" font-weight="700" font-size="54" fill="{WHITE}">Underdog del jueves</text>'
        f'<text x="540" y="1130" text-anchor="middle" font-family="Libre Franklin" font-weight="400" font-size="44" fill="#d9e8f0">+ claves de los {PARTIDOS} partidos</text>'
        f'<text x="540" y="1270" text-anchor="middle" font-family="Libre Franklin" font-weight="400" font-size="38" fill="#a9c9da">Líneas explicadas en corto.</text>'
        + link_block +
        f'<text x="540" y="1800" text-anchor="middle" font-family="Libre Franklin" font-weight="400" font-size="28" fill="#7fa3b8">Solo mayores de 18 · Apuesta con responsabilidad</text>'
    )
    return svg(1080, 1920, body)


os.makedirs(args.out, exist_ok=True)
for ig, name in [(False, "whatsapp"), (True, "instagram")]:
    path = os.path.join(args.out, f"historia-{name}-semana-{SEMANA}.png")
    cairosvg.svg2png(bytestring=story(ig).encode(), write_to=path, output_width=1080)
    print(path)
