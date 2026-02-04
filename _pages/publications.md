---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 3
---

<style>
.pubs-year { margin-top: 1.1rem; }
.pub-item { padding: 0.35rem 0; border-bottom: 1px solid rgba(0,0,0,0.08); }
.pub-title { font-size: 0.95rem; font-weight: 600; line-height: 1.2; margin: 0; }
.pub-meta { font-size: 0.82rem; opacity: 0.75; margin-top: 0.15rem; }
.pub-actions { margin-top: 0.35rem; display: flex; gap: 0.35rem; flex-wrap: wrap; align-items: center; }
.pub-actions .btn { padding: 0.12rem 0.45rem; font-size: 0.78rem; line-height: 1.2; }
.pub-status { font-size: 0.78rem; opacity: 0.75; margin-left: 0.15rem; }
</style>

{% assign pubs = site.data.publications %}

{% for block in pubs %}
<h2 class="pubs-year">{{ block.year }}</h2>

{% for p in block.papers %}
<div class="pub-item">
  <p class="pub-title">{{ p.title }}</p>

  <div class="pub-meta">
    {% if p.date %}{{ p.date }}{% endif %}
    {% if p.authors %}{% if p.date %} · {% endif %}{{ p.authors }}{% endif %}
  </div>

  <div class="pub-actions">
    {% if p.arxiv %}
      <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener"
         href="https://arxiv.org/abs/{{ p.arxiv }}">arXiv</a>

      {% if p.doi %}
        <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
           href="https://doi.org/{{ p.doi }}">DOI</a>
      {% elsif p.inspire %}
        <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
           href="{{ p.inspire }}">Record</a>
      {% endif %}

      <button class="btn btn-sm btn-outline-success" type="button"
              onclick="strongCopyBibtex('{{ p.arxiv }}', this)">
        Copy BibTeX
      </button>

      <span class="pub-status" data-bibtex-status></span>
    {% endif %}
  </div>
</div>
{% endfor %}

{% endfor %}

<script>
async function strongCopyBibtex(arxivId, btnEl) {
  const statusEl = btnEl.parentElement.querySelector('[data-bibtex-status]');
  const url = `https://inspirehep.net/api/arxiv/${arxivId}?format=bibtex`;

  try {
    if (statusEl) statusEl.textContent = "Fetching…";
    const r = await fetch(url, { headers: { "Accept": "text/plain" } });
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const bib = await r.text();

    await navigator.clipboard.writeText(bib);
    if (statusEl) statusEl.textContent = "Copied!";
    setTimeout(() => { if (statusEl) statusEl.textContent = ""; }, 2000);
  } catch (e) {
    if (statusEl) statusEl.textContent = "Copy failed (opening BibTeX)…";
    window.open(url, "_blank", "noopener");
    setTimeout(() => { if (statusEl) statusEl.textContent = ""; }, 2500);
  }
}
</script>
