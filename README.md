# HRM Building Model Changes

Tracking repo for GIS schema-change tickets against the Building model (`BLD_*` feature
classes/tables) at Halifax Regional Municipality (HRM), reviewed through the GIS Design
Authority process. Source RFCs (Excel change forms) come from
`R:\ICT\ICT GIS\GIS Design Authority\Change Requests\`; a copy of each one pulled into this
repo lives in `changes/`.

## Workstreams

| Workstream | Tickets | Status | Details |
|---|---|---|---|
| Building Components | TASK0327172–TASK0327179 (8 parallel tickets, one per `BLD_*` component) | 🔵 In Progress | `workstreams/building_components/project.md` |
| `BLD_building_assetpoint` | TASK0326632 | 🔵 In Progress (priority workstream) | `workstreams/bld_asset_point/bld_asset_point.md` |
| Polygon / Symbols / Use family | TASK0312692, TASK0320355, TASK0320358, TASK0320365 | 🟡 Partially blocked | `workflow.md` |

## Repo layout

- `workstreams/` — one folder per active workstream, each holding its own working docs
  (and, for `bld_asset_point`, the deployment `scripts/` and captured `sql/` view definitions
  specific to that ticket).
- `tickets/` — ServiceNow ticket records (fields + full description, verbatim) for tickets
  that don't have their own dedicated workstream folder. One file per ticket number.
- `changes/` — source-of-truth Excel change forms pulled from the GIS Design Authority
  network share, referenced by ticket/workstream docs.
- `workflow.md` — the cross-ticket dependency map (which table is driven by which ticket,
  what blocks what) plus the ticket summary and ad hoc checklists for the Polygon/Symbols/Use
  workstream, which doesn't yet have its own folder.

## Status legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
