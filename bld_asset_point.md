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

**Also cross-checked against the RFC** (`changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab), which is now in this repo. All 17 deletes, all 3 adds, and all 6 alias targets match between the schema export and the RFC, with FMO comments confirming each of the 17 deletes explicitly ("Yes, this can be deleted" on every row). One discrepancy worth flagging: see §2 below on the `HRMINTRST` vs `HERITAGE` naming question.

**Still to do:** this export only covers production RW. Pull the same export for prod RO, QA RW/RO, Dev RW/RO, and the three `web_RO.gdb`s before deploying, to catch the kind of environment drift already seen on the `SOURCE` domain problem.

### 2. Confirm changes to Building table
The RFC (`changes/Add fields to Building Assetpoint.xlsx`, FORM tab) confirms this is real, not a guess:

> **Requirements:** "There are also changes submitted for the Building table that should be verified and implemented together."
>
> **Reason for Change:** "As part of the clean up of fields in the Building table, there are several fields that are duplicated in the building assetpoints. Previously there was a script to keep the datasets in sync but it was cumbersome so it was removed. There are some fields currently in the building table to keep track of the official name of the HRM owned buildings in the building table that make more sense to move over to the building assetpoint. These same fields are already associated to bridge and recreation assets."

So this is specifically about `NAMESTATUS` and `NAMEAPRDTE`: they already exist on "the Building table" today, a sync script used to keep the two datasets aligned but was removed as too cumbersome, and the fix here is to give `BLD_building_assetpoint` its own copy of those fields (the same pattern already used for bridge and recreation assets), not to re-sync them.

**Which table: confirmed `BLD_BUILDING`.** Verified against schema exports for both candidates, pulled from production, 2026-08-19:
- `SDEADM.BLD_BUILDING` has both `NAMESTATUS` and `NAMEAPRDTE`. `SDEADM.BLD_BUILDING_USE` has neither, so it's ruled out.
- The field definitions match exactly what's specified for the assetpoint copy: `NAMESTATUS` is String, length 1, domain `Bldg_Official_Name` with the same four coded values (Administrative, Not Applicable, Commemorative, Naming Rights) on both tables. `NAMEAPRDTE` is Date on both. No drift, the assetpoint additions are a true match, not a near-match.
- `BLD_BUILDING` also has `HRMINTRST`, String length 1, domain `AAA_yes_no`, same definition as the existing `HRMINTRST` on `BLD_building_assetpoint`. Consistent with that field already existing on both, and supports treating the `HRMINTRST` mention on the FORM tab as an unrelated typo (see below) rather than an in-scope change.
- No attribute rule on `BLD_BUILDING` touches `NAMESTATUS` or `NAMEAPRDTE` today (its only rule generates `BL_ID`). Consistent with the RFC's claim that the old sync script was removed rather than replaced with something else, there's nothing currently keeping these fields in sync between the two tables.
- `BLD_BUILDING` duplicates a number of other assetpoint fields too (`OWNER`, `CONST_YEAR`, `TOTAL_SQFT`, `INSTYRCONF`, `SIZE1UNIT`, `SIZE1CONF`, `DISPOSAL`, `HRMINTRST`), which lines up with the RFC's framing of this as "part of the clean up of fields in the Building table." The separate "changes submitted for the Building table" RFC is likely about trimming these duplicates now that `BLD_building_assetpoint` carries its own copies, worth confirming once that RFC is located.

Still to do:
- Find the specific "changes submitted for the Building table" RFC/ticket number, still not located. Ask Lisa O'Toole, or check `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\`. It's not TASK0320358 / TASK0320365, those cover `BLD_BUILDING_USE`, now ruled out as "the Building table" above.
- Record the outcome here before starting the schema DDL in step 3 of the workflow order above.

**Worth noting as supporting precedent for the `ROLLUPID` attribute-rule question** (`attribute_rules.md` §2, also flagged in Deferred / Follow-up Items below): `BLD_BUILDING_USE` has two working cross-table calculation rules that write back to `BLD_BUILDING` (`OCC_FSA` to `FSA_INSP`, `DWEL_UNITS` to `TL_RES_UNITS`). So a cross-table attribute rule between related building tables is a proven pattern here already, not unprecedented.

**Also worth double-checking:** the FORM tab's "Field Name(s)" line reads `HRMINTRST, NAMESTATUS, NAMEAPRDTE`, but `HRMINTRST` already exists on `BLD_building_assetpoint` today (confirmed in the schema export) and its own row in the DATASET DETAILS tab says "No change to field at this time." The field that's actually new is `HERITAGE`, not `HRMINTRST`, this looks like a typo on the form. Worth a quick confirmation with Lisa before treating `HRMINTRST` as in scope for anything.

### 3. Check whether `FCODE` is in use
This question comes straight from the RFC itself (`changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab, `FCODE` row): "Is this field being used for anything? Check." Whoever filled out the form flagged it as an open question and never resolved it, it's not tied to a planned delete.

**Why it matters even though `FCODE` isn't being added or deleted:** it doesn't, for this round. It's not gating any of the schema DDL in steps 3 to 4 of the workflow order. It only matters for closing out the open question the RFC itself raised, so the ticket doesn't leave a loose end, and as a heads-up for later if `FCODE` becomes a delete candidate in some future round.

