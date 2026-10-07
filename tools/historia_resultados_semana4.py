import sys, os, cairosvg
src = open("/home/claude/flipperbet/tools/historias.py", encoding="utf-8").read()
base = src.split("def story(")[0]
sys.argv = ["x", "--semana", "4", "--partidos", "16"]
g = {"__file__": "/home/claude/flipperbet/tools/historias.py", "__name__": "lib"}
exec(base, g)
mark, svg, two_tone, WORD = g["mark"], g["svg"], g["two_tone"], g["WORD"]
DEEP, GOLD, WHITE, SKY, OCEAN = g["DEEP"], g["GOLD"], g["WHITE"], g["SKY"], g["OCEAN"]
WIN = "#1f7a4d"; WIN_L = "#2fa36a"
FR = 'font-family="Libre Franklin"'

DOGS = [("JUE", "Browns", "+130", "27-24", "vs Steelers"),
        ("DOM", "Cowboys", "+140", "34-30", "en Houston"),
        ("LUN", "Falcons", "+125", "45-24", "en Nueva Orleans")]

def check(cx, cy, r=34):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{WIN_L}"/>'
            f'<path d="M{cx-15},{cy+1} L{cx-4},{cy+12} L{cx+17},{cy-12}" fill="none" stroke="#fff" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')

def rows(y0):
    out = ""
    for i, (day, team, ml, score, where) in enumerate(DOGS):
        y = y0 + i * 170
        out += (f'<rect x="80" y="{y}" width="920" height="140" rx="16" fill="#ffffff" fill-opacity=".06" stroke="{WIN_L}" stroke-width="3"/>'
                + check(160, y + 70) +
                f'<text x="225" y="{y+64}" {WORD} font-size="64" fill="{WHITE}">{team.upper()}</text>'
                f'<text x="227" y="{y+108}" {FR} font-weight="400" font-size="30" fill="#a9c9da">{day} · {where}</text>'
                f'<text x="960" y="{y+64}" text-anchor="end" font-family="Barlow Condensed" font-weight="800" font-size="60" fill="{GOLD}">{ml}</text>'
                f'<text x="960" y="{y+108}" text-anchor="end" {FR} font-weight="700" font-size="32" fill="{WHITE}">Ganó {score}</text>')
    return out

from PIL import ImageFont
def picks_line():
    fa = ImageFont.truetype(os.path.expanduser("~/.fonts/LibreFranklin_600SemiBold.ttf"), 38)
    fb = ImageFont.truetype(os.path.expanduser("~/.fonts/LibreFranklin_800ExtraBold.ttf"), 44)
    a, b = "Picks de la semana: ", "11-5"
    wa, wb = fa.getlength(a), fb.getlength(b); wa += 4; x0 = 540 - (wa + wb) / 2
    return (f'<text x="{x0:.1f}" y="1380" {FR} font-weight="600" font-size="38" fill="#d9e8f0" xml:space="preserve">{a}</text>'
            f'<text x="{x0+wa:.1f}" y="1380" {FR} font-weight="800" font-size="44" fill="{GOLD}">{b}</text>')

def story(ig):
    link = (
        f'<text x="540" y="1565" text-anchor="middle" {FR} font-weight="700" font-size="44" fill="{WHITE}">Semana 5 este jueves · toca el link</text>'
        f'<path d="M540,1595 L540,1665 M507,1633 L540,1666 L573,1633" fill="none" stroke="{GOLD}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        if ig else
        f'<text x="540" y="1555" text-anchor="middle" {FR} font-weight="600" font-size="38" fill="#a9c9da">Semana 5 este jueves en:</text>'
        f'<rect x="90" y="1590" width="900" height="116" rx="14" fill="{GOLD}"/>'
        f'<text x="540" y="1666" text-anchor="middle" {FR} font-weight="800" font-size="46" fill="#1c1405">jlmz2010.github.io/flipperbet</text>')
    body = (
        f'<rect width="1080" height="1920" fill="{DEEP}"/><rect width="1080" height="1920" fill="url(#yards)"/>'
        + mark(250, 215, 0.55, arcs=False) +
        two_tone(380, 245, 96, "Flipp", "BetBlog", GOLD, WHITE, anchor="start") +
        f'<text x="384" y="292" {FR} font-weight="600" font-size="28" letter-spacing="7" fill="{SKY}">NFL EN ESPAÑOL · SEMANA 4</text>'
        f'<text x="540" y="590" text-anchor="middle" {WORD} font-size="320" fill="{GOLD}">3 DE 3</text>'
        f'<text x="540" y="680" text-anchor="middle" {FR} font-weight="700" font-size="52" fill="{WHITE}">Underdogs que ganaron directo</text>'
        f'<text x="540" y="740" text-anchor="middle" {FR} font-weight="400" font-size="36" fill="#d9e8f0">Fuimos contra Vegas y pegaron los tres</text>'
        + rows(810) +
        picks_line() +
        link +
        f'<text x="540" y="1830" text-anchor="middle" {FR} font-weight="400" font-size="27" fill="#7fa3b8">Resultados pasados no garantizan resultados futuros · Solo +18</text>'
    )
    return svg(1080, 1920, body)

out = "/home/claude/flipperbet/historias"
for ig, name in [(False, "whatsapp"), (True, "instagram")]:
    p = f"{out}/historia-{name}-semana-4-resultados.png"
    cairosvg.svg2png(bytestring=story(ig).encode(), write_to=p, output_width=1080)
    print(p)
