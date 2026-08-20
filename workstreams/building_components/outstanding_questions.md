# Outstanding Questions: Building Component Changes (BLD_* Feature Classes/Tables)

Consolidated from the 8 change forms (TASK0327172–TASK0327179). See `project.md` for full change details.

## Resolved

1. ~~Are these 8 tasks dependent on the AMO confirmation blocking TASK0326632?~~ **Confirmed independent.**
2. ~~ASTLABEL / Siemens sync~~ — "AHU 01" is a recommended data-entry value shown to users, not a field definition requirement. No blocker to adding ASTLABEL.
3. ~~ASTFLOOR granularity (sub-basement / sub-sub-basement)~~ — keep the domain values exactly as listed in the spreadsheet (`BLD_floor_level`: B1, L1–L7, MZ, PH, RF, P1–P3). No further decision needed.
4. ~~RMLIFE auto-calculation (INSTYR + BASELIFE)~~ — implement as an attribute rule rather than a manual field or schema-level calculation. Not a blocker to the field add/rename itself. See `attribute_rules.md` (§3) for the implementation-facing breakdown.
5. ~~ROLLUPID auto-calculation (from BL_ID / Land ID)~~ — implement as an attribute rule, same as RMLIFE. See `attribute_rules.md` (§2) for the implementation-facing breakdown.

## Still open

### Cross-cutting
1. **Generic material domain.** Can a single `BLD_material` domain (values: N/A, Unknown) be created and reused across any subtype that has no meaningful material values, instead of shipping near-empty component-specific placeholder domains? Affects TASK0327172, 74, 75, 77, 78, 79 to varying degrees. `BLD_material_lifesafety` (TASK0327175) and `BLD_material_structure` (TASK0327179) are explicitly flagged for deletion once this exists. See `domain_changes.md` for the full domain-level breakdown.

2. **ASSETSTAT / hiding disposed records.** Is there an application-level way to hide Disposed components from data entry while keeping them viewable for historical lookups (e.g. two related tables/views in the app)? This is a UI/app question, not a schema change, but it's raised on every form.

3. **ASSETID standardization.** Facilities wants a single ID field surfaced in the app rather than both ASSETID and the component-specific ID (e.g. ELECTID). Which field should be the standard, and does ASSETID get dropped from the app view or deleted outright? (TASK0327175/BLD_LIFESAFETY already confirms ASSETID stays — this question is about the other 7 tickets.)

### Component-specific

**TASK0327178 (BLD_SPECIALTY):** PERFRMRA's FMO comment reads "Keep this field. Check Legacy ID equip #" — appears copied from the LEGACYID row in error. Confirm whether PERFRMRA should be deleted (per the standard cross-cutting pattern) or intentionally kept.
   - **Smoking gun:** `fields_to_keep.md`'s actual LEGACYID entry reads "FMO wants to populate with legacy component equipment IDs. Action: check the Legacy ID equipment number before finalizing." — nearly identical wording to the stray PERFRMRA comment. Strongly suggests the PERFRMRA note was pasted from the LEGACYID row rather than an intentional override, i.e. PERFRMRA likely *should* be deleted per the standard pattern. Still needs explicit confirmation before deleting, not treated as resolved.

**BLPOLY_ID (`fields_to_delete.md`, all 8 tickets):** No other doc in this suite mentions this field — it doesn't appear in `fields_to_add.md`, `domain_changes.md`, or anywhere else, and its naming convention (`BLPOLY_ID`) matches `BLD_building_polygon` (a separate table tracked in `../../workflow.md` / TASK0320365), not the 8 building-component tables. Verify against the source `.xlsx` change forms that this was genuinely listed as a deletable field on all 8 component tables before deleting it — it may be a copy/reference error from the polygon table's field set.

**TASK0327179 (BLD_STRUCTURE):**
- Confirm BASELIFE is measured in years (every other component confirms this explicitly; STRUCTURE's form only asks the question).
- Confirm whether RMLIFE represents the actual year the building/component is expected to be replaced, and whether it should be renamed to "Expected Life." Note: this is a distinct question from the RMLIFE attribute-rule resolution above — the other 7 components asked about auto-calculating RMLIFE, but STRUCTURE's form doesn't mention auto-calc at all, only naming/meaning.

**TASK0327177 (BLD_ROOF):** INSRVAL has no domain yet — FDC confirmed there are currently no values to build one from, "might create one in the future." No action needed now; flagged here as a placeholder in case it resurfaces once EXTERIOR's mirrored INSRVAL field is built out.
