# JR Techfolio

This repository publishes **jrtechfolio.com**. The separate name-domain site is not managed here.

The main experience is the overview (`index.html`) and four evidence pages:

- `innovation.html`
- `inspiring.html`
- `consultancy.html`
- `influencer.html`

These are static HTML pages. They work without a server and retain their evidence when JavaScript is disabled. JavaScript only adds an optional enlarged image preview. Full certificates are displayed inline and link to originals.

## Updating content

Edit `scripts/build_evidence.py`, then run it with Python 3 and Pillow. It generates the five HTML pages. The script checks image dimensions while building. Edit `evidence.css` for presentation and `evidence.js` for the optional viewer.

Certificate assets live in `assets/certificates/`; event photos live in `assets/events/`. Keep original documents intact. Do not copy private application forms, resumes, internal client records or supporter contact details into the public repository.

The October 2026 content revision follows the supplied final application for topic scope. Internal outcomes remain identified as supporter-verifiable. Organiser certificates support specific appointments and activities; company sources establish business context, not personal attribution.

GitHub Pages deploys `main` at the repository root. Preserve `CNAME` and the existing noindex directives.
