__author__ = 'fabio.lana'

import os,os.path,shutil
from osgeo import ogr,osr

import shapely.wkt

srcFile = ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
layer = srcFile.GetLayer(0)
aRobbaDerLayer = layer.GetLayerDefn()

thailand = None
myanmar = None

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    if feature.GetField("ISO2") == "TH":
        geometry = feature.GetGeometryRef()
        thailand = shapely.wkt.loads(geometry.ExportToWkt())
    elif feature.GetField("ISO2") == "MM":
        geometry = feature.GetGeometryRef()
        myanmar = shapely.wkt.loads(geometry.ExportToWkt())

commonBorder = thailand.intersection(myanmar)

if os.path.exists("data/common-border"):
    shutil.rmtree("data/common-border")
    os.mkdir("data/common-border")
else:
    os.mkdir("data/common-border")

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')

driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("data/common-border","border.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer",spatialReference)

wkt = shapely.wkt.dumps(commonBorder)
feature = ogr.Feature(dstLayer.GetLayerDefn())
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
dstLayer.CreateFeature(feature)

feature.Destroy()
dstFile.Destroy()