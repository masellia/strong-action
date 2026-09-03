# STRONG Website

- This is a Jekyll site deployed by `.github/workflows/pages.yml`.
- The intended routes are Home, About, Network, Publications, Contacts, and 404.
- Run `JEKYLL_ENV=production bundle exec jekyll build --trace` before committing.
- Run `npx prettier . --check` and `pre-commit run --all-files` for formatting and repository checks.
- Update publication data with `python3 bin/update_publications.py`; it contacts INSPIRE HEP.
- Network data belongs in `assets/data/nodes.geojson`.
- Do not add generated `_site`, caches, credentials, or private keys.
