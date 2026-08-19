# Fields to Keep (AMO suggested deletion, FMO overrode)

## Common to all 8 tickets
TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

| Field | Reason to keep |
|---|---|
| INSTDATE | Relevant to building components and linked to warranties. |
| LEGACYID | FMO wants to populate with legacy component equipment IDs. Action: check the Legacy ID equipment number before finalizing. |

## Component-specific
### TASK0327175 — BLD_LIFESAFETY
- **ASSETID** — explicitly confirmed to keep on this form (unlike the other 7 components, where ASSETID standardization is still an open question — see `outstanding_questions.md`).

---

# Alias-Only Updates (field kept, label/description changes only)

Applies to all 8 tickets: TASK0327172–TASK0327179.

| Field | Change |
|---|---|
| OWNER | Update alias. |
| BASELIFE | Update alias ("Base Life (years)"), confirmed to be in years. |

**Exception — TASK0327179 (BLD_STRUCTURE):** BASELIFE and RMLIFE are not simple alias updates here. The form poses open questions instead (units for BASELIFE, meaning/rename for RMLIFE) — tracked in `outstanding_questions.md`, not finalized as alias-only.
