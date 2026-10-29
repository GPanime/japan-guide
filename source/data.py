import urllib.parse

HOTEL = {"name": "Best Western Plus Hotel Fino Osaka Kitahama", "lat": 34.6902, "lon": 135.5069,
         "maps": "https://www.google.com/maps/search/?api=1&query=Best+Western+Plus+Hotel+Fino+Osaka+Kitahama"}

def photos(q):
    return "https://www.google.com/search?tbm=isch&q=" + urllib.parse.quote_plus(q)

CATS = {
    "must":   {"title": "Must-eats",  "jp": "絶対", "color": "#E2604A", "tint": "#FDE7E1", "icon": "curry",
               "lead": "The two places not to miss."},
    "food":   {"title": "More food",  "jp": "ごはん", "color": "#E8952F", "tint": "#FDF0DC", "icon": "takoyaki",
               "lead": "Curry, burgers, takoyaki and fried-everything, for whatever the mood is."},
    "sweets": {"title": "Sweets",     "jp": "甘味", "color": "#D2648E", "tint": "#FBE5EE", "icon": "dango",
               "lead": "Cake, matcha and Japanese-style desserts."},
    "coffee": {"title": "Coffee",     "jp": "珈琲", "color": "#9A6B4B", "tint": "#F4E9DF", "icon": "coffee",
               "lead": "Osaka does great coffee. Honmachi has three of these within a few minutes' walk."},
    "drinks": {"title": "Drinks",     "jp": "乾杯", "color": "#8A5AA6", "tint": "#F1E8F6", "icon": "glass",
               "lead": "All three are in Namba, a few minutes apart, so they work as a little bar crawl."},
    "onsen":  {"title": "Hot springs", "jp": "温泉", "color": "#6C7FC4", "tint": "#E8ECF8", "icon": "onsen",
               "lead": "Hot spring baths."},
    "trips":  {"title": "Day trips",  "jp": "日帰り", "color": "#3E8FA8", "tint": "#E1F0F5", "icon": "train",
               "lead": "Further afield."},
    "sights": {"title": "Sights",     "jp": "名所", "color": "#4F9A6A", "tint": "#E3F2E7", "icon": "torii",
               "lead": "Nightlife, a castle, and two half-day trips out of the city."},
}

P = [
 # cat, name, area, km, tags, desc, maps, photo query, lat, lon
 ("must","Go Go Curry Tsutenkaku","Shinsekai","4.2 km",["Must-go"],
  "The best curry ever. Kushikatsu Shinsekai is round the corner for a second round later.",
  "https://maps.app.goo.gl/mSh6H6RMG7RDmiTG8","Go Go Curry Tsutenkaku Osaka",34.6521,135.5057),
 ("must","MENSTYLE TANIMOTOKE","Honmachi","1.1 km · walkable",["Must-go"],
  "Amazing ramen. aoma and Notequal coffee are a couple of minutes away, so it pairs with a coffee stop.",
  "https://maps.app.goo.gl/NhvNePS4b8ttajJi9","MENSTYLE TANIMOTOKE Honmachi ramen",34.6812,135.5014),
 ("food","NICO CAFE","Dōjima","1.1 km · walkable",[],
  "Small restaurant run by a husband and wife, mostly locals. Famous for its curry, which is really good and a bit spicy. There's also a soup we haven't tried. Very friendly, and last time came with a free coffee.",
  "https://maps.app.goo.gl/Jb78hnzRPkMNrCUb8","NICO CAFE Osaka curry",34.6975,135.4991),
 ("food","Craft Burger co.","Horie, by Amerikamura","2.0 km",[],
  "American-style burgers in the fashion district. A classic burger, but ultra tasty. Good for when the mood strikes. Saturdays NYC is nearby.",
  "https://maps.app.goo.gl/JrwxHjaBxJ9EccBL8","Craft Burger co. Kitahorie",34.6741,135.4963),
 ("food","Kushikatsu Shinsekai","Shinsekai","4.4 km",["Late night"],
  "Kushikatsu is Osaka's deep-fried-everything-on-a-skewer specialty. Good for late-night snacks and drinks; Go Go Curry is round the corner.",
  "https://maps.app.goo.gl/VtEc4GhdFGU9hUdx9","Kushikatsu Shinsekai Osaka",34.6510,135.5061),
 ("food","Takoyaki Umaiya","Tenma","2.0 km",["Quick bite"],
  "One of the oldest takoyaki shops in Osaka, featured on a Netflix show. Pretty tasty. Right next to Roji Cafe.",
  "https://maps.app.goo.gl/Zspo5bN73neMdk7N9","Takoyaki Umaiya Osaka",34.7076,135.5105),
 ("food","Takocha","Umeda","1.9 km",["Quick bite","Outdoors"],
  "Small takoyaki stall run by a friendly uncle. A quick bite if you're in the area.",
  "https://maps.app.goo.gl/PnMj9Jjo5gAx1RqG7","Takocha takoyaki Umeda",34.7067,135.5002),
 ("food","OYASUMI ICE & HOTEL","Namba","2.6 km",["Quick bite"],
  "A hotel with tasty matcha ice cream in the lobby. Next door to Manmanki.",
  "https://maps.app.goo.gl/Mz9ySLd1bpXPP1hc6","OYASUMI ICE HOTEL Namba matcha",34.6676,135.4994),
 ("food","Marukome","Kishinosato, south of Shinsekai","5.9 km",[],
  "Famous oden restaurant we haven't tried yet, one to satisfy curiosity. It's out of the way, so it's easiest combined with a Shinsekai day.",
  "https://maps.app.goo.gl/8SopKeSroLo64Nnd9","Marukome oden Osaka",34.6381,135.4963),
 ("food","Hanakujira honten","Fukushima","1.9 km",[],
  "Another famous oden restaurant. Not tried yet, but high on the list. Much closer than Marukome, so it's the easier oden pick.",
  "https://maps.app.goo.gl/hRHXdwzPzJUmRGfN9","Hanakujira honten oden Osaka",34.6946,135.4871),
 ("coffee","aoma coffee","Honmachi","1.1 km · walkable",["Must-go"],
  "Small and trendy. The best latte in Osaka.",
  "https://maps.app.goo.gl/a6caNjRxmH4DXR44A","aoma coffee Osaka",34.6814,135.5024),
 ("coffee","Roji Cafe","Tenma","2.0 km",["Low energy","Photo spot"],
  "Absolutely amazing coffee shop hidden in an alley. No talking allowed, so it's quiet and very old-style. Great for photos, and the owner allows them. Takoyaki Umaiya is next door.",
  "https://maps.app.goo.gl/oquAxfsyoLKZoGQy5","Roji Cafe Tenma Osaka",34.7081,135.5102),
 ("coffee","Notequal Coffee","Honmachi","1.1 km · walkable",[],
  "Trendy and ultra popular with locals. A couple of minutes from aoma.",
  "https://maps.app.goo.gl/5REqAHeuFbHpBB2NA","Notequal Coffee Osaka",34.6809,135.5036),
 ("coffee","Melbourne Coffee Senba","Semba","1.4 km · walkable",[],
  "Australian-style coffee with a western breakfast. Highly recommended by foreign photographers for the food. A good breakfast pick.",
  "https://maps.app.goo.gl/XkVRKpE85pUuTRae8","Melbourne Coffee Senba Osaka",34.6779,135.5020),
 ("coffee","Mole & Hosoi Coffees","Kitahama","0.5 km · closest to hotel",["Photo spot"],
  "Coffee in a historic European-style building. Go for the vibes if you're nearby.",
  "https://maps.app.goo.gl/Fvj66Dr9hDiCtFwt9","Mole Hosoi Coffees Kitahama",34.6891,135.5018),
 ("coffee","SHIMATONERIKO","Tennōji","5.1 km",["Queue"],
  "Healthy-style brunch: tasty but small portions, and good coffee. Very popular with Japanese visitors, so expect a short queue.",
  "https://maps.app.goo.gl/1YsWrF6HHS12GM6N7","SHIMATONERIKO coffee roaster Osaka",34.6447,135.5151),
 ("coffee","Saturdays NYC","Minamisenba","1.8 km",[],
  "A clothing store with a coffee shop inside. Worth a look if you're in the area; Craft Burger is nearby.",
  "https://maps.app.goo.gl/Ea2XRYr1iyjBxmsu5","Saturdays NYC Osaka cafe",34.6756,135.4979),
 ("drinks","Manmanki","Namba","2.5 km",["Late night"],
  "Tiny izakaya bar with friendly, loud staff. The food is normal, but the drinks and vibes are amazing. OYASUMI ICE is next door.",
  "https://maps.app.goo.gl/5ox63xbe6cpLZXsg6","Manmanki Namba izakaya",34.6684,135.4995),
 ("drinks","Bar Seven","Namba","2.5 km",["Late night","Low energy"],
  "A quieter bar to chill with a late-night drink.",
  "https://maps.app.goo.gl/vPcRWdro36thTdjF6","Bar Seven Namba Osaka",34.6679,135.5018),
 ("drinks","Luv Wine Namba","Namba","2.8 km",["Low energy","Pricier"],
  "Small, chill wine bar, a bit fancier. Good for a casual quick drink on a lazy day.",
  "https://maps.app.goo.gl/Z6AciSS3z4qhoNPv9","Luv Wine Namba Osaka",34.6663,135.4989),
 ("sights","Ebisu Bridge & Dotonbori","Namba","2.4 km",["Late night","Outdoors"],
  "The centre of Osaka's nightlife and tourism. Worth going at least once. Very crowded and everything is overpriced, but a drink in a local bar while watching the night crowd is an experience.",
  "https://maps.app.goo.gl/WaDFD5NCBPPYQLx7A","Ebisubashi Dotonbori night",34.6691,135.5013),
 ("sights","Osaka Castle","Osaka Castle Park","1.8 km",["Outdoors","Photo spot"],
  "A decent park and good photos of the castle; inside is a museum, open during the day. Not a must.",
  "https://www.google.com/maps/search/?api=1&query=Osaka+Castle","Osaka Castle autumn",34.6873,135.5259),
 ("sights","Shitennō-ji","Tennōji","4.1 km",["Outdoors","Photo spot"],
  "The most famous temple in Osaka. Big and very photogenic. Worth going. Shinsekai and Go Go Curry are a short walk away.",
  "https://maps.app.goo.gl/C1XpHUcgMBRRREwk8","Shitennoji temple Osaka",34.6545,135.5165),
 ("sights","Shubodai","Ikeda, hills north of the city","17 km · half-day trip",["Must-go","Outdoors","Photo spot"],
  "A torii gate overlooking all of Osaka. An amazing viewpoint and high on the wish list. Best saved for a clear day.",
  "https://maps.app.goo.gl/g1hxcX8Ah5Q3S4nc9","Shubodai Ikeda torii view",34.8318,135.4272),
 ("sights","Ishikiri Tsurugiya Jinja","Higashiōsaka, east of the city","13 km · half-day trip",["Low energy","Outdoors"],
  "A nice shrine on a hill in the suburbs, with an old-style shopping street. Not a must, but a calm, chill spot if you're out that way.",
  "https://maps.app.goo.gl/dgJnc7e3JwWpEw2HA","Ishikiri Tsurugiya Shrine",34.6823,135.6463),
]

