---
layout: page
title: Network
permalink: /network/
nav: true
nav_order: 3
---

## STRONG Action Network

<div class="row">
  <div class="col-md-8">
    <div id="strong-map" style="height: 560px; border-radius: 14px; overflow: hidden;"></div>
    <div id="strong-map-legend" style="margin-top: 0.75rem; font-size: 0.9rem;"></div>
  </div>
  <div class="col-md-4">
    <h5 class="mt-3 mt-md-0">Nodes</h5>
    <p style="font-size: 0.9rem;">
      Click on a node in the list to focus the map, or click a marker to see details.
    </p>
    <ul id="strong-map-sidebar" style="list-style: none; padding-left: 0; max-height: 520px; overflow-y: auto; font-size: 0.9rem;"></ul>
  </div>
</div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
(function () {
  const map = L.map('strong-map', { scrollWheelZoom: false }).setView([25, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const dataUrl = "{{ site.baseurl }}/assets/data/nodes.geojson";

  const roleStyle = function (role) {
    const r = (role || "").toLowerCase();

    // all blue for coordinator + beneficiary, red for partner
    if (r === "coordinator") {
      return { color: "#0050b3", fillColor: "#0066ff", radius: 9, weight: 3 };
    }
    if (r === "partner") {
      return { color: "#b30000", fillColor: "#ff4d4f", radius: 7, weight: 2 };
    }
    // default: beneficiary
    return { color: "#0050b3", fillColor: "#0066ff", radius: 7, weight: 2 };
  };

  fetch(dataUrl)
    .then(r => {
      if (!r.ok) throw new Error("Failed to load " + dataUrl + " (" + r.status + ")");
      return r.json();
    })
    .then(geojson => {
      const sidebarEl = document.getElementById('strong-map-sidebar');
      const markers = [];

      const layer = L.geoJSON(geojson, {
        pointToLayer: (feature, latlng) => {
          const style = roleStyle(feature.properties && feature.properties.role);
          return L.circleMarker(latlng, Object.assign({
            opacity: 1,
            fillOpacity: 0.8
          }, style));
        },
        onEachFeature: (feature, l) => {
          const p = feature.properties || {};
          const name = p.name || "Node";
          const dept = p.department;
          const coord = p.local_coordinator;
          const role = p.role || "Beneficiary";
          const loc = [p.city, p.country].filter(Boolean).join(", ");
          const address = p.address;

          let html = `<strong>${name}</strong>`;
          if (dept) html += `<br>${dept}`;
          if (coord) html += `<br><em>${coord}</em>`;
          html += `<br>${role}`;
          if (loc) html += `<br>${loc}`;
          if (address) html += `<br><span style="font-size: 0.85em; color: #555;">${address}</span>`;

          l.bindPopup(html);

          // sidebar entry
          const li = document.createElement('li');
          li.style.cursor = 'pointer';
          li.style.padding = '4px 0';
          li.innerHTML = `
            <strong>${name}</strong><br>
            <span style="color:#555;">${loc || role}</span><br>
            <span style="font-size:0.8em;color:#777;">${role}${coord ? " · " + coord : ""}</span>
          `;
          li.addEventListener('click', () => {
            const latlng = l.getLatLng();
            map.setView(latlng, 4, { animate: true });
            l.openPopup();
          });
          sidebarEl.appendChild(li);

          markers.push(l);
        }
      }).addTo(map);

      // Fit to all nodes
      try {
        if (markers.length > 1) {
          const group = L.featureGroup(markers);
          map.fitBounds(group.getBounds().pad(0.3));
        } else if (markers.length === 1) {
          map.setView(markers[0].getLatLng(), 4);
        }
      } catch (e) {
        console.error(e);
      }

      // Legend
      const legendEl = document.getElementById('strong-map-legend');
      legendEl.innerHTML = `
        <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#0066ff;border:2px solid #0050b3;margin-right:6px;"></span>
        Beneficiary / Coordinator
        &nbsp;&nbsp;
        <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff4d4f;border:2px solid #b30000;margin-right:6px;"></span>
        Partner
      `;
    })
    .catch(err => {
      console.error(err);
      document.getElementById('strong-map').innerHTML =
        `<div style="padding:12px;border:1px solid #ddd;border-radius:12px;">
          Could not load map data. Check <code>${dataUrl}</code>.
        </div>`;
    });
})();
</script>
