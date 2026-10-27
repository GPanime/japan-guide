"""Autumn leaves forecast for each stop. build_site.py draws it as a timeline in every tab and adds a line to matching cards.

How to refresh it (details in docs/GUIDE.md, "Autumn leaves forecast"):
  1. Open the Weathernews spot pages (weathernews.jp/koyo/area/kinki/ lists them by prefecture).
     Each page says 見頃予想 "見頃 X月Y日頃〜" (peak from) and "落葉はじめ X月Y日頃" (leaves start to fall).
  2. Update the "peak" and "fall" dates below, and CHECKED.
  3. Rebuild. The stay badges (at peak, still colouring...) are worked out from the dates.

SPOTS[city] lists forecast spots, in the order shown: (name, peak from "M/D", falling from "M/D").
CARDS[city] links a card (by its name in data.py) to a spot: (spot name, estimate). estimate=False when the forecast is for
that exact place; otherwise a short text such as "Eikando nearby", shown as "estimate from Eikando nearby".
A spot with no linked card is drawn as "nearby, not on our list".
"""
import datetime as _dt

YEAR = 2026
CHECKED = "Oct 27, 2026"
START, END = "11/1", "12/20"          # the chart's date range

SOURCES = [
    ("Weathernews autumn leaves forecast (Kinki)", "https://weathernews.jp/koyo/area/kinki/"),
    ("Japan Meteorological Agency: usual autumn leaf dates", "https://www.data.jma.go.jp/sakura/data/phn_014.html"),
    ("Kyoto City: autumn leaves reports (from Oct 30)", "https://ja.kyoto.travel/flower/momiji/"),
]

# the days we are there (or could go, for optional stops): (label, first day, last day)
STAYS = {
    "osaka": [("Our stay", "11/16", "11/20")],
    "wakayama": [("Our stop", "11/20", "11/20")],
    "shirahama": [("Our stay", "11/20", "11/23")],
    "kyoto": [("Stay 1", "11/23", "11/27"), ("Stay 2", "11/29", "12/2")],
    "nara": [("Osaka", "11/17", "11/19"), ("Kyoto 1", "11/24", "11/26"), ("Kyoto 2", "11/30", "12/1")],   # days we could go, from each base
    "hikone": [("Our stay", "11/27", "11/29")],
}

VERDICT = {
    "osaka": "Still a bit early. Osaka Castle Park and Expo Park are forecast to reach peak around Nov 19-20, our last days here. Expect colour starting rather than full peak.",
    "wakayama": "Not the right time in the city. The garden at Wakayama Castle peaks from about Dec 2. Koyasan, up in the mountains, will already be past peak by Nov 20.",
    "shirahama": "Not a leaves stop. The coast stays green, and the nearest forecast spots inland peak after we leave.",
    "kyoto": "The best timing of the trip. Most temples in the city are forecast to peak from about Nov 21-24, so both stays should be at or near peak. Mount Hiei comes earlier and will be past peak by the second stay.",
    "nara": "Go early. Nara Park is forecast to peak from Nov 11 and start falling from Nov 30, so a day trip from Osaka or early in the first Kyoto stay is best.",
    "hikone": "Peak is just arriving. Genkyū-en garden below the castle is forecast to peak from Nov 28, during our stay, and its evening light-up runs until Nov 29.",
}

SPOTS = {
    "osaka": [("Expo '70 Commemorative Park", "11/19", "12/8"), ("Osaka Castle Park", "11/20", "12/10"),
              ("Katsuo-ji, Minoh", "11/21", "12/9"), ("Minoo Park", "11/24", "12/9")],
    "wakayama": [("Koyasan", "11/4", "11/16"), ("Momijidani garden, Wakayama Castle", "12/2", "12/19"),
                 ("Negoro-ji", "12/3", "12/14")],
    "shirahama": [("Kumano Nachi Taisha", "11/26", "12/6"), ("Kozagawa gorge", "12/2", "12/12")],
    "kyoto": [("Enryaku-ji, Mount Hiei", "11/8", "11/26"), ("Ōhara Sanzen-in", "11/15", "12/3"),
              ("Jōjakkō-ji", "11/21", "12/8"), ("Hiyoshi Taisha, Sakamoto", "11/21", "12/4"),
              ("Tōfuku-ji", "11/22", "12/9"), ("Nanzen-ji", "11/23", "12/7"), ("Eikandō", "11/23", "12/5"),
              ("Arashiyama", "11/23", "12/9"), ("Kiyomizu-dera", "11/24", "12/9"),
              ("Kyoto Gyoen ginkgo trees", "11/25", "12/5"), ("Ryōan-ji", "11/27", "12/14")],
    "nara": [("Nara Park", "11/11", "11/30"), ("Hase-dera", "11/17", "12/4"), ("Shōryaku-ji", "11/19", "12/7"),
             ("Chōgaku-ji", "11/21", "12/7"), ("Murō-ji", "11/24", "12/9")],
    "hikone": [("Koto Sanzan (Hyakusai-ji)", "11/12", "12/2"), ("Eigen-ji", "11/11", "11/29"),
               ("Genkyū-en, Hikone Castle", "11/28", "12/11"), ("Kyorinbo", "11/30", "12/14")],
}

CARDS = {
    "osaka": {"Osaka Castle": ("Osaka Castle Park", False)},
    "wakayama": {"Wakayama Castle": ("Momijidani garden, Wakayama Castle", False), "Koyasan": ("Koyasan", False)},
    "kyoto": {
        "Mount Hiei": ("Enryaku-ji, Mount Hiei", False),
        "Kurama Onsen": ("Ōhara Sanzen-in", "Ōhara, also in the northern hills"),
        "Jōjakkō-ji": ("Jōjakkō-ji", False),
        "Daihikaku Senkō-ji": ("Arashiyama", "Arashiyama"),
        "Arashiyama Yusai-Tei": ("Arashiyama", "Arashiyama"),
        "Former Chikurin-in": ("Hiyoshi Taisha, Sakamoto", "Hiyoshi Taisha next door"),
        "Tōfuku-ji": ("Tōfuku-ji", False),
        "Nanzen-ji": ("Nanzen-ji", False),
        "Ginkaku-ji": ("Eikandō", "Eikandō, on the same hillside"),
        "Anraku-ji": ("Eikandō", "Eikandō, on the same hillside"),
        "Kiyomizu-dera": ("Kiyomizu-dera", False),
        "Honnō-ji": ("Kyoto Gyoen ginkgo trees", "the ginkgo trees at Kyoto Gyoen"),
        "Kinkaku-ji": ("Ryōan-ji", "Ryōan-ji nearby"),
    },
    "hikone": {"Hikone Castle": ("Genkyū-en, Hikone Castle", False), "Kyorinbo": ("Kyorinbo", False)},
}


def day(s):
    m, d = s.split("/")
    return _dt.date(YEAR, int(m), int(d))


def fmt(d):
    return f"{d.strftime('%b')} {d.day}"


def fmt_range(a, b):
    if a == b: return fmt(a)
    return f"{fmt(a)}-{b.day}" if a.month == b.month else f"{fmt(a)}-{fmt(b)}"


STAY_TITLE = {"nara": "Days we could go from"}   # legend wording for the shaded days, when "our stay" doesn't fit


def status(peak, fall, a, b):
    """What the leaves look like during the days a..b (dates). Returns (css class, label)."""
    if b < peak: return "early", "still colouring"
    if a >= fall: return "late", "leaves falling"
    if peak > a: return "peak", f"peak from {fmt(peak)}"
    if fall <= b: return "peak", f"peak, falling from {fmt(fall)}"
    return "peak", "at peak"
