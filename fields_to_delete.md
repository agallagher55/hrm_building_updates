# Fields to Delete

AMO-suggested, FMO-confirmed. Same field set across all 8 tickets:

TASK0327172 (BLD_ELECTRICAL), TASK0327173 (BLD_EXTERIOR), TASK0327174 (BLD_INTERIOR), TASK0327175 (BLD_LIFESAFETY), TASK0327176 (BLD_MECHANICAL), TASK0327177 (BLD_ROOF), TASK0327178 (BLD_SPECIALTY), TASK0327179 (BLD_STRUCTURE)

| Field | Notes |
|---|---|
| MATCONF | Material Confidence |
| INSTYRCONF | Install Year Confidence |
| INSTCSCONF | Install Cost Confidence |
| REPLCSTOTL | Replacement Cost Total |
| REPLCSCONF | Replacement Cost Confidence |
| RMLIFECONF | Remaining Life Confidence |
| ASSETRAW | — |
| PROFCNCAT | Profile Key Concatenation |
| CRIT | Criticality |
| CRITCONF | Criticality Confidence |
| REPLCSRA | Replacement Cost Rate |
| REPLRACONF | Replacement Rate Confidence |
| TCACAT | TCA Category |
| PERFRMRA | Performance Rate — **see flag below for TASK0327178** |
| PERFRMCONF | Performance Rate Confidence |
| BLPOLY_ID | Not populated in any of the 8 components |

## Flag: TASK0327178 (BLD_SPECIALTY)
PERFRMRA's FMO comment reads "Keep this field. Check Legacy ID equip #" — looks copy-pasted from the LEGACYID row rather than an intentional override. Tracked in `outstanding_questions.md`; treat as pending until confirmed, don't delete without checking.
