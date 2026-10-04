# Metric Sheet

Six dimensions, tracked weekly. Fill the baseline in Week 1, then update every week.
A number without a date and a method is a rumor.

| Week | Quality (eval score) | Reliability (success rate) | p95 latency | Cost per 1k tasks | Security notes | Recovery notes |
|---|---|---|---|---|---|---|
| 0 | n/a (no system yet) | n/a | n/a | n/a | Secrets strategy set (.env, gitignored) | n/a |
| 1 | | | | | | |

## How each metric is measured

- **Quality:** score on the golden eval set in `evals/` (same prompts, model, dataset every run).
- **Reliability:** % of scripted tasks completed without human intervention.
- **p95 latency:** 95th-percentile response time of the main endpoint/task, measured locally.
- **Cost:** tracked LLM spend per 1,000 tasks (log tokens per run from Phase 1 on).
- **Security:** notes on what was hardened or what is still exposed.
- **Recovery:** notes from failure-injection drills (what broke, how fast it recovered).
