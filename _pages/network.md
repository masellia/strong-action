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

    <div class="d-flex flex-wrap align-items-center mb-2" style="gap: 8px;">
      <div class="btn-group btn-group-sm" role="group" aria-label="Filter nodes">
        <button type="button" class="btn btn-outline-primary" data-strong-filter="all">All</button>
        <button type="button" class="btn btn-outline-primary" data-strong-filter="beneficiary">Beneficiaries</button>
        <button type="button" class="btn btn-outline-danger" data-strong-filter="partner">Partners</button>
      </div>

      <button type="button" class="btn btn-sm btn-outline-secondary" id="strong-download-geojson">Download GeoJSON</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" id="strong-download-csv">Download CSV</button>
    </div>

    <div id="strong-map" style="height: 560px; border-radius: 14px; overflow: hidden;"></div>
    <div id="strong-map-legend" style="margin-top: 0.75rem; font-size: 0.9rem;"></div>

  </div>

  <div class="col-md-4">
    <h5 class="mt-3 mt-md-0">Nodes</h5>

    <input id="strong-sidebar-search" class="form-control form-control-sm mb-2" type="text" placeholder="Search (name, city, country, coordinator)…" />

    <div id="strong-sidebar-meta" style="font-size: 0.9rem; color: #555; margin-bottom: 0.5rem;"></div>

    <div id="strong-map-sidebar" style="max-height: 520px; overflow-y: auto;"></div>
  </div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
