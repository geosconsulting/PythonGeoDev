__author__ = 'fabio.lana'
import osgeo.ogr

shapefile = osgeo.ogr.Open("data/tl_2012_us_state.shp")
numLayers = shapefile.GetLayerCount()
print "Shapefile contains %d layers" % numLayers
print

for layerNum in range(numLayers):
    layer = shapefile.GetLayer(layerNum)
    spatialRef = layer.GetSpatialRef().ExportToProj4()
    numFeatures = layer.GetFeatureCount()

print "Layer %d has spatial reference %s" % (layerNum, spatialRef)
print "Layer %d has %d features:" % (layerNum, numFeatures)
print

lista_stati = []
for featureNum in range(numFeatures):
    feature = layer.GetFeature(featureNum)
    lista_stati.append(feature.GetField("NAME"))

featureName = feature.GetField("NAME")
print "Feature %d has name %s" % (featureNum, featureName)
print

stati_sortati = sorted(lista_stati)
for stato in stati_sortati:
    print stato