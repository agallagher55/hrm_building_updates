# BLD_building_assetpoint: Schema Change Tracking

> Pulled out of `workflow.md` into its own file since this is now the priority workstream. `workflow.md` retains TASK0320358 / TASK0320365 (which cover `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK`) and the related ad hoc work, since those are different feature classes/tables.

## Ticket

| Ticket | RITM | Feature Class | Due Date | Status |
|---|---|---|---|---|
| TASK0326632 | RITM0310811 | `BLD_building_assetpoint` | Jul 10, 2026 ⚠️ | 🔵 In Progress |

**Source RFC:** `changes/Add fields to Building Assetpoint.xlsx` (also at `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\Building Assetpoints\Add fields to Building Assetpoint.xlsx`)

**Related/dependent tickets** (different tables, tracked in `workflow.md`):
- TASK0320358: view/service updates for `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`
- TASK0320365: field/domain/table deletions for the same, plus `BLD_BUILDING_CIVIC_LINK`

---

## Recommended Workflow Order

All of the work below is driven by a single ticket, TASK0326632, so there's no cross-ticket sequencing to worry about within this file. The order matters for two reasons: (1) Pre-Work is investigative and can change what the schema changes actually are, so it needs to happen first, not after; (2) Views, ETL, Open Data, and metadata all read the finished field list, so they need to happen after the schema is final, not interleaved with it (per the "view SQL can silently break when referenced fields are deleted" lesson from the related workstream in `workflow.md`).

