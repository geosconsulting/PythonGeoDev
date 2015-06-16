__author__ = 'fabio.lana'

import MySQLdb

connection = MySQLdb.connect(user="fabio", passwd="albertone")
cursor = connection.cursor()
cursor.execute("DROP DATABASE IF EXISTS spatialTest")
cursor.execute("CREATE DATABASE spatialTest")
cursor.execute("USE spatialTest")

cursor.execute("""CREATE TABLE gshhs (
                    id      INTEGER AUTO_INCREMENT,
                    level   INTEGER,
                    geom    POLYGON NOT NULL,

                    PRIMARY KEY (id),
                    INDEX (level),
                    SPATIAL INDEX (geom)) ENGINE=MyISAM
               """)


# import os.path
# from osgeo import ogr
#
# for level in [1,2,3,4]:
#     fName = os.path.join("data/gshhg-shp-2.3.4/GSHHS_shp/l","GSHHS_l_L"+str(level) + ".shp")
#     shapefile = ogr.Open(fName)
#     layer = shapefile.GetLayer(0)
#     for i in range(layer.GetFeatureCount()):
#         feature = layer.GetFeature(i)
#         geometry = feature.GetGeometryRef()
#         wkt = geometry.ExportToWkt()
#         #print "INSERT INTO gshhs(level, geom) VALUES (%s, GeomFromText(%s, 4326))" % (level,wkt)
#         if wkt:
#             cursor.execute("INSERT INTO gshhs (level, geom) " +
#                        "VALUES (%s, GeomFromText(%s, 4326))",
#                        (level, wkt))
#
#     connection.commit()


import shapely.wkt
LONDON = 'POINT(-0.1263 51.4980)'

cursor.execute("SELECT id,AsText(geom) FROM gshhs " +
               "WHERE (level=%s) AND " +
               "(MBRContains(geom, GeomFromText(%s, 4326)))",
               (1, LONDON))

shoreline = None
for id,wkt in cursor:
    polygon = shapely.wkt.loads(wkt)
    point   = shapely.wkt.loads(LONDON)
    if polygon.contains(point):
        shoreline = wkt