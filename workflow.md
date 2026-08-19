# Workflow – GIS Building Tables Schema Changes

## Ticket Summary

| Ticket | Feature Classes / Tables | Due Date | Status |
|---|---|---|---|
| TASK0326632 | `BLD_building_assetpoint` | Jul 10, 2026 | 🔵 In Progress |
| TASK0320358 | `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols` (view updates) | Jan 30, 2026 ⚠️ | ⚪ Not Started |
| TASK0320365 | `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK` (field/domain/table deletions) | Jan 30, 2026 ⚠️ | 🟡 Blocked on TASK0320358 |

> **Sequencing:** TASK0320358 (view updates) must be completed before TASK0320365 (field/domain/table deletions) can proceed. The `BLD_building_polygon` field deletions in TASK0320365 are the only exception — those are already done.

---

## TASK0326632 – BLD_building_assetpoint

### Pre-Work
- [ ] Verify current schema of `BLD_building_assetpoint` in SDE
- [ ] Confirm changes to Building table (coordinate implementation together per ticket requirements)
- [ ] Check whether `FCODE` field is in use before deleting or modifying
- [ ] Confirm Asset Registry visibility settings for all fields flagged `Visible in AR = No`

### Domain / Field Fixes — Completed June 7, 2026
- [x] Remove `AAA_operator_asset` domain from `ADDBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Remove `AAA_operator_asset` domain from `MODBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Reassign `SOURCE` domain from `Bldg_FC_source` → `Bldg_TBL_source` (prod RW, RO; QA RW, RO; Dev RO) ✅
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` domain (prod RW, RO, web_RO.gdb) ✅
- [ ] 🔴 Fix `SOURCE` domain assignment in **all three `web_RO.gdb`** (Dev, QA, Prod) — `Bldg_TBL_source` does not exist in file geodatabases; domain needs to be added to GDBs first
- [ ] Confirm editor tracking is enabled for `BLD_building_assetpoint`

### Schema Changes – Add Fields
- [ ] Add `HERITAGE` (String, 1, domain: `AAA_yes_no`)
- [ ] Add `NAMESTATUS` (Text, 1, domain: `Bldg_Official_Name`)
- [ ] Add `NAMEAPRDTE` (Date)

### Schema Changes – Delete Fields
- [ ] Delete `REPLCSTOTL`
- [ ] Delete `MAT`
- [ ] Delete `MATCONF`
- [ ] Delete `LANDID`
- [ ] Delete `ASSETRAW`
- [ ] Delete `ASSETDESC`
- [ ] Delete `CRIT`
- [ ] Delete `CRITCONF`
- [ ] Delete `RMLIFECONF`
- [ ] Delete `INSTCSCONF`
- [ ] Delete `REPLCSRA`
- [ ] Delete `REPLRACONF`
- [ ] Delete `REPLCSCONF`
- [ ] Delete `TCACAT`
- [ ] Delete `PERFRMRA`
- [ ] Delete `PERFRMCONF`
- [ ] Delete `PROFCNCAT`

### Metadata / Alias Updates
- [ ] Update alias for `INSTYRCONF` → Year of Construction Confidence
- [ ] Update alias for `INSTDATE` → Building Official Opened Date
- [ ] Update alias for `INSTCS` → Total Construction Cost
- [ ] Update alias for `RMLIFE` → Expected Life
- [ ] Update alias for `BASELIFE` → Base Life (Years)
- [ ] Update alias for `OWNER` *(confirm new alias)*

### Domain Updates
- [x] Reassign `SOURCE` field domain to `Bldg_TBL_source` — SDE environments ✅
- [ ] 🔴 Add `Bldg_TBL_source` domain to Dev/QA/Prod `web_RO.gdb`, then re-run assign for `SOURCE` field
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` ✅
- [ ] Add `FMO` (Facilities Maintenance & Operations) to `Bldg_FC_source` domain *(still needed per RFC)*
- [ ] Add `FDC` (Facilities Design & Construction) to `Bldg_FC_source` domain *(still needed per RFC)*

