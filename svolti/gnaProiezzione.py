__author__ = 'fabio.lana'
import os,os.path,shutil
from osgeo import osr
from osgeo import ogr
from osgeo import gdal

srcProjection = osr.SpatialReference()
srcProjection.SetUTM(17)

dstProjection = osr.SpatialReference()
dstProjection.SetWellKnownGeogCS('WGS84')

transform = osr.CoordinateTransformation(srcProjection,dstProjection)

srcFile = ogr.Open("data/Miami.shp")
layer = srcFile.GetLayer(0)
layerDefinition = layer.GetLayerDefn()

print "Name" + "\t" + "Type" + "\t" + "Width" + "\t" +  "Precision"
for i in range(layerDefinition.GetFieldCount()):
    fieldName =  layerDefinition.GetFieldDefn(i).GetName()
    fieldTypeCode = layerDefinition.GetFieldDefn(i).GetType()
    fieldType = layerDefinition.GetFieldDefn(i).GetFieldTypeName(fieldTypeCode)
    fieldWidth = layerDefinition.GetFieldDefn(i).GetWidth()
    GetPrecision = layerDefinition.GetFieldDefn(i).GetPrecision()

    print fieldName + "\t" + fieldType + "\t" + str(fieldWidth) + "\t " + str(GetPrecision)

if os.path.exists("data/miami-reprojected"):
    shutil.rmtree("data/miami-reprojected")
    os.mkdir("data/miami-reprojected")
else:
    os.mkdir("data/miami-reprojected")

driver = ogr.GetDriverByName("ESRI Shapefile")
dstPath = os.path.join("data/miami-reprojected", "miami.shp")
dstFile = driver.CreateDataSource(dstPath)
dstLayer = dstFile.CreateLayer("layer",dstProjection)

for i in range(layer.GetFeatureCount()):
    feature = layer.GetFeature(i)
    geometry = feature.GetGeometryRef()

    newGeometry = geometry.Clone()
    newGeometry.Transform(transform)

    feature = ogr.Feature(dstLayer.GetLayerDefn())
    feature.SetGeometry(newGeometry)
    dstLayer.CreateFeature(feature)
    feature.Destroy()

srcFile.Destroy()
dstFile.Destroy()

