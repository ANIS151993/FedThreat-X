# FedThreat-X Implementation Guide

This guide translates the published FedThreat-X research into a practical GitHub Pages and SOC implementation artifact.

## Production Rollout

1. Prepare multi-cloud telemetry with consistent schema normalization, categorical cleanup, rare-category grouping, timestamp features, deduplication, and z-score scaling.
2. Train lightweight local MLP clients inside each cloud boundary.
3. Synchronize through federated rounds without moving raw logs outside the owner environment.
4. Weight client updates by validation accuracy, data quality, and threat drift.
5. Apply proximal regularization to reduce harmful divergence in non-IID settings.
6. Deploy the converged global model behind a real-time SOC scoring API.
7. Monitor drift, confidence, false positives, and client contribution quality.

## GitHub Pages Deployment

Use branch-based GitHub Pages:

1. Repository Settings -> Pages
2. Source: Deploy from a branch
3. Branch: `main`
4. Folder: `/docs`

The published portal entry point is `docs/index.html`.

## Local Verification

```bash
bash scripts/check-js.sh
```
