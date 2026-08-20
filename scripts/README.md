# scripts

Deployment scripts for TASK0326632 (`BLD_building_assetpoint` schema changes).
See `work/bld_asset_point/bld_asset_point.md` for the full change tracking.

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

## Run order

| # | Script | Change |
|---|--------|--------|
| 1 | `1_add_fields_bld_building_assetpoint.py` | Add `HERITAGE`, `NAMESTATUS`, `NAMEAPRDTE` |
| 2 | `2_delete_fields_bld_building_assetpoint.py` | Delete the 17 unpopulated fields |
| 3 | `3_update_aliases_bld_building_assetpoint.py` | Update 5 confirmed field aliases |
| 4 | `4_add_domain_codes_bld_building_assetpoint.py` | Add `FMO` / `FDC` codes to `Bldg_FC_source` (used by this table's `SOURCE` field) |

Not scripted yet: the `web_RO.gdb` `Bldg_TBL_source` domain-creation gap
(needs the domain created in each GDB before `SOURCE` can be reassigned
there), and the `OWNER` alias update (new alias not yet confirmed). See the
"Domain Updates" and "Metadata / Alias Updates" sections of
`work/bld_asset_point/bld_asset_point.md`.

## completed/

Historical scripts, already executed against real environments (mostly Prod),
uploaded 2026-08-20 for the record — not part of the run order above, and not
guaranteed to run as-is (e.g. `3_assign_domain.py` depends on a legacy
`HRMutils` module that isn't `gispy` and isn't in this repo). Each file has a
header noting what it changed, when/where it ran, and what it confirms or
flags in the tracking docs. `20260607_loggies.log` is the real run log for
`3_assign_domain.py`. See `tickets/TASK0320355.md` for the flagged
`4_new_field.py` feature-class mismatch.
