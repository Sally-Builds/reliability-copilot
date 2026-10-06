import json, os
import psycopg2
from dotenv import load_dotenv

load_dotenv()
conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()
data = json.load(open("data/incidents.json"))

for inc in data:
    cur.execute(
        "INSERT INTO incidents (id, title, service, severity, status, opened_at, customer_impact)"
        " VALUES (%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING",
        (inc["id"], inc["title"], inc["service"], inc["severity"],
         inc["status"], inc["opened_at"], inc["customer_impact"]),
    )
    cur.execute("DELETE FROM incident_events WHERE incident_id = %s", (inc["id"],))
    cur.execute(
        "INSERT INTO incident_events (incident_id, event_type, payload, created_at)"
        " VALUES (%s,'opened',%s::jsonb,%s)",
        (inc["id"], json.dumps({"root_cause": inc["root_cause"], "logs": inc["logs"]}), inc["opened_at"]),
    )
    cur.execute(
        "INSERT INTO incident_events (incident_id, event_type, payload, created_at)"
        " VALUES (%s,'resolved',%s::jsonb,%s)",
        (inc["id"], json.dumps({"resolution": inc["resolution"], "duration_minutes": inc["duration_minutes"]}), inc["resolved_at"]),
    )

conn.commit()
print(f"Loaded {len(data)} incidents")
conn.close()
