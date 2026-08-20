-- Captured from ArcGIS Pro (View Properties > Definition), Prod, 2026-08-19.
-- Note: this view does not select any BLD_building_assetpoint field directly.
-- It joins BLD_BUILDING_POLYGON to BLD_HRM_INTEREST_FINAL on BL_ID.
-- Flagged as impacted by TASK0326632 in the RFC's IMPACTS tab, so worth
-- confirming whether BLD_HRM_INTEREST_FINAL is itself derived from
-- BLD_building_assetpoint before assuming this view needs changes.

CREATE VIEW sdeadm.BLD_HRM_INTEREST_VW
AS
SELECT   P.OBJECTID, P.SHAPE, P.BL_ID, A.BL_NAME, A.OWNER,
         A.CONST_YEAR, A.CLASS, A.USE_, A.USE_NAME, A.DWEL_UNITS,
         A.PRIM_USE, A.BL_MAINT, A.ACQ_DATE, A.ACQ_TYPE, A.ACQ_COST,
         A.CONST_COST, A.CIV_ID,
         A.CIV_NUM, A.CIV_ALPHA, A.UNIT_NUM, A.STR_NAME,
         A.STR_TYPE, A.GSA_NAME
FROM     sdeadm.BLD_BUILDING_POLYGON AS P INNER JOIN
         sdeadm.BLD_HRM_INTEREST_FINAL AS A ON P.BL_ID = A.BL_ID