AREAS = [
 ("Kitahama / Dōjima", "0.5-1 km", ["Mole & Hosoi Coffees", "NICO CAFE"]),
 ("Honmachi / Semba", "1-1.5 km · walk", ["MENSTYLE TANIMOTOKE", "aoma coffee", "Notequal Coffee", "Melbourne Coffee Senba"]),
 ("Osaka Castle", "2 km", ["Osaka Castle"]),
 ("Tenma / Umeda", "2 km", ["Roji Cafe", "Takoyaki Umaiya", "Takocha"]),
 ("Fukushima", "2 km", ["Hanakujira honten"]),
 ("Horie / Shinsaibashi", "2 km", ["Craft Burger co.", "Saturdays NYC"]),
 ("Namba / Dotonbori", "2.5 km", ["Ebisu Bridge & Dotonbori", "Manmanki", "Bar Seven", "Luv Wine Namba", "OYASUMI ICE & HOTEL"]),
 ("Shinsekai / Tennōji", "4-6 km", ["Shitennō-ji", "Go Go Curry Tsutenkaku", "Kushikatsu Shinsekai", "SHIMATONERIKO", "Marukome"]),
 ("Half-day trips", "13-17 km", ["Shubodai", "Ishikiri Tsurugiya Jinja"]),
]
OUTLIERS = ["Shubodai", "Ishikiri Tsurugiya Jinja"]

TAGS = [
 ("Must-go", "favourites, don't skip"),
 ("Quick bite", "snack or short stop"),
 ("Late night", "good after dark"),
 ("Low energy", "sit down and chill"),
 ("Outdoors", "better on a dry day"),
 ("Photo spot", "bring the camera"),
 ("Autumn leaves", "has a leaves forecast"),
 ("Queue", "expect a short wait"),
 ("Pricier", "a bit more expensive"),
]


# ================= cities =================
import math

def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    d = 2 * 6371 * math.asin(math.sqrt(math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2))
    return d

OSAKA = dict(
    key="osaka", name="Osaka", jp="大阪", stop=1, dates="Nov 16-20", nights="4 nights",
    sub="curry, coffee, takoyaki &amp;<br>a torii with a view", art="osaka",
    hotel=HOTEL, hotel_name="Best Western Plus Hotel Fino Osaka Kitahama", hotel_note="by Kitahama station",
    day1=("Day 1 · Mon Nov 16", "Late arrival, so just a late dinner. Easiest is something near the hotel. With energy left, the Namba bars are about 2.5 km away, a short taxi ride."),
    planner="Days 2-4", places=P, areas=AREAS,
    leads={k: v["lead"] for k, v in CATS.items()}, icons={},
    map=dict(k=17.0, W=100.0, H=150.0, scale_km=1.0, scale_lbl="1 km", ycenter_shift=4,
             labels=[("UMEDA · TENMA", 34.7080, 135.4945, "end"), ("KITAHAMA", 34.6935, 135.5130, "start"),
                     ("HONMACHI", 34.6830, 135.4925, "end"), ("HORIE", 34.6745, 135.4915, "end"), ("FUKUSHIMA", 34.6975, 135.4871, "middle"),
                     ("NAMBA", 34.6640, 135.4920, "end"), ("SHINSEKAI", 34.6505, 135.5000, "end"),
                     ("TENNŌJI", 34.6430, 135.5195, "start"), ("KISHINOSATO", 34.6370, 135.4990, "start"),
                     ("CASTLE", 34.6905, 135.5262, "middle")],
             outliers=[("Shubodai", 27, "↑ Shubodai · 17 km north"), ("Ishikiri Tsurugiya Jinja", 70, "Ishikiri · 13 km east →")]),
)

