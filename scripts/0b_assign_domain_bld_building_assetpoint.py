"""
TASK0326632 — Re-run the Bldg_TBL_source -> SOURCE field assignment against web_RO.gdb,
now that 0a_create_domain_bld_building_assetpoint.py has created the domain there.
Source: work/bld_asset_point/bld_asset_point.md, "Domain / Field Fixes",
"Fix SOURCE domain assignment in all three web_RO.gdb".

RW/RO SDE connections already have this assignment (see scripts/completed/3_assign_domain.py
and its log) - only the web_RO.gdb file geodatabases still need it.
"""

import logging
import os

from configparser import ConfigParser
from datetime import date

import arcpy

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_assign_domain_bld_building_assetpoint.log")

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

UPDATE_FEATURE = "SDEADM.BLD_building_assetpoint"
FIELD_DOMAIN_INFO = {
    "SOURCE": "Bldg_TBL_source",
}

if __name__ == "__main__":

    PC_NAME = os.environ['COMPUTERNAME']
    run_from = "SERVER" if "APP" in PC_NAME else "LOCAL"

    for db in [

        config.get(run_from, "dev_web_ro_gdb"),

        # config.get(run_from, "qa_web_ro_gdb"),
        # config.get(run_from, "prod_web_ro_gdb"),

    ]:

        if db:
            logger.info(f"DATABASE: {db}")

            update_feature = UPDATE_FEATURE.replace("SDEADM.", "") if db.lower().endswith(".gdb") else UPDATE_FEATURE

            logger.info(f"Feature: {update_feature}")

            with arcpy.EnvManager(workspace=db):

                if not arcpy.Exists(update_feature):
                    raise ValueError(f"\tFeature, '{update_feature}', does not exist.")

                for field, domain in FIELD_DOMAIN_INFO.items():
                    logger.info(f"{field}: {domain}")

                    arcpy.AssignDomainToField_management(
                        in_table=update_feature,
                        field_name=field,
                        domain_name=domain,
                        subtype_code=None,
                    )
                    logger.info(arcpy.GetMessages())
