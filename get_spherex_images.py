"""Download up to 4 real SPHEREx images of one sky position as PNGs for SPHEREx Sky Explorer.

Setup:   pip install astroquery astropy pillow numpy
Run:     python get_spherex_images.py RA_DEG DEC_DEG [SIZE_PIXELS]
Example: python get_spherex_images.py 304.6935 42.4437 300

Saves pass1.png ... pass4.png (oldest first) in the current folder.
Then choose those files under "Real images" in the web app.
Note: each SPHEREx exposure records one wavelength at a given spot on the
detector, so images from different dates can show different bands.
"""
import sys
import numpy as np
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.io import fits
from astropy.nddata import Cutout2D
from astropy.utils.data import conf
from astropy.wcs import WCS
from astroquery.ipac.irsa import Irsa
from PIL import Image

conf.remote_timeout = 120
ra, dec = float(sys.argv[1]), float(sys.argv[2])
size = int(sys.argv[3]) if len(sys.argv) > 3 else 300
coord = SkyCoord(ra, dec, unit="deg")

res = Irsa.query_sia(pos=(coord, 1 * u.arcsec), collection=["spherex_dr1", "spherex_qr3"])
if "t_min" in res.colnames:
    res = res[np.argsort(res["t_min"])]
n = len(res)
print(n, "images found")
if n == 0:
    sys.exit("No SPHEREx images cover this position. Try another RA/Dec.")

for k, i in enumerate(np.unique(np.linspace(0, n - 1, 4).astype(int)), 1):
    with fits.open(res["access_url"][i], memmap=False) as hdul:
        img = hdul["IMAGE"].data.astype(float)
        wcs = WCS(hdul["IMAGE"].header)
    cut = Cutout2D(img, coord, (size, size), wcs=wcs, mode="partial", fill_value=np.nan)
    a = np.nan_to_num(cut.data, nan=np.nanmedian(cut.data))
    lo, hi = np.percentile(a, [1, 99.5])
    a = np.clip((a - lo) / (hi - lo + 1e-9), 0, 1)
    a = np.arcsinh(a * 10) / np.arcsinh(10)
    Image.fromarray((a[::-1] * 255).astype("uint8")).resize((512, 512)).save(f"pass{k}.png")
    print("saved", f"pass{k}.png")
