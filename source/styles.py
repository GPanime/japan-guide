"""Stylesheet for the guide.

BASE_CSS is the original design (tokens, layout, cards, map, hero). scoped_css() turns it into a version
where every rule sits under #jp26, so the guide can live inside another site (it was first embedded in
Squarespace) without its styles leaking out or the host's styles leaking in. The GitHub page uses the same
scoped CSS plus a dark-mode block added in build_site.py.
"""
import re

R = "#jp26"

BASE_CSS = r'''
/* Layout: sticky city tabs on top; hero; then a two-column planner — option cards on the left, a sticky map on the right (stacks on phones). */
:root {
  --bg: #FFF8EE; --surface: #FFFFFF; --surface2: #FFFDF8; --ink: #3A2E2A; --soft: #6A4A3C; --muted: #8A766A;
  --line: #F0E2CF; --chip: #F3ECE3; --accent: #D9483B; --sun: #F7B267; --dark: #3A2E2A; --onDark: #FFF3E3; --day: #3A2E2A;
  --hero1: #FFE2C6; --hero2: #FBC1A3; --mapgrid: #E6D6C1; --maplbl: #B79E88;
  --display: "Fredoka", ui-rounded, "Arial Rounded MT Bold", system-ui, sans-serif;
  --body: "Nunito", system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --jpf: "Noto Sans JP", "Hiragino Sans", "Yu Gothic", "PingFang SC", sans-serif;
  --r: 22px;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #1C1613; --surface: #28201C; --surface2: #221B17; --ink: #F4E8DA; --soft: #E2CDB8; --muted: #B29D8D;
  --line: #3B302A; --chip: #362B25; --accent: #F07261; --dark: #F4E8DA; --onDark: #2A211C; --day: #4A3229;
  --hero1: #3B2A2B; --hero2: #5E3B34; --mapgrid: #3E3330; --maplbl: #8C7869; color-scheme: dark; } }
:root[data-theme="dark"] {
  --bg: #1C1613; --surface: #28201C; --surface2: #221B17; --ink: #F4E8DA; --soft: #E2CDB8; --muted: #B29D8D;
  --line: #3B302A; --chip: #362B25; --accent: #F07261; --dark: #F4E8DA; --onDark: #2A211C; --day: #4A3229;
  --hero1: #3B2A2B; --hero2: #5E3B34; --mapgrid: #3E3330; --maplbl: #8C7869; color-scheme: dark; }

* { box-sizing: border-box; }
[hidden] { display: none !important; }
html { scroll-padding-top: 84px; }
body { margin: 0; background: var(--bg); color: var(--ink); font-family: var(--body); font-size: 16px; line-height: 1.55; -webkit-font-smoothing: antialiased; }
a { color: inherit; }
h1, h2, h3 { font-family: var(--display); font-weight: 600; margin: 0; text-wrap: balance; line-height: 1.12; }
button { font: inherit; color: inherit; }
:focus-visible { outline: 3px solid var(--sun); outline-offset: 2px; border-radius: 8px; }
.wrap { max-width: 1180px; margin: 0 auto; padding-inline: 16px; }

/* top bar */
.bar { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 10; background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); border-bottom: 1.5px solid var(--line); }
.bar .wrap { display: flex; align-items: center; gap: 18px; padding-block: 10px; }
.brand { font-family: var(--display); font-weight: 600; font-size: 18px; white-space: nowrap; display: flex; align-items: center; gap: 8px; text-decoration: none; }
.brand i { width: 12px; height: 12px; border-radius: 50%; background: var(--accent); box-shadow: 0 0 0 3px color-mix(in srgb, var(--accent) 25%, transparent); }
.tabs { display: flex; gap: 6px; overflow-x: auto; scrollbar-width: none; min-width: 0; flex: 1; }
.tabs::-webkit-scrollbar { display: none; }
.tab { display: flex; flex-direction: column; line-height: 1.15; padding: 6px 14px; border-radius: 14px; text-decoration: none; white-space: nowrap; flex: none; }
.tab b { font-family: var(--display); font-weight: 600; font-size: 15px; }
.tab small { font-size: 11.5px; font-weight: 700; color: var(--muted); font-variant-numeric: tabular-nums; }
.tab.on { background: var(--dark); color: var(--onDark); }
.tab.on small { color: color-mix(in srgb, var(--onDark) 70%, transparent); }
.tab.off { opacity: .55; }

/* hero */
.hero { margin-top: 18px; border-radius: 30px; background: linear-gradient(160deg, var(--hero1), var(--hero2)); display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); overflow: hidden; }
.hero .txt { padding: 40px 36px 36px; align-self: center; }
.kicker { font-family: var(--display); font-weight: 500; letter-spacing: .18em; font-size: 12.5px; text-transform: uppercase; color: var(--accent); }
.hero h1 { font-size: clamp(54px, 9vw, 92px); line-height: .95; margin-top: 10px; }
.jpbig { font-family: var(--jpf); font-weight: 900; font-size: clamp(26px, 4vw, 36px); color: var(--accent); letter-spacing: .12em; margin-top: 4px; }
.sub { font-family: var(--display); font-size: 21px; color: var(--soft); margin-top: 12px; line-height: 1.3; }
.pill { display: inline-block; margin-top: 18px; background: var(--surface); border: 2px solid var(--ink); border-radius: 99px; padding: 6px 16px;
  font-family: var(--display); font-weight: 500; font-size: 15px; font-variant-numeric: tabular-nums; }
.hero .art { align-self: end; display: flex; }
.coverart { width: 100%; height: auto; display: block; }

/* basics */
.basics { display: grid; grid-template-columns: 1.3fr 1fr 1fr; gap: 14px; margin-top: 14px; }
.box { background: var(--surface); border: 1.5px solid var(--line); border-radius: var(--r); padding: 18px 20px; min-width: 0; }
.box h3 { font-size: 17px; margin-bottom: 6px; }
.box p { margin: 0; color: var(--soft); font-size: 15px; }
.box.dark { background: var(--day); color: #FFF3E3; border-color: transparent; }
.box.dark h3 { color: var(--sun); }
.box.dark p { color: #F1DFCB; }
.box .btn { margin-top: 12px; }
.small { font-size: 13.5px; color: var(--muted); font-weight: 700; }

/* planner layout */
.planner { display: grid; grid-template-columns: minmax(0, 1fr) 360px; gap: 28px; margin-top: 34px; align-items: start; }
.controls { display: flex; flex-direction: column; gap: 12px; }
.ctrlhead { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap; }
.ctrlhead h2 { font-size: 30px; }
.ctrlhead h2 span { font-family: var(--display); font-weight: 500; font-size: 16px; color: var(--accent); margin-left: 8px; }
.seg { display: inline-flex; background: var(--chip); border-radius: 99px; padding: 4px; }
.seg button { border: 0; background: transparent; padding: 7px 16px; border-radius: 99px; font-family: var(--display); font-weight: 500; font-size: 15px; cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--surface); box-shadow: 0 1px 3px rgba(0,0,0,.12); }
.row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
.rowlbl { font-family: var(--display); font-weight: 500; font-size: 14px; color: var(--muted); margin-right: 4px; }
.chip { display: inline-flex; align-items: center; gap: 6px; border: 1.5px solid var(--line); background: var(--surface); border-radius: 99px;
  padding: 6px 13px; font-weight: 800; font-size: 14px; cursor: pointer; transition: background .15s, border-color .15s; }
.chip:hover { border-color: var(--muted); }
.chip i { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.chip em { font-style: normal; font-weight: 700; font-size: 12px; color: var(--muted); font-variant-numeric: tabular-nums; }
.chip[aria-pressed="true"] { background: var(--dark); color: var(--onDark); border-color: var(--dark); }
.chip[aria-pressed="true"] em { color: color-mix(in srgb, var(--onDark) 70%, transparent); }
.chip.must[aria-pressed="true"] { background: #E2604A; border-color: #E2604A; color: #fff; }
.chip .ti svg { width: 12px; height: 12px; display: block; color: #E2604A; }
.chip.must[aria-pressed="true"] .ti svg { color: #fff; }
.status { display: flex; align-items: center; gap: 14px; flex-wrap: wrap; font-size: 14px; color: var(--muted); font-weight: 700; }
.linkbtn { border: 0; background: none; padding: 0; color: var(--accent); font-weight: 800; cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }

/* sections + cards */
.sec { margin-top: 30px; }
.sechead { display: flex; align-items: center; gap: 16px; margin-bottom: 14px; }
.secicon { width: 70px; height: 70px; border-radius: 50%; background: var(--t); border: 2px solid var(--c); flex: none; display: flex; align-items: center; justify-content: center; }
.secicon svg { width: 48px; height: 48px; }
.sechead .jp { font-family: var(--jpf); font-weight: 700; font-size: 12px; letter-spacing: .3em; color: color-mix(in srgb, var(--c) 80%, var(--ink)); }
.sechead h2 { font-size: 30px; color: color-mix(in srgb, var(--c) 82%, var(--ink)); }
.lead { margin: 2px 0 0; color: var(--soft); font-family: var(--display); font-size: 16px; line-height: 1.35; }
.ahead { display: flex; align-items: baseline; justify-content: space-between; gap: 10px; flex-wrap: wrap; border-bottom: 2px dashed var(--line); padding-bottom: 8px; margin-bottom: 14px; }
.ahead h2 { font-size: 24px; }
.ahead span { font-size: 13.5px; font-weight: 700; color: var(--muted); }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(290px, 1fr)); gap: 14px; }

.card { display: flex; gap: 12px; background: var(--surface); border: 1.5px solid var(--line); border-radius: var(--r); padding: 16px 16px 16px 14px;
  box-shadow: 0 5px 0 color-mix(in srgb, var(--c) 20%, var(--bg)); min-width: 0; transition: opacity .2s; }
.num { flex: none; width: 32px; height: 32px; border-radius: 50%; background: var(--c); color: #fff; font-family: var(--display); font-weight: 600;
  font-size: 15px; display: flex; align-items: center; justify-content: center; font-variant-numeric: tabular-nums; }
.cbody { flex: 1; min-width: 0; display: flex; flex-direction: column; }
.card h3 { font-size: 19px; padding-top: 3px; }
.meta { font-size: 13.5px; color: var(--muted); font-weight: 700; margin-top: 2px; }
.meta .dot { color: var(--c); }
.catlbl { display: none; color: color-mix(in srgb, var(--c) 82%, var(--ink)); }
#byArea .catlbl { display: inline; }
.tags { display: flex; flex-wrap: wrap; gap: 5px; margin-top: 8px; }
.tag { display: inline-flex; align-items: center; gap: 4px; font-size: 12px; font-weight: 800; padding: 2px 9px; border-radius: 99px; background: var(--chip); color: var(--soft); }
.tag.must { background: #E2604A; color: #fff; }
.ti svg { width: 11px; height: 11px; display: block; }
.card p { margin: 9px 0 14px; font-size: 15px; }
.btns { display: flex; gap: 8px; flex-wrap: wrap; margin-top: auto; }
.btn { display: inline-flex; align-items: center; gap: 6px; background: var(--c, var(--dark)); color: #fff; font-family: var(--display); font-weight: 500;
  font-size: 14.5px; padding: 7px 15px; border-radius: 99px; text-decoration: none; border: 1.5px solid var(--c, var(--dark)); }
.btn:hover { filter: brightness(1.06); }
.btn.ghost { background: transparent; color: color-mix(in srgb, var(--c) 82%, var(--ink)); }
.box.dark .btn { background: var(--sun); border-color: var(--sun); color: #3A2E2A; }
.bi svg { width: 15px; height: 15px; display: block; }
.card.flash { animation: flash 1.4s ease-out; }
@keyframes flash { 0%, 30% { outline: 3px solid var(--c); outline-offset: 3px; } 100% { outline: 3px solid transparent; outline-offset: 8px; } }
.empty { margin-top: 28px; padding: 26px; text-align: center; border: 2px dashed var(--line); border-radius: var(--r); color: var(--muted); font-weight: 700; }

/* map */
.mapcol { position: sticky; top: 84px; }
.mapbox { background: var(--surface); border: 1.5px solid var(--line); border-radius: var(--r); padding: 14px; }
.mapbox summary { font-family: var(--display); font-weight: 600; font-size: 19px; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }
.mapbox summary::-webkit-details-marker { display: none; }
.mapbox summary span { font-family: var(--body); font-size: 13px; font-weight: 700; color: var(--muted); }
.mapbox summary::after { content: "▾"; font-size: 14px; color: var(--muted); transition: transform .2s; margin-left: 8px; }
.mapbox:not([open]) summary::after { transform: rotate(-90deg); }
.map { width: 100%; height: auto; display: block; margin-top: 10px; max-height: calc(100vh - 190px); }
.map .mbg { fill: var(--surface2); stroke: var(--line); }
.map .mgrid { fill: var(--mapgrid); }
.map .mlead, .map .mscale { stroke: var(--ink); }
.map .manchor { fill: var(--ink); }
.map .mhotel { fill: #3A2E2A; stroke: var(--ink); stroke-width: .4; }
.map .mpin { stroke: var(--surface2); }
.map .area { font-family: var(--display); font-weight: 600; font-size: 2.6px; letter-spacing: .12em; fill: var(--maplbl); }
.map .pinnum { font-family: var(--display); font-weight: 600; font-size: 3.1px; fill: #fff; pointer-events: none; }
.map .hotel { font-size: 3.6px; fill: #F7B267; }
.map .hotellbl { font-family: var(--display); font-size: 3.4px; fill: var(--ink); font-weight: 600; }
.map .far { font-family: var(--display); font-size: 2.8px; font-weight: 500; fill: var(--ink); }
.map .scale { font-family: var(--display); font-size: 2.6px; fill: var(--muted); }
.map a { cursor: pointer; transition: opacity .2s; }
.map a:hover .mpin { stroke: var(--ink); }
.map a.dim { opacity: .16; }
.mapnote { font-size: 13px; color: var(--muted); margin: 8px 2px 0; }

/* later */
.later { margin-top: 56px; }
.later > h2 { font-size: 30px; }
.later > p { color: var(--soft); margin: 4px 0 16px; }
.latgrid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 14px; }
.lat { background: var(--surface); border: 1.5px dashed color-mix(in srgb, var(--c) 55%, var(--line)); border-radius: var(--r); padding: 18px; min-width: 0; }
.latjp { font-family: var(--jpf); font-weight: 700; font-size: 13px; letter-spacing: .3em; color: color-mix(in srgb, var(--c) 82%, var(--ink)); }
.lat h3 { font-size: 21px; margin-top: 2px; }
.latd { font-weight: 800; font-size: 14px; font-variant-numeric: tabular-nums; }
.latn { color: var(--muted); font-size: 14px; margin-top: 4px; }
.soon { display: inline-block; margin-top: 12px; font-size: 12px; font-weight: 800; padding: 2px 10px; border-radius: 99px; background: color-mix(in srgb, var(--c) 16%, var(--surface)); color: color-mix(in srgb, var(--c) 82%, var(--ink)); }
footer { margin: 50px 0 40px; text-align: center; color: var(--muted); font-size: 13.5px; font-weight: 700; }

@media (max-width: 1020px) {
  .planner { grid-template-columns: minmax(0, 1fr); }
  .mapcol { position: static; order: -1; }
  .map { max-height: none; max-width: 460px; margin-inline: auto; }
  .latgrid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .basics { grid-template-columns: 1fr 1fr; }
  .basics .how { grid-column: 1 / -1; }
}
@media (max-width: 680px) {
  .hero { grid-template-columns: minmax(0, 1fr); border-radius: 24px; }
  .hero .txt { padding: 28px 22px 4px; }
  .hero .art { max-height: 230px; overflow: hidden; }
  .basics { grid-template-columns: minmax(0, 1fr); }
  .brand span { display: none; }
  .grid { grid-template-columns: minmax(0, 1fr); }
  .ctrlhead h2 { font-size: 26px; }
  .sechead h2 { font-size: 26px; }
  .secicon { width: 58px; height: 58px; } .secicon svg { width: 40px; height: 40px; }
  .latgrid { grid-template-columns: minmax(0, 1fr); }
}
@media (prefers-reduced-motion: reduce) { * { transition: none !important; animation: none !important; } html { scroll-behavior: auto; } }
'''