SH_HOTEL = {"name": "Dormitory Sandanya Guesthouse", "lat": 33.6662113, "lon": 135.3368365,
            "maps": "https://maps.app.goo.gl/6sgeUW4YiEcYHqxr9"}

def dist(lat, lon, hotel=SH_HOTEL):
    d = km((hotel["lat"], hotel["lon"]), (lat, lon))
    s = f"{d:.1f} km"
    return s + (" · walk" if d < 1.2 else "")

SH_RAW = [
 ("food", "Tsumugi Cafe", "By the guesthouse", [],
  "A highly rated local cafe. Not tried yet. A few minutes' walk from the guesthouse, so an easy breakfast or lunch.",
  "https://maps.app.goo.gl/cVsnAEcKvUkGaXHL8", "Tsumugi Cafe Shirahama", 33.668306, 135.334818),
 ("food", "Miyuki Sushi", "Near Saki-no-yu", [],
  "An interesting sushi restaurant we haven't tried yet. One to check out for dinner.",
  "https://maps.app.goo.gl/1zX18KPgxKSMuwFJ8", "Miyuki Sushi Shirahama", 33.6750843, 135.3402668),
 ("sights", "Senjojiki Rock Plateau", "Shirahama coast", ["Outdoors", "Photo spot"],
  "A famous scenic spot. Wide, flat rock runs down to the sea, with big ocean views. The name means 1,000 tatami mats, after its size.",
  "https://maps.app.goo.gl/X7obhxQpo7ApiCdNA", "Senjojiki Shirahama", 33.6707012, 135.3304584),
]
SH_RAW += [
 ('must', 'Dakishimetai', 'Near Saki-no-yu', ['Must-go'],
  'Must go. Tasty ramen, and the big shrimp ramen is the one we want. Their signature bowl is a sea bream tantanmen. Inside the Key Terrace Hotel Seamore. Lunch 11:00-15:00, dinner 17:00-22:00.',
  'https://maps.google.com/?cid=10240352576288176698', 'Dakishimetai ramen Shirahama', 33.674535999999996, 135.33741179999998),
 ('must', 'Yakiniku Man', 'Shirahama town', ['Must-go'],
  'Must go for Japanese BBQ (yakiniku). Opens for dinner from 16:30. Called 南紀白浜 焼肉萬 on the map.',
  'https://maps.google.com/?cid=4356415629714341682', '南紀白浜 焼肉萬', 33.6832646, 135.3485744),
 ('must', 'Toretore Market', 'Katata, east of town', ['Must-go', 'Quick bite'],
  'Must go. The whole tuna cutting show is usually around 11:00, but the time can shift, so check the board. Fresh tuna, seafood and wagyu, with BBQ seats where you can grill what you buy. Go in the morning and take food home too. A short taxi ride from the guesthouse.',
  'https://maps.google.com/?cid=7938307802199390379', 'Toretore Market tuna cutting', 33.6813502, 135.3752515),
 ('food', 'Ikesu Warouda / Sushi Yata', 'Near Saki-no-yu', ['Book ahead', 'Photo spot'],
  'Omakase or set meals with an amazing sunset and sea view. Needs a reservation. In the same hotel building as Dakishimetai.',
  'https://maps.google.com/?cid=10848447305798194294', 'Ikesu Warouda Sushi Yata Shirahama', 33.675353099999995, 135.3373919),
 ('food', 'Ban-ya', "Fisherman's Wharf", ['Quick bite'],
  "Cheap sashimi where the locals go, inside Fisherman's Wharf Shirahama.",
  'https://maps.google.com/?cid=15270952934666379931', "Ban-ya Fisherman's Wharf Shirahama", 33.676940699999996, 135.3413859),
 ('food', 'Sumibi Dining Hayate', 'Shirahama town', [],
  'Charcoal-grilled skewers. Dinner from 17:30. Called 炭火ダイニング 颯 on the map.',
  'https://maps.google.com/?cid=14075486803131133320', '炭火ダイニング 颯 白浜', 33.6835692, 135.3502521),
 ('coffee', 'Mame no Yu', 'Shirahama town', ['Must-go'],
  'Must go for a coffee brunch: breakfast and specialty coffee from 8:00. Virtual Market, a clothing shop, is in the same row. Called 豆の湯 on the map.',
  'https://maps.google.com/?cid=3195587893017237390', '豆の湯 白浜 cafe', 33.6825212, 135.3463572),
 ('drinks', 'Popular Bar Chokyu', 'Shirahama town', ['Late night'],
  'A small izakaya for dinner with drinks, with grilled seafood at the counter. Opens at 16:00.',
  'https://maps.google.com/?cid=7785594314647488227', '大衆酒場 長久 白浜', 33.6795273, 135.34422469999998),
 ('onsen', 'Saki-no-Yu', 'On the rocks by the sea', ['Outdoors', 'Photo spot'],
  "A historic public hot spring right on the rocks, open to the sea. One we really want to try. Open 8:00-17:00, closed Wednesdays, which doesn't clash with our dates.",
  'https://maps.google.com/?cid=17602803442712138027', 'Sakinoyu Shirahama onsen', 33.676823999999996, 135.3369842),
 ('onsen', 'Hamachidori-no-yu Kaishu', 'Seaside hotel', ['Low energy'],
  'Our pick for a day-visit hot spring, in a seaside hotel. Check the day-visitor hours before going.',
  'https://maps.google.com/?cid=3390272157845678808', 'Hamachidori no yu Kaishu bath', 33.673034, 135.334343),
 ('sights', 'Ura-Senjojiki', 'Next to Senjojiki', ['Outdoors', 'Photo spot'],
  'The quieter rock shelf next to Senjojiki, a short walk from the guesthouse. Called 裏千畳敷 on the map.',
  'https://maps.google.com/?cid=12856806204964319956', '裏千畳敷 白浜', 33.6689484, 135.33135099999998),
 ('sights', 'Kumano Sansho Shrine', 'Shirahama town', [],
  "A local shrine in town, saved without a note. A quick stop if we're passing.",
  'https://maps.google.com/?cid=11663528559639994824', 'Kumano Sansho Shrine Shirahama', 33.6851069, 135.34242949999998),
]
SH_RAW += [
 ("trips", "Kumano Kodo Nakahechi", "Tanabe, inland", ["Outdoors", "Photo spot"],
  "The best-known route of the Kumano Kodo pilgrimage trails, through forested mountains. A short section makes a good half-day hike from Shirahama.",
  "https://maps.google.com/?cid=8946960721844952529", "Kumano Kodo Nakahechi", 33.7836, 135.5166),
]
SH_P = [(c, n, a, dist(la, lo), t, d, m, q, la, lo) for c, n, a, t, d, m, q, la, lo in SH_RAW]

