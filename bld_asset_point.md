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

## Recommended Workflow Order

All of the work below is driven by a single ticket, TASK0326632 — there's no cross-ticket sequencing to worry about within this file. The order matters for two reasons: (1) Pre-Work is investigative and can change what the schema changes actually are, so it needs to happen first, not after; (2) Views, ETL, Open Data, and metadata all read the finished field list, so they need to happen after the schema is final, not interleaved with it (per the "view SQL can silently break when referenced fields are deleted" lesson from the related workstream in `workflow.md`).

1. **Pre-Work** — gating checks (confirm current schema, `FCODE` usage, AR visibility settings, coordinate with Building table changes). Do this before touching schema so the Add/Delete lists below don't need revisiting.
2. **Finish the leftover Domain/Field Fix** — the 🔴 `Bldg_TBL_source` domain gap in the three `web_RO.gdb`s. Independent cleanup left over from June; not blocked by anything above and doesn't block anything below — can run in parallel with Pre-Work.
3. **Schema Changes – Add Fields**, then **Delete Fields** — do these together as one deployment pass across Dev → QA → Prod (+ `web_RO.gdb`), since they hit the same table in the same environments.
4. **Metadata / Alias Updates** and **Domain Updates** — same deployment pass as #3; batch them together rather than as separate rounds.
5. **Post-Schema – Views and Services** — only once #3–4 are confirmed in all environments, so views are built against the final field set instead of needing a second pass.
6. **Post-Schema – Data Warehouse / ETL** — after views, since staging/dimension tables and the FDM Property ETL process mirror the same final schema.
7. **Open Data** — after the internal-facing layers (views, ETL) are confirmed working.
8. **SDE Metadata / CMDB** — documentation should reflect final state, so update last, once schema is closed out.
9. **Deferred / Follow-up Items** — explicitly out of the main path; several are gated on AMO confirmation (`ASSETGRP`) and aren't blockers to closing the core ticket.

So: field changes (steps 3–4) can go right after Pre-Work — just not before it, and not interleaved with the downstream view/ETL/Open Data work in steps 5–7.

---

## Pre-Work
*Driving ticket: TASK0326632*
- [ ] Verify current schema of `BLD_building_assetpoint` in SDE
- [ ] Confirm changes to Building table (coordinate implementation together per ticket requirements)
- [ ] Check whether `FCODE` field is in use before deleting or modifying
- [ ] Confirm Asset Registry visibility settings for all fields flagged `Visible in AR = No`

## Domain / Field Fixes — Completed June 7, 2026
*Driving ticket: TASK0326632 — carryover cleanup, predates the Add/Delete/Alias/Domain items below*
- [x] Remove `AAA_operator_asset` domain from `ADDBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Remove `AAA_operator_asset` domain from `MODBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Reassign `SOURCE` domain from `Bldg_FC_source` → `Bldg_TBL_source` (prod RW, RO; QA RW, RO; Dev RO) ✅
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` domain (prod RW, RO, web_RO.gdb) ✅
- [ ] 🔴 Fix `SOURCE` domain assignment in **all three `web_RO.gdb`** (Dev, QA, Prod) — `Bldg_TBL_source` does not exist in file geodatabases; domain needs to be added to GDBs first
- [ ] Confirm editor tracking is enabled for `BLD_building_assetpoint`

## Schema Changes – Add Fields
*Driving ticket: TASK0326632*
- [ ] Add `HERITAGE` (String, 1, domain: `AAA_yes_no`)
- [ ] Add `NAMESTATUS` (Text, 1, domain: `Bldg_Official_Name`)
- [ ] Add `NAMEAPRDTE` (Date)

## Schema Changes – Delete Fields
*Driving ticket: TASK0326632*
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
*Driving ticket: TASK0326632*
- [ ] Update alias for `INSTYRCONF` → Year of Construction Confidence
- [ ] Update alias for `INSTDATE` → Building Official Opened Date
- [ ] Update alias for `INSTCS` → Total Construction Cost
- [ ] Update alias for `RMLIFE` → Expected Life
- [ ] Update alias for `BASELIFE` → Base Life (Years)
- [ ] Update alias for `OWNER` *(confirm new alias)*

## Domain Updates
*Driving ticket: TASK0326632*
- [x] Reassign `SOURCE` field domain to `Bldg_TBL_source` — SDE environments ✅
- [ ] 🔴 Add `Bldg_TBL_source` domain to Dev/QA/Prod `web_RO.gdb`, then re-run assign for `SOURCE` field
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` ✅
- [ ] Add `FMO` (Facilities Maintenance & Operations) to `Bldg_FC_source` domain *(still needed per RFC)*
- [ ] Add `FDC` (Facilities Design & Construction) to `Bldg_FC_source` domain *(still needed per RFC)*

## Post-Schema – Views and Services
*Driving ticket: TASK0326632 — must run after Add/Delete/Alias/Domain changes above are final*
- [ ] Update `BLD_HRM_OWNED_VW`
- [ ] Update `BLD_HRM_INTEREST_VW`
- [ ] Update Cityworks Assets / Building Asset Points service
- [ ] Update HRMBaseData / Building Asset Point service
- [ ] Update Facilities / Building Asset Point service
- [ ] Update Cityworks Map / Building Asset Points service

## Post-Schema – Data Warehouse / ETL
*Driving ticket: TASK0326632 — must run after Add/Delete/Alias/Domain changes above are final*
- [ ] Update `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING`
- [ ] Update `DM_01.BUILDING.DIM_BUILDING_NEW`
- [ ] Coordinate with FDM Property ETL process owner

## Open Data
*Driving ticket: TASK0326632*
- [ ] Complete Open Data metadata (tab was blank in RFC)
- [ ] Confirm open data release scope and filters

## SDE Metadata
*Driving ticket: TASK0326632*
- [ ] Update SDE Metadata Summary, Description, Tags for `BLD_building_assetpoint`
- [ ] Update CMDB record

## Deferred / Follow-up Items
*Driving ticket: TASK0326632 — deferred out of the main path, several gated on AMO confirmation*
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