def prefix_sel(sel):
    out = []
    for s in sel.split(","):
        s = s.strip()
        if not s: continue
        if s in (":root", "body"): out.append(R)
        elif s == "*": out.extend([R, f"{R} *"])
        elif s == "html": continue
        elif s.startswith(":root"): out.append(R + s[5:])
        elif s.startswith("#jp-") or s.startswith("#"): out.append(f"{R} {s}")
        else: out.append(f"{R} {s}")
    return ", ".join(out)


def scope(block):
    res, i, n = [], 0, len(block)
    while i < n:
        j = block.find("{", i)
        if j < 0: res.append(block[i:]); break
        head = block[i:j]
        # find matching brace
        depth, k = 1, j + 1
        while depth:
            if block[k] == "{": depth += 1
            elif block[k] == "}": depth -= 1
            k += 1
        body = block[j + 1:k - 1]
        # keep comments before the selector untouched
        cm = ""
        while "/*" in head and "*/" in head:
            a, b = head.index("/*"), head.index("*/") + 2
            cm += head[a:b] + "\n"; head = head[:a] + head[b:]
        h = head.strip()
        if h.startswith("@media"):
            res.append(f"{cm}{h} {{{scope(body)}}}\n")
        elif h.startswith("@keyframes"):
            res.append(f"{cm}{h} {{{body}}}\n")
        else:
            sel = prefix_sel(h)
            if sel: res.append(f"{cm}{sel} {{{body}}}\n")
        i = k
    return "".join(res)



