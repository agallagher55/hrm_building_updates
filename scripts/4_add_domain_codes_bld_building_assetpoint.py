"""
TASK0326632 — Add FMO / FDC codes to the Bldg_FC_source domain
(used by BLD_building_assetpoint's SOURCE field).
Source: work/bld_asset_point/bld_asset_point.md, "Domain Updates"
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

log_file = os.path.join(SCRIPT_DIR, f"{date.today()}_add_domain_codes_bld_building_assetpoint.log")

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

ADD_CODE_VALUES = {
    "Bldg_FC_source": {
        "FMO": "Facilities Maintenance & Operations",
        "FDC": "Facilities Design & Construction",
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

                for domain_name, code_values in ADD_CODE_VALUES.items():

                    domain_found, unfound_domains, db_domains = domains.domains_in_db(db, [domain_name])

                    if not domain_found:
                        raise ValueError(
                            f"Did not find domain '{domain_name}' in {db}. Unfound domains: {', '.join(unfound_domains)}"
                        )

                    for code, value in code_values.items():
                        logger.info(f"Domain and Code: {code} & {value}")
                        domains.add_code_value(db, domain_name, code, value)

                    logger.info(arcpy.GetMessages())