What's known so far:
- From the schema export: `FCODE` has no domain, isn't a subtype field (this feature class has no subtypes), and isn't referenced by the one existing attribute rule or by any index.
- `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG` has an `FCODE` field, confirmed. So it's at least carried into staging structurally, whether it's populated or used downstream from there is still unknown.
- No access to `DM_01.BUILDING.DIM_BUILDING` or `DM_01.BUILDING.DIM_BUILDING_NEW` to check further.

Since Digital Services needs to be notified of this ticket anyway (§4 below), fold this question into that same email rather than chasing table access separately: ask Somya to check `FCODE` usage on the two `DM_01` tables and confirm whether anything downstream (dashboard, report) reads it.

### 4. Notify Digital Services of upcoming field changes
Somya is part of **Digital Services**, not Data Services, that's the ServiceNow assignment group on this ticket (`Data Services Support`), a different thing from her team.
- Send the notice to Somya, referencing TASK0326632.
- List the exact fields in the notice:
  - **Adds:** `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`
  - **Deletes:** all 17 fields in the Delete Fields section below
  - **Alias-only changes:** `INSTYRCONF`, `INSTDATE`, `INSTCS`, `RMLIFE`, `BASELIFE`, `OWNER`
  - **Domain changes:** `SOURCE` reassignment, plus the pending `FMO` / `FDC` additions to `Bldg_FC_source`
- Include the `FCODE` question from §3 above in the same email: ask her to check `DM_01.BUILDING.DIM_BUILDING` and `DM_01.BUILDING.DIM_BUILDING_NEW` for `FCODE` usage, and whether anything downstream reads it.
- Call out the ETL objects that will need matching updates, confirmed per the RFC's IMPACTS tab: `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`, `DM_01.BUILDING.DIM_BUILDING`, `DM_01.BUILDING.DIM_BUILDING_NEW`.
- Ask how much lead time she needs before deployment, so the notice goes out early enough rather than the day of.
- Confirm whether her team maintains anything downstream of this table beyond the ETL objects already listed (e.g. a CSV feed or dashboard, similar to the `buildingdetails.csv` note for a different table in `workflow.md`).
- Log the date the notice was sent, and any response, here once done.

### 5. Confirm Asset Registry visibility settings
Now sourced from the RFC (`changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab), which does carry a "Visible in AR" column per field.

**Every field on the Delete Fields list is already `Visible in AR = No`** (or blank, for `ASSETRAW`, which has no value entered either way), confirmed against the RFC. So none of the 17 deletions remove something currently visible in Asset Registry.

**The three new fields are all set to `Visible in AR = Yes`:**

| Field | Target AR Visibility | Notes |
|---|---|---|
| `HERITAGE` | Yes | No FMO comment on the row either way |
| `NAMESTATUS` | Yes | FMO: "Yes, Add new field" |
| `NAMEAPRDTE` | Yes | FMO: "Yes, Add new field" |

**Fields with an open AR-visibility question beyond simple Yes/No, worth a decision before closing this ticket:**

| Field | Current AR Visibility | Note from the RFC |
|---|---|---|
| `SIZE1UNIT` | No | "Can we hide this field in Asset Registry? The field already says Total Sqft so we don't need a separate field identifying the unit of measure." Already `No`, confirm it's actually hidden in the live app, not just marked so on the form. |
| `ASSETSTAT` | Yes | "Facilities would like to see Disposed asset in AR, is there a way to be able to turn on/off the asset status so it is not automatically visible but they do have the ability to click them on if they need to see disposed?" This needs an app-level toggle, not a simple visibility flag, already tracked in Deferred / Follow-up Items below. |

- No copy-paste inconsistencies like the `PERFRMRA` one flagged for a different ticket in `outstanding_questions.md` turned up on this form, its `PERFRMRA` row reads cleanly: "AMO has suggested this field be deleted" / "Yes, this can be deleted."
- Remaining step: confirm the RFC's "Visible in AR" column still matches how Asset Registry is actually configured today (the RFC is a proposal, not necessarily the live state), before relying on it for the deploy.

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
- ~~Which table "Building table" refers to in the Pre-Work item "Confirm changes to Building table"~~ **Confirmed `BLD_BUILDING`**, 2026-08-19, verified against schema exports for both `BLD_BUILDING` and `BLD_BUILDING_USE`. See Pre-Work §2 for the field-level evidence. Still open: locating the specific RFC/ticket number for the "changes submitted for the Building table" that need to ship alongside this one.

### Still open
- AMO confirmation on `ASSETGRP` deletion is still outstanding; it gates the default-value item above.
- `ROLLUPID` is also referenced as an attribute-rule candidate for the 8 building-component tables (`attribute_rules.md` §2), which depends on `BLD_building_assetpoint` having Land ID populated. Worth confirming that dependency is satisfied before those rules are built.
- The FORM tab's field list for this ticket says `HRMINTRST, NAMESTATUS, NAMEAPRDTE`, but `HRMINTRST` already exists and its own row says "No change to field at this time." Likely a typo for `HERITAGE`, the field that's actually new. Confirm with Lisa O'Toole.
- `BLD_HRM_OWNED_VW` and `BLD_HRM_INTEREST_VW` are listed as impacted by this ticket in the RFC's IMPACTS tab, but their SQL (`sql/views/`) selects only from `BLD_BUILDING_POLYGON` and `BLD_HRM_OWNED_FINAL` / `BLD_HRM_INTEREST_FINAL`, no `BLD_building_assetpoint` field appears directly. Confirm whether those `_FINAL` tables are derived from `BLD_building_assetpoint` before assuming these views need changes.

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
