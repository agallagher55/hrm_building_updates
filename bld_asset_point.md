# BLD_building_assetpoint: Schema Change Tracking

> Pulled out of `workflow.md` into its own file since this is now the priority workstream. `workflow.md` retains TASK0320358 / TASK0320365 (which cover `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK`) and the related ad hoc work, since those are different feature classes/tables.

## Ticket

| Ticket | Feature Class | Due Date | Status |
|---|---|---|---|
| TASK0326632 | `BLD_building_assetpoint` | Jul 10, 2026 ⚠️ | 🔵 In Progress |

**Related/dependent tickets** (different tables, tracked in `workflow.md`):
- TASK0320358: view/service updates for `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`
- TASK0320365: field/domain/table deletions for the same, plus `BLD_BUILDING_CIVIC_LINK`

---

## Recommended Workflow Order

All of the work below is driven by a single ticket, TASK0326632, so there's no cross-ticket sequencing to worry about within this file. The order matters for two reasons: (1) Pre-Work is investigative and can change what the schema changes actually are, so it needs to happen first, not after; (2) Views, ETL, Open Data, and metadata all read the finished field list, so they need to happen after the schema is final, not interleaved with it (per the "view SQL can silently break when referenced fields are deleted" lesson from the related workstream in `workflow.md`).

1. **Pre-Work**: gating checks (confirm current schema, `FCODE` usage, AR visibility settings, coordinate with Building table changes, notify Data Services). Do this before touching schema so the Add/Delete lists below don't need revisiting.
2. **Finish the leftover Domain/Field Fix**: the 🔴 `Bldg_TBL_source` domain gap in the three `web_RO.gdb`s. Independent cleanup left over from June, not blocked by anything above and doesn't block anything below, can run in parallel with Pre-Work.
3. **Schema Changes, Add Fields**, then **Delete Fields**: do these together as one deployment pass across Dev, QA, and Prod (plus `web_RO.gdb`), since they hit the same table in the same environments.
4. **Metadata / Alias Updates** and **Domain Updates**: same deployment pass as #3, batch them together rather than as separate rounds.
5. **Post-Schema, Views and Services**: only once steps 3 and 4 are confirmed in all environments, so views are built against the final field set instead of needing a second pass.
6. **Post-Schema, Data Warehouse / ETL**: after views, since staging/dimension tables and the FDM Property ETL process mirror the same final schema.
7. **Open Data**: after the internal-facing layers (views, ETL) are confirmed working.
8. **SDE Metadata / CMDB**: documentation should reflect final state, so update last, once schema is closed out.
9. **Deferred / Follow-up Items**: explicitly out of the main path, several are gated on AMO confirmation (`ASSETGRP`) and aren't blockers to closing the core ticket.

So: field changes (steps 3 and 4) can go right after Pre-Work, just not before it, and not interleaved with the downstream view/ETL/Open Data work in steps 5 through 7.

---

## Pre-Work
*Driving ticket: TASK0326632*

### 1. Verify current schema of `BLD_building_assetpoint` in SDE
- [x] Verified against `BLD_building_assetpoint_SCHEMA.json`, a schema export pulled from **production read-write** (`GISRW01`), dated 2026-08-19.

**Findings from this export:**
- 65 fields total on the feature class today.
- Editor tracking is confirmed **enabled**: creator field `ADDBY` / `ADDDATE`, last-editor field `MODBY` / `MODDATE`. This also answers the "Confirm editor tracking is enabled" item under Domain/Field Fixes below, marked complete now.
- `SOURCE` already carries the `Bldg_TBL_source` domain in this environment, consistent with the June 7 fix log.
- `ASSETGRP` already has the `AAA_asset_group` domain assigned, but no default value is set yet. Matches the pending AMO item in Deferred/Follow-up Items.
- `CONDITEXP` already exists as a field, **and already has an attribute rule attached**: `AssetReg - CONDITEXP - ConditionDateExpiry`, created July 1, 2025, calculating from `CONDITDTE` and `CONDITPERD`. This resolves the open question in `attribute_rules.md` (§4) about whether the rule already exists in any SDE environment, it does, at least in production RW. It also corrects that file's formula description: the rule reads `CONDITDTE` + `CONDITPERD` (the update period, in days), not `CONDITDTE` + `CONDITEXP` as originally written there, since `CONDITEXP` is the field the rule writes *to*, not an input.
- All 17 fields on the Delete Fields list below exist in this current schema, so that list matches production with no drift.
- None of `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE` exist yet, confirming the Add Fields list is still accurate.
- No subtypes, no relationship classes, and no indexes are defined on this feature class today.

