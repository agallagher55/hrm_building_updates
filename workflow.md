# Workflow – GIS Building Tables Schema Changes

## Ticket Summary

| Ticket | Feature Classes / Tables | Due Date | Status |
|---|---|---|---|
| TASK0326632 | `BLD_building_assetpoint` | Jul 10, 2026 | 🔵 In Progress |
| TASK0320358 | `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols` (view updates) | Jan 30, 2026 ⚠️ | ⚪ Not Started |
| TASK0320365 | `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK` (field/domain/table deletions) | Jan 30, 2026 ⚠️ | 🟡 Blocked on TASK0320358 |
| *(no ticket number)* | `BLD_BUILDING` (field deletions) | *(not tracked)* | ⚪ Not Started |

---

## Cross-Ticket Dependency Map

Every table in this workstream, which ticket drives it, its source RFC, and what it's blocked by or blocking. Kept here as the single place to check sequencing before starting work on any of these tables.

| Table | Driving Ticket | Source RFC | Depends On |
|---|---|---|---|
| `BLD_building_assetpoint` | TASK0326632 (see `bld_asset_point.md`) | `changes/Add fields to Building Assetpoint.xlsx` | Nothing, but gates the row below |
| `BLD_BUILDING` (field deletions) | *no ticket number found yet* | `changes/Delete fields in Building table.xlsx` | **`BLD_building_assetpoint`'s `NAMESTATUS` / `NAMEAPRDTE` adds (TASK0326632) must land first.** That RFC's own notes column says, verbatim, "Add field to `BLD_building_assetpoint` and then delete" for both fields. Its other three deletes (`INSTYRCONF`, `SIZE1UNIT`, `SIZE1CONF`, `DISPOSAL`) carry no such dependency, they already exist on assetpoint independently. |
| `BLD_building_polygon` | TASK0320358 (views) → TASK0320365 (deletes), see `tickets/TASK0320365.md` | `R:\...\Building Polygons\Changes to BLD_building_polygon feature class.xlsx` (not yet in this repo) | TASK0320365's polygon deletes are already done, ahead of the rest of that ticket |
| `BLD_BUILDING_USE` | TASK0320358 (views) → TASK0320365 (deletes + domain values), see `tickets/TASK0320365.md` | `R:\...\Building Use\Delete fields in Building Use table.xlsx` (not yet in this repo) | TASK0320358 views must land first |
| `BLD_Building_Symbols` | TASK0320358 (views) → TASK0320365 (domain values), see `tickets/TASK0320365.md` | `R:\...\Building Symbols\Building Symbol Fcode Changes.xlsx` (not yet in this repo) | TASK0320358 views must land first |
| `BLD_BUILDING_CIVIC_LINK` | TASK0320365 (table deletion), see `tickets/TASK0320365.md` | `R:\...\Building Civic Link\Delete Building Civic Link table.xlsx` (not yet in this repo) | Full impact inventory (EMO views/services) before the table itself can be dropped |

> **Sequencing, in short:** TASK0326632's assetpoint adds must land before `BLD_BUILDING` can delete `NAMESTATUS` / `NAMEAPRDTE`. TASK0320358 (view updates) must be completed before TASK0320365 (field/domain/table deletions) can proceed, the `BLD_building_polygon` field deletions in TASK0320365 are the only exception, those are already done.

---

## TASK0326632 – BLD_building_assetpoint

**Now tracked in its own file: `bld_asset_point.md`** (moved out since this became the priority workstream). Ticket record (ServiceNow fields, full description) in `tickets/TASK0326632.md`. This file keeps only the ticket summary row above and the related/dependent tickets below.

---

## Other / Untracked Work

### BLD_building_polygon – ad hoc changes (Jun 2026)
- [ ] 🔴 Update alias for `ZVALUE` → "Roofline Height metres" — was commented out in `1_update_field_alias.py`; not yet done
- [x] `HGTSOURCE` field — already existed in all SDE envs as of Jun 14 ✅; confirmed in Prod web_RO.gdb Jun 19 ✅
- [ ] 🔴 `HGTSOURCE` missing from QA web_RO.gdb — confirmed absent; needs targeted run of `2_new_field.py` against `qa_web_ro_gdb`
- [x] Delete `FOOT_SQFT`, `FLOORS`, `SCALE` — ✅ confirmed complete all envs (Dev RW/RO, QA RW/RO, QA web_RO.gdb, Prod RW/RO, Prod web_RO.gdb) via Jun 15 log

