# Working on the trip guide

This repo is a travel guide web page, live at **https://japan.zhunior.com** (GitHub Pages, `main` branch). The full documentation is in `docs/GUIDE.md`; read it before making structural changes.

## The loop for every change
1. Edit content in `source/data.py` (places, stops, hotels), or the page in `source/build_site.py` / `source/common.py` / `source/styles.py`.
2. Bump `VERSION`, `VDATE` and `CHANGELOG` in `source/build_site.py`: x.y for content or features, x.y.z for fixes.
3. `python3 source/build_site.py`, which regenerates `index.html`. Never edit `index.html` by hand. The build needs the page password (it locks the page): put it in `source/.guide_password` (git-ignored) or `GUIDE_PASSWORD`. The password is in the Claude Project doc `claude/guide-handbook.md`; ask the user if you can't find it. Never commit it.
4. `python3 source/test_site.py`. Everything must pass. Look at `source/out/test/*.png`, and check the drawn map whenever places change.
5. Commit the source and `index.html` together, then push to `main`. Then verify the live footer shows the new version: `python3 source/test_site.py https://japan.zhunior.com/`.
6. Tell the user the new version number and what changed.

## Content rules
- Use the user's own words for descriptions. Don't invent experiences. Use plain, short sentences.
- No long dashes (the em dash, or a spaced en dash) anywhere on the page. Ranges use a plain hyphen ("Nov 16-20").
- No personal names on the page (the build checks this).
- Get coordinates from the Maps link's `!3d<lat>!4d<lon>`, not from `@lat,lon`.
- Check practical facts before publishing (closures, closing days, reservations, seasonal hours) and give the user sources.
- Card photos are ones the user sends, or, when the user asks you to find one, a photo of the actual place found on the web (Google Images style: the shop's own page, a blog, a travel guide; the user accepts this for the private guide) or a freely licensed one from Wikimedia Commons. Prepare every photo with `python3 source/add_photo.py <file> <stop> <slug>` (strips metadata) and list it in `PHOTOS` in data.py. A photo that isn't the user's own must carry its source link: the page it comes from, or for Commons the file page with author and licence. Say so in the credit when it shows another branch or a nearby view. Food places get a dish or the inside of the restaurant; shops get the storefront or the inside. The "Photos" button stays a Google image search link.
- Shared Google Maps lists: `python3 source/read_gmaps_list.py <link> <hotel lat> <hotel lon>`.

## Don't break
- `CNAME` (custom domain) and `.nojekyll` must stay.
- The noindex meta tags must stay, and don't add a robots.txt Disallow.
- Tabs and filters must keep working without JavaScript on the unlocked page (`index-plain.html`, the test checks this). The published `index.html` is the password-locked version and needs JavaScript only to unlock.
- The Squarespace variant (`source/out/squarespace-*.html`) is frozen. Don't spend effort on it unless asked.
