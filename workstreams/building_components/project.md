# Project: Building Component Changes (BLD_* Feature Classes/Tables)

## Purpose & Context

Requestor: Lisa O'Toole
Assigned to: Alex Gallagher
Assignment Group: Data Services Support
Configuration Item: Data Services
Priority: Medium (target end of summer, some flexibility noted)
Opened: 2026-06-30
Due date: 2026-07-31

This is a set of 8 parallel Catalog Tasks, one per Building Component, covering changes discussed at the GIS Design Authority. Each task follows the same template:

- Fields suggested for removal by AMO
- New asset codes and fields added to support Tai's work with Facilities Design & Construction
- Changes reviewed and approved by Facilities Maintenance & Operations
- Change form details stored in `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\Building Components\Changes to <COMPONENT>.xlsx`
This work appears related to the AMO confirmation dependency already tracked against TASK0326632 (`BLD_building_assetpoint`), since these tasks reference AMO-suggested field removals across building components.

## Tickets

| Task | RITM | Component | Change Form |
|---|---|---|---|
| TASK0327172 | RITM0311304 | BLD_ELECTRICAL | Changes to BLD_ELECTRICAL.xlsx |
| TASK0327173 | RITM0311305 | BLD_EXTERIOR | Changes to BLD_EXTERIOR.xlsx |
| TASK0327174 | RITM0311306 | BLD_INTERIOR | Changes to BLD_INTERIOR.xlsx |
| TASK0327175 | RITM0311308 | BLD_LIFESAFETY | Changes to BLD_LIFESAFETY.xlsx |
| TASK0327176 | RITM0311309 | BLD_MECHANICAL | Changes to BLD_MECHANICAL.xlsx |
| TASK0327177 | RITM0311310 | BLD_ROOF | Changes to BLD_ROOF.xlsx |
| TASK0327178 | RITM0311311 | BLD_SPECIALTY | Changes to BLD_SPECIALTY.xlsx |
| TASK0327179 | RITM0311312 | BLD_STRUCTURE | Changes to BLD_STRUCTURE.xlsx |

All 8 are currently **Open**, same due date (2026-07-31) and follow-up date (2026-06-30).

## Documentation Suite

Change details from the 8 source spreadsheets are broken out into the following supporting docs (all in this repo):

| File | Contents |
|---|---|
| `fields_to_add.md` | New fields, common and component-specific |
| `fields_to_delete.md` | AMO-suggested, FMO-confirmed deletions |
| `fields_to_keep.md` | AMO suggested deletion, FMO overrode |
| `alias_updates.md` | Fields never up for deletion, alias/label change only |
| `domain_changes.md` | New domains, domains to delete, domains getting new codes/values |
| `attribute_rules.md` | Fields needing calculated/automated behavior — implementation-facing breakdown |
| `outstanding_questions.md` | Open decisions and flagged ambiguities, resolved and unresolved |

## Open Items / Action Items

- ~~Pull each `Changes to <COMPONENT>.xlsx` change form from the GIS Design Authority folder~~ Done — all 8 forms plus the assetpoint/polygon/Building-table forms are in `../../changes/`.
- ~~Confirm whether these 8 tasks are dependent on or independent of the AMO confirmation already blocking items in TASK0326632~~ Resolved: confirmed independent, see `outstanding_questions.md`.
- Determine build order across the 8 components (schema-only vs. also touching views/services, similar to the BLD_building_polygon work).
- No environment-specific tracking yet (SDE Dev/QA/Prod, file GDB) for any of these 8. Will need same per-environment verification pattern used on prior tickets.

## Related Prior Work (for reference)

See `../bld_asset_point/bld_asset_point.md` for status on TASK0326632 (`BLD_building_assetpoint`, now the priority workstream), `../../workflow.md` for the cross-ticket dependency map and TASK0320358, and `../../tickets/TASK0320365.md` for TASK0320365, which covers `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, and `BLD_BUILDING_CIVIC_LINK`.

