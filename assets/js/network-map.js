(() => {
  const mapElement = document.getElementById("strong-map");
  const listElement = document.getElementById("node-list");
  if (!mapElement || !listElement) return;

  const map = L.map(mapElement, { scrollWheelZoom: false }).setView([30, 10], 2);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 18,
    attribution: "&copy; OpenStreetMap contributors",
  }).addTo(map);

  const roleColor = (role) => {
    if (role === "coordinator") return "#2e7d32";
    if (role === "partner") return "#c62828";
    return "#1565c0";
  };

  const escapeHtml = (value) =>
    String(value || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");

  const getPerson = (properties) => ({
    name: properties.person || properties.coordinator || properties.local_coordinator || "",
    url: properties.person_url || properties.coordinator_url || properties.local_coordinator_url || properties.website || properties.url || "",
  });

  const personHtml = (person) => {
    if (!person.name) return "";
    if (!person.url) return `<span class="strong-person">Local Coordinator: ${escapeHtml(person.name)}</span>`;

    return `<span class="strong-person">Local Coordinator: <a href="${escapeHtml(person.url)}" target="_blank" rel="noopener">${escapeHtml(person.name)}</a></span>`;
  };

  const rolePillHtml = (properties) => {
    const color = roleColor(properties.role);
    const label = properties.role_label || properties.role || "";
    return `<span class="strong-pill" style="background:${color};">${escapeHtml(label)}</span>`;
  };

  fetch(mapElement.dataset.geojsonUrl)
    .then((response) => {
      if (!response.ok) throw new Error(`Network data request failed: ${response.status}`);
      return response.json();
    })
    .then((featureCollection) => {
      const markers = [];

      featureCollection.features.forEach((feature) => {
        const properties = feature.properties || {};
        const coordinates = feature.geometry.coordinates;
        const color = roleColor(properties.role);
        const person = getPerson(properties);

        const marker = L.circleMarker([coordinates[1], coordinates[0]], {
          radius: properties.role === "coordinator" ? 9 : 7,
          weight: 2,
          color,
          fillColor: color,
          fillOpacity: 0.85,
        }).addTo(map);

        const location = [properties.city, properties.country].filter(Boolean).join(", ");
        const popup = [
          `<div style="margin-bottom:6px;">${rolePillHtml(properties)}</div>`,
          `<strong>${escapeHtml(properties.institution)}</strong>`,
          properties.department ? `<br>${escapeHtml(properties.department)}` : "",
          person.name ? `<br><span class="strong-person">Local Coordinator: ${escapeHtml(person.name)}</span>` : "",
          location ? `<br>${escapeHtml(location)}` : "",
        ].join("");

        marker.bindPopup(`<div>${popup}</div>`);
        markers.push(marker);

        const item = document.createElement("div");
        item.className = "strong-node";
        item.tabIndex = 0;
        item.setAttribute("role", "button");

        const coordinator = personHtml(person) || '<span class="strong-person" style="opacity:0.75">Local Coordinator: (missing)</span>';

        item.innerHTML = `
          <div style="margin-bottom:6px;">${rolePillHtml(properties)}</div>
          <div class="strong-node-title">${escapeHtml(properties.institution)}</div>
          <div class="strong-node-meta">
            ${properties.department ? `${escapeHtml(properties.department)}<br>` : ""}
            ${coordinator}<br>
            <span>${escapeHtml(location)}</span>
          </div>`;

        const openMarker = () => {
          map.setView([coordinates[1], coordinates[0]], 6);
          marker.openPopup();
        };
        item.addEventListener("click", openMarker);
        item.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            openMarker();
          }
        });

        listElement.appendChild(item);
      });

      if (markers.length) map.fitBounds(L.featureGroup(markers).getBounds().pad(0.25));
    })
    .catch((error) => {
      console.error(error);
      listElement.innerHTML = '<div class="text-danger">Failed to load network data.</div>';
    });
})();
