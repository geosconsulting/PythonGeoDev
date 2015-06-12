__author__ = 'fabio.lana'

from osgeo import ogr,osr
import os, os.path, shutil

srcFile = ogr.Open("data/TM_WORLD_BORDERS-0.3.shp")
srcLayer = srcFile.GetLayer(0)

if os.path.exists("data/bounding-boxes"):
    shutil.rmtree("data/bounding-boxes")
    os.mkdir("data/bounding-boxes")
else:
    os.mkdir("data/bounding-boxes")

spatialReference = osr.SpatialReference()
spatialReference.SetWellKnownGeogCS('WGS84')

driver = ogr.GetDriverByName("ESRI Shapefile")
dstFile = driver.CreateDataSource("data/bounding-boxes/boundingBoxes.shp")
dstLayer = dstFile.CreateLayer("layer", spatialReference)

fieldDef = ogr.FieldDefn("COUNTRY",ogr.OFTString)
fieldDef.SetWidth(50)
dstLayer.CreateField(fieldDef)

fieldDef = ogr.FieldDefn("CODE",ogr.OFTString)
fieldDef.SetWidth(3)
dstLayer.CreateField(fieldDef)

countries = []

for i in range(srcLayer.GetFeatureCount()):

    feature = srcLayer.GetFeature(i)
    countryCode = feature.GetField("ISO3")
    countryName = feature.GetField("NAME")
    geometry = feature.GetGeometryRef()
    minLong, maxLong, minLat, maxLat = geometry.GetEnvelope()
    countries.append((countryName, countryCode, minLat, maxLat, minLong, maxLong))

    linearRing = ogr.Geometry(ogr.wkbLinearRing)
    linearRing.AddPoint(minLong, minLat)
    linearRing.AddPoint(maxLong, minLat)
    linearRing.AddPoint(maxLong, maxLat)
    linearRing.AddPoint(minLong, maxLat)
    linearRing.AddPoint(minLong, minLat)

    polygon = ogr.Geometry(ogr.wkbPolygon)
    polygon.AddGeometry(linearRing)

    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(polygon)
    feature.SetField("COUNTRY",countryName)
    feature.SetField("CODE",countryCode)
    dstLayer.CreateFeature(feature)
    feature.Destroy()

srcFile.Destroy()
dstFile.Destroy()

# for i in range(layer.GetFeatureCount()):
#     feature = layer.GetFeature(i)
#     countryCode = feature.GetField("ISO3")
#     countryName = feature.GetField("NAME")
#     geometry = feature.GetGeometryRef()
#     minLong,maxLong,minLat,maxLat = geometry.GetEnvelope()
#
#     countries.append((countryName,countryCode,minLat,maxLat,minLong,maxLong))

countries.sort()
for name,code,minLat,maxLat,minLong,maxLong in countries:
    print "%s (%s) lat=%0.4f..%0.4f, long=%0.4f..%0.4f" % (name, code, minLat, maxLat, minLong, maxLong)