# Bi-Temporal Progress Tracking

## Purpose

ScanMeNow task planning now changes along two timelines:

- **Effective project time:** when a task definition, status, dependency, or decision is considered true for the project.
- **Recorded system time:** when the backlog system learned, stored, or corrected that fact.

The current `docs/backlog.json` file is a current-state projection. It shows what is true now, but it overwrites how the project got there. Bi-temporal tracking keeps the current projection while adding an append-only history that can answer questions like:

- What did we believe Task C meant before Task H was split out?
- When did Scott decide that Task C depends on Tasks D, G, and H?
- Was a status retroactively corrected, or was it true at the time it was recorded?
- Which task graph was active when a session started?

## Recommended Files

Keep the existing backlog file as the fast current-state view:

```text
docs/backlog.json
```

Add an append-only event ledger:

```text
docs/backlog-events.jsonl
```

Each line in `backlog-events.jsonl` is one JSON object. The ledger is the source of historical truth. `backlog.json` remains the current projection consumed by simple UI and workflow code.

## Event Schema

Minimum event shape:

```json
{
  "event_id": "evt_20260527_001",
  "task": 4,
  "event_type": "dependency_changed",
  "field": "dependencies",
  "old_value": [],
  "new_value": [5, 9, 10],
  "valid_from": "2026-05-27T00:00:00-06:00",
  "valid_to": null,
  "recorded_at": "2026-05-27T08:00:00-06:00",
  "recorded_by": "scott",
  "session_id": "codex_1779887175842",
  "reason": "Task C now consumes extraction, PII scope, and independent testing data."
}
```

Required fields:

| Field | Meaning |
|---|---|
| `event_id` | Stable unique event identifier. |
| `task` | Numeric task identifier from `docs/backlog.json`. |
| `event_type` | Machine-readable event name. |
| `field` | Backlog field changed, or `null` for whole-task events. |
| `old_value` | Prior projected value, if known. |
| `new_value` | New projected value. |
| `valid_from` | When this fact became true in project time. |
| `valid_to` | When this fact stopped being true in project time, usually `null` when first recorded. |
| `recorded_at` | When the system recorded the event. |
| `recorded_by` | Human or agent responsible for recording. |
| `session_id` | Polaris session that recorded the event, when available. |
| `reason` | Short human-readable explanation. |

## Event Types

Initial event types should stay small:

- `task_created`
- `task_renamed`
- `description_changed`
- `status_changed`
- `dependency_changed`
- `scope_changed`
- `priority_changed`
- `plan_changed`
- `proof_units_changed`
- `correction_recorded`

Use `correction_recorded` when the recorded history was wrong. Do not rewrite previous events except for mechanical repair of invalid JSON before the file is consumed.

## Projection Rules

`docs/backlog.json` should remain the current projection:

1. Read all active tasks from `docs/backlog.json`.
2. Append a matching event to `docs/backlog-events.jsonl` for every meaningful task change.
3. Apply the change to `docs/backlog.json`.
4. Keep the event append and projection update in the same commit.

For a future implementation, a projection command can rebuild `backlog.json` from the event ledger:

```text
scanmenow backlog project --events docs/backlog-events.jsonl --output docs/backlog.json
```

Until that exists, the workflow can update both files directly.

## Query Patterns

The implementation should support these questions:

- **Current state:** read `docs/backlog.json`.
- **State as recorded at time T:** replay events where `recorded_at <= T`.
- **State effective at time T:** replay events where `valid_from <= T` and `valid_to` is null or greater than T.
- **Retroactive changes:** find events where `valid_from` is materially earlier than `recorded_at`.
- **Task lineage:** list all events for a task ordered by `recorded_at`.

## Task C/G/H Example

The Task C split should be representable as events:

1. `task_renamed`: Task C changed from synthetic corpus ownership to benchmark runner and accuracy gate.
2. `task_created`: Task G added PII scope and capability.
3. `task_created`: Task H added independent testing data for Task C.
4. `dependency_changed`: Task C dependencies changed to `[5, 9, 10]`.

The current projection remains simple: Task C has `dependencies: [5, 9, 10]`. The event ledger preserves why and when that became true.

## Acceptance Criteria

- `docs/backlog-events.jsonl` exists and validates as newline-delimited JSON.
- New task changes write one event per meaningful field change.
- `docs/backlog.json` remains valid JSON and reflects the latest projected state.
- A small validation script can detect malformed events, missing required fields, unknown task references, and dependency references to nonexistent tasks.
- Documentation explains how to query current state, recorded-at state, and effective-at state.
