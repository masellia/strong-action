---
layout: page
title: Network
permalink: /network/
nav: true
nav_order: 3
---

<div class="row">
  <div class="col-md-4">
    <div class="card p-3 mb-3">
      <h4 class="mb-2">STRONG Network</h4>

      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#2e7d32;margin-right:6px;"></span>
        Coordinator
      </div>
      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#1565c0;margin-right:6px;"></span>
        Beneficiary
      </div>
      <div class="mb-2">
        <span style="display:inline-block;width:12px;height:12px;border-radius:50%;background:#c62828;margin-right:6px;"></span>
        Partner
      </div>

      <hr/>
      <div id="node-list" style="font-size:0.9rem; max-height:60vh; overflow:auto;"></div>
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

  fetch(geojsonUrl)
    .then(r => r.json())
    .then(fc => {
      const listEl = document.getElementById("node-list");
      const markers = [];

      fc.features.forEach(f => {
        const p = f.properties || {};
        const coords = f.geometry.coordinates;
        const color = roleColor(p.role);

        const marker = L.circleMarker([coords[1], coords[0]], {
          radius: p.role === "coordinator" ? 9 : 7,
          weight: 2,
          color: color,
          fillColor: color,
          fillOpacity: 0.85
        }).addTo(map);

        let popup = "<strong>" + esc(p.institution || "") + "</strong>";
        if (p.department) popup += "<br/>" + esc(p.department);

        if (p.person) {
          if (p.person_url) {
            popup += "<br/><a href='" + esc(p.person_url) + "' target='_blank' rel='noopener'>" + esc(p.person) + "</a>";
          } else {
            popup += "<br/>" + esc(p.person);
          }
        }

        popup += "<br/>" + esc([p.city, p.country].filter(Boolean).join(", "));
        popup += "<br/><em>" + esc(p.role_label || p.role) + "</em>";

        marker.bindPopup(popup);
        markers.push(marker);

        // Sidebar entry
        const div = document.createElement("div");
        div.style.cursor = "pointer";
        div.style.marginBottom = "8px";
        div.innerHTML =
          "<strong>" + esc(p.institution || "") + "</strong><br/>" +
          (p.person_url
            ? "<a href='" + esc(p.person_url) + "' target='_blank' rel='noopener'>" + esc(p.person || "") + "</a>"
            : esc(p.person || "")
          ) +
          "<br/><span style='color:#555'>" + esc([p.city, p.country].filter(Boolean).join(", ")) + "</span>";

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
