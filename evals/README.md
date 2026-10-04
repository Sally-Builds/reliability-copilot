# Evals

Golden datasets and the harnesses that grade the system against them.

## Rules

1. Same prompts, same model, same dataset on every run. A test that quietly changes
   any of these proves nothing.
2. Score history goes here, dated. `scores/2026-10-12-summarization.md`, etc.
3. The golden set starts small (see `golden-set.json`) and grows to 30-50 hand-labeled
   examples by Phase 5. Writing good evals is part of the work, not a chore before it.

## Golden set format

Each entry names an incident, the task, and the facts a correct answer must include.
A summary that misses a required fact fails, even if it reads beautifully.
