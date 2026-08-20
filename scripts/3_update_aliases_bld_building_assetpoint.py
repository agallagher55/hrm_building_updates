"""
TASK0326632 — Update field aliases on BLD_building_assetpoint.
Source: work/bld_asset_point/bld_asset_point.md, "Metadata / Alias Updates"

OWNER is left out: its new alias isn't confirmed yet (see that section's note).
"""

import logging
import os
import sys
import traceback

from configparser import ConfigParser
from datetime import date

import arcpy

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_update_aliases_bld_building_assetpoint.log")

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

update_feature_info = {
    "SDEADM.BLD_building_assetpoint": [
        {
            "field": "INSTYRCONF",
            "new_alias": "Year of Construction Confidence",
        },
        {
            "field": "INSTDATE",
            "new_alias": "Building Official Opened Date",
        },
        {
            "field": "INSTCS",
            "new_alias": "Total Construction Cost",
        },
        {
            "field": "RMLIFE",
            "new_alias": "Expected Life",
        },
        {
            "field": "BASELIFE",
            "new_alias": "Base Life (Years)",
        },
    ]
}


def update_field_alias(feature, field, alias):
    logger.info(f"Updating alias for '{field}' -> '{alias}'...")

    arcpy.AlterField_management(
        in_table=feature,
        field=field,
        new_field_alias=alias,
        clear_field_alias='#'
    )
    logger.info(arcpy.GetMessages())


if __name__ == "__main__":

    PC_NAME = os.environ['COMPUTERNAME']
    run_from = "SERVER" if "APP" in PC_NAME else "LOCAL"

    try:

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

                    for feature_key, field_infos in update_feature_info.items():

                        update_feature = (
                            feature_key.replace("SDEADM.", "")
                            if db.lower().endswith(".gdb")
                            else feature_key
                        )

                        with arcpy.EnvManager(workspace=db):

                            if not arcpy.Exists(update_feature):
                                raise ValueError(f"\tFeature, '{update_feature}', does not exist.")

                            for field_info in field_infos:
                                update_field_alias(
                                    feature=update_feature,
                                    field=field_info["field"],
                                    alias=field_info["new_alias"],
                                )

    except arcpy.ExecuteError:
        logger.error(arcpy.GetMessages(2))

    except Exception as e:
        logger.error(e)
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        logger.error("PYTHON ERRORS:\n" + tbinfo + "\n" + str(sys.exc_info()))
        logger.error("GP ERRORS:\n" + arcpy.GetMessages(2))
        sys.exit()
