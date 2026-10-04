# Week 1 Baseline Checklist

Complete before writing any product code. Check each box with evidence, not vibes.

- [ ] Repo cloned fresh and `cp .env.example .env` done (key filled in, `.env` gitignored)
- [ ] `python3 scripts/seed.py` runs and produces `data/incidents.json` (250 incidents)
- [ ] `scripts/schema.sql` reviewed and understood (can explain every table)
- [ ] First ADR written: `adrs/0001-modular-monolith.md` (why start with a modular monolith)
- [ ] Metric sheet baseline row filled (Week 1): test count, build time, one p95 latency
- [ ] Weekly changelog has a Week 1 entry
- [ ] Slow-query plan captured before indexing (save output under `docs/`)
- [ ] Can explain the transaction boundary and one rejected alternative without notes

Exit gate for Phase 0 (end of Week 2): a fresh clone starts with one documented command,
passes unit + integration tests, and the API contract, schema migration, and worker retry
behavior are all versioned.
