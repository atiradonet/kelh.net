# kelh.net

Static site for the kelh.net domain owned by @atiradonet. This repository hosts the public landing page served via GitHub Pages.

## About

- Purpose: provide a concise, standards-compliant HTML home page for kelh.net.
- Tech: plain HTML and CSS; no build step.
- Hosting: GitHub Pages (from the default branch).

## BIMI

- BIMI logo is served at `https://kelh.net/bimi/kelh-bimi.svg` (SVG Tiny, square).
- DNS TXT record to publish (once ready):  
  `default._bimi.kelh.net. IN TXT "v=BIMI1; l=https://kelh.net/bimi/kelh-bimi.svg; a=<VMC_URL>"`  
  Replace `<VMC_URL>` with your Verified Mark Certificate location when issued; omit `a=` only if the receiver allows BIMI without a VMC.
- Prereqs: DMARC at enforcement (`p=quarantine` or `p=reject`) with aligned SPF/DKIM for mail you send as kelh.net.
- If you move the logo, update `l=` in DNS and keep the file public over HTTPS.

## Contributing

No public contributions are expected. For any changes or reuse of content, please contact the domain owner (@atiradonet) for explicit permission.
