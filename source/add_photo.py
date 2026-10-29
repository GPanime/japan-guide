"""Prepare one of our own photos for the guide.

    python3 source/add_photo.py <image file> <stop key> <slug>
    e.g. python3 source/add_photo.py ~/Downloads/IMG_1234.jpg osaka aoma-coffee

Writes photos/<stop>/<slug>-800.webp (card) and <slug>-1600.webp (tap to enlarge), with all metadata removed
(GPS location, date, phone model). Then add the card to PHOTOS in data.py: "Card name": "<slug>".
Only use photos we took ourselves.
"""
import os, sys
from PIL import Image, ImageOps

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def prepare(src, stop, slug):
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")   # apply the phone's rotation, then drop everything else
    out = os.path.join(REPO, "photos", stop)
    os.makedirs(out, exist_ok=True)
    for w, q in ((800, 78), (1600, 80)):
        im2 = im.copy()
        if im2.width > w:
            im2 = im2.resize((w, round(im2.height * w / im2.width)), Image.LANCZOS)
        path = os.path.join(out, f"{slug}-{w}.webp")
        Image.frombytes("RGB", im2.size, im2.tobytes()).save(path, "WEBP", quality=q, method=6)   # fresh image: no EXIF, XMP or ICC
        print(f"{os.path.relpath(path, REPO)}  {im2.width}x{im2.height}  {os.path.getsize(path) // 1024} KB")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    prepare(*sys.argv[1:])
