## Query
```py
EXPLAIN ANALYZE SELECT * FROM incident_events WHERE payload->>'root_cause' LIKE '%pool%';
```

## Result

```py
Seq Scan on incident_events  (cost=0.00..21.35 rows=4 width=192) (actual time=0.025..0.211 rows=31.00 loops=1)
  Filter: ((payload ->> 'root_cause'::text) ~~ '%pool%'::text)
  Rows Removed by Filter: 459
  Buffers: shared hit=14
Planning:
  Buffers: shared hit=86
Planning Time: 4.301 ms
Execution Time: 0.289 ms
```

* Ran a sequential scan, read all rows, got result from 31 of them, planning took about 4.301ms