"""
Seed generator for Reliability Copilot demo data.

Produces 250 synthetic incidents shaped like real production postmortems
(database failovers, deploy regressions, traffic spikes, cert expiries,
queue backlogs, cache stampedes). Deterministic: same seed, same data,
so evals stay comparable across runs.

Five incidents are hand-authored to match evals/golden-set.json exactly;
the rest are generated from archetype templates.

Usage:  python3 scripts/seed.py
Output: data/incidents.json
"""

import json
import random
from datetime import datetime, timedelta, timezone

random.seed(20261003)

SERVICES = [
    "payments-api", "checkout-web", "auth-service", "search-api",
    "notifications-worker", "inventory-db", "cdn-edge", "billing-cron",
]

ARCHETYPES = [
    {
        "title": "Database connection pool exhaustion",
        "severity": "SEV2",
        "root_cause": "connection pool exhaustion after deploy {ver}",
        "resolution": "rolled back to {prev_ver} and doubled pool size",
        "logs": [
            "FATAL: remaining connection slots are reserved for superuser",
            "pool timeout after 30s waiting for connection",
            "deploy {ver} finished at {t}",
        ],
    },
    {
        "title": "Traffic spike saturates web tier",
        "severity": "SEV2",
        "root_cause": "unexpected traffic spike ({mult}x baseline) after marketing send",
        "resolution": "scaled web tier 4 -> 12 replicas, added rate limit",
        "logs": [
            "upstream timeout after 5s",
            "p99 latency 8.2s (baseline 240ms)",
            "autoscaler at max replicas",
        ],
    },
    {
        "title": "Deploy regression in {service}",
        "severity": "SEV2",
        "root_cause": "null pointer in request validation introduced in {ver}",
        "resolution": "rolled back to {prev_ver}, added regression test",
        "logs": [
            "TypeError: Cannot read properties of null",
            "5xx rate 12% on /v1/orders",
            "deploy {ver} finished at {t}",
        ],
    },
    {
        "title": "Queue backlog delays background jobs",
        "severity": "SEV3",
        "root_cause": "queue backlog after a bulk import, not a code bug",
        "resolution": "drained queue with extra workers, no code change needed",
        "logs": [
            "queue depth 48,211 (baseline < 200)",
            "oldest message age 3h 12m",
            "worker CPU pegged at 100%",
        ],
    },
    {
        "title": "TLS certificate expiry on edge",
        "severity": "SEV1",
        "root_cause": "TLS certificate expired; renewal job silently failing for 9 days",
        "resolution": "manually renewed cert, fixed renewal job alerting",
        "logs": [
            "certificate has expired",
            "TLS handshake failures 100% on edge pop",
            "renewal cron last success 9 days ago",
        ],
    },
    {
        "title": "Cache stampede after cold restart",
        "severity": "SEV3",
        "root_cause": "cache stampede: cold restart sent all traffic to database",
        "resolution": "enabled request coalescing, warmed cache gradually",
        "logs": [
            "cache hit rate 4% (baseline 96%)",
            "database CPU 98%, query queue 1200",
            "thundering herd on /v1/products",
        ],
    },
    {
        "title": "Intermittent login failures",
        "severity": "SEV1",
        "root_cause": "session store failover loop dropping writes",
        "resolution": "failed over to replica region, patched failover logic",
        "logs": [
            "session write failed: quorum not reached",
            "login success rate 61% (baseline 99.9%)",
            "failover flapping between regions",
        ],
    },
    {
        "title": "CDN cache hit-rate dip",
        "severity": "SEV4",
        "root_cause": "cache key change lowered edge hit rate, no user impact",
        "resolution": "monitored, hit rate recovered after TTL expiry",
        "logs": [
            "edge hit rate 71% (baseline 94%)",
            "origin traffic +22%, within capacity",
            "no elevated error rate",
        ],
    },
]

