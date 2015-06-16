__author__ = 'fabio.lana'

import os, os.path, shutil
from osgeo import ogr, osr
import pyproj

import shapely.wkt

srcFile = ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
layer = srcFile.GetLayer(0)
spatialRef = layer.GetSpatialRef()

if spatialRef == None:
    print "Shapefile has no spatial reference using WGS84"
    spatialRef = osr.SpatialReference()
    spatialRef.SetWellKnownGeogCS('WGS84')

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
dstPath = os.path.join("data/common-border", "border.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer",spatialReference)

wkt = shapely.wkt.dumps(commonBorder)
feature = ogr.Feature(dstLayer.GetLayerDefn())
feature.SetGeometry(ogr.CreateGeometryFromWkt(wkt))
dstLayer.CreateFeature(feature)

feature.Destroy()
dstFile.Destroy()

def getLineSegmentsFromGeometry(geometry):
    segments = []
    if geometry.GetPointCount() > 0:
        segment = []
        for i in range(geometry.GetPointCount()):
            segment.append(geometry.GetPoint_2D(i))
        segments.append(segment)
    for i in range(geometry.GetGeometryCount()):
        subGeometry = geometry.GetGeometryRef(i)
        segments.extend(getLineSegmentsFromGeometry(subGeometry))

    return segments

confine = layer.GetFeature(0)
geometria_confine = confine.GetGeometryRef()
segments = getLineSegmentsFromGeometry(geometria_confine)

geod = pyproj.Geod(ellps = 'WGS84')

totLength = 0
for segment in segments:

    for i in range(len(segment)-1):

        pt1 = segment[i]
        pt2 = segment[i+1]

        long1, lat1 = pt1
        long2, lat2 = pt2
        angle1, angle2, distance = geod.inv(long1, lat1, long2, lat2)
        totLength += distance

print "Total border length = %0.2f km" % (totLength/1000)
