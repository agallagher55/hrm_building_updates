# Domain Changes

## 1. New Domains

### Shared across all 8 tickets
TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

- **`BLD_floor_level`** — supports the new ASTFLOOR field. Values: B1 Basement, L1–L7 (Main through Seventh Floor), MZ Mezzanine, PH Penthouse, RF Roof, P1–P3 Parkade Levels. Use exactly as listed in the spreadsheets — no further decision needed.

### TASK0327172 — BLD_ELECTRICAL
- `BLD_electrical1_assetcode` through `BLD_electrical5_assetcode` (per-subtype Asset Code, 5 subtypes)
- `BLD_electrical_assettype2` (Asset Type, subtype 2 only)

### TASK0327173 — BLD_EXTERIOR
- `BLD_ext1_assetcode` through `BLD_ext7_assetcode` (per-subtype Asset Code, 7 subtypes)
- `BLD_ext_material1` (Stairs/Ramps), `BLD_ext_material2` (Decks), `BLD_ext_material3` (Façade)

### TASK0327174 — BLD_INTERIOR
- `BLD_interior1_assetcode` through `BLD_interior5_assetcode` (per-subtype Asset Code, 5 subtypes)
- `BLD_interior_assettype4` (Asset Type)
- `BLD_interior_material2` (Wall/Ceiling) — explicitly flagged "new domain" on the form
- `BLD_interior_material4` (Interior Finish) — explicitly flagged "new domain" on the form

### TASK0327175 — BLD_LIFESAFETY
- `BLD_lifesafety1_assetcode`, `BLD_lifesafety2_assetcode` (per-subtype Asset Code, 2 subtypes)
- `BLD_lifesafety_assettype1`, `BLD_lifesafety_assettype2` (Asset Type)

### TASK0327176 — BLD_MECHANICAL
- `BLD_mech1_assetcode` through `BLD_mech7_assetcode` (per-subtype Asset Code, 7 subtypes — HVAC alone has ~19 codes)
- `BLD_mech_assettype1`, `BLD_mech_assettype4`, `BLD_mech_assettype6` (Asset Type)
- `BLD_mech_placement` (new field: Tank Placement, subtype 2 only)
- `BLD_fueltype` (new field: Fuel Type, subtypes 2/6/7)
- `BLD_mech_material` (subtype-specific material values)

### TASK0327177 — BLD_ROOF
- `BLD_roof1_assetcode` (Roof), `BLD_roof3_assetcode` (Drains) — only 2 subtypes in use
- `BLD_roof_material` (subtype 1 only, full roofing-material picklist)

### TASK0327178 — BLD_SPECIALTY
- `BLD_specialty1_assetcode` through `BLD_specialty4_assetcode` (existing subtypes)
- `BLD_specialty5_assetcode` — explicitly flagged **"new domain and subtype"** (Gymnasium)
- `BLD_specialty6_assetcode` — explicitly flagged **"new domain and subtype"** (Fitness)
- `BLD_specialty_assettype1`, `2`, `5`, `6` (Asset Type)
- `BLD_specialty_material` (subtype 5/Gymnasium only)

### TASK0327179 — BLD_STRUCTURE
- `BLD_structure1_assetcode` — single domain, no subtype split (only component with just one Asset Code domain)

---

## 2. Domains to Be Deleted

| Domain | Ticket | Status |
|---|---|---|
| `BLD_material_lifesafety` | TASK0327175 (BLD_LIFESAFETY) | Explicitly flagged for deletion once the generic `BLD_material` domain is created — see `outstanding_questions.md` item 1. |
| `BLD_material_structure` | TASK0327179 (BLD_STRUCTURE) | Same as above — pending the generic `BLD_material` domain decision. |

**Pending the same decision** (not yet confirmed for deletion, but would be superseded if the generic `BLD_material` domain is approved): the existing single-value material domains being split into subtype-specific versions, e.g. `BLD_electrical_material` (TASK0327172) and the prior single `BLD_interior_material` domain that TASK0327174's form proposes replacing with `BLD_interior_material1`. Don't delete these until the generic domain question is resolved.

---

## 3. Domains Getting New Codes / Values (existing domain, not a new one)

### TASK0327178 — BLD_SPECIALTY
`BLD_specialty1_assetcode` — description corrections on existing codes:
- `POOLSU`: "Pool Surface" → **"Pool Structure"**
- `POOLSY`: "Pool System" → **"Pool Operating System"**

No other tickets have confirmed cases of new codes being added to an already-existing domain — most of the domain work across these 8 tickets is new domain creation to support the subtype split, rather than extending existing domains. Flag if any of the source spreadsheets turn out to reference a domain that already exists in Prod with a different code set; that would belong here instead of in the "New Domains" section above.
