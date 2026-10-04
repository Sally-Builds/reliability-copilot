# Local Development

## Prereqs

- Python 3.10+
- PostgreSQL 14+ running locally
- An LLM API key in `.env` (see `.env.example`)

## Start from zero

```bash
cp .env.example .env          # fill in your key
python3 scripts/seed.py       # generate data/incidents.json
psql $DATABASE_URL -f scripts/schema.sql
```

One documented command must bring up a fresh clone. That command gets written here
once Phase 0 code exists.
