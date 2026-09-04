---
layout: page
title: News
permalink: /news/
nav: true
nav_order: 5
---

<style>
.news-list {
  border-top: 1px solid var(--global-divider-color);
}

.news-row {
  display: grid;
  grid-template-columns: minmax(7rem, 0.8fr) minmax(10rem, 1.25fr) minmax(16rem, 2.5fr) minmax(9rem, 1fr);
  gap: 1.5rem;
  align-items: start;
  padding: 1.25rem 0;
  border-bottom: 1px solid var(--global-divider-color);
}

.news-header {
  padding: 0.65rem 0;
  color: var(--global-text-color-light);
  font-size: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.04em;
  text-transform: uppercase;
}

.news-header span {
  color: inherit;
}

.news-date {
  color: var(--global-text-color-light);
  white-space: nowrap;
}

.news-name {
  font-weight: 500;
}

.news-description {
  margin: 0;
}

.news-image {
  display: block;
  width: 100%;
  max-height: 9rem;
  object-fit: cover;
  border-radius: 0.5rem;
  cursor: zoom-in;
}

@media (max-width: 767.98px) {
  .news-header {
    display: none;
  }

  .news-row {
    grid-template-columns: 1fr;
    gap: 0.45rem;
  }

  .news-image {
    width: min(100%, 24rem);
    margin-top: 0.5rem;
  }
}
</style>

<div class="news-list">
  <div class="news-row news-header" aria-hidden="true">
    <span>Date</span>
    <span>Event</span>
  </div>

{% assign news_items = site.data.news | sort: 'date' | reverse %}
{% for item in news_items %}

<article class="news-row">
<time class="news-date" datetime="{{ item.date | date: '%Y-%m-%d' }}">{{ item.date | date: '%-d %B %Y' }}</time>
<div class="news-name">{{ item.name }}</div>
<p class="news-description">{{ item.description }}</p>
<div>
{% if item.image %}
<img
            class="news-image"
            src="{{ item.image | prepend: '/assets/img/news/' | relative_url }}"
            alt="{{ item.image_alt | escape }}"
            loading="lazy"
            data-zoomable
          >
{% endif %}
</div>
</article>
{% endfor %}

</div>