RESET = f'''
/* Defensive reset: stop the Squarespace theme's type styles leaking in */
{R} :where(h1, h2, h3, p, a, span, div, b, em, i, small, button, label, input, summary, details, nav, header, section, article, aside, main, footer) {{
  font-family: inherit; letter-spacing: normal; text-transform: none; text-decoration: none; color: inherit; line-height: inherit;
  margin: 0; padding: 0; border: 0; background: none; box-shadow: none; font-size: inherit; font-weight: inherit; text-align: inherit; max-width: none; }}
{R} {{ text-align: left; isolation: isolate; }}
{R} b {{ font-weight: 800; }}
{R} h1, {R} h2, {R} h3 {{ line-height: 1.12; }}
{R} .bar {{ position: static; }}
{R} .mapcol {{ top: 110px; }}
{R} svg text {{ letter-spacing: normal; text-transform: none; }}
'''


def scoped_css():
    css = BASE_CSS
    # the original dark blocks are dropped here; build_site.py adds its own dark mode for the GitHub page
    css = re.sub(r'@media \(prefers-color-scheme: dark\) \{ :root:not\(\[data-theme="light"\]\) \{.*?\} \}\n', '', css, flags=re.S)
    css = re.sub(r':root\[data-theme="dark"\] \{.*?\}\n', '', css, flags=re.S)
    css = css.replace("@keyframes flash", "@keyframes jp26flash").replace("animation: flash", "animation: jp26flash")
    css = css.replace("\nfooter {", "\n.foot {")
    css = scope(css)
    for idn in ["byArea", "byType"]:
        css = css.replace(f"#{idn}", f"#jp-{idn}")
    return RESET + css
