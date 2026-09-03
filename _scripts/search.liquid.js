---
permalink: /assets/js/search-data.js
---
const ninja = document.querySelector("ninja-keys");

ninja.data = [
  {
    id: "nav-home",
    title: "Home",
    section: "Navigation",
    handler: () => {
      window.location.href = "{{ '/' | relative_url }}";
    },
  },
  {%- assign sorted_pages = site.pages | sort: "nav_order" -%}
  {%- for nav_page in sorted_pages -%}
    {%- if nav_page.nav -%}
      {
        id: "nav-{{ nav_page.title | slugify }}",
        title: {{ nav_page.title | jsonify }},
        description: {{ nav_page.description | strip_html | strip_newlines | jsonify }},
        section: "Navigation",
        handler: () => {
          window.location.href = "{{ nav_page.url | relative_url }}";
        },
      },
    {%- endif -%}
  {%- endfor -%}
  {% if site.enable_darkmode %}
    {
      id: "light-theme",
      title: "Change theme to light",
      section: "Theme",
      handler: () => setThemeSetting("light"),
    },
    {
      id: "dark-theme",
      title: "Change theme to dark",
      section: "Theme",
      handler: () => setThemeSetting("dark"),
    },
    {
      id: "system-theme",
      title: "Use system theme",
      section: "Theme",
      handler: () => setThemeSetting("system"),
    },
  {% endif %}
];