### BLD_Building_Symbols – ad hoc changes (Jun 2026)
- [x] Alias updates (`ADDDATE`, `SOURCE`, `SACC`, `MODDATE`) — ✅ done QA + Prod (Jun 14 log)
- [ ] ⚠️ Remove `AAA_operator_asset` from `ADDBY`/`MODBY` — in task.txt but no script or log; confirm if done
- [x] Add `SYGROUP` field (Text/25, "Symbol Group", domain `Bldg_symbol_group`) — ✅ added all envs Jun 15; confirmed already exists in Prod web_RO.gdb Jun 19. No explicit "Succeeded" in log — confirm field is functional.
- [ ] ⚠️ Create `Bldg_symbol_group` domain — `0_new_domain.py` prepared for QA + Prod; no log provided; confirm if run
- [ ] ⚠️ Remove `BLISPSND`, `BLISPO` from `Bldg_symbol_fcode` domain — `domain_value_changes.py` has `TODO: Incomplete`; only targeted prod_rw; no log; confirm status
- [ ] Implement attribute rule to populate `SYGROUP` from FCODE query — not yet done

---

## TASK0320358 – View and Service Updates (prerequisite to TASK0320365)

### Open Questions to Resolve First
- [ ] Decide on `BLD_BUILDING_VW` approach: update existing views now for current apps, or hold until all apps can migrate to new design at once? *(formal design request coming)*
- [ ] Confirm whether `BLD_SYMBOL_ANNO_10K_EVW`, `BLD_SYMBOL_ANNO_20K_EVW`, `BLD_SYMBOL_ANNO_40K_EVW` are still in use
- [ ] Determine which views the new **Symbol Group** field needs to appear in (targeting Open Data release)
- [ ] Check for any views not listed in CMDB or scripts that reference affected feature classes

### BLD_building_polygon – View Investigation
- [x] Investigate `BLD_building_polygon_insp_VW` — ✅ deployed. Final definition: selects all polygon fields (OBJECTID, BLPOLY_ID, BL_ID, FCODE, ZVALUE, HGTSOURCE, LOAD_ID, SOURCE, SACC, GLOBALID, ADDBY, ADDDATE, MODBY, MODDATE, SHAPE, GDB_GEOMATTR_DATA) plus FOOT_SQM, STORIES, HEIGHT_M, FSA_INSP from BLD_BUILDING join. Deleted fields (FOOT_SQFT, FLOORS, SCALE) replaced by BLD_BUILDING equivalents. No aliases.
- [ ] Investigate `BLD_building_polygon_dissolve` — check if it references deleted fields; update if needed
- [ ] Investigate `BLD_BUILDING_VW` — check if it references deleted fields; update if needed

### BLD_BUILDING_USE – View Updates
*(All views: also update to replace `BLD_BUILDING_CIVIC_LINK` join with `BLD_BUILDING_USE.CIV_ID`)*
- [ ] Update `BLD_BUILDING_VW` — remove refs to deleted fields (`WEBURL`, `FIREALARMS`, `COMBUSCONS`, `LICENS_LIQ`); replace civic link join
- [ ] Update `BLD_BLDG_PLUS_USE` — investigate and update
- [ ] Update `BLD_building_use_multi` — investigate and update
- [ ] Update `BLD_BUILDING_VW_IMS` — investigate and update
- [ ] Update `BLD_CIVIC_ADD` — investigate and update
- [ ] Update `BLD_EMO_MORGUE_STAGE` — remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_EMO_SHELTER_STAGE` — remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_EMO_TEMPORARY_MORGUE` — remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_USE_CLASS_LUT` — investigate and update
- [ ] Coordinate with Somya on `buildingdetails.csv` ETL and dashboard updates

### BLD_Building_Symbols – View Updates
*(EMO views: also replace `BLD_BUILDING_CIVIC_LINK` join with `BLD_BUILDING_USE.CIV_ID`)*
- [ ] Update `BLD_EMO_SPEC_POP_VW` — remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_SERVICES_VW_IMS` — investigate and update
- [ ] Update `BLD_SERVICES_VW` — investigate and update
- [ ] Update `BLD_emo_spec_pop_fc` — EMO; remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_EMO_SPEC_POP_STAGE` — EMO; remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_EMO_SPECIAL_POPULATION` — EMO; remove deleted fields/domains; replace civic link join
- [ ] Update `BLD_FIRE_STATION_VW` — investigate and update
- [ ] Update `BLD_FIRE_STATION_VW_IMS` — investigate and update
- [ ] Update `BLD_SCHOOL_VW` — investigate and update
- [ ] Update `BLD_SCHOOL_VW_IMS` — investigate and update
- [ ] Decide fate of `BLD_SYMBOL_ANNO_10K_EVW` — keep or retire? *(pending answer to open question above)*
- [ ] Decide fate of `BLD_SYMBOL_ANNO_20K_EVW` — keep or retire?
- [ ] Decide fate of `BLD_SYMBOL_ANNO_40K_EVW` — keep or retire?
- [ ] Update `BLD_SYMBOL_FCODE_LUT` — investigate and update

---

## TASK0320365 – Multi-Table Cleanup *(blocked on TASK0320358)*

**Now tracked in its own file: `tickets/TASK0320365.md`** (full ServiceNow description, source RFC paths per component, and the actionable checklist). This file keeps only the ticket summary row and the dependency map above.

---

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
