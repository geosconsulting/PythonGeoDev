print 'Content-Type: text/html; charset=UTF-8\n\n'
print '<html>'
print '<head><title>Select Country</title></head>'
print '<body>'

import pyproj
import cgi

form = cgi.FieldStorage()

coord1 = float(form['coord1_lat'].value)
coord2 = float(form['coord1_lon'].value)
coord3 = float(form['coord2_lat'].value)
coord4 = float(form['coord2_lon'].value)

#lat1, long1 = (37.82,-122.42)
#lat2, long2 = (37.80,-122.44)

lat1, long1 = (coord1,coord2)
lat2, long2 = (coord3,coord4)

geod = pyproj.Geod(ellps="WGS84")
angle1, angle2, distance = geod.inv(long1, lat1, long2, lat2)

print '<h2><b>Distance is %0.2f meters' % distance + '</b></h2>'
print '</body>'
print '</html>'


