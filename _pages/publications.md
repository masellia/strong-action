---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 3
---

Here you can find research publications produced by members of STRONG within the 
project action.

Each entry links to the corresponding **arXiv preprint**, and—once available—to the 
**journal publication** via its DOI. 
For convenience, a **BibTeX citation** can be copied directly for use in articles, 
reports, and presentations.


<style>
.pubs-year { margin-top: 1.2rem; }
.pub-item { padding: 0.45rem 0; border-bottom: 1px solid rgba(0,0,0,0.08); }
.pub-title { font-size: 0.96rem; font-weight: 600; line-height: 1.25; margin: 0; }
.pub-authors { font-size: 0.82rem; opacity: 0.8; margin-top: 0.15rem; }
.pub-journal { font-size: 0.82rem; font-style: italic; opacity: 0.75; margin-top: 0.1rem; }
.pub-actions { margin-top: 0.35rem; display: flex; gap: 0.35rem; flex-wrap: wrap; align-items: center; }
.pub-actions .btn { padding: 0.12rem 0.45rem; font-size: 0.78rem; line-height: 1.2; box-shadow: none !important; }
.pub-status { font-size: 0.78rem; opacity: 0.75; margin-left: 0.15rem; }
</style>

{% assign pubs = site.data.publications %}

{% for block in pubs %}
<h2 class="pubs-year">{{ block.year }}</h2>

{% for p in block.papers %}
<div class="pub-item">

  <!-- Title -->
  <p class="pub-title">{{ p.title }}</p>

  <!-- Authors -->
  {% if p.authors %}
  <div class="pub-authors">
    {{ p.authors }}
  </div>
  {% endif %}

  <!-- Journal (only when available) -->
  {% if p.journal %}
  <div class="pub-journal">
    {{ p.journal }}
  </div>
  {% endif %}

  <!-- Actions -->
  <div class="pub-actions">
    {% if p.arxiv %}
      <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener"
         href="https://arxiv.org/abs/{{ p.arxiv }}">arXiv</a>
    {% endif %}

    {% if p.doi %}
      <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
         href="https://doi.org/{{ p.doi }}">DOI</a>
    {% endif %}

    {% if p.bibtex %}
      <button class="btn btn-sm btn-outline-success" type="button"
              data-bibtex="{{ p.bibtex | escape }}"
              onclick="strongCopyBibtexLocal(this)">
        Copy BibTeX
      </button>
      <span class="pub-status" data-bibtex-status></span>
    {% endif %}
  </div>

</div>
{% endfor %}

{% endfor %}

<script>
async function strongCopyBibtexLocal(btnEl) {
  const statusEl = btnEl.parentElement.querySelector('[data-bibtex-status]');
  const bib = btnEl.getAttribute('data-bibtex') || '';
  const txt = new DOMParser().parseFromString(bib, "text/html").documentElement.textContent;

  try {
    if (statusEl) statusEl.textContent = "Copying…";
    await navigator.clipboard.writeText(txt);
    if (statusEl) statusEl.textContent = "Copied!";
    setTimeout(() => { if (statusEl) statusEl.textContent = ""; }, 2000);
  } catch (e) {
    if (statusEl) statusEl.textContent = "Copy failed";
    setTimeout(() => { if (statusEl) statusEl.textContent = ""; }, 2000);
  }
}
</script>
