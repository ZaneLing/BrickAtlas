# Web workspace

The maintained website lives here: React/Three.js source in `src/`, served
models and versioned evidence in `public/`, HTML entry points, frontend
configuration, tests and website documentation in `docs/`.

Run commands from the repository root:

```sh
npm run dev
npm run typecheck
npm test
npm run build
npm run build:ldraw-v2
npm run test:e2e -- --project=desktop-chrome
```

| Local URL | Purpose |
|---|---|
| `/` | Interactive model workspace |
| `/benchmark` | Original source models, numbered parts and 3D replay |
| `/benchmark/visual-repair-v1/review.html` | Current blind qualification and JSON export |
| `/benchmark/evidence-v3/index.html` | Historical evidence inspection with answers |
| `/ldraw-v2.html` | Historical construction review |
| `/paper/complex-render.html` | Source-geometry capture for historical examples |

`benchmark/`, `scripts/`, `atlas.config.ts`, `assets-source/` and `assets-built/`
are relative symlink mounts of shared repository resources, not duplicate data.
Frozen benchmark packages retain their versioned render/review pages beside
their native packets and source locks. Vite exposes them through this mount.
Research review pages are intended for the local dev server; the standard
production build retains the existing main-app scope.

Vite and TypeScript output goes to `../tem/build/`. Playwright output goes to
`../tem/verification/`. Root `src` and `public` are compatibility links for
frozen scripts; root `vite.config.ts` delegates to the configuration here.
Deployment platforms discover the root links to `netlify.toml` and
`vercel.json`; their project root remains the repository root.

See [deployment](docs/DEPLOYMENT.md) and [architecture](docs/ARCHITECTURE.md).
