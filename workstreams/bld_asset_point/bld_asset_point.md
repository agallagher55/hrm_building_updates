# BLD_building_assetpoint: Schema Change Tracking

> Pulled out of `../../workflow.md` into its own file since this is now the priority workstream. `../../workflow.md` retains TASK0320358 / TASK0320365 (which cover `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, `BLD_BUILDING_CIVIC_LINK`) and the related ad hoc work, since those are different feature classes/tables.

## Ticket

| Ticket | RITM | Feature Class | Due Date | Status |
|---|---|---|---|---|
| TASK0326632 | RITM0310811 | `BLD_building_assetpoint` | Jul 10, 2026 ⚠️ | 🔵 In Progress |

**Source RFC:** `../../changes/Add fields to Building Assetpoint.xlsx` (also at `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\Building Assetpoints\Add fields to Building Assetpoint.xlsx`)

**Ticket record:** `../../tickets/TASK0326632.md` (ServiceNow fields and full description verbatim). This file (`bld_asset_point.md`) remains the working doc.

**Related/dependent tickets** (different tables, tracked in `../../workflow.md`):
- TASK0320358: view/service updates for `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`
- TASK0320365: field/domain/table deletions for the same, plus `BLD_BUILDING_CIVIC_LINK`

---

## Recommended Workflow Order

All of the work below is driven by a single ticket, TASK0326632, so there's no cross-ticket sequencing to worry about within this file. The order matters for two reasons: (1) Pre-Work is investigative and can change what the schema changes actually are, so it needs to happen first, not after; (2) Views, ETL, Open Data, and metadata all read the finished field list, so they need to happen after the schema is final, not interleaved with it (per the "view SQL can silently break when referenced fields are deleted" lesson from the related workstream in `../../workflow.md`).

**Planned timeline (per Alex, 2026-08-19):** Dev this week, QA early next week (week of August 25). Prod not yet scheduled.

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
- [x] Cross-check that export against the RFC (`../../changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab). Done, all 17 deletes, all 3 adds, and all 6 alias targets match, with FMO comments confirming each of the 17 deletes explicitly.
- [x] Check for copy-paste inconsistencies on the Delete Fields list, like the `PERFRMRA` one flagged for a different ticket in `../building_components/outstanding_questions.md`. None found on this form, its `PERFRMRA` row reads cleanly: "AMO has suggested this field be deleted" / "Yes, this can be deleted."

**Findings from the production RW export:**
- 65 fields total on the feature class today.
- Editor tracking is confirmed **enabled**: creator field `ADDBY` / `ADDDATE`, last-editor field `MODBY` / `MODDATE`. This also answers the "Confirm editor tracking is enabled" item under Domain/Field Fixes below, marked complete now.
- `SOURCE` already carries the `Bldg_TBL_source` domain in this environment, consistent with the June 7 fix log.
- `ASSETGRP` already has the `AAA_asset_group` domain assigned, but no default value is set yet. Matches the pending AMO item in Deferred/Follow-up Items.
- `CONDITEXP` already exists as a field, **and already has an attribute rule attached**: `AssetReg - CONDITEXP - ConditionDateExpiry`, created July 1, 2025, calculating from `CONDITDTE` and `CONDITPERD`. This resolves the open question in `../building_components/attribute_rules.md` (§4) about whether the rule already exists in any SDE environment, it does, at least in production RW. It also corrects that file's formula description: the rule reads `CONDITDTE` + `CONDITPERD` (the update period, in days), not `CONDITDTE` + `CONDITEXP` as originally written there, since `CONDITEXP` is the field the rule writes *to*, not an input.
- No subtypes, no relationship classes, and no indexes are defined on this feature class today.

