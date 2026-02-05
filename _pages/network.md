---
layout: page
title: Network 
permalink: /network/
body_class: page-network
nav: true
nav_order: 3
header: false
---

<style>
.network-text {
  text-align: justify;
}

.network-text p {
  margin-bottom: 0.9rem;
}

.network-text ul {
  margin-left: 1.2rem;
  margin-bottom: 0.9rem;
}

.network-text strong {
  font-weight: 600;
}
</style>


### The STRONG Network

The STRONG Action brings together a distributed network of research groups with complementary expertise in gravitational physics, compact objects, and strong-field tests of gravity.

A central element of the network is the **secondment programme**, which allows senior researchers 
as well as early-career researchers (PhD students and postdoctoral fellows) from European 
beneficiary institutions to undertake research visits at partner nodes abroad. 
These secondments are designed to promote the transfer of knowledge, methodologies, and technical skills across institutions and geographical regions.

The network is organised around:
- **Beneficiaries**, which form the core of the consortium and host the main research activities;
- **Partners**, including leading research centres outside Europe, which provide specialised expertise and an international research environment.

Use the interactive map and sidebar below to explore the individual nodes and local coordinators.


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
    <div id="strong-map" style="height: 70vh; border-radius: 12px;"></div>
  </div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
(function () {
  const geojsonUrl = "{{ site.baseurl }}/assets/data/nodes.geojson";

  const map = L.map("strong-map", { scrollWheelZoom: false }).setView([30, 10], 2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  function roleColor(role) {
    if (role === "coordinator") return "#2e7d32";
    if (role === "partner") return "#c62828";
    return "#1565c0";
  }

  function esc(s) {
    return String(s || "")
      .replace(/&/g,"&amp;")
      .replace(/</g,"&lt;")
      .replace(/>/g,"&gt;")
      .replace(/"/g,"&quot;");
  }

  // Accept multiple schemas (person/coordinator/local_coordinator + person_url/coordinator_url)
  function getPerson(p) {
    const name = p.person || p.coordinator || p.local_coordinator || "";
    const url  = p.person_url || p.coordinator_url || p.local_coordinator_url || p.website || p.url || "";
    return { name, url };
  }

  function personHtml(person) {
    if (!person.name) return "";
    if (person.url) {
      return "<span class='strong-person'>Local Coordinator: <a href='" + esc(person.url) +
             "' target='_blank' rel='noopener'>" + esc(person.name) + "</a></span>";
    }
    return "<span class='strong-person'>Local Coordinator: " + esc(person.name) + "</span>";
  }

  function rolePillHtml(p) {
    const color = roleColor(p.role);
    const label = p.role_label || p.role || "";
    return "<span class='strong-pill' style='background:" + esc(color) + ";'>" + esc(label) + "</span>";
  }

  fetch(geojsonUrl)
    .then(r => r.json())
    .then(fc => {
      const listEl = document.getElementById("node-list");
      const markers = [];

      fc.features.forEach(f => {
        const p = f.properties || {};
        const coords = f.geometry.coordinates;
        const color = roleColor(p.role);
        const person = getPerson(p);

        const marker = L.circleMarker([coords[1], coords[0]], {
          radius: p.role === "coordinator" ? 9 : 7,
          weight: 2,
          color: color,
          fillColor: color,
          fillOpacity: 0.85
        }).addTo(map);

        // Popup
        let popup = "<div>";
        popup += "<div style='margin-bottom:6px;'>" + rolePillHtml(p) + "</div>";
        popup += "<strong>" + esc(p.institution || "") + "</strong>";
        if (p.department) popup += "<br/>" + esc(p.department);

        if (person.name) popup += "<br/><span class='strong-person'>Local Coordinator: " + esc(person.name) + "</span>";

        const loc = [p.city, p.country].filter(Boolean).join(", ");
        if (loc) popup += "<br/>" + esc(loc);
        popup += "</div>";

        marker.bindPopup(popup);
        markers.push(marker);

        // Sidebar entry
        const div = document.createElement("div");
        div.className = "strong-node";
        div.style.cursor = "pointer";

        const loc2 = esc([p.city, p.country].filter(Boolean).join(", "));
        const who = personHtml(person) || "<span class='strong-person' style='opacity:0.75'>Local Coordinator: (missing)</span>";

        div.innerHTML =
          "<div style='margin-bottom:6px;'>" + rolePillHtml(p) + "</div>" +
          "<div class='strong-node-title'>" + esc(p.institution || "") + "</div>" +
          "<div class='strong-node-meta'>" +
            (p.department ? (esc(p.department) + "<br/>") : "") +
            who + "<br/>" +
            "<span>" + loc2 + "</span>" +
          "</div>";

        div.onclick = function () {
          map.setView([coords[1], coords[0]], 6);
          marker.openPopup();
        };

        listEl.appendChild(div);
      });

      if (markers.length) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.25));
      }
    })
    .catch(err => {
      console.error(err);
      document.getElementById("node-list").innerHTML =
        "<div class='text-danger'>Failed to load network data.</div>";
    });
})();
</script>
