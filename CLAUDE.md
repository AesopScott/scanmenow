# ScanMeNow

## Standing rules
- **Project isolation:** Do not read files, inspect git history, or browse the directory structure of any other project directory without explicit approval from Scott. Cross-project access is permitted only when Scott explicitly names the other project in the request.

## Branch & Worktree Rules (enforced 2026-05-27)

### Main branch protection
- `main` is **protected** on GitHub — direct pushes are rejected. All changes reach main via PR only.
- PRs do not require an external reviewer (solo project) but MUST pass any configured CI status checks before merge.
- Force pushes and deletions on `main` are disabled.

### Worktree structure
Each parallel session must work in its own isolated git worktree:

| Worktree path | Branch | Purpose |
|---|---|---|
| `C:/Users/scott/Code/scanmenow` | `task/5-group-d-filesystem-walker-integration` | Task D active build |
| `C:/AppData/Local/Temp/main-wt` | `main` | Read-only monitoring — no commits |
| `C:/AppData/Local/Temp/orchestrator-wt` | `chore/orchestrator-sync` | Orchestrator cross-session corrections |
| Polaris session worktrees (`/polaris-wt/chat_*`) | task/N-* (per session) | Each build session's isolated branch |

### Branch ownership
- **Build sessions** commit only to their `task/N-*` branch (enforced by `/start-build`).
- **Orchestrator session** commits only to `chore/orchestrator-sync`; opens a PR to merge.
- **`main` worktree** is read-only — used by the monitor to observe the current stable state.
- Nothing lands on `main` except via an approved and merged PR.

### New task branches
When a new build session starts via `/start-build`, it:
1. Creates a `task/N-*` branch from the current `main` HEAD.
2. Gets its own Polaris worktree (`/polaris-wt/chat_*`) pinned to that branch.
3. Never commits to `main` directly.

### PR merge workflow
1. Build session completes → `/finish-build` opens PR from `task/N-*` → `main`.
2. `/review-pr task N` or `/codex-review task N` runs in a reviewer session.
3. PR is merged after review passes (0 required approvers configured; CI must be green).
4. Orchestrator corrections (from `chore/orchestrator-sync`) follow the same PR flow.
