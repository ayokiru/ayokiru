"""Generates the profile header and project cards in assets/ (dark and light)."""

import html
import textwrap

FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif"
EASE = "cubic-bezier(.2,.7,.2,1)"
THEMES = {
    "dark": dict(card="#161B22", border="#30363D", title="#F0F6FC", text="#9198A1", faint="#6E7681"),
    "light": dict(card="#FFFFFF", border="#D1D9E0", title="#1F2328", text="#59636E", faint="#818B98"),
}
LANG = {"Rust": "#DEA584", "Python": "#3572A5", "Steam": "#66C0F4", "Pak mod": "#C8102E"}
REDUCED = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"
W, H = 396, 160  # every card: two per row, 800 px in all


def balanced(text, maxw):
    """Wraps text into the fewest, most even lines without a one-word last line."""
    best = None
    for w in range(maxw, maxw - 18, -1):
        lines = textwrap.wrap(text, w)
        if len(lines) > 2:
            continue
        orphan = len(lines) > 1 and len(lines[-1].split()) < 2
        score = (len(lines), orphan, max(map(len, lines)) - min(map(len, lines)))
        if best is None or score < best[0]:
            best = (score, lines)
    if best is None:
        raise ValueError(f"does not fit in two lines: {text}")
    return best[1]


def header(mode):
    t = THEMES[mode]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="800" height="150" viewBox="0 0 800 150" role="img" aria-label="ayokiru: tools for the Windows desktop and Unreal Engine modding">
  <style>
    .w {{ animation: up .7s {EASE} both; }}
    .s {{ animation: up .7s {EASE} .12s both; }}
    .bar {{ transform-origin: 2px 128px; animation: draw .6s {EASE} .45s both; }}
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
    <clipPath id="bar"><rect x="2" y="126" width="56" height="4" rx="2"/></clipPath>
  </defs>
  <text class="w" x="0" y="66" font-family="{FONT}" font-size="62" font-weight="700" letter-spacing="-2.5" fill="{t['title']}">ayokiru</text>
  <text class="s" x="2" y="104" font-family="{FONT}" font-size="20" letter-spacing="-0.2" fill="{t['text']}">Tools for the Windows desktop and for Unreal Engine game mods.</text>
  <g class="bar" clip-path="url(#bar)"><rect class="flow" x="2" y="126" width="168" height="4" fill="url(#g)"/></g>
</svg>
"""


def card(mode, name, desc, lang, label, colors, mark, delay):
    t = THEMES[mode]
    lines = balanced(desc, 46)
    text = "".join(
        f'<text x="24" y="{96 + i * 21}" font-family="{FONT}" font-size="14" fill="{t["text"]}">{html.escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    meta = (
        f'<circle cx="29" cy="{H - 24}" r="5" fill="{LANG[lang]}"/>'
        f'<text x="41" y="{H - 19.5}" font-family="{FONT}" font-size="12.5" fill="{t["faint"]}">{lang}</text>'
    )
    if label:
        meta += f'<text x="{W - 24}" y="{H - 19.5}" text-anchor="end" font-family="{FONT}" font-size="12.5" fill="{t["faint"]}">{html.escape(label)}</text>'
    a, b = colors
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{html.escape(name)}: {html.escape(desc)}">
  <style>
    .c {{ animation: up .6s {EASE} {delay}s both; }}
    @keyframes up {{ from {{ opacity: 0; transform: translateY(10px); }} }}
    {REDUCED}
  </style>
  <defs><linearGradient id="m" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>
  <g class="c">
    <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="12" fill="{t['card']}" stroke="{t['border']}"/>
    <rect x="24" y="24" width="40" height="40" rx="10" fill="url(#m)"/>
    <text x="44" y="51" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" letter-spacing="-0.3" fill="#FFFFFF">{html.escape(mark)}</text>
    <text x="78" y="50" font-family="{FONT}" font-size="19" font-weight="600" letter-spacing="-0.3" fill="{t['title']}">{html.escape(name)}</text>
    <path d="M{W - 34} 38 l6 6 -6 6" fill="none" stroke="{t['faint']}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    {text}
    {meta}
  </g>
</svg>
"""


# slug, name, description, language, right label, monogram colors, monogram, delay
CARDS = [
    ("stillward", "Stillward Display", "Window animations, your own taskbar and dock, an island and widgets for Windows.", "Steam", "stillwarddisplay.com", ("#4FC3FF", "#7B61FF"), "S", 0.5),
    ("winrice", "winrice", "Dotfiles for your Windows look. Share a whole desktop and apply it with one command.", "Rust", "MIT", ("#FF6FA8", "#9B7BFF"), "w", 0.58),
    ("pakwatch", "pakwatch", "See which of your mods a game update touched. UE5 IoStore and .pak, Steam aware.", "Python", "PyPI", ("#0A84FF", "#5E5CE6"), "p", 0.66),
    ("modrelease", "modrelease", "Check, pack and ship game mods without leaking who you are.", "Python", "PyPI", ("#30D158", "#0A84FF"), "m", 0.74),
    ("bladesmith", "Bladesmith", "Weapon transmog for Phantom Blade Zero: any weapon's look, trails and blade color.", "Python", "Nexus Mods", ("#FF9F0A", "#FF453A"), "B", 0.82),
    ("sanguine", "Sanguine Skins", "The Sanguine blades, scabbards and blood trails on other weapons in Phantom Blade Zero.", "Pak mod", "Nexus Mods", ("#C8102E", "#5A0A12"), "S", 0.9),
]

for mode in THEMES:
    with open(f"assets/header-{mode}.svg", "w", encoding="utf-8", newline="\n") as f:
        f.write(header(mode))
    for slug, name, desc, lang, label, colors, mark, delay in CARDS:
        with open(f"assets/{slug}-{mode}.svg", "w", encoding="utf-8", newline="\n") as f:
            f.write(card(mode, name, desc, lang, label, colors, mark, delay))
