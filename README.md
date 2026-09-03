# STRONG website

Website for the STRONG research network, built with Jekyll and deployed to GitHub Pages.

## Local development

```sh
docker compose up --build
```

The site is available at <http://localhost:8080/strong-action/>.

## Verification

```sh
npm ci
npx prettier . --check
pre-commit run --all-files
JEKYLL_ENV=production bundle exec jekyll build --trace
```

Publication data is generated from `_data/publications_arxiv.txt`:

```sh
python3 bin/update_publications.py
```
