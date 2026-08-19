# BLD_building_assetpoint — Schema Change Tracking

> Pulled out of `workflow.md` into its own file since this is now the priority workstream. `workflow.md` retains TASK0320358 / TASK0320365 (which cover `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK`) and the related ad hoc work, since those are different feature classes/tables.

## Ticket

| Ticket | Feature Class | Due Date | Status |
|---|---|---|---|
| TASK0326632 | `BLD_building_assetpoint` | Jul 10, 2026 ⚠️ | 🔵 In Progress |

**Related/dependent tickets** (different tables, tracked in `workflow.md`):
- TASK0320358 — view/service updates for `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`
- TASK0320365 — field/domain/table deletions for the same, plus `BLD_BUILDING_CIVIC_LINK`

---

## Pre-Work
- [ ] Verify current schema of `BLD_building_assetpoint` in SDE
- [ ] Confirm changes to Building table (coordinate implementation together per ticket requirements)
- [ ] Check whether `FCODE` field is in use before deleting or modifying
- [ ] Confirm Asset Registry visibility settings for all fields flagged `Visible in AR = No`

## Domain / Field Fixes — Completed June 7, 2026
- [x] Remove `AAA_operator_asset` domain from `ADDBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Remove `AAA_operator_asset` domain from `MODBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Reassign `SOURCE` domain from `Bldg_FC_source` → `Bldg_TBL_source` (prod RW, RO; QA RW, RO; Dev RO) ✅
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` domain (prod RW, RO, web_RO.gdb) ✅
- [ ] 🔴 Fix `SOURCE` domain assignment in **all three `web_RO.gdb`** (Dev, QA, Prod) — `Bldg_TBL_source` does not exist in file geodatabases; domain needs to be added to GDBs first
- [ ] Confirm editor tracking is enabled for `BLD_building_assetpoint`

## Schema Changes – Add Fields
- [ ] Add `HERITAGE` (String, 1, domain: `AAA_yes_no`)
- [ ] Add `NAMESTATUS` (Text, 1, domain: `Bldg_Official_Name`)
- [ ] Add `NAMEAPRDTE` (Date)

## Schema Changes – Delete Fields
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

## Metadata / Alias Updates
- [ ] Update alias for `INSTYRCONF` → Year of Construction Confidence
- [ ] Update alias for `INSTDATE` → Building Official Opened Date
- [ ] Update alias for `INSTCS` → Total Construction Cost
- [ ] Update alias for `RMLIFE` → Expected Life
- [ ] Update alias for `BASELIFE` → Base Life (Years)
- [ ] Update alias for `OWNER` *(confirm new alias)*

## Domain Updates
- [x] Reassign `SOURCE` field domain to `Bldg_TBL_source` — SDE environments ✅
- [ ] 🔴 Add `Bldg_TBL_source` domain to Dev/QA/Prod `web_RO.gdb`, then re-run assign for `SOURCE` field
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` ✅
- [ ] Add `FMO` (Facilities Maintenance & Operations) to `Bldg_FC_source` domain *(still needed per RFC)*
- [ ] Add `FDC` (Facilities Design & Construction) to `Bldg_FC_source` domain *(still needed per RFC)*

## Post-Schema – Views and Services
- [ ] Update `BLD_HRM_OWNED_VW`
- [ ] Update `BLD_HRM_INTEREST_VW`
- [ ] Update Cityworks Assets / Building Asset Points service
- [ ] Update HRMBaseData / Building Asset Point service
- [ ] Update Facilities / Building Asset Point service
- [ ] Update Cityworks Map / Building Asset Points service

## Post-Schema – Data Warehouse / ETL
- [ ] Update `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING_NEW`
- [ ] Coordinate with FDM Property ETL process owner

## Open Data
- [ ] Complete Open Data metadata (tab was blank in RFC)
- [ ] Confirm open data release scope and filters

## SDE Metadata
- [ ] Update SDE Metadata Summary, Description, Tags for `BLD_building_assetpoint`
- [ ] Update CMDB record

## Deferred / Follow-up Items
- [ ] Evaluate whether to create a relationship class to `BLD_BUILDING_NAME`
- [ ] Confirm with AMO whether `ASSETGRP` can be deleted; in the meantime add default value and hide from Asset Registry
- [ ] Work with FMO & CRE on `HRMINTRST` domain refinement (Y – HRM Owned / Y – Leased / Y – HRM Funding)
- [ ] Work with FMO & CRE on `ASSETSTAT` disposal value refinement (Sold / Bldg Demo'd Land Retained / Bldg Demo'd Land Sold)
- [ ] Evaluate `ROLLUPID` population via intersect / attribute rule
- [ ] Evaluate `ACCESSIBLE` field – possible score vs. Y/N in future
- [ ] Evaluate `DISPOSAL` field – add disposal method field (Demolished, Sold, Transferred) in future

---

## Open Questions
- AMO confirmation on `ASSETGRP` deletion is still outstanding — gates the default-value item above.
- `ROLLUPID` is also referenced as an attribute-rule candidate for the 8 building-component tables (`attribute_rules.md` §2), which depends on `BLD_building_assetpoint` having Land ID populated. Worth confirming that dependency is satisfied before those rules are built.

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