### 2. Confirm changes to Building table
- [x] Confirm which table "Building table" refers to. Confirmed `BLD_BUILDING`, 2026-08-19, verified against schema exports for both `BLD_BUILDING` and `BLD_BUILDING_USE` (the latter has neither `NAMESTATUS` nor `NAMEAPRDTE`, ruled out).
- [x] Confirm `NAMESTATUS` / `NAMEAPRDTE` type, length, and domain match exactly between `BLD_BUILDING` and the assetpoint additions. Confirmed, exact match on both, including all four `Bldg_Official_Name` coded values on `NAMESTATUS`.
- [x] Locate the specific "changes submitted for the Building table" RFC. Found: `../../changes/Delete fields in Building table.xlsx` ("Delete fields in Building table," GIS Design Authority RFC, requestor Lisa O'Toole, dated 2026-04-09, High Priority, **not yet presented at GIS Design Authority** per a note on its DATASET DETAILS tab). **Not the same as TASK0320365** (`../../tickets/TASK0320365.md`), that ticket covers `BLD_building_polygon`, `BLD_BUILDING_USE`, `BLD_Building_Symbols`, and `BLD_BUILDING_CIVIC_LINK`, not `BLD_BUILDING` itself. This RFC is its own, separate, still-untracked item.
- [x] Confirm the sequencing dependency between the two tickets. Confirmed and important: that RFC's own notes column says, verbatim, **"Add field to `BLD_building_assetpoint` and then delete"** for both `NAMESTATUS` and `NAMEAPRDTE`. So this ticket's adds are a hard prerequisite for that ticket's deletes on those two fields specifically, not just a "verify together" courtesy.
- [ ] Find the ServiceNow TASK/RITM number for the "Delete fields in Building table" RFC. The xlsx itself doesn't carry one, it's a GIS Design Authority form, not a ServiceNow export like the others in this suite. Still open, not yet found. Ask Lisa O'Toole (requestor on both this RFC and TASK0326632), or search `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\` directly. **Independent of the Digital Services notification in §4**, that's a separate thread with Somya about `FCODE` and ETL objects, not about this ticket number.
- [ ] Record final coordination outcome here before starting the schema DDL in step 3 of the workflow order above. Depends on the item above, not on the Digital Services email.

The order-of-operations requirement itself (`BLD_building_assetpoint`'s adds must land before `BLD_BUILDING` can delete `NAMESTATUS` / `NAMEAPRDTE`) isn't a separate checklist item here, it's tracked once, at the cross-ticket level, in `../../workflow.md`'s Cross-Ticket Dependency Map, alongside the sequencing for every other table in this workstream. Check there for current status rather than duplicating it as a checkbox in this file.

**More detail on the "Delete fields in Building table" RFC:**
- **Reason for Change:** "Changes were made to the Building model a couple of years ago to better align with information from POSSE, new fields were added in the Building table. Recently the FDM Property ETL process to update building data for Fire in FDM has been updated. Part of the process was to repoint data to the new fields. Therefore, now those old fields need to be deleted as they are redundant." Unrelated to this ticket's own reasoning, it's a separate cleanup driven by the FDM ETL repoint.
- Its own Requirements line reads: "There are also changes submitted for the Building Polygons and Building tables that should be all verified and implemented together." **Very likely the same `Changes to BLD_building_polygon feature class.xlsx` RFC already tracked under TASK0320365** (`../../tickets/TASK0320365.md`), both live in the same `Building Polygons` folder on the network share. Worth a quick confirmation, but this isn't a new, unlocated document.
- Fields flagged "Delete field, already in `BLD_building_assetpoint`" on that RFC: `INSTYRCONF`, `SIZE1UNIT`, `SIZE1CONF`, `DISPOSAL`. These four don't carry the "add first" dependency, they already exist on assetpoint today, so `BLD_BUILDING` can drop its copies independently of this ticket's timeline.
- Its IMPACTS tab lists `BLD_BUILDING_VW` (already tracked in `../../workflow.md` under TASK0320358 for `BLD_BUILDING_USE` field deletions, same view, two different reasons to update it), `BLD_BLDG_PLUS_USE`, `buildingdetails.csv` (Somya's ETL/dashboard source, also already tracked in `../../workflow.md`), and `STG_01.ARCGIS.BLD_BUILDING`, `STG_01.ODS.OPENDATA_BUILDING_DETAIL` on the ETL side.

**Worth noting as supporting precedent for the `ROLLUPID` attribute-rule question** (`../building_components/attribute_rules.md` §2, also flagged in Deferred / Follow-up Items below): `BLD_BUILDING_USE` has two working cross-table calculation rules that write back to `BLD_BUILDING` (`OCC_FSA` to `FSA_INSP`, `DWEL_UNITS` to `TL_RES_UNITS`). So a cross-table attribute rule between related building tables is a proven pattern here already, not unprecedented.

### 3. Check whether `FCODE` is in use
- [x] Check the schema export for domain, subtype, attribute-rule, or index references to `FCODE`. Done, none found, `FCODE` has no domain, isn't a subtype field (this feature class has no subtypes), and isn't referenced by the one existing attribute rule or by any index.
- [x] Check whether `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG` carries an `FCODE` field. Confirmed yes, it's at least carried into staging structurally, whether it's populated or used downstream from there is still unknown.
- [ ] Get confirmation on `FCODE` usage from Digital Services. Everything else in this section, `DM_01.BUILDING.DIM_BUILDING` / `DIM_BUILDING_NEW` usage and whether anything downstream reads it, is folded into the notification email in §4 rather than being separate legwork here. Nothing to do on this item until Somya replies.

This question traces back to an unresolved note on the RFC itself (DATASET DETAILS tab, `FCODE` row): "Is this field being used for anything? Check." It's not tied to a planned delete, so it isn't gating the schema DDL in steps 3 to 4 of the workflow order, it only matters for closing out the open question the RFC raised and as a heads-up if `FCODE` becomes a delete candidate later.

### 4. Notify Digital Services of upcoming field changes
**Deployment timeline (per Alex, 2026-08-19):** Dev this week, QA early next week (week of August 25). Notice should go out ahead of the Dev start given this.

**Recipients (per Alex, 2026-08-19):** To: Blair Jeffers, Mukesh Maji, Andrea Assanuma, Somya Agarwal. Cc: Michael Potter, Lisa O'Toole. Broader distribution than just Somya, subject line: "Upcoming field changes to BLD_building_assetpoint (TASK0326632)". Sent 2026-08-19 (ahead of the Thu, Aug 20 scheduled-send suggestion Outlook offered).

- [x] Draft the notice. Done, 2026-08-19.
- [x] Send the notice, referencing TASK0326632, to the Digital Services distribution listed above. Somya is part of **Digital Services**, not Data Services, that's the ServiceNow assignment group on this ticket (`Data Services Support`), a different thing from her team. Sent, 2026-08-19.
- [x] List the exact fields in the notice. Adds and deletes included in full; alias-only changes and domain changes list trimmed down to just the domain changes, alias-only changes left out of the final version, a reasonable call since ETL reads by field name, not alias.
  - **Adds:** `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE`
  - **Deletes:** all 17 fields in the Delete Fields section below
  - **Domain changes:** `SOURCE` reassignment, plus the pending `FMO` / `FDC` additions to `Bldg_FC_source`
- [x] Include the `FCODE` question from §3. Included.
- [x] Call out the ETL objects that will need matching updates, confirmed per the RFC's IMPACTS tab: `STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG`, `DM_01.BUILDING.DIM_BUILDING`, `DM_01.BUILDING.DIM_BUILDING_NEW`. Included.
- [ ] ~~Ask how much lead time she needs before deployment~~ Left out of the final version. Not blocking, worth asking separately once QA wraps up and Prod timing needs to be set.
- [x] Confirm whether her team maintains anything downstream of this table beyond the ETL objects already listed. Included.
- [x] Log the date the notice was sent, and any response, here once done. **Sent 2026-08-19.** Response pending, awaiting confirmation on the `FCODE` question, the 17-field-delete impact check, and whether anything else downstream needs to be flagged.

**Final text (about to send, 2026-08-19):**

> Hey guys,
>
> Just wanted to give a heads-up on some upcoming schema changes to BLD_building_assetpoint (TASK0326632) that may touch some fields your team's ETL processes read from.
> I'm planning to deploy to Dev this week and QA sometime next week (week of August 24).
>
> Fields being added:
> - HERITAGE
> - NAMESTATUS
> - NAMEAPRDTE
>
> Fields being deleted (17 total):
> - REPLCSTOTL, MAT, MATCONF, LANDID, ASSETRAW, ASSETDESC, CRIT, CRITCONF, RMLIFECONF, INSTCSCONF, REPLCSRA, REPLRACONF, REPLCSCONF, TCACAT, PERFRMRA, PERFRMCONF, PROFCNCAT
>
> Domain changes:
> - SOURCE reassigned from Bldg_FC_source to Bldg_TBL_source
> - Bldg_FC_source getting two new codes added: FMO and FDC
>
> I think these tables have already been identified as being impacted:
> - STG_01.ARCGIS.BLD_BUILDING_ASSETPOINT_STG, DM_01.BUILDING.DIM_BUILDING, and DM_01.BUILDING.DIM_BUILDING_NEW.
>
> A few things I wanted to check with you directly:
>
> 1. Can you confirm none of the 17 fields being deleted above are referenced in those three objects? Want to make sure nothing breaks on your end when they're dropped.
> 2. Separately, do you know if FCODE is used anywhere downstream, on DM_01.BUILDING.DIM_BUILDING, DIM_BUILDING_NEW, or in any dashboard or report your team maintains? It's an existing field I'm not touching in this round.
> 3. Is there anything else downstream of BLD_building_assetpoint your team maintains beyond what's listed above, a CSV feed or dashboard, for example, that I should know about before deploying?
>
> Let me know if you have questions.
>
> Thanks!

### 5. Asset Registry visibility (reference only, not a database concern)
Asset Registry visibility is controlled at the service layer, not in the geodatabase schema (confirmed earlier, there's no AR-visibility flag anywhere in the schema export). Out of scope for database work, no live-app confirmation needed here.
- [x] Pull the "Visible in AR" column from the RFC (`../../changes/Add fields to Building Assetpoint.xlsx`, DATASET DETAILS tab), as due-diligence context for the deletes below. Done.
- [x] Confirm none of the 17 fields on the Delete Fields list are currently AR-visible, so the database deletes don't remove anything the service currently shows. Confirmed, all `No` (or blank, for `ASSETRAW`, which has no value entered either way).

**The three new fields, AR visibility per the RFC (informational, whoever owns the service sets this, not a database step):**

| Field | AR Visibility per RFC |
|---|---|
| `HERITAGE` | Yes |
| `NAMESTATUS` | Yes |
| `NAMEAPRDTE` | Yes |

## Domain / Field Fixes (Completed June 7, 2026)
*Driving ticket: TASK0326632 (carryover cleanup, predates the Add/Delete/Alias/Domain items below)*
- [x] Remove `AAA_operator_asset` domain from `ADDBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Remove `AAA_operator_asset` domain from `MODBY` (prod RW, RO, web_RO.gdb) ✅
- [x] Reassign `SOURCE` domain from `Bldg_FC_source` → `Bldg_TBL_source` (prod RW, RO; QA RW, RO; Dev RO) ✅
- [ ] 🔴 **Needs re-check:** Add `CRE` / Corporate Real Estate to `Bldg_TBL_source` domain (prod RW, RO, web_RO.gdb) — was marked ✅ complete including `web_RO.gdb`, but a live re-run of the domain assignment on 2026-08-20 (below) shows `Bldg_TBL_source` still does **not** exist in `prod_web_ro_gdb`. `domains.add_code_value` can't succeed against a domain that isn't there, so either the CRE add only actually landed on `prod_rw`/`prod_ro` (which share the domain via SDE) and the "web_RO.gdb" part of this checkmark is inaccurate, or the domain was removed again since. Worth confirming which.
- [ ] 🔴 Fix `SOURCE` domain assignment in **all three `web_RO.gdb`** (Dev, QA, Prod): `Bldg_TBL_source` does not exist in file geodatabases; domain needs to be added to GDBs first. Confirmed twice now:
  - `20260607_loggies.log` (`scripts/completed/3_assign_domain.py`, 2026-06-07): `AssignDomainToField` failed with `ERROR 000112: Domain does not exist` on `qa_web_ro_gdb` and `prod_web_ro_gdb` (Dev RW/RO, QA RW/RO, Prod RW/RO all succeeded then). Dev's `web_RO.gdb` wasn't targeted in that run.
  - Live re-run against just `qa_web_ro_gdb` and `prod_web_ro_gdb`, 2026-08-20: same `ERROR 000112: Domain does not exist` on both, over two months later — confirms this is still unresolved, not a transient/ordering issue. `dev_web_ro_gdb` still untested.
  - **Next step:** create `Bldg_TBL_source` in the three `web_RO.gdb`s (with its current coded values, via `gispy.domains.transfer_domains` from an SDE workspace where it already exists) before re-running the `SOURCE` field assignment there. Scripted in `scripts/0a_create_domain_bld_building_assetpoint.py` and `scripts/0b_assign_domain_bld_building_assetpoint.py`, dev-only for now.
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
- ~~Locate the specific "changes submitted for the Building table" RFC~~ **Found**, 2026-08-19: `../../changes/Delete fields in Building table.xlsx`. Confirms a hard sequencing dependency, `NAMESTATUS` and `NAMEAPRDTE` must be added here before that RFC deletes them from `BLD_BUILDING`. See Pre-Work §2. This dependency is now tracked at the cross-ticket level in `../../workflow.md`'s Cross-Ticket Dependency Map.
- ~~Whether `HRMINTRST` on the FORM tab's field list is a typo for `HERITAGE`~~ **No, it's not a typo.** Confirmed by Alex, 2026-08-19: `HRMINTRST` is the legitimate, already-existing "HRM Interest" field, unrelated to `HERITAGE`. The FORM tab's summary line simply doesn't mention `HERITAGE` even though it's a genuine add per the DATASET DETAILS tab, an incomplete summary line, not a data error. No action needed.
- ~~That same RFC references a third one, "changes submitted for the Building Polygons"~~ **Very likely already known**, 2026-08-19: matches `Changes to BLD_building_polygon feature class.xlsx`, already tracked under TASK0320365 (`../../tickets/TASK0320365.md`), both live in the same `Building Polygons` network folder. Worth a quick confirmation, but not a new unlocated document.

### Still open
- AMO confirmation on `ASSETGRP` deletion is still outstanding; it gates the default-value item above.
- `ROLLUPID` is also referenced as an attribute-rule candidate for the 8 building-component tables (`../building_components/attribute_rules.md` §2), which depends on `BLD_building_assetpoint` having Land ID populated. Worth confirming that dependency is satisfied before those rules are built.
- `BLD_HRM_OWNED_VW` and `BLD_HRM_INTEREST_VW` are listed as impacted by this ticket in the RFC's IMPACTS tab, but their SQL (`sql/views/`) selects only from `BLD_BUILDING_POLYGON` and `BLD_HRM_OWNED_FINAL` / `BLD_HRM_INTEREST_FINAL`, no `BLD_building_assetpoint` field appears directly. Confirm whether those `_FINAL` tables are derived from `BLD_building_assetpoint` before assuming these views need changes.
- No ServiceNow TASK/RITM number found for "Delete fields in Building table," it's a GIS Design Authority RFC without one attached, and a note on its own DATASET DETAILS tab says it "has not been presented at GIS Design Authority yet."

## Status Legend

| Symbol | Meaning |
|---|---|
| 🔵 | In Progress |
| 🟡 | Blocked / Waiting |
| 🟢 | Complete |
| ⚪ | Not Started |
| 🔴 | Issue / Needs Attention |
