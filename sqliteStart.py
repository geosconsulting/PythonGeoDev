__author__ = 'fabio.lana'
from pysqlite2 import dbapi2 as sqlite

db = sqlite.connect("test.db")
db.enable_load_extension(True)
#db.execute('SELECT load_extension("libspatialite-2.dll")')
#curs = db.cursor()
