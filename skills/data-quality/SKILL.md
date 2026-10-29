---
name: data-quality
description: >-
  Validate datasets and training data — schema, nulls, duplicates, source freshness, PII.
allowed-tools: Read, Bash, Grep, Glob, Write
---

# Data quality

## Datasets

- `deepiri-dataset-processor` output schema vs what `diri-helox` training reads
- Row counts vs the manifest/source it was generated from
- Stale generation dates — retrain sets go stale faster than market CSVs

## Training data

- Dataset-processor export → Helox training required fields
- Label leakage checks
- PII presence check before anything reaches a training run

## Handoff

- **deepiri-dataset-processor**, **deepiri-tombstone**