SHIRAHAMA = dict(
    key="shirahama", name="Shirahama", jp="白浜", stop=2, dates="Nov 20-23", nights="3 nights",
    sub="sea views, sushi &amp;<br>rocks by the ocean", art="shirahama",
    hotel=SH_HOTEL, hotel_name="Dormitory Sandanya Guesthouse", hotel_note="about 800 m from Senjojiki",
    day1=("Getting around", "Most places are within about 2 km of the guesthouse. Toretore Market is about 4 km away, a short taxi ride."),
    planner="Options", places=SH_P,
    areas=[("By the guesthouse · Senjojiki", "under 1 km", ["Tsumugi Cafe", "Ura-Senjojiki", "Senjojiki Rock Plateau", "Hamachidori-no-yu Kaishu"]),
           ("Saki-no-yu & the harbour", "1-1.3 km", ["Dakishimetai", "Ikesu Warouda / Sushi Yata", "Miyuki Sushi", "Saki-no-Yu", "Ban-ya"]),
           ("Shirahama town", "1.5-2.3 km", ["Popular Bar Chokyu", "Mame no Yu", "Yakiniku Man", "Kumano Sansho Shrine", "Sumibi Dining Hayate"]),
           ("Toretore Market", "4 km", ["Toretore Market"]),
           ("Day trip · Kumano Kodo", "21 km", ["Kumano Kodo Nakahechi"])],
    leads={"must": "Ramen, BBQ and the tuna market.",
           "food": "Sushi with a sunset view, cheap local sashimi, skewers and a cafe.",
           "coffee": "Breakfast and specialty coffee.",
           "drinks": "An izakaya for dinner and drinks.",
           "onsen": "Shirahama is a hot spring town. One public bath right by the sea, and one hotel bath for a day visit.",
           "sights": "The rocky coast is the main event.",
           "trips": "The Kumano Kodo pilgrimage trails are inland from Shirahama. The Wakayama city options now have their own tab."},
    icons={"food": "sushi"}, titles={"food": "Food", "trips": "Day trip"},
    map=dict(k=34.0, W=100.0, H=118.0, scale_km=0.5, scale_lbl="500 m", ycenter_shift=10,
             labels=[("PACIFIC OCEAN", 33.6645, 135.3255, "start")],
             outliers=[("Kumano Kodo Nakahechi", 8, "Kumano Kodo 21 km →", "right"),
                       ("Toretore Market", 16, "Toretore 4 km →", "right")]),
)

KY_HOTEL = {"name": "Hotel ZIZI Horikawa Gojo", "lat": 34.9976817, "lon": 135.7540521,
            "maps": "https://maps.app.goo.gl/jgtEtLKyQvY8QCyL6"}

KY_HOTEL2 = {"name": "Kyoto Plaza Hotel Kintetsu Jujo", "lat": 34.9734786, "lon": 135.7472537,
             "maps": "https://maps.app.goo.gl/QCL8hgja5Wy7ZZxy6"}

def kdist(lat, lon, note=""):
    d1 = km((KY_HOTEL["lat"], KY_HOTEL["lon"]), (lat, lon))
    d2 = km((KY_HOTEL2["lat"], KY_HOTEL2["lon"]), (lat, lon))
    s = f"{d1:.1f} km / {d2:.1f} km"
    return s + (f" · {note}" if note else "")

