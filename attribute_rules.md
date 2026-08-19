# Potential Attribute Rules

Fields where the change forms describe automatic/calculated behavior rather than manual data entry. These are candidates for GIS attribute rules (calculated or constraint rules) rather than plain schema field additions. Cross-referenced against `outstanding_questions.md` — the calc/automation questions there are resolved as "build an attribute rule," this file is the implementation-facing breakdown of what those rules need to do and where.

## 1. LOCATION — concatenated description field

**Applies to all 8 tickets** — TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

- **Field:** LOCATION (existing field, "Visible in AR" = Yes but not editable — already expected to be system-populated, not manually entered)
- **Requested behavior:** auto-populate using the building component framework naming convention, concatenating: `<Asset Code Description>, <ASTLABEL>, <MAKE>, <MODEL>, <SERIALNUM>, <ASTTYPE>, <ASTFLOOR>, <ASTROOM>`
- **Rule type:** Calculation attribute rule, triggered on insert/update.
- **Dependency:** relies on ASTLABEL, ASTFLOOR, ASTROOM all existing first (see `fields_to_add.md`) — build this rule after those fields are added on each feature class.
- **Note:** since ASTTYPE doesn't exist on TASK0327177 (BLD_ROOF) or TASK0327179 (BLD_STRUCTURE), the concatenation logic for those two feature classes needs to skip or omit that segment.

## 2. ROLLUPID — calculated from BL_ID / Building Assetpoint

**Applies to all 8 tickets** — TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

- **Field:** ROLLUPID ("Roll Up ID" — rolls assets up to the Land ID level so everything on an HRM land parcel can be grouped for reporting)
- **Requested behavior:** calculate from BL_ID, referencing the Land ID stored in `BLD_building_assetpoint`.
- **Rule type:** Calculation attribute rule, likely requiring a cross-table/related-table lookup (BL_ID → BLD_building_assetpoint → Land ID), so this may need a batch or referential rule rather than a simple same-record calculation — worth confirming feasibility before committing to the approach across all 8 feature classes.
- **Dependency:** relies on `BLD_building_assetpoint` already having the Land ID populated (per your memory notes, this was part of the TASK0326632 work).

## 3. RMLIFE — calculated as INSTYR + BASELIFE

**Applies to 7 of the 8 tickets** — TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY)

**Does NOT apply to TASK0327179 (BLD_STRUCTURE)** — its form raises a different, unresolved question about what RMLIFE actually represents and whether it should be renamed, with no auto-calc requested. See `outstanding_questions.md` for that open item; don't build this rule on BLD_STRUCTURE until that's clarified.

- **Field:** RMLIFE ("Expected Life Year" on the 7 applicable components)
- **Requested behavior:** `RMLIFE = INSTYR + BASELIFE`
- **Rule type:** Calculation attribute rule, straightforward same-record arithmetic (no cross-table lookup needed, unlike ROLLUPID).
- **Dependency:** relies on BASELIFE alias update being finalized first (see `alias_updates.md`).

## 4. CONDITEXP — Condition Date Expiry

**Appears on all 8 tickets** — TASK0327172, 73, 74, 75, 76, 77, 78, 79 (all 8 feature classes)

- **Field:** CONDITEXP ("Condition Date Expiry")
- **Description on every form:** "Dynamic field to calculate the date for condition inspection (CONDITDTE + CONDITEXP)"
- **Confirmed:** treat as a genuine attribute rule candidate. Check each SDE environment to see whether it's already implemented; if not, build it as a calculation rule (`CONDITDTE + CONDITEXP` → resulting inspection date), same pattern as RMLIFE (same-record arithmetic, no cross-table lookup needed).

## 5. ASSETGRP — Asset Group (confirmed: default value, not an attribute rule)

**Appears on all 8 tickets** — TASK0327172, 73, 74, 75, 76, 77, 78, 79 (all 8 feature classes)

- **Field:** ASSETGRP ("Asset Group")
- **Note:** "We can add a default value to the database and this field can automatically get populated. Hide from Asset Registry."
- **Confirmed:** this is a constant field default (e.g. always "Building" for these feature classes), not a calculation derived from other fields — there's no other-record input that would ever produce a different value, so an attribute rule isn't the right mechanism here. Set it as a schema-level field default instead.
- **Dependency:** still pending the AMO confirmation on deletion (see `outstanding_questions.md`). Don't set the default until that's resolved — it may end up deleted rather than defaulted.

---

## Summary by ticket

| Ticket | Feature Class | LOCATION | ROLLUPID | RMLIFE | CONDITEXP | ASSETGRP (default, not an attribute rule) |
|---|---|---|---|---|---|---|
| TASK0327172 | BLD_ELECTRICAL | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327173 | BLD_EXTERIOR | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327174 | BLD_INTERIOR | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327175 | BLD_LIFESAFETY | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327176 | BLD_MECHANICAL | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327177 | BLD_ROOF | Yes (no ASTTYPE segment) | Yes | Yes | Yes | Pending AMO |
| TASK0327178 | BLD_SPECIALTY | Yes | Yes | Yes | Yes | Pending AMO |
| TASK0327179 | BLD_STRUCTURE | Yes (no ASTTYPE segment) | Yes | **No — open question, don't build yet** | Yes | Pending AMO |
