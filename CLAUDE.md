# Working on the trip guide

This repo is a travel guide web page, live at **https://japan.zhunior.com** (GitHub Pages, `main` branch). The full documentation is in `docs/GUIDE.md`; read it before making structural changes.

## The loop for every change
1. Edit content in `source/data.py` (places, stops, hotels), or the page in `source/build_site.py` / `source/common.py` / `source/styles.py`.
2. Bump `VERSION`, `VDATE` and `CHANGELOG` in `source/build_site.py`: x.y for content or features, x.y.z for fixes.
3. `python3 source/build_site.py`, which regenerates `index.html`. Never edit `index.html` by hand.
4. `python3 source/test_site.py`. Everything must pass. Look at `source/out/test/*.png`, and check the drawn map whenever places change.
5. Commit the source and `index.html` together, then push to `main`. Then verify the live footer shows the new version: `python3 source/test_site.py https://japan.zhunior.com/`.
6. Tell the user the new version number and what changed.

## Content rules
- Use the user's own words for descriptions. Don't invent experiences. Use plain, short sentences.
- No long dashes (the em dash, or a spaced en dash) anywhere on the page. Ranges use a plain hyphen ("Nov 16-20").
- No personal names on the page (the build checks this).
- Get coordinates from the Maps link's `!3d<lat>!4d<lon>`, not from `@lat,lon`.
- Check practical facts before publishing (closures, closing days, reservations, seasonal hours) and give the user sources.
- Don't pick or copy photos yourself. Card photos are only ones the user sends: prepare them with `python3 source/add_photo.py <file> <stop> <slug>` (strips location data) and list them in `PHOTOS` in data.py. A photo that isn't the user's own must carry its source link. The "Photos" button stays a Google image search link.
- Shared Google Maps lists: `python3 source/read_gmaps_list.py <link> <hotel lat> <hotel lon>`.

## Don't break
- `CNAME` (custom domain) and `.nojekyll` must stay.
- The noindex meta tags must stay, and don't add a robots.txt Disallow.
- Tabs and filters must keep working without JavaScript (the test checks this).
- The Squarespace variant (`source/out/squarespace-*.html`) is frozen. Don't spend effort on it unless asked.
