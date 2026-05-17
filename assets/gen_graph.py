#!/usr/bin/env python3
"""
Fetch real contribution data from GitHub GraphQL API and regenerate
assets/hero.svg + assets/graph.svg.

Requires GITHUB_TOKEN environment variable.
Run: python3 assets/gen_graph.py
"""

import json, os, sys, urllib.request

USERNAME = "ducwithoutk"
TOKEN    = os.environ.get("GITHUB_TOKEN", "")

ORANGE = "#e8812b"; CREAM = "#f0e6d0"; DIM = "#6e6354"
MID    = "#8a7a65"; BORDER= "#2d2820"; BG  = "#0f0e0c"
MONO   = "'Courier New', Courier, monospace"
SERIF  = "Georgia, 'Times New Roman', serif"

QUERY = '''{
  user(login: "%s") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { contributionCount } }
      }
    }
  }
}''' % USERNAME

# ── API ────────────────────────────────────────────────────────────────────────

def fetch():
    body = json.dumps({"query": QUERY}).encode()
    req  = urllib.request.Request(
        "https://api.github.com/graphql",
        data=body,
        headers={
            "Authorization": f"Bearer {TOKEN}",
            "Content-Type": "application/json",
        },
    )
    res = json.loads(urllib.request.urlopen(req).read())
    cal = res["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], cal["weeks"]

# ── Helpers ────────────────────────────────────────────────────────────────────

def fmt_total(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

# 4-step palette: empty → dark amber → mid amber → orange → cream
_PALETTE = ["#1e1a14", "#3d2206", "#8f4c0a", "#e8812b", "#f0d5a0"]

def _color(count, high):
    if count == 0:
        return _PALETTE[0]
    r = count / max(high, 1)
    if r < .25: return _PALETTE[1]
    if r < .50: return _PALETTE[2]
    if r < .75: return _PALETTE[3]
    return _PALETTE[4]

# ── hero.svg ───────────────────────────────────────────────────────────────────

def make_hero(total_n):
    W, H  = 800, 168
    label = fmt_total(total_n)

    css = (
        "@keyframes fadeIn{from{opacity:0}to{opacity:1}}"
        "@keyframes scaleIn{from{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.85)}"
        "to{opacity:1;transform-box:fill-box;transform-origin:center;transform:scale(1)}}"
        "@keyframes caretBlink{0%,100%{opacity:1}50%{opacity:0}}"
        ".f0{animation:fadeIn .35s 0s ease-out both}"
        ".f1{animation:fadeIn .3s .35s ease-out both}"
        ".f2{animation:fadeIn .3s .55s ease-out both}"
        ".f3{animation:fadeIn .3s .70s ease-out both}"
        ".f4{animation:fadeIn .3s .84s ease-out both}"
        ".f5{animation:fadeIn .3s .98s ease-out both}"
        ".f6{animation:fadeIn .3s 1.10s ease-out both}"
        ".sq0{animation:scaleIn .35s .60s ease-out both}"
        ".sq1{animation:scaleIn .35s .85s ease-out both}"
        ".cr{animation:caretBlink .5s 1.7s step-start 3 forwards}"
    )

    els = [
        f'<rect class="f0" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="7" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>',
        f'<line class="f0" x1=".5" y1="30" x2="{W-.5}" y2="30" stroke="{BORDER}" stroke-width="1"/>',
        f'<text class="f1" x="14" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}">README.md</text>',
        f'<text class="f1" x="{W-14}" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}" text-anchor="end">{label} contributions</text>',
        f'<text class="f2" x="14" y="48" font-family="{MONO}" font-size="12" fill="{ORANGE}">// intro</text>',
        f'<text class="cr" x="72" y="48" font-family="{MONO}" font-size="12" fill="{ORANGE}">&#9612;</text>',
        # ornamental quote marks rendered before text so text sits on top
        f'<text class="sq0" x="10" y="92" font-family="{SERIF}" font-size="48" fill="{ORANGE}">“</text>',
        f'<text class="sq1" x="{W-10}" y="150" font-family="{SERIF}" font-size="48" fill="{ORANGE}" text-anchor="end">”</text>',
        f'<text class="f3" x="50" y="90" font-family="{MONO}" font-size="17" fill="{CREAM}">black coffee without sugar, hopefully some thinking in between.</text>',
        f'<text class="f4" x="50" y="113" font-family="{MONO}" font-size="13" fill="{MID}">—</text>',
        f'<text class="f5" x="64" y="132" font-family="{MONO}" font-size="11" fill="{DIM}">self-taught the engineering parts;</text>',
        f'<text class="f6" x="64" y="149" font-family="{MONO}" font-size="11" fill="{DIM}">still figuring out which parts i actually understand.</text>',
    ]

    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">',
        f'<style>{css}</style>',
        *els,
        '</svg>',
    ])