KY_RAW = [
 ("must", "Ramen Mugyu Vol. 2", "Karasuma Takoyakushi", ["Must-go", "Queue"],
  "Amazing ramen with an amazing chicken broth. We've been before and it's a must-visit. There's always a queue.",
  "https://maps.app.goo.gl/MTMqmLb44jYt3tQr7", "Ramen Mugyu Kyoto chicken", 35.006548, 135.7602896, ""),
 ("must", "Rokkaku Ace", "Rokkaku, downtown", ["Must-go", "Book ahead", "Late night"],
  "A very famous izakaya. We couldn't get in last time, so it's a must-visit this trip. Needs a reservation.",
  "https://maps.app.goo.gl/t3BPCqP94pLCnFpY8", "Rokkaku Ace Kyoto izakaya", 35.0074364, 135.7638627, ""),
 ("food", "Kyogoku Kaneyo", "Shinkyogoku, downtown", [],
  "Unagi (grilled eel over rice). We've been before. Really tasty and pretty old school.",
  "https://maps.app.goo.gl/d1dSvUQgKdxh59pw8", "Kyogoku Kaneyo unagi Kyoto", 35.007592, 135.767949, ""),
 ("food", "Kitchen Gon Rokkaku", "Rokkaku, downtown", ["Low energy"],
  "Japanese-style western food. A good pick for something chill to eat when we're tired.",
  "https://maps.app.goo.gl/JHsjYDhMVoTa2JYR8", "Kitchen Gon Rokkaku Kyoto", 35.0072273, 135.7627796, ""),
 ("food", "Gyukatsu Kyoto Katsugyu", "Teramachi Kyogoku, downtown", ["Book ahead"],
  "Super famous local speciality: gyukatsu, a breaded and fried beef cutlet. Most likely needs a reservation.",
  "https://maps.app.goo.gl/pxXWHSLYfdYrQe2C8", "Gyukatsu Kyoto Katsugyu", 35.005403, 135.7669232, ""),
 ("food", "Kyo-Motsunabe Kamehachi", "Kiyamachi, downtown", ["Pricier", "Low energy"],
  "A famous nabe hotpot place. Expensive, but worth it on a cold day for a long, relaxing meal.",
  "https://maps.app.goo.gl/KH59QUEssErBdUuRA", "Kyo Motsunabe Kamehachi", 35.0072749, 135.7707854, ""),
 ("food", "Ten no Meshi Gion", "Gion", ["Pricier", "Queue"],
  "Ultra famous tempura restaurant. Very expensive and probably packed.",
  "https://maps.app.goo.gl/Qphf8UeRnZ5U9pX67", "Kyoto Tempura Ten no Meshi Gion", 35.0042282, 135.7745187, ""),
 ("sweets", "Second House Cake Works", "Higashinotoin", ["Quick bite"],
  "A famous western-style cake shop. Ramen Mugyu is around the corner.",
  "https://maps.app.goo.gl/3CBqHFL6P8rh8Zab6", "Second House Cake Works Kyoto", 35.0064319, 135.7609654, ""),
 ("sweets", "Micasadeco & Cafe", "Downtown", ["Quick bite"],
  "A pretty famous dessert place, Japanese style.",
  "https://maps.app.goo.gl/4L5zU4MjY3mS6PuR8", "Micasadeco Cafe Kyoto pancakes", 35.0058856, 135.7657151, ""),
 ("sweets", "Itoh Kyuemon Sabo", "Gion Shijo", ["Quick bite", "Low energy"],
  "A matcha sweets cafe. Yasaka Shrine is a short walk away.",
  "https://maps.app.goo.gl/qP44cdyMzwYrJ8hZA", "Itoh Kyuemon Gion Shijo matcha", 35.0036759, 135.7731794, ""),
 ("sights", "Kinkaku-ji", "Kita, northwest Kyoto", ["Must-go", "Photo spot"],
  "The Golden Pavilion. We couldn't make it last time, so it's a must-visit this trip.",
  "https://maps.app.goo.gl/C7yMTuzNasRxVTK87", "Kinkakuji autumn", 35.03937, 135.7292431, ""),
 ("sights", "Yasaka Shrine", "Gion", ["Late night", "Photo spot", "Outdoors"],
  "Right in the city. We've been here at night before and it's lit up, so it's great for night photos.",
  "https://maps.app.goo.gl/r2T89NW5XDg5C6Gn6", "Yasaka Shrine night", 35.0036559, 135.7785534, ""),
 ("sights", "Nanzen-ji", "Okazaki, east Kyoto", ["Outdoors", "Photo spot"],
  "A huge Buddhist temple. Should be good for autumn leaves photos.",
  "https://maps.app.goo.gl/42GvsGz7u1fjYyRs8", "Nanzenji autumn leaves", 35.0114138, 135.7944841, ""),
 ("sights", "Anraku-ji", "Shishigatani, east Kyoto", ["Outdoors", "Photo spot"],
  "A small, cute temple we saw in a travel video. Nice in the fall. It only opens on weekends and holidays in November, which on our dates means Mon Nov 23 (a public holiday) or Sun Nov 29.",
  "https://maps.app.goo.gl/98J73Gu88dbsEw5i9", "Anrakuji Shishigatani autumn", 35.0216167, 135.7966367, ""),
 ("sights", "Tōfuku-ji", "Higashiyama, south Kyoto", ["Outdoors", "Photo spot"],
  "A large, old temple. Should also be great for autumn photos.",
  "https://maps.app.goo.gl/J86VZzDy6UqLb7Jm8", "Tofukuji autumn leaves", 34.976025, 135.7737627, ""),
 ("sights", "Arashiyama Yusai-Tei", "Arashiyama", ["Photo spot", "Book ahead"],
  "An art gallery we saw in a travel video, super nice for photos. It was closed on our last trip. In the second half of November it's reservation only, with timed tickets bought online.",
  "https://maps.app.goo.gl/BxhAA4TK4mPumWgk7", "Arashiyama Yusai-tei gallery", 35.0141337, 135.6709556, ""),
 ("sights", "Jōjakkō-ji", "Arashiyama", ["Outdoors", "Photo spot"],
  "A temple in Arashiyama. Should be good for autumn leaves photos, and pairs with Yusai-Tei.",
  "https://maps.app.goo.gl/Zs3ALEwkemQo9Ury8", "Jojakkoji autumn", 35.0198102, 135.6686405, ""),
]
KY_RAW += [
 ("food", "Hikiniku to Come", "Gion side, by the Kamo River", ["Book ahead"],
  "Charcoal-grilled hamburg steak with fresh rice, a very popular spot. Seats go through paid online registration on TableCheck, so sort it out in advance. Closed Wednesdays.",
  "https://maps.google.com/?cid=5604413755966420161", "Hikiniku to Come Kyoto", 35.0051, 135.7746, ""),
 ("food", "Kunton Akutagawa", "Downtown", [],
  "Ramen built around smoked pork. A good second ramen pick after Mugyu.",
  "https://maps.google.com/?cid=13196192196322562881", "Kunton Akutagawa ramen Kyoto", 35.0064, 135.7667, ""),
 ("food", "Nishiki Market", "Downtown", ["Quick bite"],
  "Kyoto's long covered food market. Graze from stall to stall. Go earlier in the day, as many stalls close by early evening.",
  "https://maps.google.com/?cid=13159134450370243740", "Nishiki Market Kyoto", 35.0050, 135.7647, ""),
 ("sweets", "Cafe Bibliotic Hello!", "Nijo, north of downtown", ["Low energy"],
  "A popular cafe with walls of books. A calm place to sit for a while.",
  "https://maps.google.com/?cid=9811042860654385097", "Cafe Bibliotic Hello Kyoto", 35.0137, 135.7642, ""),
 ("sights", "Kiyomizu-dera", "Higashiyama", ["Photo spot", "Late night"],
  "The temple with the famous wooden stage over the hillside. It usually opens in the evening in autumn for a light-up (in 2025 it ran Nov 22-Dec 7). The 2026 dates are not announced yet.",
  "https://maps.google.com/?cid=7111013964196361402", "Kiyomizudera autumn illumination", 34.9947, 135.7847, ""),
 ("sights", "Ginkaku-ji", "Sakyo, east Kyoto", ["Outdoors", "Photo spot"],
  "The Silver Pavilion and its garden. The Philosopher's Path starts here and runs south past Anraku-ji towards Nanzen-ji, so they make a good walk together.",
  "https://maps.google.com/?cid=2705196751698570185", "Ginkakuji autumn", 35.0270, 135.7982, ""),
 ("sights", "Honnō-ji", "Teramachi, downtown", ["Photo spot"],
  "A downtown temple famous for its old fire-protecting ginkgo tree, which turns bright yellow in late autumn.",
  "https://maps.google.com/?cid=2201652011559631590", "Honnoji ginkgo autumn", 35.0103, 135.7683, ""),
 ("sights", "Rokudō Chinnō-ji", "Higashiyama", ["Low energy"],
  "A small, quiet temple said to sit at the entrance to the underworld. Close to Yasaka Shrine and Kiyomizu-dera.",
  "https://maps.google.com/?cid=5165877923149119340", "Rokudo Chinnoji temple", 34.9983, 135.7754, ""),
 ("sights", "Saihō-ji (Kokedera)", "Matsuo, west Kyoto", ["Book ahead", "Photo spot"],
  "The moss temple, with a garden of over a hundred kinds of moss. Visits are by advance reservation only, and you need to arrive at your booked time.",
  "https://maps.google.com/?cid=12604676872959930581", "Saihoji moss temple", 34.9922, 135.6837, ""),
 ("sights", "Daihikaku Senkō-ji", "Arashiyama", ["Outdoors", "Photo spot"],
  "A small temple up the hillside above the river in Arashiyama, with views over the valley. Pairs with Jōjakkō-ji and Yusai-Tei.",
  "https://maps.google.com/?cid=14257992469760671362", "Daihikaku Senkoji Arashiyama", 35.0158, 135.6656, ""),
 ("sights", "Arashiyama Monkey Park", "Arashiyama", ["Outdoors"],
  "A hilltop park with free-roaming wild monkeys and a view over Kyoto. Expect an uphill walk to get there.",
  "https://maps.google.com/?cid=1960354123061081266", "Arashiyama Monkey Park Iwatayama", 35.0114, 135.6766, ""),
 ("sights", "Mount Hiei", "Northeast of Kyoto", ["Outdoors", "Photo spot"],
  "The mountain on Kyoto's northeast edge, home to the Enryaku-ji temple complex, with big views. Pairs with Former Chikurin-in at its foot.",
  "https://maps.google.com/?cid=16309124816119328751", "Mount Hiei Enryakuji autumn", 35.0622, 135.8315, ""),
 ("sights", "Former Chikurin-in", "Sakamoto, Shiga side of Hiei", ["Outdoors", "Low energy"],
  "A garden at the foot of Mount Hiei in Sakamoto. Easy to combine with Mount Hiei.",
  "https://maps.google.com/?cid=13309011099031202891", "Former Chikurinin Sakamoto autumn", 35.0716, 135.8658, ""),
 ("sights", "Kurama Onsen", "Kurama, north of Kyoto", ["Low energy", "Outdoors"],
  "A hot spring in the mountain village of Kurama. A relaxing half-day out of the city.",
  "https://maps.google.com/?cid=6234670849390713272", "Kurama Onsen outdoor bath", 35.1192, 135.7766, ""),
 ("sights", "Kyoto Tower", "Kyoto Station", ["Late night"],
  "The observation deck across from Kyoto Station, good for a city view at night.",
  "https://maps.google.com/?cid=17017157882742292436", "Kyoto Tower night view", 34.9875, 135.7593, ""),
 ("sights", "GEAR non-verbal theatre", "Downtown", ["Late night", "Book ahead"],
  "A long-running, very highly rated show with no dialogue, mixing mime, dance and magic. Book tickets ahead.",
  "https://maps.google.com/?cid=590976552152252111", "GEAR non-verbal theatre Kyoto", 35.0085, 135.7665, ""),
 ("sights", "Naniwa Camera", "Downtown", [],
  "A camera shop, handy for gear or a browse.",
  "https://maps.google.com/?cid=9608848783477973023", "Naniwa Camera Kyoto", 35.0039, 135.7662, ""),
]
KY_P = [(c, n, a, kdist(la, lo, note), t, d, m, q, la, lo) for c, n, a, t, d, m, q, la, lo, note in KY_RAW]

