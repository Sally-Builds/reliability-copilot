# ADR 0001: Start with a modular monolith

- **Status:** accepted
- **Date:** 2026-10-06

## Context

Phase 0 of the roadmap: rebuilding coding fluency after time away from active
development. The goal of this phase is reasoning fluency and the core principles
of observability, design, and clear thinking, so the architecture should serve
that goal, not distract from it.

The system being built is Reliability Copilot: an incident API, a background
worker, and Postgres with an append-only event table. Team of one.

## Decision

Build as a modular monolith. One deployable, with the API, worker, and domain
logic as separate modules that communicate through clean interfaces, never
through network calls.

## Alternatives considered

1. **Microservices** — rejected. Premature distribution for a team of one:
   cross-module transactions disappear, debugging spans network boundaries
   while relearning the fundamentals, and the operational overhead (service
   discovery, distributed tracing, multi-pipeline CI) is pure cost with no
   benefit at this stage.
2. **Serverless** — rejected. Cold starts, an awkward fit for the stateful
   worker, harder local development, and vendor coupling before the design
   has earned it.

## Consequences

- **Gains:** single deployment; real transactions across modules, which the
  append-only event design depends on; cheap refactoring; fast local iteration.
- **Costs:** module boundaries are enforced by discipline, not by the network.
  Modules must not reach into each other's tables directly.
- **Follow-up:** if the worker ever outgrows the monolith, it is the first
  candidate for extraction. Revisit at Phase 6 (scaling), not before.
