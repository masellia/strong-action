---
layout: page
title: Network
permalink: /network/
body_class: page-network
nav: true
nav_order: 3
leaflet: true
---

<style>
.network-text {
  text-align: justify;
  text-justify: inter-word;
  hyphens: auto;
}
</style>

<div class="network-text" markdown="1">

The **STRONG network** brings together a distributed network of research groups with complementary expertise in gravitational physics, compact objects, and strong-field tests of gravity.

A central element of the network is the **secondment programme**, which allows senior researchers
as well as early-career researchers (PhD students and postdoctoral fellows) from European
beneficiary institutions to undertake research visits at partner nodes abroad.
These secondments are designed to promote the transfer of knowledge, methodologies, and technical skills across institutions and geographical regions.

The network is organised around:

- **Beneficiaries**, which form the core of the consortium and host the main research activities;
- **Partners**, including leading research centres outside Europe, which provide specialised expertise and an international research environment.

Use the interactive map and sidebar below to explore the individual nodes and local coordinators.

</div>

<style>
  .strong-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 2px 8px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #fff;
    line-height: 1.2;
  }
  .strong-person a {
    text-decoration: underline !important;
    font-weight: 600;
  }
  /* Force links to look like links even if theme overrides */
  .strong-person a:link,
  .strong-person a:visited {
    color: #0d6efd !important;
  }
  .strong-node {
    margin-bottom: 12px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(0,0,0,0.08);
    cursor: pointer;
  }
  .strong-node-title { font-weight: 700; }
  .strong-node-meta { color: #555; font-size: 0.9rem; margin-top: 2px; }
</style>

<div class="row">
  <div class="col-md-4">
    <div class="card p-3 mb-3">
      <h4 class="mb-2">STRONG Network</h4>

      <div class="mb-2">
        <span class="strong-pill" style="background:#2e7d32;">Coordinator</span>
      </div>
      <div class="mb-2">
        <span class="strong-pill" style="background:#1565c0;">Beneficiary</span>
      </div>
      <div class="mb-2">
        <span class="strong-pill" style="background:#c62828;">Partner</span>
      </div>

      <hr/>
      <div id="node-list" style="max-height:60vh; overflow:auto;"></div>
    </div>

  </div>

  <div class="col-md-8">
    <div
      id="strong-map"
      data-geojson-url="{{ site.baseurl }}/assets/data/nodes.geojson"
      style="height: 70vh; border-radius: 12px;"
    ></div>
  </div>
</div>