1. **Pre-Work**: gating checks (confirm current schema, `FCODE` usage, AR visibility settings, coordinate with Building table changes, notify Digital Services). Do this before touching schema so the Add/Delete lists below don't need revisiting.
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
- [x] Pull a schema export from production RW and check it against the tracked Add/Delete/Alias lists. Done, 2026-08-19, against `BLD_building_assetpoint_SCHEMA.json` (`GISRW01`).
- [x] Cross-check that export against the RFC (`changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab). Done, all 17 deletes, all 3 adds, and all 6 alias targets match, with FMO comments confirming each of the 17 deletes explicitly.
- [ ] Pull the same schema export for prod RO, QA RW/RO, Dev RW/RO, and the three `web_RO.gdb`s, to catch the kind of environment drift already seen on the `SOURCE` domain problem. Only prod RW checked so far.

**Findings from the production RW export:**
- 65 fields total on the feature class today.
- Editor tracking is confirmed **enabled**: creator field `ADDBY` / `ADDDATE`, last-editor field `MODBY` / `MODDATE`. This also answers the "Confirm editor tracking is enabled" item under Domain/Field Fixes below, marked complete now.
- `SOURCE` already carries the `Bldg_TBL_source` domain in this environment, consistent with the June 7 fix log.
- `ASSETGRP` already has the `AAA_asset_group` domain assigned, but no default value is set yet. Matches the pending AMO item in Deferred/Follow-up Items.
- `CONDITEXP` already exists as a field, **and already has an attribute rule attached**: `AssetReg - CONDITEXP - ConditionDateExpiry`, created July 1, 2025, calculating from `CONDITDTE` and `CONDITPERD`. This resolves the open question in `attribute_rules.md` (§4) about whether the rule already exists in any SDE environment, it does, at least in production RW. It also corrects that file's formula description: the rule reads `CONDITDTE` + `CONDITPERD` (the update period, in days), not `CONDITDTE` + `CONDITEXP` as originally written there, since `CONDITEXP` is the field the rule writes *to*, not an input.
- No subtypes, no relationship classes, and no indexes are defined on this feature class today.

### 2. Confirm changes to Building table
- [x] Confirm which table "Building table" refers to. Confirmed `BLD_BUILDING`, 2026-08-19, verified against schema exports for both `BLD_BUILDING` and `BLD_BUILDING_USE` (the latter has neither `NAMESTATUS` nor `NAMEAPRDTE`, ruled out).
- [x] Confirm `NAMESTATUS` / `NAMEAPRDTE` type, length, and domain match exactly between `BLD_BUILDING` and the assetpoint additions. Confirmed, exact match on both, including all four `Bldg_Official_Name` coded values on `NAMESTATUS`.
- [x] Locate the specific "changes submitted for the Building table" RFC. Found: `changes/Delete fields in Building table.xlsx` ("Delete fields in Building table," GIS Design Authority RFC, requestor Lisa O'Toole, dated 2026-04-09, High Priority, **not yet presented at GIS Design Authority** per a note on its DATASET DETAILS tab).
- [x] Confirm the sequencing dependency between the two tickets. Confirmed and important: that RFC's own notes column says, verbatim, **"Add field to `BLD_building_assetpoint` and then delete"** for both `NAMESTATUS` and `NAMEAPRDTE`. So this ticket's adds are a hard prerequisite for that ticket's deletes on those two fields specifically, not just a "verify together" courtesy.
- [ ] Find the ServiceNow TASK/RITM number for the "Delete fields in Building table" RFC. The xlsx itself doesn't carry one, it's a GIS Design Authority form, not a ServiceNow export like the others in this suite.
- [ ] Confirm this ticket's `HERITAGE` / `NAMESTATUS` / `NAMEAPRDTE` adds land (or are at least scheduled ahead of) the Building-table deletion, so the dependency direction in the note above isn't violated.
- [ ] Confirm with Lisa O'Toole whether `HRMINTRST` on this ticket's FORM tab is a typo for `HERITAGE` (see below).
- [ ] Record final coordination outcome here before starting the schema DDL in step 3 of the workflow order above.

**More detail on the "Delete fields in Building table" RFC:**
- **Reason for Change:** "Changes were made to the Building model a couple of years ago to better align with information from POSSE, new fields were added in the Building table. Recently the FDM Property ETL process to update building data for Fire in FDM has been updated. Part of the process was to repoint data to the new fields. Therefore, now those old fields need to be deleted as they are redundant." Unrelated to this ticket's own reasoning, it's a separate cleanup driven by the FDM ETL repoint.
- Its own Requirements line reads: "There are also changes submitted for the Building Polygons and Building tables that should be all verified and implemented together," so there's a third related RFC (Building Polygons) in this same coordination web, on top of this one and the assetpoint one. Not yet located, worth asking Lisa about at the same time.
- Fields flagged "Delete field, already in `BLD_building_assetpoint`" on that RFC: `INSTYRCONF`, `SIZE1UNIT`, `SIZE1CONF`, `DISPOSAL`. These four don't carry the "add first" dependency, they already exist on assetpoint today, so `BLD_BUILDING` can drop its copies independently of this ticket's timeline.
- Its IMPACTS tab lists `BLD_BUILDING_VW` (already tracked in `workflow.md` under TASK0320358 for `BLD_BUILDING_USE` field deletions, same view, two different reasons to update it), `BLD_BLDG_PLUS_USE`, `buildingdetails.csv` (Somya's ETL/dashboard source, also already tracked in `workflow.md`), and `STG_01.ARCGIS.BLD_BUILDING`, `STG_01.ODS.OPENDATA_BUILDING_DETAIL` on the ETL side.

**Worth noting as supporting precedent for the `ROLLUPID` attribute-rule question** (`attribute_rules.md` §2, also flagged in Deferred / Follow-up Items below): `BLD_BUILDING_USE` has two working cross-table calculation rules that write back to `BLD_BUILDING` (`OCC_FSA` to `FSA_INSP`, `DWEL_UNITS` to `TL_RES_UNITS`). So a cross-table attribute rule between related building tables is a proven pattern here already, not unprecedented.

**Also worth double-checking:** the FORM tab's "Field Name(s)" line reads `HRMINTRST, NAMESTATUS, NAMEAPRDTE`, but `HRMINTRST` already exists on `BLD_building_assetpoint` today (confirmed in the schema export) and its own row in the DATASET DETAILS tab says "No change to field at this time." The field that's actually new is `HERITAGE`, not `HRMINTRST`, this looks like a typo on the form.

### 3. Check whether `FCODE` is in use
- [x] Check the schema export for domain, subtype, attribute-rule, or index references to `FCODE`. Done, none found, `FCODE` has no domain, isn't a subtype field (this feature class has no subtypes), and isn't referenced by the one existing attribute rule or by any index.
- [x] Check whether `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG` carries an `FCODE` field. Confirmed yes, it's at least carried into staging structurally, whether it's populated or used downstream from there is still unknown.
- [ ] Check `DM_01.BUILDING.DIM_BUILDING` and `DM_01.BUILDING.DIM_BUILDING_NEW` for `FCODE` usage. No access, folded into the Digital Services notification in §4 below instead of chasing table access separately.
- [ ] Query production for non-null `FCODE` counts and spot-check distinct values on `BLD_building_assetpoint` itself.
- [ ] Ask Somya (via §4) whether anything downstream reads `FCODE`.

This question traces back to an unresolved note on the RFC itself (DATASET DETAILS tab, `FCODE` row): "Is this field being used for anything? Check." It's not tied to a planned delete, so it isn't gating the schema DDL in steps 3 to 4 of the workflow order, it only matters for closing out the open question the RFC raised and as a heads-up if `FCODE` becomes a delete candidate later.

### 4. Notify Digital Services of upcoming field changes
- [ ] Send the notice to Somya, referencing TASK0326632. Somya is part of **Digital Services**, not Data Services, that's the ServiceNow assignment group on this ticket (`Data Services Support`), a different thing from her team.
- [ ] List the exact fields in the notice:
  - **Adds:** `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`
  - **Deletes:** all 17 fields in the Delete Fields section below
  - **Alias-only changes:** `INSTYRCONF`, `INSTDATE`, `INSTCS`, `RMLIFE`, `BASELIFE`, `OWNER`
  - **Domain changes:** `SOURCE` reassignment, plus the pending `FMO` / `FDC` additions to `Bldg_FC_source`
- [ ] Include the `FCODE` question from §3: ask her to check `DM_01.BUILDING.DIM_BUILDING` and `DM_01.BUILDING.DIM_BUILDING_NEW` for `FCODE` usage, and whether anything downstream reads it.
- [ ] Call out the ETL objects that will need matching updates, confirmed per the RFC's IMPACTS tab: `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`, `DM_01.BUILDING.DIM_BUILDING`, `DM_01.BUILDING.DIM_BUILDING_NEW`.
- [ ] Ask how much lead time she needs before deployment, so the notice goes out early enough rather than the day of.
- [ ] Confirm whether her team maintains anything downstream of this table beyond the ETL objects already listed (e.g. a CSV feed or dashboard, similar to the `buildingdetails.csv` note for a different table in `workflow.md`).
- [ ] Log the date the notice was sent, and any response, here once done.

### 5. Confirm Asset Registry visibility settings
- [x] Pull the "Visible in AR" column from the RFC (`changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab). Done.
- [x] Confirm none of the 17 fields on the Delete Fields list are currently AR-visible. Confirmed, all `No` (or blank, for `ASSETRAW`, which has no value entered either way).
- [x] Confirm target AR visibility for the 3 new fields. Confirmed, all `Yes` (`HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`).
- [x] Check for copy-paste inconsistencies like the `PERFRMRA` one flagged for a different ticket in `outstanding_questions.md`. None found on this form, its `PERFRMRA` row reads cleanly: "AMO has suggested this field be deleted" / "Yes, this can be deleted."
- [ ] Confirm `SIZE1UNIT`'s hide-from-AR request has actually been applied in the live Asset Registry app, not just proposed on the form.
- [ ] Decide on `ASSETSTAT`'s toggle-visibility request (show/hide Disposed assets on demand), an app-level feature, not a simple visibility flag, already tracked in Deferred / Follow-up Items below.
- [ ] Confirm the RFC's "Visible in AR" column still matches how Asset Registry is actually configured today (the RFC is a proposal, not necessarily the live state), before relying on it for the deploy.

