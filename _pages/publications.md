---
layout: page
title: Publications
permalink: /publications/
nav: true
nav_order: 3
---

{% assign pubs = site.data.publications %}

{% for block in pubs %}
## {{ block.year }}

{% for p in block.papers %}
<div class="card p-3 mb-3" style="border-radius: 12px;">
  <div class="row align-items-center">
    {% if p.image %}
    <div class="col-md-3 mb-2 mb-md-0">
      <img src="{{ site.baseurl }}{{ p.image }}" alt="paper image" style="width:100%; border-radius: 10px;">
    </div>
    <div class="col-md-9">
    {% else %}
    <div class="col-12">
    {% endif %}

      <div style="font-size: 1.05rem; font-weight: 600; line-height: 1.25;">
        {{ p.title }}
      </div>

      {% if p.authors %}
      <div class="text-muted" style="margin-top: 6px;">
        {{ p.authors }}
      </div>
      {% endif %}

      {% if p.date %}
      <div class="text-muted" style="margin-top: 4px;">
        {{ p.date }}
      </div>
      {% endif %}

      <div style="margin-top: 10px;">
        {% if p.arxiv %}
        <a class="btn btn-sm btn-outline-primary" target="_blank" rel="noopener"
           href="https://arxiv.org/abs/{{ p.arxiv }}">
          arXiv
        </a>
        {% endif %}
      </div>

    </div>
  </div>
</div>
{% endfor %}

{% endfor %}
