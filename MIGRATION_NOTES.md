# Migration notes (Wowchemy 5.1 -> HugoBlox)

Deploying to Netlify (existing site):
1. In your repo, create a branch (e.g. `hugoblox`) and replace the repo contents with this folder
   (delete the old `themes/`, `resources/`, `index.html`, `config.yaml`, `layouts/` etc.).
2. Push the branch. Netlify will build a branch deploy / preview - check it there first.
3. When happy, merge to `main`. Netlify settings: build command and Hugo/Node/Go versions come from `netlify.toml`.

Local preview: `pnpm install && hugo server` (needs Hugo extended 0.162+, Go, Node 22).

Local override: `layouts/_partials/functions/build_links.html` patches a bug in the HugoBlox blox module
under Hugo 0.162 (SetInMap on an empty dict). Delete it once upstream fixes it.
