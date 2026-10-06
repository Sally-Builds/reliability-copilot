# Weekly Changelog

One entry per week. Four lines: what changed, what was measured, what failed, next risk.

## Week 0 (scaffold)

- **Changed:** Repo created with evidence-system structure (docs, adrs, evals, runbooks,
  load-tests, postmortems), templates, seed-data generator, baseline checklist. Repo cloned, .env created, data seeded, db created, data loaded into db, virtual environment created,, requirement.txt created
- **Measured:** Nothing yet. Baseline week is Week 1.
- **Failed:** The last character of my password was an @ symbol which collided with the db, the db url was `DATABASE_URL=postgresql://postgres:mypass@@localhost:5432/reliability_copilot`. This caused an error when trying to access the db! so to resolve it I fixed using percent-encoding by replacing the @ in the password with `%40`
- **Note:** The data is an append only kind of data. incidents are not updated when status changes but new ones are created with a reference to the incident.
- **Next risk:** Keeping the weekly shipping rhythm once real life competes for the 9 hours.
