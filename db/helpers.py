#pylint: skip-file

from tables import (ReleaseTable, ReleaseInfoTable, ReleaseUrlsTable,
    ReleaseCoverartTable, ReleaseDownloadedStatusTable)

from classes import Release

class ReleaseHelper(object):

    @staticmethod
    def addRelease(release, dbConnection):

        dbConnection.execute("INSERT INTO " + ReleaseTable.TABLE_NAME
            + "(" + ReleaseTable.COLUMN_ID 
            + ")" + "VALUES "
            + "(" + str(release.id)
            + ")")

        print "release"
        print release.id
        print release.artist
        print release.label
        print release.catalog_number
        print release.release_date
        print release.style
        if (release.artist is not None and
            release.album is not None and
            release.label is not None and
            release.catalog_number is not None and
            release.release_date is not None and
            release.style is not None and
            release.release_url is not None and
            release.weblink_url is not None and
            release.discogs_url is not None and
            release.coverart_url is not None and
            release.coverart_ext is not None and
            release.downloaded_status is not None):

            print "adding release to db"

            dbConnection.execute("INSERT INTO " + ReleaseInfoTable.TABLE_NAME
                + "(" + ReleaseInfoTable.COLUMN_ID
                + "," + ReleaseInfoTable.COLUMN_ARTIST
                + "," + ReleaseInfoTable.COLUMN_ALBUM
                + "," + ReleaseInfoTable.COLUMN_LABEL
                + "," + ReleaseInfoTable.COLUMN_CATALOG_NUMBER
                + "," + ReleaseInfoTable.COLUMN_RELEASE_DATE
                + "," + ReleaseInfoTable.COLUMN_STYLE
                + ")"

                + "VALUES "
                + "('" + str(release.id)
                + "','" + release.artist
                + "','" + release.album
                + "','" + release.label
                + "','" + release.catalog_number
                + "','" + release.release_date
                + "','" + release.style
                + "')")

            print release.id
            print release.release_url
            print release.weblink_url
            print release.discogs_url

            dbConnection.execute("INSERT INTO " + ReleaseUrlsTable.TABLE_NAME
                + "(" + ReleaseUrlsTable.COLUMN_ID
                + "," + ReleaseUrlsTable.COLUMN_RELEASE_URL
                + "," + ReleaseUrlsTable.COLUMN_WEBLINK_URL
                + "," + ReleaseUrlsTable.COLUMN_DISCOGS_URL
                + ")"

                + "VALUES "
                + "('" + str(release.id)
                + "','" + release.release_url
                + "','" + release.weblink_url
                + "','" + release.discogs_url
                + "')")



            dbConnection.execute("INSERT INTO " + ReleaseCoverartTable.TABLE_NAME
                + "(" + ReleaseCoverartTable.COLUMN_ID
                + "," + ReleaseCoverartTable.COLUMN_COVERART_URL
                + "," + ReleaseCoverartTable.COLUMN_COVERART_EXT
                + ")"

                + "VALUES "
                + "('" + str(release.id)
                + "','" + release.coverart_url
                + "','" + release.coverart_ext
                + "')")

            dbConnection.execute("INSERT INTO " + ReleaseDownloadedStatusTable.TABLE_NAME
                + "(" + ReleaseDownloadedStatusTable.COLUMN_ID
                + "," + ReleaseDownloadedStatusTable.COLUMN_DOWNLOADED_STATUS
                + ")"

                + "VALUES "
                + "('" + str(release.id)
                + "','" + str(release.downloaded_status)
                + "')")

            dbConnection.commit()

        else:
            print "did not add release to db"


    @staticmethod
    def addReleases(releases, dbConnection):
        print "releases"
        print releases
        # adfladsf
        for release in releases:
            print release
            ReleaseHelper.addRelease(release, dbConnection)

    @staticmethod
    def getReleases(dbConnection):
        releases = []

        print "getReleases"

        # cursor = dbConnection.cursor()
        # cursor.execute("SELECT * FROM " + ReleaseTable.TABLE_NAME)

        # for row in cursor:
        #     print "select *"
        #     print row[0]


        cursor = dbConnection.execute("SELECT "
            + ReleaseTable.COLUMN_ID 
            + " FROM " + ReleaseTable.TABLE_NAME)

        for row in cursor:
            release = Release()
            release.id = row[0]
            releases.append(release)
            print "release id "
            print release.id


        cursor = dbConnection.execute("SELECT " 
            + ReleaseInfoTable.COLUMN_ID + ","
            + ReleaseInfoTable.COLUMN_ARTIST + "," 
            + ReleaseInfoTable.COLUMN_ALBUM + "," 
            + ReleaseInfoTable.COLUMN_LABEL + "," 
            + ReleaseInfoTable.COLUMN_CATALOG_NUMBER + "," 
            + ReleaseInfoTable.COLUMN_RELEASE_DATE + ","
            + ReleaseInfoTable.COLUMN_STYLE
            + " FROM " + ReleaseInfoTable.TABLE_NAME)

        for idx, row in enumerate(cursor):
            release = releases[idx]
            assert release.id == row[0]
            release.artist = row[1]
            release.album = row[2]
            release.label = row[3]
            release.catalog_number = row[4]
            release.release_date = row[5]
            release.style = row[6]


        cursor = dbConnection.execute("SELECT " 
            + ReleaseUrlsTable.COLUMN_ID + ","
            + ReleaseUrlsTable.COLUMN_RELEASE_URL + ","
            + ReleaseUrlsTable.COLUMN_WEBLINK_URL + ","
            + ReleaseUrlsTable.COLUMN_DISCOGS_URL
            + " FROM " + ReleaseUrlsTable.TABLE_NAME)

        for idx, row in enumerate(cursor):
            release = releases[idx]
            assert release.id == row[0]
            release.release_url = row[1]
            release.weblink_url = row[2]
            release.discogs_url = row[3]


        cursor = dbConnection.execute("SELECT "
            + ReleaseCoverartTable.COLUMN_ID + ","
            + ReleaseCoverartTable.COLUMN_COVERART_URL + ","
            + ReleaseCoverartTable.COLUMN_COVERART_EXT
            + " FROM " + ReleaseCoverartTable.TABLE_NAME)

        for idx, row in enumerate(cursor):
            release = releases[idx]
            assert release.id == row[0]
            release.coverart_url = row[1]
            release.coverart_ext = row[2]

        cursor = dbConnection.execute("SELECT "
            + ReleaseDownloadedStatusTable.COLUMN_ID + ","
            + ReleaseDownloadedStatusTable.COLUMN_DOWNLOADED_STATUS
            + " FROM " + ReleaseDownloadedStatusTable.TABLE_NAME)

        for idx, row in enumerate(cursor):
            release = releases[idx]
            assert release.id == row[0]
            release.downloaded_status = row[1]

        print "releases"
        print releases
        return releases