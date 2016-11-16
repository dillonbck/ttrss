#pylint: skip-file

from rss import Rss
from gui import Gui
from db.db import ReleasesDbHelper


if __name__=="__main__":
	dbHelper = ReleasesDbHelper()
	# dbHelper.onUpgrade()

	rss = Rss(dbHelper)
	rss.run()

	dbHelper.close()

	gui = Gui(rss.releases)
	gui.run()
	