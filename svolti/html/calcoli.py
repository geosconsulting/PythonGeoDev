#!C:/Python27/ArcGIS10.2/python.exe

print 'Content-Type: text/html; charset=UTF-8\n\n'
print '<html>'
print '<head><title>Select Country</title></head>'

print '<body>'
print '<form method="POST" action="coords.py">'
print '<input type="text" id="coord1_lat" name="coord1_lat"/>'
print '<input type="text" id="coord1_lon" name="coord1_lon"/>'
print '</br>'
print '<input type="text" id="coord2_lat" name="coord2_lat"/>'
print '<input type="text" id="coord2_lon" name="coord2_lon"/>'
print '</br>'
print '<input type="submit" value="Calcola">'
print '</form>'
print '</body>'
print '</html>'