**The three new fields, target AR visibility:**

| Field | Target AR Visibility | Notes |
|---|---|---|
| `HERITAGE` | Yes | No FMO comment on the row either way |
| `NAMESTATUS` | Yes | FMO: "Yes, Add new field" |
| `NAMEAPRDTE` | Yes | FMO: "Yes, Add new field" |

**Fields with an open AR-visibility question beyond simple Yes/No:**

| Field | Current AR Visibility | Note from the RFC |
|---|---|---|
| `SIZE1UNIT` | No | "Can we hide this field in Asset Registry? The field already says Total Sqft so we don't need a separate field identifying the unit of measure." |
| `ASSETSTAT` | Yes | "Facilities would like to see Disposed asset in AR, is there a way to be able to turn on/off the asset status so it is not automatically visible but they do have the ability to click them on if they need to see disposed?" |

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

Confirmed against the RFC's IMPACTS tab, which also lists which application maps ride on each service, worth knowing before touching any of them:

- [ ] Update `BLD_HRM_OWNED_VW` (feeds Property Map, Government & Admin Map). Definition saved to `sql/views/BLD_HRM_OWNED_VW.sql`, captured from Prod 2026-08-19. **Open question:** this view selects only from `BLD_BUILDING_POLYGON` and `BLD_HRM_OWNED_FINAL`, no `BLD_building_assetpoint` field appears in it directly. Worth confirming whether `BLD_HRM_OWNED_FINAL` is itself derived from `BLD_building_assetpoint` before assuming this view actually needs changes for this ticket.
- [ ] Update `BLD_HRM_INTEREST_VW` (feeds Property Map, Government & Admin Map). Definition saved to `sql/views/BLD_HRM_INTEREST_VW.sql`, captured from Prod 2026-08-19. Same open question as above, it joins `BLD_BUILDING_POLYGON` to `BLD_HRM_INTEREST_FINAL`, no direct `BLD_building_assetpoint` field reference.
- [ ] Update Cityworks Assets / Building Asset Points service
- [ ] Update HRMBaseData / Building Asset Point service (feeds Parks & Recreation Map, Registry Editor Map, Climate Related Hazards)
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
- [ ] Evaluate `ROLLUPID` population via intersect / attribute rule (FMO also wants HRM Land visible in the mapping app once this is built, per the RFC)
- [ ] Evaluate `ACCESSIBLE` field – possible score vs. Y/N in future
- [ ] Evaluate `DISPOSAL` field – add disposal method field (Demolished, Sold, Transferred) in future
- [ ] Evaluate whether `RMLIFE` should become an attribute rule calculating `CONST_YEAR + BASELIFE`, per the requestor's question on the RFC. Not yet confirmed by FMO, currently tracked here as alias-only in Metadata / Alias Updates.

