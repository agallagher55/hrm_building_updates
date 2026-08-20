# scripts

Deployment scripts for TASK0326632 (`BLD_building_assetpoint` schema changes).
See `../bld_asset_point.md` for the full change tracking.

## Setup

1. These scripts import from [`gispy`](https://github.com/agallagher55/gispy)
   (`gispy.features.Feature`, `gispy.domains`). Make sure the parent directory
   of your local `gispy` checkout is on `PYTHONPATH`, or install it in
   editable mode: `pip install -e /path/to/gispy`.
2. Copy `config.ini.example` to `config.ini` in this folder and fill in your
   real SDE connection file / GDB paths. `config.ini` is gitignored, it never
   gets committed.

## Running

Each script currently targets `dev_rw` only; the `qa_*` / `prod_*` database
groups are commented out in the `dbs` loop at the bottom of each file.
Uncomment them once a change is verified in Dev/QA and ready to promote.

## Status

Everything below is `BLD_building_assetpoint` work under **TASK0326632**, except the last
`completed/` row (`4_new_field.py`), which is **TASK0320355** (targeted the wrong feature class,
confirmed to have caused no harm — see `../../../tickets/TASK0320355.md`).

`completed/` = already run historically, kept for the record — not part of the active run order,
not guaranteed to run as-is (`3_assign_domain.py` depends on a legacy `HRMutils` module that isn't
`gispy` and isn't in this repo). `20260607_loggies.log` is the real run log for `completed/3_assign_domain.py`.

| Order | Script | Change | Environment(s) | Status |
|---|---|---|---|---|
| *(done)* | `completed/1_domain_value_changes.py` | Add `CRE` code to `Bldg_TBL_source` | Prod RW, RO, `web_RO.gdb` | ✅ Done |
| *(done)* | `completed/2_remove_domain.py` | Remove `AAA_operator_asset` domain from `ADDBY`/`MODBY` | Prod RW, RO, `web_RO.gdb` | ✅ Done |
| *(done)* | `completed/3_assign_domain.py` | Assign `Bldg_TBL_source` to `SOURCE` field | Dev RO, QA RW/RO, Prod RW/RO | ✅ Done — but ❌ still fails on `dev_web_ro_gdb`/`qa_web_ro_gdb`/`prod_web_ro_gdb` (`Bldg_TBL_source` doesn't exist there; re-confirmed 2026-08-20). Fixed by `0a`/`0b` below. |
| *(done)* | `completed/4_new_field.py` | Add `HGTSOURCE` (meant for `BLD_building_polygon`, mistakenly targeted `BLD_building_symbol`) | Prod RW, RO | ⚠️ Ran, but field doesn't exist on `BLD_building_symbol` in QA or Prod — confirmed harmless, nothing to clean up. Ticket: **TASK0320355** |
| 0a | `0a_create_domain_bld_building_assetpoint.py` | Create `Bldg_TBL_source` in `web_RO.gdb` (transferred from an SDE workspace) | `dev_web_ro_gdb` (QA/Prod commented out) | ⬜ Not run |
| 0b | `0b_assign_domain_bld_building_assetpoint.py` | Assign `Bldg_TBL_source` to `SOURCE` field in `web_RO.gdb` | `dev_web_ro_gdb` (QA/Prod commented out) | ⬜ Not run |
| 1 | `1_add_fields_bld_building_assetpoint.py` | Add `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE` | `dev_rw` (QA/Prod commented out) | ⬜ Not run |
| 2 | `2_delete_fields_bld_building_assetpoint.py` | Delete the 17 unpopulated fields | `dev_rw` (QA/Prod commented out) | ⬜ Not run |
| 3 | `3_update_aliases_bld_building_assetpoint.py` | Update 5 confirmed field aliases | `dev_rw` (QA/Prod commented out) | ⬜ Not run |
| 4 | `4_add_domain_codes_bld_building_assetpoint.py` | Add `FMO` / `FDC` codes to `Bldg_FC_source` (used by this table's `SOURCE` field) | `dev_rw` (QA/Prod commented out) | ⬜ Not run |

`0a`/`0b` are numbered ahead of `1-4` because they close out older, independent leftover work
(`bld_asset_point.md`'s Domain / Field Fixes section) rather than because anything in `1-4`
depends on them — the two groups touch different domains and workspaces, so either order works.

Not scripted yet: the `OWNER` alias update (new alias not yet confirmed). See "Metadata /
Alias Updates" in `../bld_asset_point.md`.
