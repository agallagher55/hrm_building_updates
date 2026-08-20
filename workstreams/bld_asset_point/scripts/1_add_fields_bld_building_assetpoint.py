"""
TASK0326632 — Add fields to BLD_building_assetpoint.
Source: ../bld_asset_point.md, "Schema Changes - Add Fields"
"""

import logging
import os

from configparser import ConfigParser
from datetime import date

import arcpy

from gispy.features import Feature

arcpy.env.overwriteOutput = True
arcpy.SetLogHistory(False)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_add_fields_bld_building_assetpoint.log")

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

new_field_info = {

    "SDEADM.BLD_building_assetpoint": {

        "HERITAGE": {
            "alias": "Heritage",
            "field_type": "TEXT",
            "field_length": "1",
            "domain": "AAA_yes_no",
        },
        "NAMESTATUS": {
            "alias": "Name Status",
            "field_type": "TEXT",
            "field_length": "1",
            "domain": "Bldg_Official_Name",
        },
        "NAMEAPRDTE": {
            "alias": "Name Approved Date",
            "field_type": "DATE",
            "field_length": "",
            "domain": "",
        },

    },

}

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

                for feature_key in new_field_info:

                    update_feature = feature_key.replace("SDEADM.", "") if db.lower().endswith(".gdb") else feature_key

                    logger.info(f"Feature: {update_feature}")

                    with arcpy.EnvManager(workspace=db):

                        if not arcpy.Exists(update_feature):
                            if db.lower().endswith(".gdb"):
                                logger.warning(f"\tFeature, '{update_feature}', does not exist in {db}. Skipping...")
                                continue
                            raise ValueError(f"\tFeature, '{update_feature}', does not exist.")

                        desc = arcpy.Describe(update_feature)

                        my_feature = Feature(db, desc.baseName, "POINT")
                        current_fields = [x.name for x in arcpy.ListFields(update_feature)]

                        update_feature_new_field_info = new_field_info[feature_key]

                        for field in update_feature_new_field_info:
                            logger.info(f"Field to add: '{field}'")

                            if field in current_fields:
                                logger.info(f"Field, {field} already exists in {update_feature}..!")
                                continue

                            logger.info(f"Adding {field} to {update_feature}...")
                            my_feature.add_field(
                                field_name=field,
                                field_type=update_feature_new_field_info[field]["field_type"],
                                length=update_feature_new_field_info[field].get("field_length", "#"),
                                alias=update_feature_new_field_info[field]["alias"],
                                domain_name=update_feature_new_field_info[field]["domain"],
                            )