---

## Open Questions

### Resolved
- ~~Which table "Building table" refers to in the Pre-Work item "Confirm changes to Building table"~~ **Confirmed `BLD_BUILDING`**, 2026-08-19, verified against schema exports for both `BLD_BUILDING` and `BLD_BUILDING_USE`. See Pre-Work §2 for the field-level evidence.
- ~~Locate the specific "changes submitted for the Building table" RFC~~ **Found**, 2026-08-19: `changes/Delete fields in Building table.xlsx`. Confirms a hard sequencing dependency, `NAMESTATUS` and `NAMEAPRDTE` must be added here before that RFC deletes them from `BLD_BUILDING`. See Pre-Work §2.

### Still open
- AMO confirmation on `ASSETGRP` deletion is still outstanding; it gates the default-value item above.
- `ROLLUPID` is also referenced as an attribute-rule candidate for the 8 building-component tables (`attribute_rules.md` §2), which depends on `BLD_building_assetpoint` having Land ID populated. Worth confirming that dependency is satisfied before those rules are built.
- The FORM tab's field list for this ticket says `HRMINTRST, NAMESTATUS, NAMEAPRDTE`, but `HRMINTRST` already exists and its own row says "No change to field at this time." Likely a typo for `HERITAGE`, the field that's actually new. Confirm with Lisa O'Toole.
- `BLD_HRM_OWNED_VW` and `BLD_HRM_INTEREST_VW` are listed as impacted by this ticket in the RFC's IMPACTS tab, but their SQL (`sql/views/`) selects only from `BLD_BUILDING_POLYGON` and `BLD_HRM_OWNED_FINAL` / `BLD_HRM_INTEREST_FINAL`, no `BLD_building_assetpoint` field appears directly. Confirm whether those `_FINAL` tables are derived from `BLD_building_assetpoint` before assuming these views need changes.
- No ServiceNow TASK/RITM number found for "Delete fields in Building table," it's a GIS Design Authority RFC without one attached, and a note on its own DATASET DETAILS tab says it "has not been presented at GIS Design Authority yet."
- That same RFC references a third one, "changes submitted for the Building Polygons," not yet located either. Ask Lisa O'Toole for both at once.

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
