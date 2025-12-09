class SiteNav extends HTMLElement {
  async connectedCallback() {
    try {
      const resp = await fetch('/partials/nav.html', { cache: 'force-cache' });
      this.innerHTML = resp.ok ? await resp.text() : '';
    } catch (err) {
      this.innerHTML = '';
    }
  }
}

customElements.define('site-nav', SiteNav);
