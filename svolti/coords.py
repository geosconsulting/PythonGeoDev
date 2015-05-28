__author__ = 'fabio.lana'
import pyproj
lat1,long1 = (37.82,-122.42)
lat2,long2 = (37.80,-122.44)
geod = pyproj.Geod(ellps="WGS84")
angle1,angle2,distance = geod.inv(long1, lat1, long2, lat2)
print "Distance is %0.2f meters" % distance
