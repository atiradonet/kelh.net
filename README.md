# kelh.net

Static site for the kelh.net domain owned by @atiradonet. This repository hosts the public landing page served via GitHub Pages.

## About

- Purpose: provide a concise, standards-compliant HTML home page for kelh.net.
- Tech: plain HTML and CSS; no build step.
- Hosting: GitHub Pages (from the default branch).

## BIMI

- BIMI logo is served at `https://kelh.net/bimi/kelh-bimi.svg` (SVG Tiny, square).
- DNS TXT record without a VMC (limited provider support):  
  `default._bimi.kelh.net. IN TXT "v=BIMI1; l=https://kelh.net/bimi/kelh-bimi.svg;"`  
- When you obtain a VMC, update the record to include it:  
  `default._bimi.kelh.net. IN TXT "v=BIMI1; l=https://kelh.net/bimi/kelh-bimi.svg; a=<VMC_URL>"`  
  Many providers (e.g., Gmail, Yahoo) require a VMC to display the mark.
- Prereqs: DMARC at enforcement (`p=quarantine` or `p=reject`) with aligned SPF/DKIM for mail you send as kelh.net.
- If you move the logo, update `l=` in DNS and keep the file public over HTTPS.

## Contributing

No public contributions are expected. For any changes or reuse of content, please contact the domain owner (@atiradonet) for explicit permission.