# ── graph.svg ──────────────────────────────────────────────────────────────────

def make_graph(weeks_data):
    W, H = 800, 158
    MONTH_C = "#3a3328"
    CELL, STEP, GX, GY = 11, 14, 32, 44

    # Use the most recent 52 weeks
    weeks_data = list(weeks_data)[-52:]
    while len(weeks_data) < 52:
        weeks_data.insert(0, {"contributionDays": []})

    all_counts = [
        d["contributionCount"]
        for w in weeks_data
        for d in w.get("contributionDays", [])
    ]
    high = max(all_counts) if all_counts else 1

    MONTHS = [
        ("Jan",0),("Feb",4),("Mar",9),("Apr",13),("May",17),("Jun",22),
        ("Jul",26),("Aug",30),("Sep",35),("Oct",39),("Nov",43),("Dec",48),
    ]
    DAY_LABELS = [("Mon",1), ("Wed",3), ("Fri",5)]  # Sun-first grid

    css = (
        "@keyframes cf{from{opacity:0}to{opacity:1}}"
        "@keyframes cp{"
          "0%{opacity:0;transform-box:fill-box;transform-origin:center;transform:scale(.88)}"
          "65%{opacity:1;transform-box:fill-box;transform-origin:center;transform:scale(1.06)}"
          "100%{opacity:1;transform-box:fill-box;transform-origin:center;transform:scale(1)}}"
        "@keyframes caretBlink{0%,100%{opacity:1}50%{opacity:0}}"
        "@keyframes fadeIn{from{opacity:0}to{opacity:1}}"
        ".ce{animation:cf .18s ease-out both}"
        ".ca{animation:cp .22s ease-out both}"
        ".cr{animation:caretBlink .5s 3.4s step-start 3 forwards}"
        ".lbl{animation:fadeIn .3s .1s ease-out both}"
        ".hdr{animation:fadeIn .35s 0s ease-out both}"
    )

    els = [
        f'<rect class="hdr" x=".5" y=".5" width="{W-1}" height="{H-1}" rx="7" fill="{BG}" stroke="{BORDER}" stroke-width="1"/>',
        f'<text class="lbl" x="14" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}">// contribution graph</text>',
        f'<text class="cr" x="166" y="20" font-family="{MONO}" font-size="12" fill="{ORANGE}">&#9612;</text>',
    ]

    for name, wk in MONTHS:
        els.append(f'<text class="lbl" x="{GX + wk*STEP}" y="36" font-family="{MONO}" font-size="9" fill="{MONTH_C}">{name}</text>')

    for name, row in DAY_LABELS:
        dy = GY + row * STEP + CELL // 2 + 3
        els.append(f'<text class="lbl" x="{GX-4}" y="{dy}" font-family="{MONO}" font-size="9" fill="{MONTH_C}" text-anchor="end">{name}</text>')

    for wk_idx, week in enumerate(weeks_data):
        delay = wk_idx * 14  # 14ms stagger per column
        days  = [d["contributionCount"] for d in week.get("contributionDays", [])]
        while len(days) < 7:
            days.append(0)

        for d_idx, count in enumerate(days):
            fill = _color(count, high)
            cls  = "ca" if count > 0 else "ce"
            cx, cy = GX + wk_idx * STEP, GY + d_idx * STEP
            els.append(
                f'<rect class="{cls}" style="animation-delay:{delay}ms" '
                f'x="{cx}" y="{cy}" width="{CELL}" height="{CELL}" rx="2" fill="{fill}"/>'
            )

    return '\n'.join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet">',
        f'<style>{css}</style>',
        *els,
        '</svg>',
    ])

# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not TOKEN:
        print("error: GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)

    print("Fetching contribution data …")
    total, weeks = fetch()
    print(f"  {total} total contributions across {len(weeks)} weeks")

    base = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(base, "hero.svg"), "w") as f:
        f.write(make_hero(total))
    print(f"  hero.svg  → {fmt_total(total)} contributions")

    with open(os.path.join(base, "graph.svg"), "w") as f:
        f.write(make_graph(weeks))
    print(f"  graph.svg → done")
