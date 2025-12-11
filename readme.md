# HHA 504 – Final Project: Cloud Integration Mini-Capstone

## Project Title
Cloud-Based Sepsis Early Warning & Monitoring Pipeline

## Files

- `use_case.md`
- `architecture_plan.md`
- `reflection.md`

## Prototype (Extra Credit)

A small Flask prototype is included under `prototype/`.  
It has:

- A home route (`/`) that describes the sepsis early-warning demo.
- A `/files` route that attempts to list objects from a Google Cloud Storage bucket using the `google-cloud-storage` library. If no bucket is configured, it returns a clear message instead.

See `prototype/README.md` for instructions on how to run it locally.