**Still to do:** this export only covers production RW. Pull the same export for prod RO, QA RW/RO, Dev RW/RO, and the three `web_RO.gdb`s before deploying, to catch the kind of environment drift already seen on the `SOURCE` domain problem.

### 2. Confirm changes to Building table
"Building table" most likely refers to `BLD_BUILDING` or `BLD_BUILDING_USE`, given the wider workstream already tracked in `workflow.md`. To confirm:
- Open the TASK0326632 RFC in `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\` and check whether it names a related or dependent table.
- Ask Lisa O'Toole whether the Building table changes referenced on the form are a separate ticket, or are meant to ship in the same window as TASK0326632.
- Check whether this actually points at the TASK0320358 / TASK0320365 work already tracked in `workflow.md` (those cover `BLD_BUILDING_USE` field deletions), since that would mean the coordination is already tracked rather than new.
- If it's a separate, untracked set of changes, get the change form or RFC number for it and add it to this documentation suite the same way `BLD_building_assetpoint` was pulled out.
- Confirm with Erin Covill (data custodian) the current state of that table before finalizing anything here, since the `HERITAGE` / `NAMESTATUS` / `NAMEAPRDTE` additions here may need a matching addition there.
- Record the outcome here (either "no dependency, confirmed independent" or a cross-reference) before starting the schema DDL in step 3 of the workflow order above.

### 3. Check whether `FCODE` is in use
Not documented anywhere else in this doc suite for `BLD_building_assetpoint` specifically (checked `workflow.md`, `outstanding_questions.md`, `project.md`; `FCODE` only comes up there for `BLD_Building_Symbols` and `BLD_building_polygon`, different tables). So this needs to be run down manually:
- From the schema export: `FCODE` has no domain, isn't a subtype field (this feature class has no subtypes at all), and isn't referenced by the one existing attribute rule or by any index. The schema alone can't confirm usage.
- Query production: count non-null `FCODE` values on `BLD_building_assetpoint` and spot-check the distinct values, to see whether it's actually populated.
- Search the view definitions for `FCODE`: `BLD_HRM_OWNED_VW`, `BLD_HRM_INTEREST_VW`.
- Search the four downstream services for an `FCODE` field mapping: Cityworks Assets, HRMBaseData, Facilities, Cityworks Map Building Asset Points.
- Search the ETL layer for `FCODE`: `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`, `DM_01.BUILDING.DIM_BUILDING`, `DM_01.BUILDING.DIM_BUILDING_NEW`.
- Ask Somya whether `FCODE` feeds any dashboard or report.

`FCODE` isn't currently on either the Add or Delete list, so this check is precautionary. Flag it here only if a use turns up that conflicts with a planned change.

### 4. Notify Data Services of upcoming field changes
- Send the notice to Data Services (Somya), referencing TASK0326632.
- List the exact fields in the notice:
  - **Adds:** `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`
  - **Deletes:** all 17 fields in the Delete Fields section below
  - **Alias-only changes:** `INSTYRCONF`, `INSTDATE`, `INSTCS`, `RMLIFE`, `BASELIFE`, `OWNER`
  - **Domain changes:** `SOURCE` reassignment, plus the pending `FMO` / `FDC` additions to `Bldg_FC_source`
- Call out the ETL objects that will need matching updates, so Data Services can plan around them: `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`, `DM_01.BUILDING.DIM_BUILDING`, `DM_01.BUILDING.DIM_BUILDING_NEW`.
- Ask Data Services how much lead time they need before deployment, so the notice goes out early enough rather than the day of.
- Confirm whether Somya's team maintains anything downstream of this table beyond the ETL objects already listed (e.g. a CSV feed or dashboard, similar to the `buildingdetails.csv` note for a different table in `workflow.md`).
- Log the date the notice was sent, and any response, here once done.

### 5. Confirm Asset Registry visibility settings
The original RFC's "Visible in AR" column for `BLD_building_assetpoint` isn't in this repo (only the 8 building-component change forms are under `changes/`), and the schema export doesn't carry an AR-visibility flag either, since that's an application-level setting, not a geodatabase property. Steps to actually confirm it:
- Pull the TASK0326632 RFC from `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\` and find every field marked `Visible in AR = No`.
- Cross-reference each of those fields against however Asset Registry visibility is actually configured today (whichever app or config manages that, e.g. Cityworks) to confirm the flag matches reality before relying on it.
- For every field on the Delete Fields list: confirm nothing in Asset Registry references it even if it's marked not visible, since a hidden field can still be read by a calculated field or a filter behind the scenes.
- For the three new fields (`HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`): confirm what their AR visibility should be at creation, rather than leaving it at whatever the default is.
- Watch for the same kind of copy-paste error already caught on `PERFRMRA` in `outstanding_questions.md`, where an AR flag looked carried over from the wrong row on the form. Don't take the column at face value without a second look.
- Once confirmed, record it here:

| Field | Current AR Visibility | Target AR Visibility | Notes |
|---|---|---|---|
| *(pending RFC review)* | | | |

## Domain / Field Fixes (Completed June 7, 2026)
*Driving ticket: TASK0326632 (carryover cleanup, predates the Add/Delete/Alias/Domain items below)*
- [x] Remove `AAA_operator_asset` domain from `ADDBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Remove `AAA_operator_asset` domain from `MODBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Reassign `SOURCE` domain from `Bldg_FC_source` → `Bldg_TBL_source` (prod RW, RO; QA RW, RO; Dev RO) ✅
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` domain (prod RW, RO, web_RO.gdb) ✅
- [ ] 🔴 Fix `SOURCE` domain assignment in **all three `web_RO.gdb`** (Dev, QA, Prod): `Bldg_TBL_source` does not exist in file geodatabases; domain needs to be added to GDBs first
- [x] Confirm editor tracking is enabled for `BLD_building_assetpoint` ✅ Confirmed via production RW schema export, 2026-08-19 (`editorTrackingEnabled: true`)

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
- [x] Reassign `SOURCE` field domain to `Bldg_TBL_source` (SDE environments) ✅
- [ ] 🔴 Add `Bldg_TBL_source` domain to Dev/QA/Prod `web_RO.gdb`, then re-run assign for `SOURCE` field
- [x] Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` ✅
- [ ] Add `FMO` (Facilities Maintenance & Operations) to `Bldg_FC_source` domain *(still needed per RFC)*
- [ ] Add `FDC` (Facilities Design & Construction) to `Bldg_FC_source` domain *(still needed per RFC)*

## Post-Schema – Views and Services
*Driving ticket: TASK0326632 (must run after Add/Delete/Alias/Domain changes above are final)*
- [ ] Update `BLD_HRM_OWNED_VW`
- [ ] Update `BLD_HRM_INTEREST_VW`
- [ ] Update Cityworks Assets / Building Asset Points service
- [ ] Update HRMBaseData / Building Asset Point service
- [ ] Update Facilities / Building Asset Point service
- [ ] Update Cityworks Map / Building Asset Points service

## Post-Schema – Data Warehouse / ETL
*Driving ticket: TASK0326632 (must run after Add/Delete/Alias/Domain changes above are final)*
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
*Driving ticket: TASK0326632 (deferred out of the main path, several gated on AMO confirmation)*
- [ ] Evaluate whether to create a relationship class to `BLD_BUILDING_NAME`
- [ ] Confirm with AMO whether `ASSETGRP` can be deleted; in the meantime add default value and hide from Asset Registry
- [ ] Work with FMO & CRE on `HRMINTRST` domain refinement (Y – HRM Owned / Y – Leased / Y – HRM Funding)
- [ ] Work with FMO & CRE on `ASSETSTAT` disposal value refinement (Sold / Bldg Demo'd Land Retained / Bldg Demo'd Land Sold)
- [ ] Evaluate `ROLLUPID` population via intersect / attribute rule
- [ ] Evaluate `ACCESSIBLE` field – possible score vs. Y/N in future
- [ ] Evaluate `DISPOSAL` field – add disposal method field (Demolished, Sold, Transferred) in future

---

## Open Questions
- AMO confirmation on `ASSETGRP` deletion is still outstanding; it gates the default-value item above.
- `ROLLUPID` is also referenced as an attribute-rule candidate for the 8 building-component tables (`attribute_rules.md` §2), which depends on `BLD_building_assetpoint` having Land ID populated. Worth confirming that dependency is satisfied before those rules are built.

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
