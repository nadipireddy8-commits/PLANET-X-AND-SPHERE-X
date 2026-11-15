# SPHEREx Sky Explorer

**Team Gravity Wells** — N R Jitendar Reddy, Devadula Siva Praneeth, Kalyan Kumar
NASA Space Apps Challenge 2026 · Advanced challenge: *Planet X and SPHEREx*

A free, install-free web tool that compares sky images taken months apart, finds what moved, and measures how far.

## Run it
Open `index.html` in Chrome or Edge (double-click). No server, no install. Images you upload stay in your browser.
Try the sample images in `samples/` (upload all four).

## What it does
- Sky view: pass slider (+0 to +18 months), 102-band slider, blink compare, mover highlights, object info cards
- Measure distance: click P2 and a line is drawn from the P1 object to the P2 object; longitude/latitude are shown, then the Euclidean distance
- AI analyst + Train AI: small neural network (121-16-8-1) scores real mover vs artifact
- Space Lab: 3D sky dome, orbit, spacecraft, outer Solar System
- Auto-generated downloadable reports

## Method
- Image differencing (mean + 3.5 sigma), 7x7 local peaks, nearest-neighbour pairing
- Pixel to sky: flat-sky approximation from a user-given centre and width
- Distance: d = 60 * sqrt((dLon*cos(lat))^2 + dLat^2) arcmin
- Significance: sigma = FWHM / (2.355 SNR), displacement error = sqrt(2) sigma

## Honest limits
- The demo sky is synthetic; the neural network is trained on synthetic stamps.
- No WCS/FITS reading yet (user calibration is used instead).
- Detections are candidates, not confirmed objects. Two epochs cannot give an orbit.

## Planned
Real SPHEREx FITS + WCS (astropy), CNN filter on real data, 3+ epoch tracking, catalogue cross-match (SIMBAD, Gaia, Minor Planet Center).

`tools/get_spherex_images.py <RA> <Dec>` downloads public images from NASA/IPAC IRSA (run on your own machine).

Data: NASA/IPAC IRSA, SPHEREx. License: MIT.
