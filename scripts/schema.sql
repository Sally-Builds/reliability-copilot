-- Reliability Copilot schema (Phase 0).
-- One append-only event table: incidents are never updated in place,
-- every state change is a new event. History is the product.

CREATE TABLE IF NOT EXISTS incidents (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    service         TEXT NOT NULL,
    severity        TEXT NOT NULL CHECK (severity IN ('SEV1','SEV2','SEV3','SEV4')),
    status          TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open','acknowledged','mitigated','resolved')),
    opened_at       TIMESTAMPTZ NOT NULL,
    customer_impact BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS incident_events (
    event_id    BIGSERIAL PRIMARY KEY,
    incident_id TEXT NOT NULL REFERENCES incidents(id),
    event_type  TEXT NOT NULL,  -- opened, acknowledged, note_added, mitigated, resolved, ...
    payload     JSONB NOT NULL DEFAULT '{}',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_events_incident ON incident_events (incident_id, event_id);
CREATE INDEX IF NOT EXISTS idx_incidents_service ON incidents (service);
CREATE INDEX IF NOT EXISTS idx_incidents_opened ON incidents (opened_at DESC);
