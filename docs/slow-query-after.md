
## Query
```py
EXPLAIN ANALYZE SELECT * FROM incident_events WHERE payload->>'root_cause' LIKE '%pool%';
```

## Result
```py
Seq Scan on incident_events  (cost=0.00..21.35 rows=4 width=192) (actual time=0.032..0.196 rows=31.00 loops=1)
  Filter: ((payload ->> 'root_cause'::text) ~~ '%pool%'::text)
  Rows Removed by Filter: 459
  Buffers: shared hit=14
Planning:
  Buffers: shared hit=119
Planning Time: 4.812 ms
Execution Time: 0.218 ms
```

## Index Created
```
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE INDEX idx_events_root_cause_trgm
  ON incident_events USING gin ((payload->>'root_cause') gin_trgm_ops);
```

## Why Triagram Index instead of B-tree
B-tree stores values in sorted order. That makes it great for equality(=), ranges(<, >) and prefix matches(LIKE 'pool%'), because all of those corresponds to a sorted order.

LIKE '%pool%' has a leading wildcard, so a match could start at any position in the string. There is no contiguous chunk of sorted values that contains all possible matches, which means a B-tree can't narrow anything down and the planner ignores it.

Trigrams solve this differently. pg_trgm chops text into overlapping 3-character chunks: "pool" becomes " po", "poo", "ool", "ol ". The GIN index maps each trigram to the rows containing it. For this query, Postgres extracts the trigrams from "pool", finds rows containing all of them via the index, then verifies each candidate. That's why it handles leading wildcards.

## Cost
size of index = 64KB becaue the table is small. GIN indexes are heavier than B-trees on writes too. Every index is a trade, which is why it was measured instead of assuming.

## Notes
Planning also was longer than before index. Planning time dwarfs execution time. On small fast queries, planning dominates