(function () {
  const map = L.map('strong-map', { scrollWheelZoom: false }).setView([25, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 18,
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  const dataUrl = "{{ site.baseurl }}/assets/data/nodes.geojson";

  const roleStyle = (role) => {
    const r = (role || "").toLowerCase();
    if (r === "coordinator") return { color: "#0050b3", fillColor: "#0066ff", radius: 9, weight: 3, fillOpacity: 0.85 };
    if (r === "partner")     return { color: "#b30000", fillColor: "#ff4d4f", radius: 7, weight: 2, fillOpacity: 0.85 };
    return { color: "#0050b3", fillColor: "#0066ff", radius: 7, weight: 2, fillOpacity: 0.85 };
  };

  const normalizeRoleBucket = (role) => {
    const r = (role || "").toLowerCase();
    if (r === "partner") return "partner";
    // coordinator is grouped with beneficiaries for filtering, because both are blue
    return "beneficiary";
  };

  const escapeHtml = (s) => String(s || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");

  const sidebarEl = document.getElementById('strong-map-sidebar');
  const metaEl = document.getElementById('strong-sidebar-meta');
  const searchEl = document.getElementById('strong-sidebar-search');

  let allFeatures = [];
  let currentFilter = "all";
  let currentSearch = "";

  const markers = []; // { feature, layer, bucket, country, searchText }

  function setActiveFilterButton(filter) {
    document.querySelectorAll('[data-strong-filter]').forEach(btn => {
      btn.classList.toggle('active', btn.getAttribute('data-strong-filter') === filter);
    });
  }

  function buildPopupHtml(p) {
    const name = p.name || "Node";
    const dept = p.department;
    const coord = p.local_coordinator;
    const role = p.role || "Beneficiary";
    const loc = [p.city, p.country].filter(Boolean).join(", ");
    const address = p.address;
    const url = p.url;

    let html = `<strong>${escapeHtml(name)}</strong>`;
    if (dept) html += `<br>${escapeHtml(dept)}`;

    if (coord) {
      if (url) html += `<br><em><a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(coord)}</a></em>`;
      else html += `<br><em>${escapeHtml(coord)}</em>`;
    }

    html += `<br>${escapeHtml(role)}`;
    if (loc) html += `<br>${escapeHtml(loc)}`;
    if (address) html += `<br><span style="font-size: 0.85em; color: #555;">${escapeHtml(address)}</span>`;
    return html;
  }

  function downloadBlob(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  }

  function toCSV(features) {
    const header = ["role","name","department","local_coordinator","url","address","city","country","lon","lat"];
    const rows = [header];

    for (const f of features) {
      const p = f.properties || {};
      const coords = (f.geometry && f.geometry.coordinates) || [null, null];
      const row = [
        p.role || "",
        p.name || "",
        p.department || "",
        p.local_coordinator || "",
        p.url || "",
        p.address || "",
        p.city || "",
        p.country || "",
        coords[0] ?? "",
        coords[1] ?? ""
      ].map(v => `"${String(v).replaceAll('"','""')}"`);
      rows.push(row);
    }
    return rows.map(r => r.join(",")).join("\n");
  }

  function applyUI() {
    // filter markers by role + search
    const visible = [];
    for (const m of markers) {
      const roleOk = (currentFilter === "all") || (m.bucket === currentFilter);
      const searchOk = !currentSearch || m.searchText.includes(currentSearch);
      const show = roleOk && searchOk;
      if (show) visible.push(m);

      // show/hide layer
      if (show) {
        if (!map.hasLayer(m.layer)) m.layer.addTo(map);
      } else {
        if (map.hasLayer(m.layer)) map.removeLayer(m.layer);
      }
    }

    // rebuild sidebar grouped by country
    sidebarEl.innerHTML = "";
    const groups = new Map(); // country => [m...]
    for (const m of visible) {
      const c = m.country || "Unknown";
      if (!groups.has(c)) groups.set(c, []);
      groups.get(c).push(m);
    }

    // sort countries, then within country by role/name
    const countries = Array.from(groups.keys()).sort((a,b) => a.localeCompare(b));
    for (const country of countries) {
      const header = document.createElement("div");
      header.style.margin = "10px 0 6px 0";
      header.style.padding = "6px 8px";
      header.style.background = "rgba(0,0,0,0.04)";
      header.style.borderRadius = "10px";
      header.innerHTML = `<strong>${escapeHtml(country)}</strong> <span style="color:#666;">(${groups.get(country).length})</span>`;
      sidebarEl.appendChild(header);

      const ul = document.createElement("ul");
      ul.style.listStyle = "none";
      ul.style.paddingLeft = "0";
      ul.style.marginBottom = "0";

      groups.get(country)
        .sort((a,b) => {
          // beneficiary/coordinator first, then partners; then by name
          if (a.bucket !== b.bucket) return a.bucket.localeCompare(b.bucket);
          const an = (a.feature.properties?.name || "");
          const bn = (b.feature.properties?.name || "");
          return an.localeCompare(bn);
        })
        .forEach(m => {
          const p = m.feature.properties || {};
          const li = document.createElement("li");
          li.style.cursor = "pointer";
          li.style.padding = "6px 4px";
          li.style.borderBottom = "1px solid rgba(0,0,0,0.05)";

          const name = p.name || "Node";
          const city = p.city || "";
          const role = p.role || "";
          const coord = p.local_coordinator || "";
          const url = p.url || "";

          const coordHtml = coord
            ? (url ? `<a href="${escapeHtml(url)}" target="_blank" rel="noopener">${escapeHtml(coord)}</a>` : escapeHtml(coord))
            : "";

          li.innerHTML = `
            <div><strong>${escapeHtml(name)}</strong></div>
            <div style="color:#555; font-size:0.88em;">${escapeHtml(city)}${city ? ", " : ""}${escapeHtml(country)}</div>
            <div style="color:#777; font-size:0.78em;">${escapeHtml(role)}${coordHtml ? " · " + coordHtml : ""}</div>
          `;

          li.addEventListener("click", () => {
            const latlng = m.layer.getLatLng();
            map.setView(latlng, 4, { animate: true });
            m.layer.openPopup();
          });

          ul.appendChild(li);
        });

      sidebarEl.appendChild(ul);
    }

    // meta
    const total = markers.length;
    const shown = visible.length;
    metaEl.textContent = `Showing ${shown} / ${total} nodes`;

    // fit bounds on visible nodes (only if >0)
    try {
      if (visible.length > 1) {
        const group = L.featureGroup(visible.map(v => v.layer));
        map.fitBounds(group.getBounds().pad(0.3));
      } else if (visible.length === 1) {
        map.setView(visible[0].layer.getLatLng(), 4);
      }
    } catch (e) {}
  }

  fetch(dataUrl)
    .then(r => {
      if (!r.ok) throw new Error("Failed to load " + dataUrl + " (" + r.status + ")");
      return r.json();
    })
    .then(geojson => {
      allFeatures = (geojson && geojson.features) ? geojson.features : [];

      // build layers
      for (const f of allFeatures) {
        const p = f.properties || {};
        const role = p.role || "Beneficiary";
        const bucket = normalizeRoleBucket(role);
        const country = p.country || "Unknown";
        const coords = (f.geometry && f.geometry.coordinates) || [0,0];
        const latlng = L.latLng(coords[1], coords[0]);

        const layer = L.circleMarker(latlng, roleStyle(role));
        layer.bindPopup(buildPopupHtml(p));

        const searchText = [
          p.name, p.department, p.local_coordinator, p.city, p.country, p.role
        ].filter(Boolean).join(" ").toLowerCase();

        markers.push({ feature: f, layer, bucket, country, searchText });
      }

      // legend
      document.getElementById('strong-map-legend').innerHTML = `
        <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#0066ff;border:2px solid #0050b3;margin-right:6px;"></span>
        Beneficiary / Coordinator
        &nbsp;&nbsp;
        <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#ff4d4f;border:2px solid #b30000;margin-right:6px;"></span>
        Partner
      `;

      // default filter state
      setActiveFilterButton("all");
      applyUI();

      // wire filter buttons
      document.querySelectorAll('[data-strong-filter]').forEach(btn => {
        btn.addEventListener("click", () => {
          currentFilter = btn.getAttribute('data-strong-filter');
          setActiveFilterButton(currentFilter);
          applyUI();
        });
      });

      // search
      searchEl.addEventListener("input", () => {
        currentSearch = searchEl.value.trim().toLowerCase();
        applyUI();
      });

      // downloads
      document.getElementById("strong-download-geojson").addEventListener("click", () => {
        downloadBlob("strong-nodes.geojson", JSON.stringify({ type: "FeatureCollection", features: allFeatures }, null, 2), "application/geo+json");
      });

      document.getElementById("strong-download-csv").addEventListener("click", () => {
        downloadBlob("strong-nodes.csv", toCSV(allFeatures), "text/csv;charset=utf-8");
      });
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
