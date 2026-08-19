
/
HRM Building Model Changes
HRM Building Model Changes







Recents
Organizing ticket changes in project documentation
Jul 27
GIS building tables project tracking
Jun 25
Instructions
Add instructions to tailor Claude’s responses

Memory
Only you
Purpose & context Alex is a GIS data services professional at Halifax Regional Municipality (HRM), working within an enterprise GIS environment governed by a GIS Design Authority review process. Work centers on schema change tickets for building-related feature classes and tables, coordinated with stakeholders including Lisa O'Toole (requestor/operational data steward), Erin Covill (data custodian), Paul Shaffelburg (SDS signoff), Somya (ETL/dashboard updates), Reyhan (future EMO redesign), Tai (Facilities Design & Construction), and AMO (Asset Management Office) and FMO (Facilities Maintenance & Operations) as the primary requesting bodies. Change requests are tracked in ServiceNow and stored under R:\ICT\ICT GIS\GIS Design Authority\Change Requests\. The work involves field additions, deletions, alias updates, domain changes, attribute rules, and view/service updates across multiple SDE environments and file geodatabases (including webRO.gdb targets). --- Current state Two active workstreams are in progress: Workstream 1 — Building Component tickets (TASK0327172–TASK0327179, due 2026-07-31): Eight parallel schema change tickets covering BLDELECTRICAL, BLDEXTERIOR, BLDINTERIOR, BLDLIFESAFETY, BLDMECHANICAL, BLDROOF, BLDSPECIALTY, and BLDSTRUCTURE. A documentation suite has been built from eight Excel change forms, comprising six markdown files (project.md, outstandingquestions.md, fieldstoadd.md, fieldstodelete.md, fieldstokeep.md, domainchanges.md) plus attributerules.md. Key decisions made: RMLIFE and ROLLUPID → implement as attribute rules CONDITEXP → attribute rule candidate (same-record arithmetic: CONDITDTE + CONDITEXP); verify whether it already exists in SDE before building fresh ASSETGRP → schema-level field default (not an attribute rule); gated on pending AMO deletion confirmation ASTLABEL "AHU 01" → data-entry convention only, not a field definition requirement ASTFLOOR domain values → taken exactly as listed in spreadsheets domainchanges.md structured into three explicit sections: new domains, domains to delete, domains getting new codes/values These eight tickets are independent of TASK0326632 Workstream 2 — BLDbuildingassetpoint and related tickets (TASK0326632, TASK0320358, TASK0320365): Schema changes to BLDbuildingassetpoint (adding HERITAGE, NAMESTATUS, NAMEAPRDTE; deleting ~17 unpopulated fields; alias and domain updates), with several items deferred pending AMO confirmation. TASK0320358 (prerequisite view/service update) is overdue and must be completed before field deletions in TASK0320365 can proceed. BLDBUILDINGCIVICLINK table deletion is planned; joins should be replaced with BLDBUILDINGUSE.CIVID. A new BLDBUILDINGVW design tested by Erin is pending a formal request. Completed work logged includes: domain removals and corrections on BLDbuildingassetpoint (with known failures in webRO.gdb targets where the domain doesn't exist); field deletions on BLDbuildingpolygon; alias updates and SYGROUP field addition on BLDBuildingSymbols; corrected and deployed BLDbuildingpolygoninspVW (replacing deleted fields with FOOTSQM, STORIES, HEIGHTM, and FSAINSP from BLDBUILDING join). --- On the horizon Resolve outstanding AMO confirmation items (e.g., ASSETGRP deletion) before proceeding with gated changes Confirm whether CONDITEXP attribute rule already exists in any SDE environment Complete TASK0320358 (prerequisite) to unblock TASK0320365 field deletions Formal request needed before deploying Erin's new BLDBUILDINGVW design Scripts prepared but unconfirmed for: Bldgsymbolgroup domain creation, BLISPSND/BLISPO domain value removals --- Key learnings & principles webRO.gdb file geodatabases are a recurring failure point — domains present in SDE environments may be absent there, requiring separate handling Attribute rules vs. schema defaults must be distinguished carefully: rules require another field as input; field defaults (like ASSETGRP) do not View SQL can silently break when referenced fields are deleted — scrambled aliases are a known risk requiring post-deletion view audits AMO and FMO are distinct bodies; language about who requested or confirmed a change should be precise --- Approach & patterns Works iteratively: shares scripts, logs, and SQL for Claude to interpret and immediately reflect in tracking documents Maintains structured markdown documentation files as the source of truth for ticket status and progress Flags ambiguous log entries, unconfirmed steps, and open decisions as explicit action items in outstandingquestions.md Reads source Excel change forms programmatically (openpyxl, markitdown) to extract field-level changes from DATASET DETAILS and IMPACTS tabs Prefers explicit, structured organization of domain changes (grouped by type, not flat per-ticket lists) --- Tools & resources ServiceNow (ticket tracking) Enterprise SDE environments + file geodatabases (web_RO.gdb) Excel change forms (source of truth for schema change specifications) Python (openpyxl, markitdown) for parsing spreadsheets Markdown files for project tracking (project.md, workflow.md, and supporting docs) Network path: R:\ICT\ICT GIS\GIS Design Authority\Change Requests\

