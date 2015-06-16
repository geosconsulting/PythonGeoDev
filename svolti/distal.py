__author__ = 'fabio.lana'

import psycopg2

def creazione_db():
    connection = psycopg2.connect("dbname=distal user=geonode password=geonode")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS countries")
    cursor.execute("""
        CREATE TABLE countries (
            id   SERIAL,
            name VARCHAR(255),

            PRIMARY KEY (id))
    """)
    cursor.execute("""
        SELECT AddGeometryColumn('countries', 'outline',
                                 4326, 'GEOMETRY', 2)
    """)
    cursor.execute("""
        CREATE INDEX countryIndex ON countries
            USING GIST(outline)
    """)

    cursor.execute("DROP TABLE IF EXISTS shorelines")
    cursor.execute("""
        CREATE TABLE shorelines (
            id   SERIAL,
            level INTEGER,

            PRIMARY KEY (id))
    """)
    cursor.execute("""
        SELECT AddGeometryColumn('shorelines', 'outline',
                                 4326, 'GEOMETRY', 2)
    """)
    cursor.execute("""
        CREATE INDEX shorelineIndex ON shorelines
            USING GIST(outline)
    """)

    cursor.execute("DROP TABLE IF EXISTS places")
    cursor.execute("""
        CREATE TABLE places (
            id   SERIAL,
            name VARCHAR(255),

            PRIMARY KEY (id))
    """)
    cursor.execute("""
        SELECT AddGeometryColumn('places', 'position',
                                 4326, 'POINT', 2)
    """)
    cursor.execute("""
        CREATE INDEX placeIndex ON places
            USING GIST(position)
    """)
    connection.commit()

def carico_countries_db():
    import os.path
    import psycopg2
    import osgeo.ogr

    connection = psycopg2.connect("dbname=distal user=geonode password=geonode")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM countries")

    srcFile = os.path.join("data", "TM_WORLD_BORDERS-0.3.shp")
    shapefile = osgeo.ogr.Open(srcFile)
    layer = shapefile.GetLayer(0)

    for i in range(layer.GetFeatureCount()):
        feature = layer.GetFeature(i)
        name = feature.GetField("NAME").decode("Latin-1")
        wkt = feature.GetGeometryRef().ExportToWkt()

        cursor.execute("INSERT INTO countries (name,outline) " +
                       "VALUES (%s, ST_GeometryFromText(%s, " +
                       "4326))", (name.encode("utf8"), wkt))

    connection.commit()

def carico_shorelines():
    import os.path
    import psycopg2
    import osgeo.ogr

    connection = psycopg2.connect("dbname=distal user=geonode password=geonode")
    cursor = connection.cursor()

    cursor.execute("DELETE FROM shorelines")

    for level in [1, 2, 3, 4]:
        #os.path.join("data/gshhg-shp-2.3.4/GSHHS_shp/l","GSHHS_l_L"+str(level) + ".shp")
        srcFile = os.path.join("data", "GSHHg-shp-2.3.4", "GSHHS_shp", "f","GSHHS_f_L" + str(level) + ".shp")
        shapefile = osgeo.ogr.Open(srcFile)
        layer = shapefile.GetLayer(0)

        for i in range(layer.GetFeatureCount()):
            feature = layer.GetFeature(i)
            wkt = feature.GetGeometryRef().ExportToWkt()

            cursor.execute("INSERT INTO shorelines " +
                           "(level,outline) VALUES " +
                           "(%s, ST_GeometryFromText(%s, 4326))",
                           (level, wkt))

        connection.commit()


#creazione_db()
#carico_countries_db()
carico_shorelines()