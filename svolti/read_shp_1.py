__author__ = 'fabio.lana'
import osgeo.ogr

def analyzeGeometry(geometry, indent=0):
    s = []
    s.append(" " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    if geometry.GetGeometryCount() > 0:
        s.append(" containing:")
    print "".join(s)
    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent+1)

def findPoints(geometry, results):
    for i in range(geometry.GetPointCount()):
        x,y,z = geometry.GetPoint(i)
        if results['north'] == None or results['north'][1] < y:
            results['north'] = (x,y)
        if results['south'] == None or results['south'][1] > y:
            results['south'] = (x,y)

    for i in range(geometry.GetGeometryCount()):
        findPoints(geometry.GetGeometryRef(i), results)

shapefile = osgeo.ogr.Open("data/tl_2012_us_state.shp")
layer = shapefile.GetLayer(0)
feature = layer.GetFeature(2)

attributes = feature.items()
for key, value in attributes.items():
    print "key %s = value %s" % (key, value)

geometry = feature.GetGeometryRef()
geometryName = geometry.GetGeometryName()
print
print "Feature's geometry data consists of a %s" % geometryName

analyzeGeometry(geometry)

results = {'north' : None,
           'south' : None}
findPoints(geometry, results)
print "Northernmost point is (%0.4f, %0.4f)" % results['north']
print "Southernmost point is (%0.4f, %0.4f)" % results['south']