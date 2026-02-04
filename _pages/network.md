---
layout: page
title: Network
permalink: /network/
nav: true
nav_order: 3
---

## Nodes & partners

<div id="strong-map" style="height: 560px; border-radius: 14px; overflow: hidden;"></div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
(function () {
  const map = L.map('strong-map', { scrollWheelZoom: false }).setView([20, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const dataUrl = "{{ site.baseurl }}/assets/data/nodes.geojson";

  fetch(dataUrl)
    .then(r => { if (!r.ok) throw new Error(r.status); return r.json(); })
    .then(geojson => {
      const layer = L.geoJSON(geojson, {
        pointToLayer: (f, latlng) => L.circleMarker(latlng, { radius: 7, weight: 2 }),
        onEachFeature: (f, l) => {
          const p = f.properties || {};
          const title = `<strong>${p.name || "Node"}</strong>`;
          const meta = [p.role, [p.city, p.country].filter(Boolean).join(", ")].filter(Boolean).join(" — ");
          const link = p.url ? `<br><a href="${p.url}" target="_blank" rel="noopener">Website</a>` : "";
          l.bindPopup(`${title}${meta ? "<br>" + meta : ""}${link}`);
        }
      }).addTo(map);
      if (layer.getLayers().length > 1) map.fitBounds(layer.getBounds().pad(0.25));
    })
    .catch(() => {
      document.getElementById('strong-map').innerHTML =
        `<div style="padding:12px;border:1px solid #ddd;border-radius:12px;">
          Could not load <code>${dataUrl}</code>
        </div>`;
    });
})();
</script>
