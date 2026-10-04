# Reliability Copilot

An incident-response assistant that grows up in public. It starts as a dependable incident logbook
and, phase by phase, gains language-model summaries, retrieval and memory, controlled tool use,
multi-agent teamwork, production hardening (evals, observability, guardrails), and finally a
scaled, distributed architecture.

This repo is the **evidence system** for a 28-week senior-engineering roadmap. Every claim in it
is backed by something shipped: code, measurements, decision records, or postmortems.

## The story so far

- **Phase 0:** a clean incident API (modular monolith, Postgres, append-only event log)
- **Phase 1:** LLM-written incident summaries with structured outputs
- **Phase 2:** retrieval over past incidents ("we've seen this before")
- **Phase 3:** a single agent that can act (acknowledge, diagnose, escalate)
- **Phase 4:** a multi-agent response crew (diagnoser, communicator, verifier)
- **Phase 5:** production grade (eval harness, tracing, guardrails, cost tracking)
- **Phase 6:** scaled (caching, queues, load-tested)
- **Phase 7:** distributed (event-driven, failure-injected, recoverable)
- **Phase 8:** capstone + interview-ready

## Repo map

| Path | What lives here |
|---|---|
| `docs/` | Weekly changelog, metric sheet, baseline checklist |
| `adrs/` | Architecture decision records (the *why* behind big choices) |
| `evals/` | Golden datasets, eval harnesses, score history |
| `runbooks/` | How to run, deploy, and operate the system |
| `load-tests/` | Load test scripts and results |
| `postmortems/` | Write-ups of things broken and fixed |
| `scripts/` | Seed data generator, schema, utilities |
| `data/` | Synthetic demo data (never real credentials, never real incidents) |

## Quickstart

```bash
cp .env.example .env        # then put your own LLM API key in .env (never commit it)
python3 scripts/seed.py     # generates data/incidents.json (250 synthetic incidents)
```

## Rules

1. Ship every week. A week with nothing merged didn't happen.
2. Baseline before complexity. Measure the simple thing first.
3. Secrets stay in `.env`. Real data never enters this repo.
4. Every consequential decision gets an ADR in `adrs/`.
5. Every failure worth learning from gets a postmortem in `postmortems/`.
