# GitHub Pages Deployment

The FedThreat-X research portal is a static GitHub Pages site served from `docs/`.

1. Push the `main` branch to GitHub.
2. Open **Settings -> Pages** in the `ANIS151993/FedThreat-X` repository.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select `main` and the `/docs` folder.
5. Save the configuration.

The expected public URL is:

```text
https://anis151993.github.io/FedThreat-X/
```

## Regenerate Research Assets

```bash
python3 scripts/generate_research_assets.py
```

The generator renders a paper preview and creates the six repository-native research plots used in the README and portal. The plots are derived from the paper's reported aggregate metrics, class totals, confusion-matrix narrative, and feature-importance discussion; they do not claim access to unreleased raw telemetry.
