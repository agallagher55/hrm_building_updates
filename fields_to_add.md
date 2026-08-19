# Fields to Add

## Common to all 8 tickets
TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

| Field | Alias | Type | Notes |
|---|---|---|---|
| ASTLABEL | Asset Label | TEXT(40) | "AHU 01" style values are a recommended data-entry convention shown to users, not a field definition requirement. No blocker. |
| ASTROOM | Asset Room Location | TEXT(40) | Straightforward add. |
| ASTFLOOR | Asset Floor Location | TEXT | Uses new domain `BLD_floor_level` (see domain_changes.md), values kept exactly as listed in the spreadsheets. |
| STARTDTE | Start Up Date | Date | Added alongside existing INSTDATE, to separately track install vs. turn-on dates for warranty purposes. |

## Component-specific

### TASK0327172 — BLD_ELECTRICAL
- **ASTTYPE** (Asset Type), TEXT — domain `BLD_electrical_assettype2`, applicable only to subtype 2 (Outlets/Panels); other subtypes default to N/A.

### TASK0327173 — BLD_EXTERIOR
- **ACCESSIBLE** ("Accessible button") — domain `AAA_yes_no`, applicable only to subtype 4 (Exterior Access Control Doors); default N elsewhere.
- **INSRVAL** (Insulation R Value), TEXT — applicable only to Façade; mirrors the existing INSRVAL field on BLD_ROOF.

### TASK0327174 — BLD_INTERIOR
- **ASTTYPE** — domain `BLD_interior_assettype4`.
- **ACCESSIBLE** — domain `AAA_yes_no`, applicable only to subtype 3 (Interior Access Control Doors); default N elsewhere.

### TASK0327175 — BLD_LIFESAFETY
- **ASTTYPE** — domains `BLD_lifesafety_assettype1` and `BLD_lifesafety_assettype2`.

### TASK0327176 — BLD_MECHANICAL
- **PLACEMENT** ("Tank Placement") — domain `BLD_mech_placement`, applicable only to subtype 2 (Tanks).
- **FUELTYPE** — domain `BLD_fueltype`, applicable to subtype 2 (Tanks), subtype 6 (Boiler), and subtype 7 (Generators).
- **ASTTYPE** — domains `BLD_mech_assettype1`, `BLD_mech_assettype4`, `BLD_mech_assettype6`.

### TASK0327177 — BLD_ROOF
- No new component-specific fields. (INSRVAL already exists on this component — not a new add.)

### TASK0327178 — BLD_SPECIALTY
- **ASTTYPE** — domains `BLD_specialty_assettype1`, `2`, `5`, `6`.
- **FTEQACC** ("Fitness Equipment Accessible") — domain `AAA_yes_no`, applicable only to subtype 6 (Fitness Equipment).

### TASK0327179 — BLD_STRUCTURE
- No new fields. Unlike the other 7 components, Structure gets no Asset Type addition on this form.
