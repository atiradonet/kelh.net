const createPolicy = (name) => {
  if (window.trustedTypes && window.trustedTypes.createPolicy) {
    return window.trustedTypes.createPolicy(name, {
      createHTML: (html) => html
    });
  }
  return { createHTML: (html) => html };
};

const navPolicy = createPolicy('kelh-nav');
const footerPolicy = createPolicy('kelh-footer');

class SiteNav extends HTMLElement {
  async connectedCallback() {
    try {
      const resp = await fetch('/partials/nav.html', { cache: 'force-cache' });
      const html = resp.ok ? await resp.text() : '';
      this.innerHTML = navPolicy.createHTML(html);
    } catch (err) {
      this.innerHTML = '';
    }
  }
}

customElements.define('site-nav', SiteNav);

class SiteFooter extends HTMLElement {
  async connectedCallback() {
    try {
      const resp = await fetch('/partials/footer.html', { cache: 'force-cache' });
      const html = resp.ok ? await resp.text() : '';
      this.innerHTML = footerPolicy.createHTML(html);
    } catch (err) {
      this.innerHTML = '';
    }
  }
}

customElements.define('site-footer', SiteFooter);