KYOTO = dict(
    key="kyoto", name="Kyoto", jp="京都", stop=3, dates="Nov 23-27", tabdates="Nov 23-27 · 29-Dec 2", nights="4 nights",
    sub="ramen, matcha &amp;<br>temples in autumn colours", art="kyoto",
    hotel=KY_HOTEL, hotel_name="Hotel ZIZI Horikawa Gojo", hotel_note="1-2 km from downtown",
    hotel2=KY_HOTEL2, hotel2_name="Kyoto Plaza Hotel Kintetsu Jujo", hotel2_note="by Kintetsu Jujo station, south of Kyoto Station",
    hotel2_dates="Nov 29-Dec 2", hotel2_nights="3 nights",
    day1=("Two stays in Kyoto", "Nov 23-27 at Hotel ZIZI, then Nov 29-Dec 2 at Kyoto Plaza Hotel Kintetsu Jujo, after Hikone. Each place shows two distances: from hotel 1 / from hotel 2."),
    planner="Options", places=KY_P,
    areas=[("Downtown · Shijo / Teramachi", "1-2 km / 4-5 km", ["Ramen Mugyu Vol. 2", "Second House Cake Works", "Kitchen Gon Rokkaku", "Rokkaku Ace",
                                                    "Nishiki Market", "Naniwa Camera", "Kunton Akutagawa", "Micasadeco & Cafe", "Gyukatsu Kyoto Katsugyu",
                                                    "GEAR non-verbal theatre", "Kyogoku Kaneyo", "Honnō-ji", "Kyo-Motsunabe Kamehachi", "Cafe Bibliotic Hello!"]),
           ("Gion & Higashiyama", "2-3 km / 4 km", ["Itoh Kyuemon Sabo", "Ten no Meshi Gion", "Hikiniku to Come", "Yasaka Shrine", "Rokudō Chinnō-ji", "Kiyomizu-dera"]),
           ("Kyoto Station & south", "1-3 km / 2-3 km", ["Kyoto Tower", "Tōfuku-ji"]),
           ("East · Philosopher's Path", "4-5 km / 6-7 km", ["Nanzen-ji", "Anraku-ji", "Ginkaku-ji"]),
           ("Northwest", "5 km / 8 km", ["Kinkaku-ji"]),
           ("West · Arashiyama & Matsuo", "6-8 km / 7-9 km", ["Saihō-ji (Kokedera)", "Arashiyama Monkey Park", "Arashiyama Yusai-Tei", "Jōjakkō-ji", "Daihikaku Senkō-ji"]),
           ("Out of town · Hiei, Sakamoto, Kurama", "10-14 km / 12-16 km", ["Mount Hiei", "Former Chikurin-in", "Kurama Onsen"])],
    leads={"must": "The two places we're planning the days around.",
           "food": "Eel, gyukatsu, hotpot, tempura, hamburg steak, more ramen and a food market.",
           "sweets": "Cake, desserts, matcha and a book cafe.",
           "sights": "Temples for autumn leaves, night light-ups, day trips to the hills, and a few city extras."},
    icons={}, titles={"sights": "Temples & sights"},
    map=dict(k=15.0, W=100.0, H=130.0, scale_km=1.0, scale_lbl="1 km", ycenter_shift=10,
             labels=[("DOWNTOWN", 35.0138, 135.7590, "middle"), ("GION", 35.0002, 135.7800, "start"),
                     ("KYOTO STN", 34.9840, 135.7588, "middle"), ("OKAZAKI", 35.0150, 135.7860, "end"),
                     ("KAMO RIVER", 34.9905, 135.7725, "start")],
             river=[(34.968, 135.7720), (34.9895, 135.7690), (34.9955, 135.7695), (35.004, 135.7716), (35.0090, 135.7720),
                    (35.0180, 135.7728), (35.0295, 135.7722)],
             outliers=[("Kinkaku-ji", 8, "Kinkaku-ji ↖ 5 km", "left"),
                       (["Jōjakkō-ji", "Arashiyama Yusai-Tei", "Daihikaku Senkō-ji", "Arashiyama Monkey Park"], 16, "← Arashiyama", "left"),
                       ("Saihō-ji (Kokedera)", 24, "← Saihō-ji 6 km", "left"),
                       ("Kurama Onsen", 8, "Kurama 14 km ↑", "right"),
                       (["Former Chikurin-in", "Mount Hiei"], 16, "Hiei ↗", "right")]),
)

WK_START = {"name": "JR Wakayama Station", "lat": 34.2321803, "lon": 135.1917916,
            "maps": "https://www.google.com/maps/search/?api=1&query=JR+Wakayama+Station"}

def wdist(lat, lon):
    d = km((WK_START["lat"], WK_START["lon"]), (lat, lon))
    return f"{d:.1f} km" + (" · walk" if d < 1.2 else "")

