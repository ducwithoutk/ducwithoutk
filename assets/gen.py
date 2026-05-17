#!/usr/bin/env python3
"""Generate a static hero.svg """

ORANGE = "#e8812b"
CREAM  = "#f0e6d0"
DIM    = "#6e6354"
MID    = "#8a7a65"
BORDER = "#2d2820"
BG     = "#0f0e0c"
MONO   = "'Courier New', Courier, monospace"
SERIF  = "Georgia, 'Times New Roman', serif"


def make_hero():
    W, H = 800, 168

    css = """\
    @keyframes fadeIn{from{opacity:0}to{opacity:1}}
    @keyframes scaleIn{
      from{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.85)}
      to  {opacity:1;transform-box:fill-box;transform-origin:center;transform:scale(1)}
    }
    @keyframes caretBlink{0%,100%{opacity:1}50%{opacity:0}}
    .f0{animation:fadeIn .35s 0s    ease-out both}
    .f1{animation:fadeIn .3s  .35s  ease-out both}
    .f2{animation:fadeIn .3s  .55s  ease-out both}
    .f3{animation:fadeIn .3s  .70s  ease-out both}
    .f4{animation:fadeIn .3s  .84s  ease-out both}
    .f5{animation:fadeIn .3s  .98s  ease-out both}
    .f6{animation:fadeIn .3s  1.10s ease-out both}
    .sq0{animation:scaleIn .35s .60s ease-out both}
    .sq1{animation:scaleIn .35s .85s ease-out both}
    .cr{animation:caretBlink .5s 1.7s step-start 3 forwards}"""

    els = [
        # container + header bar
        f'<rect class="f0" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="7" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>',
        f'<line class="f0" x1=".5" y1="30" x2="{W-.5}" y2="30" stroke="{BORDER}" stroke-width="1"/>',
        f'<text class="f1" x="14" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}">README.md</text>',
        f'<text class="f1" x="{W-14}" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}" text-anchor="end">7.9k contributions</text>',

        # section label + blinking caret
        f'<text class="f2" x="14" y="48" font-family="{MONO}" font-size="12" fill="{ORANGE}">// intro</text>',
        f'<text class="cr" x="72" y="48" font-family="{MONO}" font-size="12" fill="{ORANGE}">&#9612;</text>',

        # ornamental quote marks (rendered first so text sits on top)
        f'<text class="sq0" x="10" y="92" font-family="{SERIF}" font-size="48" fill="{ORANGE}">“</text>',
        f'<text class="sq1" x="{W-10}" y="150" font-family="{SERIF}" font-size="48" fill="{ORANGE}" text-anchor="end">”</text>',

        # main quote — single line, display scale
        f'<text class="f3" x="50" y="90" font-family="{MONO}" font-size="17" fill="{CREAM}">black coffee without sugar, hopefully some thinking in between.</text>',

        # em dash alone — visual pause
        f'<text class="f4" x="50" y="113" font-family="{MONO}" font-size="13" fill="{MID}">—</text>',

        # attribution, indented
        f'<text class="f5" x="64" y="132" font-family="{MONO}" font-size="11" fill="{DIM}">self-taught the engineering parts;</text>',
        f'<text class="f6" x="64" y="149" font-family="{MONO}" font-size="11" fill="{DIM}">still figuring out which parts i actually understand.</text>',
    ]

    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">',
        f'<style>{css}</style>',
        *els,
        '</svg>',
    ])


if __name__ == "__main__":
    import os
    base = os.path.dirname(__file__)
    path = os.path.join(base, "hero.svg")
    with open(path, "w") as f:
        f.write(make_hero())
    print(f"hero.svg → {path}")
    print("For graph.svg with live data: python3 assets/gen_graph.py")