# Hand-authored to match evals/golden-set.json required facts.
GOLDEN = [
    {
        "id": "inc-0007", "service": "payments-api", "severity": "SEV2",
        "title": "Checkout failures after deploy",
        "opened_at": "2026-09-14T02:11:00+00:00", "duration_minutes": 47,
        "root_cause": "database connection pool exhaustion after deploy v2.14.3",
        "resolution": "rolled back to v2.14.2 and doubled pool size",
        "customer_impact": True,
        "logs": ["FATAL: remaining connection slots are reserved",
                 "checkout error rate 34%", "rolled back v2.14.3 -> v2.14.2"],
    },
    {
        "id": "inc-0023", "service": "checkout-web", "severity": "SEV2",
        "title": "Intermittent checkout unavailability",
        "opened_at": "2026-08-30T18:02:00+00:00", "duration_minutes": 33,
        "root_cause": "load balancer misconfiguration sending traffic to drained hosts",
        "resolution": "fixed backend pool config, verified health checks",
        "customer_impact": True,
        "logs": ["502s on /checkout for 18% of requests", "no customer data affected",
                 "service fully restored at 18:35 UTC"],
    },
    {
        "id": "inc-0041", "service": "auth-service", "severity": "SEV1",
        "title": "All-users login failures",
        "opened_at": "2026-09-02T11:20:00+00:00", "duration_minutes": 26,
        "root_cause": "session store failover loop dropping writes",
        "resolution": "paged auth-service owner, froze deploys, failed over to replica region",
        "customer_impact": True,
        "logs": ["login success rate 61%", "session write quorum failures"],
    },
    {
        "id": "inc-0066", "service": "notifications-worker", "severity": "SEV3",
        "title": "Delayed transactional emails",
        "opened_at": "2026-08-18T09:05:00+00:00", "duration_minutes": 192,
        "root_cause": "queue backlog after a marketing send, not a code bug",
        "resolution": "drained queue with extra workers, no code change needed",
        "customer_impact": False,
        "logs": ["queue depth 48,211", "oldest message age 3h 12m"],
    },
    {
        "id": "inc-0090", "service": "cdn-edge", "severity": "SEV4",
        "title": "Edge cache hit-rate dip",
        "opened_at": "2026-09-25T14:40:00+00:00", "duration_minutes": 90,
        "root_cause": "cache key change lowered edge hit rate, no user impact",
        "resolution": "monitored, no page, hit rate recovered after TTL expiry",
        "customer_impact": False,
        "logs": ["edge hit rate 71% (baseline 94%)", "origin traffic within capacity"],
    },
]


def make_incident(i, arch):
    service = random.choice(SERVICES)
    ver = f"v2.{random.randint(10, 20)}.{random.randint(0, 9)}"
    prev = f"v2.{random.randint(10, 20)}.{random.randint(0, 9)}"
    opened = datetime(2026, random.randint(6, 9), random.randint(1, 28),
                      random.randint(0, 23), random.randint(0, 59),
                      tzinfo=timezone.utc)
    duration = random.randint(15, 240)
    fmt = lambda s: s.format(ver=ver, prev_ver=prev, service=service,
                             mult=random.randint(3, 9), t=opened.isoformat())
    return {
        "id": f"inc-{i:04d}",
        "title": fmt(arch["title"]),
        "service": service,
        "severity": arch["severity"],
        "status": "resolved",
        "opened_at": opened.isoformat(),
        "resolved_at": (opened + timedelta(minutes=duration)).isoformat(),
        "duration_minutes": duration,
        "root_cause": fmt(arch["root_cause"]),
        "resolution": fmt(arch["resolution"]),
        "customer_impact": arch["severity"] in ("SEV1", "SEV2"),
        "logs": [fmt(l) for l in arch["logs"]],
    }


def main():
    incidents = []
    for g in GOLDEN:
        opened = datetime.fromisoformat(g["opened_at"])
        incidents.append({
            "id": g["id"], "title": g["title"], "service": g["service"],
            "severity": g["severity"], "status": "resolved",
            "opened_at": g["opened_at"],
            "resolved_at": (opened + timedelta(minutes=g["duration_minutes"])).isoformat(),
            "duration_minutes": g["duration_minutes"],
            "root_cause": g["root_cause"], "resolution": g["resolution"],
            "customer_impact": g["customer_impact"], "logs": g["logs"],
        })
    i = len(incidents) + 1
    while len(incidents) < 250:
        incidents.append(make_incident(i, random.choice(ARCHETYPES)))
        i += 1
    with open("data/incidents.json", "w") as f:
        json.dump(incidents, f, indent=2)
    sevs = {}
    for inc in incidents:
        sevs[inc["severity"]] = sevs.get(inc["severity"], 0) + 1
    print(f"Wrote {len(incidents)} incidents to data/incidents.json")
    print("Severity mix:", sevs)


if __name__ == "__main__":
    main()
