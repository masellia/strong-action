---
layout: page
title: Network
permalink: /network/
nav: true
---

<div class="row">
  <div class="col-md-4">
    <div class="card p-3 mb-3">
      <h4 class="mb-2">STRONG Network</h4>

      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#2ca02c;margin-right:6px;"></span>
        Coordinator
      </div>
      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#1f77b4;margin-right:6px;"></span>
        Beneficiary
      </div>
      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#d62728;margin-right:6px;"></span>
        Partner
      </div>

      <hr/>

      <div class="small text-muted mb-2">Click a node on the map to see details.</div>
      <div id="node-list" class="small" style="max-height:55vh; overflow:auto;"></div>
    </div>
  </div>

  <div class="col-md-8">
    <div id="strong-map" style="height: 70vh; border-radius: 12px; overflow: hidden;"></div>
  </div>
</div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<style>
  /* keep controls minimal and clean */
  .leaflet-control-attribution { font-size: 10px; }
</style>

<script>
(function () {
  const geojsonUrl = "{{ site.baseurl }}/assets/data/nodes.geojson";

  const map = L.map("strong-map", { scrollWheelZoom: false }).setView([35, 5], 2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  function roleColor(role) {
    if (role === "coordinator") return "#2ca02c"; // green
    if (role === "partner") return "#d62728";     // red
    return "#1f77b4";                              // beneficiary (default blue)
  }

  function formatPopup(p) {
    const lines = [];
    lines.push(`<strong>${p.name || p.institution || "Node"}</strong>`);
    if (p.institution && p.institution !== p.name) lines.push(p.institution);
    if (p.department) lines.push(p.department);
    if (p.coordinator) lines.push(`<em>Local coordinator:</em> ${p.coordinator}`);
    const place = [p.city, p.country].filter(Boolean).join(", ");
    if (place) lines.push(place);
    if (p.role) lines.push(`<span class="badge badge-secondary">${p.role}</span>`);
    return `<div style="line-height:1.35">${lines.join("<br/>")}</div>`;
  }

  fetch(geojsonUrl)
    .then(r => r.json())
    .then(fc => {
      const listEl = document.getElementById("node-list");
      listEl.innerHTML = "";

      const markers = [];

      fc.features.forEach(f => {
        const p = f.properties || {};
        const coords = f.geometry && f.geometry.coordinates;
        if (!coords || coords.length < 2) return;

        const lon = coords[0], lat = coords[1];
        const color = roleColor(p.role);

        const marker = L.circleMarker([lat, lon], {
          radius: 7,
          weight: 2,
          color: color,
          fillColor: color,
          fillOpacity: 0.85
        }).addTo(map);

        marker.bindPopup(formatPopup(p));
        markers.push(marker);

        const item = document.createElement("div");
        item.style.cursor = "pointer";
        item.style.padding = "6px 0";
        item.innerHTML = `
          <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${color};margin-right:6px;"></span>
          <strong>${p.name || p.institution || "Node"}</strong>
          <div class="text-muted" style="margin-left:16px;">
            ${(p.city || "")}${p.city && p.country ? ", " : ""}${(p.country || "")}
          </div>
        `;
        item.addEventListener("click", () => {
          map.setView([lat, lon], 6);
          marker.openPopup();
        });
        listEl.appendChild(item);
      });

      if (markers.length) {
        const group = L.featureGroup(markers);
        map.fitBounds(group.getBounds().pad(0.25));
      }
    })
    .catch(err => {
      console.error("Failed to load nodes.geojson", err);
      document.getElementById("node-list").innerHTML =
        "<div class='text-danger'>Failed to load network data.</div>";
    });
})();
</script>
