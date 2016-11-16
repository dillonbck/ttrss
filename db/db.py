#pylint: skip-file

import sqlite3

from tables import (ReleaseTable, ReleaseInfoTable, ReleaseUrlsTable,
    ReleaseCoverartTable, ReleaseDownloadedStatusTable)

from helpers import ReleaseHelper


class ReleasesDbHelper(object):
    
    def __init__(self):
        self.dbConnection = sqlite3.connect('releases.db')
        print "Opened database successfully";

        self.onCreate()


    def onCreate(self):
        ReleaseTable.onCreate(self.dbConnection)
        ReleaseInfoTable.onCreate(self.dbConnection)
        ReleaseUrlsTable.onCreate(self.dbConnection)
        ReleaseCoverartTable.onCreate(self.dbConnection)
        ReleaseDownloadedStatusTable.onCreate(self.dbConnection)

    def onUpgrade(self):
        ReleaseTable.onUpgrade(self.dbConnection)
        ReleaseInfoTable.onUpgrade(self.dbConnection)
        ReleaseUrlsTable.onUpgrade(self.dbConnection)
        ReleaseCoverartTable.onUpgrade(self.dbConnection)
        ReleaseDownloadedStatusTable.onUpgrade(self.dbConnection)

    def close(self):
        self.dbConnection.close() 


    def getReleases(self):
        t = ReleaseHelper.getReleases(self.dbConnection)
        print "helper releases"
        for r in t:
            try:
                print r.id
                print r.artist
                print r.album
            except:
                pass
        return t

    def addReleases(self, releases):
        ReleaseHelper.addReleases(releases, self.dbConnection)
