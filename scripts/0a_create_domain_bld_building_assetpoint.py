"""
TASK0326632 — Create the Bldg_TBL_source domain in web_RO.gdb (doesn't exist there yet).
Source: work/bld_asset_point/bld_asset_point.md, "Domain / Field Fixes",
"Fix SOURCE domain assignment in all three web_RO.gdb".

Confirmed missing in qa_web_ro_gdb and prod_web_ro_gdb via a live re-run on 2026-08-20
(AssignDomainToField still fails with "ERROR 000112: Domain does not exist" in both).
dev_web_ro_gdb is untested but presumed to have the same gap.

Transfers the domain (with its current coded values, e.g. CRE) from an SDE workspace
where it already exists into the target web_RO.gdb, rather than recreating it from
scratch, so the coded values stay in sync. Run this before
0b_assign_domain_bld_building_assetpoint.py.
"""

import logging
import os

from configparser import ConfigParser
from datetime import date

import arcpy

from gispy import domains

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_create_domain_bld_building_assetpoint.log")

logger = logging.getLogger('locators')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

log_formatter = logging.Formatter(
    '%(asctime)s | %(levelname)s | FUNCTION: %(funcName)s | Msgs: %(message)s', datefmt='%d-%b-%y %H:%M:%S'
)

file_handler.setFormatter(log_formatter)
console_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

config = ConfigParser()
config.read(os.path.join(SCRIPT_DIR, 'config.ini'))

DOMAINS_TO_TRANSFER = ["Bldg_TBL_source"]

if __name__ == "__main__":

    PC_NAME = os.environ['COMPUTERNAME']
    run_from = "SERVER" if "APP" in PC_NAME else "LOCAL"

    from_workspace = config.get(run_from, "dev_rw")

    for target_web_ro_gdb in [

        config.get(run_from, "dev_web_ro_gdb"),

        # config.get(run_from, "qa_web_ro_gdb"),
        # config.get(run_from, "prod_web_ro_gdb"),

    ]:

        if target_web_ro_gdb:
            logger.info(f"Transferring {DOMAINS_TO_TRANSFER} from '{from_workspace}' to '{target_web_ro_gdb}'...")

            result = domains.transfer_domains(
                domains=DOMAINS_TO_TRANSFER,
                output_workspace=target_web_ro_gdb,
                from_workspace=from_workspace,
            )
            logger.info(result)
