---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 3
---

<style>
.pubs-year { margin-top: 1.2rem; }
.pub-item { padding: 0.35rem 0; border-bottom: 1px solid rgba(0,0,0,0.08); }
.pub-title { font-size: 0.95rem; font-weight: 600; line-height: 1.2; margin: 0; }
.pub-meta { font-size: 0.82rem; opacity: 0.75; margin-top: 0.15rem; }
.pub-actions { margin-top: 0.35rem; }
.pub-actions .btn { padding: 0.12rem 0.45rem; font-size: 0.78rem; line-height: 1.2; }
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
    {% endif %}

    {% if p.doi %}
      <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
         href="https://doi.org/{{ p.doi }}">DOI</a>
    {% elsif p.html %}
      <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
         href="{{ p.html }}">HTML</a>
    {% elsif p.inspire %}
      <a class="btn btn-sm btn-outline-success" target="_blank" rel="noopener"
         href="{{ p.inspire }}">Record</a>
    {% endif %}
  </div>
</div>
{% endfor %}

{% endfor %}
