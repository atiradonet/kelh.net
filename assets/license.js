const LICENSE_URL = '/LICENSE';

const target = document.getElementById('license-content');

const setText = (text) => {
  if (target) target.textContent = text;
};

const loadLicense = async () => {
  try {
    const resp = await fetch(LICENSE_URL, { cache: 'no-cache' });
    if (!resp.ok) throw new Error(`Status ${resp.status}`);
    const text = await resp.text();
    setText(text);
  } catch (err) {
    setText('Unable to load license. Please try again later.');
  }
};

loadLicense();