WK_RAW = [
 ('food', 'Katto', 'By Wakayama Station', [],
  'Ramen with a rich, creamy chicken broth, right by the station. Opens at 11:00.',
  'https://maps.google.com/?cid=3540497299708346347', 'とりそば嘉人 和歌山', 34.231044499999996, 135.1900757),
 ('food', 'Niyoro', 'By Wakayama Station', [],
  'Eel over rice (unagi). Opens at 11:00.',
  'https://maps.google.com/?cid=1221958384847454444', '二与呂 和歌山 うなぎ', 34.2330401, 135.1881569),
 ('food', 'Kalbi 1cho', 'By Wakayama Station', [],
  'Tasty local wagyu BBQ (yakiniku), with deer meat on the menu too.',
  'https://maps.google.com/?cid=11554976602232267605', 'カルビ一丁 和歌山店', 34.2335338, 135.1886719),
 ('food', 'Yakitori Kairo', 'North of the centre', ['Late night'],
  'The tastiest yakitori on the list. Dinner from 17:00.',
  'https://maps.google.com/?cid=7804657641492008548', '焼鳥 かいろ 和歌山', 34.2384353, 135.1791332),
 ('food', 'BRIDGE', 'City centre', ['Late night'],
  'Another tasty yakitori spot. Opens at 18:00.',
  'https://maps.google.com/?cid=2290438624177363043', 'BRIDGE 焼鳥 和歌山', 34.2342381, 135.1724671),
 ('food', 'Ichidai', 'Near the castle', ['Late night'],
  'An interesting yakitori place (やき鳥 一代). Dinner from 17:00.',
  'https://maps.google.com/?cid=1833223725525101210', 'やき鳥 一代 和歌山', 34.225703599999996, 135.169587),
 ('food', 'Maruman Ramen', 'Near the castle', [],
  'A local ramen shop (まる万ラーメン) a few minutes from the castle.',
  'https://maps.google.com/?cid=11560120881329501842', 'まる万ラーメン 九番丁', 34.2314699, 135.17057269999998),
 ('food', 'Umimachi Shokudo Urara', 'Saikazaki, by the sea', [],
  'Seafood omakase for about 20 euros per person, by the sea in Saikazaki. Opens at 11:00. Pairs with Bandoko Garden next door.',
  'https://maps.google.com/?cid=5911579447961568639', 'うみまち食堂うらら 雑賀崎', 34.1902445, 135.144645),
 ('drinks', 'Goen', 'By Wakayama Station', ['Late night'],
  'A tasty spot for food and drinks at night, with charcoal-grilled yakitori. Opens at 18:00. Called 焼鳥炭火笑酒屋 五縁 on the map.',
  'https://maps.google.com/?cid=16494497776411410737', '五縁 和歌山店', 34.231074899999996, 135.1910408),
 ('sights', 'Bandoko Garden', 'Saikazaki, by the sea', ['Outdoors', 'Photo spot'],
  'A garden on a headland next to the sea, for the view. Opens at 8:00. Lunch at Urara is next door.',
  'https://maps.google.com/?cid=6190730922807149711', '番所庭園 和歌山', 34.1906797, 135.14067989999998),
 ('sights', 'Wakayama Castle', 'City centre', ['Outdoors', 'Photo spot'],
  'The castle on its hill in the middle of the city, with a park around it.',
  'https://www.google.com/maps/search/?api=1&query=Wakayama+Castle', 'Wakayama Castle', 34.2276558, 135.1715109),
 ("trips", "Kishi Station", "Kinokawa, Wakayama", ["Quick bite"],
  "The little station famous for its cat stationmaster, at the end of the Kishigawa Line from Wakayama Station.",
  "https://maps.google.com/?cid=17241543118648371379", "Kishi Station cat stationmaster", 34.2093, 135.3121),
 ("trips", "Awashima Shrine", "Kada, Wakayama coast", ["Photo spot"],
  "A seaside shrine known for the thousands of dolls people leave there.",
  "https://maps.google.com/?cid=15657838165788794839", "Awashima Shrine Kada dolls", 34.2737, 135.0664),
 ("trips", "Koyasan", "Koya, Wakayama mountains", ["Outdoors", "Photo spot"],
  "A mountain-top temple town and a centre of Shingon Buddhism, with the huge Okunoin cemetery and temple stays. A full day on its own.",
  "https://maps.google.com/?cid=11714349864090713783", "Koyasan Okunoin", 34.2132, 135.5863),
]
WK_P = [(c, n, a, wdist(la, lo), t, d, m, q, la, lo) for c, n, a, t, d, m, q, la, lo in WK_RAW]

WAKAYAMA = dict(
    key="wakayama", name="Wakayama", jp="和歌山", stop=0, optional=True, dates="Nov 20", tabdates="Optional stop", nights="optional",
    sub="yakitori, ramen &amp;<br>a castle on the way south", art="wakayama",
    hotel=WK_START, hotel_name="JR Wakayama Station", hotel_note="where limited express trains between Osaka and Shirahama stop",
    hotel_box_title="Starting point", hotel_label="station", pill="Maybe · on the way, Nov 20",
    kicker="Optional stop · between Osaka and Shirahama",
    day1=("How to fit it in", "Not decided yet. Wakayama is on the train line from Osaka to Shirahama, so we could break the journey here on Nov 20, or come back for a day trip. Distances are from JR Wakayama Station."),
    planner="Options", places=WK_P,
    areas=[("By Wakayama Station", "under 0.5 km", ["Katto", "Goen", "Niyoro", "Kalbi 1cho"]),
           ("Castle & city centre", "1.4-2.2 km", ["Wakayama Castle", "Maruman Ramen", "BRIDGE", "Ichidai", "Yakitori Kairo"]),
           ("Saikazaki, by the sea", "6.5 km", ["Umimachi Shokudo Urara", "Bandoko Garden"]),
           ("Further out", "11-36 km", ["Kishi Station", "Awashima Shrine", "Koyasan"])],
    leads={"food": "Yakitori, ramen, eel, wagyu BBQ and a seafood omakase.",
           "drinks": "Night food and drinks by the station.",
           "sights": "The castle and a seaside garden.",
           "trips": "Further out from Wakayama city."},
    icons={}, titles={"trips": "Further out"},
    map=dict(k=13.0, W=100.0, H=112.0, scale_km=1.0, scale_lbl="1 km", ycenter_shift=12,
             labels=[("SAIKAZAKI", 34.1912, 135.1490, "start"), ("CASTLE", 34.2250, 135.1740, "start")],
             outliers=[("Awashima Shrine", 8, "↖ Awashima 12 km", "left"),
                       ("Kishi Station", 8, "Kishi 11 km →", "right"),
                       ("Koyasan", 16, "Koyasan 36 km →", "right")]),
)

HK_HOTEL = {"name": "Hotel Sunroute Hikone", "lat": 35.2730945, "lon": 136.262185,
            "maps": "https://maps.app.goo.gl/9NpEg9hq8h4yYqeu7"}

def hdist(lat, lon):
    return f"{km((HK_HOTEL['lat'], HK_HOTEL['lon']), (lat, lon)):.0f} km"