Last updated Jul 30

Context
1% of project capacity used

project.md
47 lines

md




Changes to BLD_ELECTRICAL.xlsx
xlsx




Changes to BLD_STRUCTURE.xlsx
xlsx




Changes to BLD_ROOF.xlsx
xlsx




Changes to BLD_LIFESAFETY.xlsx
xlsx




Changes to BLD_EXTERIOR.xlsx
xlsx




Changes to BLD_INTERIOR.xlsx
xlsx




Changes to BLD_MECHANICAL.xlsx
xlsx




Changes to BLD_SPECIALTY.xlsx
xlsx



Scheduled
Set up recurring tasks for this project.

project.md


# Project: Building Component Changes (BLD_* Feature Classes/Tables)
 
## Purpose & Context
 
Requestor: Lisa O'Toole
Assigned to: Alex Gallagher
Assignment Group: Data Services Support
Configuration Item: Data Services
Priority: Medium (target end of summer, some flexibility noted)
Opened: 2026-06-30
Due date: 2026-07-31
 
This is a set of 8 parallel Catalog Tasks, one per Building Component, covering changes discussed at the GIS Design Authority. Each task follows the same template:
 
- Fields suggested for removal by AMO
- New asset codes and fields added to support Tai's work with Facilities Design & Construction
- Changes reviewed and approved by Facilities Maintenance & Operations
- Change form details stored in `R:\ICT\ICT GIS\GIS Design Authority\Change Requests\Building Components\Changes to <COMPONENT>.xlsx`
This work appears related to the AMO confirmation dependency already tracked against TASK0326632 (`BLD_building_assetpoint`), since these tasks reference AMO-suggested field removals across building components.
 
## Tickets
 
| Task | RITM | Component | Change Form |
|---|---|---|---|
| TASK0327172 | RITM0311304 | BLD_ELECTRICAL | Changes to BLD_ELECTRICAL.xlsx |
| TASK0327173 | RITM0311305 | BLD_EXTERIOR | Changes to BLD_EXTERIOR.xlsx |
| TASK0327174 | RITM0311306 | BLD_INTERIOR | Changes to BLD_INTERIOR.xlsx |
| TASK0327175 | RITM0311308 | BLD_LIFESAFETY | Changes to BLD_LIFESAFETY.xlsx |
| TASK0327176 | RITM0311309 | BLD_MECHANICAL | Changes to BLD_MECHANICAL.xlsx |
| TASK0327177 | RITM0311310 | BLD_ROOF | Changes to BLD_ROOF.xlsx |
| TASK0327178 | RITM0311311 | BLD_SPECIALTY | Changes to BLD_SPECIALTY.xlsx |
| TASK0327179 | RITM0311312 | BLD_STRUCTURE | Changes to BLD_STRUCTURE.xlsx |
 
All 8 are currently **Open**, same due date (2026-07-31) and follow-up date (2026-06-30).
 
## Open Items / Action Items
 
- Pull each `Changes to <COMPONENT>.xlsx` change form from the GIS Design Authority folder to get the actual field additions/removals per component. Descriptions on the tasks themselves are boilerplate and don't list specifics.
- Confirm whether these 8 tasks are dependent on or independent of the AMO confirmation already blocking items in TASK0326632, since both reference AMO-suggested removals.
- Determine build order across the 8 components (schema-only vs. also touching views/services, similar to the BLD_building_polygon work).
- No environment-specific tracking yet (SDE Dev/QA/Prod, file GDB) for any of these 8. Will need same per-environment verification pattern used on prior tickets.
## Related Prior Work (for reference)
 
See `workflow.md` for status on TASK0326632, TASK0320358, and TASK0320365, which cover `BLD_building_assetpoint`, `BLD_building_polygon`, `BLD_BUILDING_USE`, and `BLD_Building_Symbols`.
 
