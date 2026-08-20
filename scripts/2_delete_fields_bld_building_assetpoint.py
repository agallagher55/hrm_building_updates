"""
TASK0326632 — Delete fields from BLD_building_assetpoint.
Source: work/bld_asset_point/bld_asset_point.md, "Schema Changes - Delete Fields"
"""

import logging
import os

from configparser import ConfigParser
from datetime import date

import arcpy

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_delete_fields_bld_building_assetpoint.log")

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

delete_fields = [
    'REPLCSTOTL',
    'MAT',
    'MATCONF',
    'LANDID',
    'ASSETRAW',
    'ASSETDESC',
    'CRIT',
    'CRITCONF',
    'RMLIFECONF',
    'INSTCSCONF',
    'REPLCSRA',
    'REPLRACONF',
    'REPLCSCONF',
    'TCACAT',
    'PERFRMRA',
    'PERFRMCONF',
    'PROFCNCAT',
]

if __name__ == "__main__":

    PC_NAME = os.environ['COMPUTERNAME']
    run_from = "SERVER" if "APP" in PC_NAME else "LOCAL"

    for dbs in [

        [
            config.get(run_from, "dev_rw"),
            # config.get(run_from, "dev_ro"),
            # config.get(run_from, "dev_web_ro_gdb"),
        ],

        # [
        #     config.get(run_from, "qa_rw"),
        #     config.get(run_from, "qa_ro"),
        #     config.get(run_from, "qa_web_ro_gdb"),
        # ],
        # [
        #     config.get(run_from, "prod_rw"),
        #     config.get(run_from, "prod_ro"),
        #     config.get(run_from, "prod_web_ro_gdb"),
        # ],

    ]:

        if dbs:
            logger.info(f"Processing dbs: {', '.join(dbs)}...")

            for db in dbs:
                logger.info(f"DATABASE: {db}")

                update_feature = UPDATE_FEATURE.replace("SDEADM.", "") if db.lower().endswith(".gdb") else UPDATE_FEATURE

                logger.info(f"Feature: {update_feature}")

                with arcpy.EnvManager(workspace=db):

                    if not arcpy.Exists(update_feature):
                        raise ValueError(f"\tFeature, '{update_feature}', does not exist.")

                    arcpy.DeleteField_management(
                        in_table=update_feature,
                        drop_field=delete_fields,
                        method="DELETE_FIELDS"
                    )
                    logger.info(arcpy.GetMessages())
