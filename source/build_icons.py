"""Builds the site icons (favicon) in the repo root:
    favicon.svg            used by modern browsers
    favicon-32.png         fallback for older browsers
    apple-touch-icon.png   180x180, used when the page is saved to a phone's home screen

    python3 source/build_icons.py
The design: a red torii in front of an orange sun, on the guide's cream colour.
"""
import os
from playwright.sync_api import sync_playwright

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INK = "#3A2E2A"

SVG = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
  <rect width="64" height="64" rx="14" fill="#FFE9D2"/>
  <circle cx="32" cy="43" r="11" fill="#F7B267"/>
  <path d="M7 15 Q32 8 57 15 L55 22 Q32 16 9 22Z" fill="#D9483B" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
  <rect x="12" y="28" width="40" height="5.5" rx="1" fill="#D9483B" stroke="{INK}" stroke-width="2.6" stroke-linejoin="round"/>
  <path d="M18 20 L16 56 M46 20 L48 56" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>
  <path d="M18 20 L16 56 M46 20 L48 56" stroke="#D9483B" stroke-width="4" stroke-linecap="round"/>
</svg>
'''


def build():
    open(os.path.join(REPO, "favicon.svg"), "w").write(SVG)
    with sync_playwright() as pw:
        b = pw.chromium.launch()
        for name, size in (("favicon-32.png", 32), ("apple-touch-icon.png", 180)):
            pg = b.new_page(viewport={"width": size, "height": size})
            svg = SVG
            if name.startswith("apple"):   # phones add their own rounded corners, so fill the square
                svg = svg.replace('rx="14"', 'rx="0"')
            pg.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg width={size} height={size} ", 1)}</body></html>')
            pg.screenshot(path=os.path.join(REPO, name), omit_background=True)
        b.close()
    print("favicon.svg, favicon-32.png, apple-touch-icon.png written")


if __name__ == "__main__":
    build()