### Post-Schema – Views and Services
- [ ] Update `BLD_HRM_OWNED_VW`
- [ ] Update `BLD_HRM_INTEREST_VW`
- [ ] Update Cityworks Assets / Building Asset Points service
- [ ] Update HRMBaseData / Building Asset Point service
- [ ] Update Facilities / Building Asset Point service
- [ ] Update Cityworks Map / Building Asset Points service

### Post-Schema – Data Warehouse / ETL
- [ ] Update `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING_NEW`
- [ ] Coordinate with FDM Property ETL process owner

### Open Data
- [ ] Complete Open Data metadata (tab was blank in RFC)
- [ ] Confirm open data release scope and filters

### SDE Metadata
- [ ] Update SDE Metadata Summary, Description, Tags for `BLD_building_assetpoint`
- [ ] Update CMDB record

### Deferred / Follow-up Items
- [ ] Evaluate whether to create a relationship class to `BLD_BUILDING_NAME`
- [ ] Confirm with AMO whether `ASSETGRP` can be deleted; in the meantime add default value and hide from Asset Registry
- [ ] Work with FMO & CRE on `HRMINTRST` domain refinement (Y – HRM Owned / Y – Leased / Y – HRM Funding)
- [ ] Work with FMO & CRE on `ASSETSTAT` disposal value refinement (Sold / Bldg Demo'd Land Retained / Bldg Demo'd Land Sold)
- [ ] Evaluate `ROLLUPID` population via intersect / attribute rule
- [ ] Evaluate `ACCESSIBLE` field – possible score vs. Y/N in future
- [ ] Evaluate `DISPOSAL` field – add disposal method field (Demolished, Sold, Transferred) in future

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

### BLD_building_polygon – Field Deletions
- [x] Delete `FOOT_SQFT` ✅ all envs confirmed (Jun 15 log)
- [x] Delete `FLOORS` ✅ all envs confirmed (Jun 15 log)
- [x] Delete `SCALE` ✅ all envs confirmed (Jun 15 log)

### BLD_BUILDING_USE – Field Deletions
- [ ] Delete `WEBURL`
- [ ] Delete `FIREALARMS`
- [ ] Delete `COMBUSCONS`
- [ ] Delete `LICENS_LIQ`

### Domain Value Deletions
- [ ] `Bldg_BLRC_uses` – remove `PRIVATE CLUB`, `SOCIETY HALL`
- [ ] `Bldg_BLRS_uses` – remove `BACKYARD SUITE`, `MOBILE HOME`, `MULTI-UNIT DWELLING`, `SINGLE UNIT DWELLING`, `TOWNHOUSE`, `TWO UNIT DWELLING`
- [ ] `Bldg_BLCM_uses` – remove `RADIO STATION`, `TELEVISION STATION`
- [ ] `Bldg_BLID_uses` – remove `MILL`
- [ ] `Bldg_BLIT_uses` – remove `DERELICT/ABANDONED`, `UNDER CONSTRUCTION`, `VACANT`
- [ ] `Bldg_symbol_fcode` – remove `BLISPSND`, `BLISPO` ⚠️ script prepared but `TODO: Incomplete`; only targeted prod_rw; no log confirming completion

### BLD_BUILDING_CIVIC_LINK – Pre-Deletion Impact Prep
- [ ] Confirm full inventory of EMO views and services that reference this table
- [ ] Coordinate with Somya – Building Details ETL and dashboard updates
- [ ] Update/remove `BuildingData FireInspections / Building Civic Link` service
- [ ] Drop `BLD_BUILDING_CIVIC_LINK_EVW` enterprise view
- [ ] Update Building Report

### BLD_BUILDING_CIVIC_LINK – Table Deletion
- [ ] Delete `BLD_BUILDING_CIVIC_LINK` table (after all above impacts resolved)

### Post-Deletion Cleanup
- [ ] Update CMDB to reflect deleted table and fields
- [ ] Update SDE Metadata for affected feature classes

---

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
