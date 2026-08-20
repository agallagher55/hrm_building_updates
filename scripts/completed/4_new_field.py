"""
HISTORICAL — already executed, kept for the record, not part of the numbered run order in scripts/.
Adds HGTSOURCE (Text/30, alias "Height Source", domain Bldg_height_source) to SDEADM.BLD_building_symbol.
Run against Prod (RW, RO) only, no log provided.

FLAGGED — likely wrong target feature class. Every source ticket/RFC/email for this field
(TASK0320355, TASK0312692, the "Building Height in GIS" email thread) specifies HGTSOURCE on
BLD_building_polygon, not BLD_Building_Symbols; the deployed BLD_building_polygon_insp_VW also
selects HGTSOURCE directly from BLD_building_polygon. See tickets/TASK0320355.md and
workflow.md's "BLD_building_polygon – ad hoc changes" section. Needs a live-schema check on
BLD_building_symbol in Prod to confirm whether this field landed there in error.
"""

from configparser import ConfigParser
from datetime import date

from os import (
    environ, getcwd, path
)

import arcpy
import logging

from gispy.features import Feature

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

log_file = path.join(
    getcwd(),
    f"{date.today()}_add_fields.log"
)

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
config.read('config.ini')

CURRENT_DIR = getcwd()

# TODO: UPDATE ME
new_field_info = {
    "SDEADM.BLD_building_symbol": {
        "HGTSOURCE": {
            "alias": "Height Source",
            "field_type": "TEXT",
            "field_length": "30",
            "nullable": "NULLABLE",
            "default": "",
            "domain": "Bldg_height_source"
        },

    },
}

if __name__ == "__main__":

    PC_NAME = environ['COMPUTERNAME']
    run_from = "SERVER" if "APP" in PC_NAME else "LOCAL"

    for dbs in [
        # WEBGIS features can use domains from SDEADM owner - don't need to create a domain for both SDEADM and WEBGIS

        # [
            # config.get(run_from, "dev_rw"),
            # config.get(run_from, "dev_ro"),
            # config.get(run_from, "dev_web_ro_gdb")
        # ],

        # [
        # config.get(run_from, "qa_rw"),
        # config.get(run_from, "qa_ro"),
        # config.get(run_from, "qa_web_ro_gdb")
        # ],
        [
            config.get(run_from, "prod_rw"),
            config.get(run_from, "prod_ro"),
        #     config.get(run_from, "prod_web_ro_gdb")
        ],
    ]:

        if dbs:
            logger.info(f"Processing dbs: {', '.join(dbs)}...")

            for db in dbs:
                logger.info(f"DATABASE: {db}")

                for update_feature in new_field_info:

                    if db.endswith(".gdb"):
                        update_feature = update_feature.replace("SDEADM.", "")

                    elif "WEBGIS" in db.upper():
                        update_feature = update_feature.replace("SDEADM.", "WEBGIS.")

                    logger.info(f"Feature: {update_feature}")

                    with arcpy.EnvManager(workspace=db):

                        # Check if feature exists
                        if not arcpy.Exists(update_feature):
                            raise ValueError(f"\tFeature, '{update_feature}', does not exist.")

                        desc = arcpy.Describe(update_feature)

                        my_feature = Feature(db, desc.baseName, "POINT")
                        current_fields = [x.name for x in arcpy.ListFields(update_feature)]

                        # TODO: Stop services

                        update_feature_new_field_info = new_field_info[update_feature]

                        for field in update_feature_new_field_info:
                            logger.info(f"Field to add: '{field}'")

                            # Check that field doesn't already exist

                            if field in current_fields:
                                logger.info(f"Field, {field} already exists in {update_feature}..!")
                                continue

                            logger.info(f"Adding {field} to {update_feature}...")
                            my_feature.add_field(
                                field_name=field,
                                field_type=update_feature_new_field_info[field]["field_type"],
                                length=update_feature_new_field_info[field].get("field_length", "#"),
                                alias=update_feature_new_field_info[field]["alias"],
                                domain_name=update_feature_new_field_info[field]["domain"]
                            )

                        # TODO: Start services
                        # * Had to manually unlock with SDE connection