HK_RAW = [
 ("sights", "Hikone Castle", "Hikone, walkable", ["Outdoors", "Photo spot"],
  "One of the few castles in Japan with its original keep still standing, and a National Treasure. Genkyu-en garden sits right below it. Walkable from the hotel.",
  "https://www.google.com/maps/search/?api=1&query=Hikone+Castle", "Hikone Castle autumn", 35.2763, 136.2519),
 ("sights", "Yutani Shrine", "Maibara, next to Hikone", ["Low energy"],
  "A small shrine in Maibara, the nearest place on the list. An easy short outing.",
  "https://maps.google.com/?cid=2770015437704597159", "Yutani Shrine Maibara", 35.3128, 136.2953),
 ("sights", "Chikubu Island", "Lake Biwa", ["Outdoors", "Photo spot"],
  "A small sacred island in Lake Biwa with a shrine and temple. Boats leave from Hikone Port in season, which runs to early December. The trip takes about 2.5 hours in total, with around 75 minutes on the island. Check the day's sailings before going.",
  "https://maps.google.com/?cid=2901414486857167280", "Chikubushima Lake Biwa", 35.4232, 136.1437),
 ("sights", "Kyorinbo", "Azuchi, south of Hikone", ["Outdoors", "Photo spot"],
  "A temple garden known for autumn leaves. It normally opens only on weekends, but in past years it has opened daily for a few weeks in autumn, with an evening light-up. Check this year's dates.",
  "https://maps.google.com/?cid=1454445400296920734", "Kyorinbo autumn leaves", 35.1389, 136.1640),
 ("sights", "Omihachiman", "Omihachiman", ["Outdoors", "Photo spot"],
  "An old merchant town with canals and traditional streets. Jinnosuke Coffee is here too.",
  "https://maps.google.com/?cid=8511313074295460791", "Omihachiman canal", 35.1284, 136.0980),
 ("coffee", "Jinnosuke Coffee", "Omihachiman", ["Low energy"],
  "A coffee shop in Omihachiman (仁之助コーヒー). A good break while exploring the town.",
  "https://maps.google.com/?cid=1420078449805569034", "仁之助コーヒー 近江八幡", 35.1392, 136.0884),
 ("sights", "Shirahige Shrine", "Takashima, west shore", ["Outdoors", "Photo spot"],
  "The shrine with a red torii standing in Lake Biwa. It's on the far side of the lake, so plan it as its own outing.",
  "https://maps.google.com/?cid=13664484576260554187", "Shirahige Shrine torii lake", 35.2745, 136.0110),
 ("sights", "Keisokuji", "Nagahama, north", ["Outdoors", "Photo spot"],
  "A temple in the hills north of Lake Biwa, known for autumn leaves along mossy stone steps.",
  "https://maps.google.com/?cid=2366704082444976644", "Keisokuji autumn leaves", 35.5061, 136.2579),
 ("sights", "Yogo Station", "Nagahama, far north", ["Low energy", "Photo spot"],
  "A quiet country station by Lake Yogo, a small lake north of Lake Biwa.",
  "https://maps.google.com/?cid=1657791961354483095", "Lake Yogo", 35.5339, 136.1997),
]
HK_P = [(c, n, a, hdist(la, lo), t, d, m, q, la, lo) for c, n, a, t, d, m, q, la, lo in HK_RAW]

HIKONE = dict(
    key="hikone", name="Hikone", jp="彦根", stop=4, dates="Nov 27-29", nights="2 nights",
    sub="a castle town &amp;<br>day trips around Lake Biwa", art="hikone",
    hotel=HK_HOTEL, hotel_name="Hotel Sunroute Hikone", hotel_note="next to Hikone Station",
    day1=("Getting around", "Everything here is a train, boat or car ride from Hikone, so one or two outings a day is plenty."),
    planner="Options", places=HK_P, next_back=("kyoto", "Kyoto, again", "Nov 29-Dec 2"),
    areas=[("Hikone & Maibara", "1-5 km", ["Hikone Castle", "Yutani Shrine"]),
           ("South · Omihachiman & Azuchi", "17-22 km", ["Kyorinbo", "Omihachiman", "Jinnosuke Coffee"]),
           ("On & across the lake", "20-23 km", ["Chikubu Island", "Shirahige Shrine"]),
           ("North · Nagahama", "26-30 km", ["Keisokuji", "Yogo Station"])],
    leads={"coffee": "One coffee stop so far.",
           "sights": "The castle, temples for autumn leaves, a lake island, a torii in the water and a canal town."},
    icons={}, titles={"sights": "Sights & outings"},
    map=dict(k=2.2, W=100.0, H=120.0, scale_km=10.0, scale_lbl="10 km", ycenter_shift=2,
             labels=[("LAKE BIWA", 35.300, 136.100, "middle"),
                     ("NAGAHAMA", 35.381, 136.270, "start")],
             outliers=[]),
)

NR_START = {"name": "Kintetsu Nara Station", "lat": 34.6842485, "lon": 135.8275275,
            "maps": "https://www.google.com/maps/search/?api=1&query=Kintetsu+Nara+Station"}

NARA = dict(
    key="nara", name="Nara", jp="奈良", stop=0, optional=True, dates="Day trip", tabdates="Optional day trip", nights="optional",
    sub="a day trip from<br>Osaka or Kyoto", art="nara",
    hotel=NR_START, hotel_name="Kintetsu Nara Station", hotel_note="the closest station to Nara Park",
    hotel_box_title="Starting point", hotel_label="station", pill="Maybe · a day trip", maybe_label="Maybe a day trip",
    kicker="Optional day trip · from Osaka or Kyoto",
    day1=("How to fit it in", "Not decided yet. Nara is about 40 minutes from Osaka-Namba, or 35-45 minutes from Kyoto Station, on the Kintetsu line to Kintetsu Nara Station. For autumn leaves, earlier is better, see the forecast below."),
    planner="Options", places=[], areas=[], leads={}, icons={},
    soon="No list yet. Places will be added here once we have one.",
    map=dict(k=15.0, W=100.0, H=70.0, scale_km=0.5, scale_lbl="500 m", ycenter_shift=0,
             labels=[("NARA PARK →", 34.6880, 135.8380, "start")], outliers=[]),
)

CITIES = [OSAKA, WAKAYAMA, SHIRAHAMA, KYOTO, NARA, HIKONE]
CATS = {k: CATS[k] for k in ["must", "food", "sweets", "coffee", "drinks", "onsen", "sights", "trips"]}
for _c in CITIES:   # number places in the order their sections appear
    _c["places"] = sorted(_c["places"], key=lambda p: list(CATS).index(p[0]))
import leaves as _lv   # cards with a leaves forecast also get the "Autumn leaves" filter tag
for _c in CITIES:
    _m = _lv.CARDS.get(_c["key"], {})
    assert all(any(p[1] == n for p in _c["places"]) for n in _m), f"leaves.CARDS names a missing card in {_c['key']}"
    _c["places"] = [p[:4] + ((p[4] + ["Autumn leaves"]) if p[1] in _m else p[4],) + p[5:] for p in _c["places"]]
# Card photos, only ones the user sends: {stop: {card name: slug or (slug, source label, source link)}}.
# Files: photos/<stop>/<slug>-800.webp and -1600.webp, made with source/add_photo.py (also strips location and other metadata).
# A photo that isn't ours always carries its source, shown as a link on the card and in the enlarged view.
PHOTOS = {
    "osaka": {"aoma coffee": ("aoma-coffee", "Photo: YouTube video", "https://www.youtube.com/watch?v=RGqhSRTqsr8")},
}
LATER = []
