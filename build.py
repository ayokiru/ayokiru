"""Generates the profile header and project cards in assets/ (dark and light)."""

import html
import textwrap

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
EASE = "cubic-bezier(.2,.7,.2,1)"
THEMES = {
    "dark": dict(card="#161B22", border="#30363D", title="#F0F6FC", text="#9198A1", ),
    "light": dict(card="#FFFFFF", border="#D1D9E0", title="#1F2328", text="#59636E", ),
}
LANG = {"Rust": "#DEA584", "Python": "#3572A5", "Steam": "#66C0F4"}
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def balanced(text, maxw):
    """Wraps text into the fewest, most even lines without a one-word last line."""
    best = None
    for w in range(maxw, maxw - 18, -1):
        lines = textwrap.wrap(text, w)
        if len(lines) > 3:
            break
        orphan = len(lines) > 1 and len(lines[-1].split()) < 2
        score = (len(lines), orphan, max(map(len, lines)) - min(map(len, lines)))
        if best is None or score < best[0]:
            best = (score, lines)
    return best[1]


def header(mode):
    fg = THEMES[mode]["title"]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="114" viewBox="0 0 800 114" role="img" aria-label="ayokiru">
  <style>
    .w {{ animation: up .7s {EASE} both; }}
    .bar {{ transform-origin: 2px 96px; animation: draw .6s {EASE} .45s both; }}
    .flow {{ animation: flow 9s linear 1.2s infinite; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(8px); }} }}
    @keyframes draw {{ from {{ transform: scaleX(0); }} }}
    @keyframes flow {{ to {{ transform: translateX(-112px); }} }}
    {REDUCED}
  </style>
  <defs>
    <linearGradient id="g" gradientUnits="userSpaceOnUse" x1="2" y1="0" x2="170" y2="0">
      <stop offset="0" stop-color="#FF6FA8"/><stop offset=".1667" stop-color="#9B7BFF"/><stop offset=".3333" stop-color="#4FC3FF"/>
      <stop offset=".5" stop-color="#9B7BFF"/><stop offset=".6667" stop-color="#FF6FA8"/><stop offset=".8333" stop-color="#9B7BFF"/><stop offset="1" stop-color="#4FC3FF"/>
    </linearGradient>
    <clipPath id="bar"><rect x="2" y="94" width="56" height="4" rx="2"/></clipPath>
  </defs>
  <text class="w" x="0" y="72" font-family="{FONT}" font-size="62" font-weight="700" letter-spacing="-2.5" fill="{fg}">ayokiru</text>
  <g class="bar" clip-path="url(#bar)"><rect class="flow" x="2" y="94" width="168" height="4" fill="url(#g)"/></g>
</svg>
"""


def card(mode, name, desc, lang, w, label, maxw, delay):
    t = THEMES[mode]
    h = 150
    lines = balanced(desc, maxw)
    text = "".join(
        f'<text x="20" y="{70 + i * 20}" font-family="{FONT}" font-size="14" fill="{t["text"]}">{html.escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    meta = (
        f'<circle cx="26" cy="{h - 24}" r="5" fill="{LANG[lang]}"/>'
        f'<text x="38" y="{h - 19}" font-family="{FONT}" font-size="12.5" fill="{t["text"]}">{lang}</text>'
    )
    if label:
        meta += f'<text x="{w - 20}" y="{h - 19}" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="{t["text"]}">{html.escape(label)}</text>'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(name)}">
  <style>
    .c {{ animation: up .6s {EASE} {delay}s both; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} }}
    {REDUCED}
  </style>
  <g class="c">
    <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="10" fill="{t['card']}" stroke="{t['border']}"/>
    <text x="20" y="40" font-family="{FONT}" font-size="19" font-weight="600" fill="{t['title']}">{html.escape(name)}</text>
    {text}
    {meta}
  </g>
</svg>
"""


BIG = [
    ("stillward", "Stillward Display", "Window animations, your own taskbar and dock, an island, pointers and widgets for Windows 10 and 11.", "Steam", "stillwarddisplay.com", 0.55),
    ("winrice", "winrice", "Dotfiles for your Windows look. Capture, share and apply a whole desktop setup with one command.", "Rust", "MIT", 0.65),
]
SMALL = [
    ("pakwatch", "pakwatch", "See which mods a game update touched. UE5 IoStore, Steam games found automatically.", "Python", None, 0.85),
    ("modrelease", "modrelease", "Check, pack and ship game mods without leaking who you are.", "Python", None, 0.95),
    ("bladesmith", "pbz-bladesmith", "Weapon transmog builder for Phantom Blade Zero.", "Python", "Nexus Mods", 1.05),
]

for mode in THEMES:
    with open(f"assets/header-{mode}.svg", "w") as f:
        f.write(header(mode))
    for cards, width, maxw in ((BIG, 396, 50), (SMALL, 262, 31)):
        for slug, name, desc, lang, label, delay in cards:
            with open(f"assets/{slug}-{mode}.svg", "w") as f:
                f.write(card(mode, name, desc, lang, width, label, maxw, delay))
