#pylint: skip-file

from abc import ABCMeta, abstractproperty

import sqlite3 as sqlite3

class DbTable(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def TABLE_NAME(self):
        return

    @abstractproperty
    def CREATE_TABLE(self):
        return

    @classmethod
    def onCreate(cls, dbConnection):
        try:
            dbConnection.execute(cls.CREATE_TABLE)
        except sqlite3.OperationalError as e:
            # Table already exists
            pass

    @classmethod
    def onUpgrade(cls, dbConnection):
        dbConnection.execute("DROP TABLE IF EXISTS " + cls.TABLE_NAME)
        cls.onCreate(dbConnection)
    

class ReleaseTable(DbTable):
    TABLE_NAME = "release"
    COLUMN_ID = "release_id"

    CREATE_TABLE = ("CREATE TABLE "
        + TABLE_NAME
        + " ("
        + COLUMN_ID + " INT PRIMARY KEY NOT NULL"
        + ");")


class ReleaseInfoTable(DbTable):
    TABLE_NAME = "release_info"
    COLUMN_ID = "release_id"
    COLUMN_ARTIST = "artist"
    COLUMN_ALBUM = "album"
    COLUMN_LABEL = "label"
    COLUMN_CATALOG_NUMBER = "catalog_number"
    COLUMN_RELEASE_DATE = "release_date"
    COLUMN_STYLE = "style"

    CREATE_TABLE = ("CREATE TABLE "
        + TABLE_NAME
        + " ("
        + COLUMN_ID + " INT PRIMARY KEY NOT NULL, "
        + COLUMN_ARTIST + " TEXT NOT NULL, "
        + COLUMN_ALBUM + " TEXT NOT NULL, "
        + COLUMN_LABEL + " TEXT NOT NULL, "
        + COLUMN_CATALOG_NUMBER + " TEXT NOT NULL, "
        + COLUMN_RELEASE_DATE + " TEXT NOT NULL, "
        + COLUMN_STYLE + " TEXT NOT NULL"
        + ");")


class ReleaseUrlsTable(DbTable):
    TABLE_NAME = "release_urls"
    COLUMN_ID = "release_id"
    COLUMN_RELEASE_URL = "release_url"
    COLUMN_WEBLINK_URL = "weblink_url"
    COLUMN_DISCOGS_URL = "discogs_url"

    CREATE_TABLE = ("CREATE TABLE "
        + TABLE_NAME
        + " ("
        + COLUMN_ID + " INT PRIMARY KEY NOT NULL, "
        + COLUMN_RELEASE_URL + " TEXT NOT NULL, "
        + COLUMN_WEBLINK_URL + " TEXT NOT NULL, "
        + COLUMN_DISCOGS_URL + " TEXT NOT NULL"
        + ");")


class ReleaseCoverartTable(DbTable):
    TABLE_NAME = "release_coverart"
    COLUMN_ID = "release_id"
    COLUMN_COVERART_URL = "coverart_url"
    COLUMN_COVERART_EXT = "coverart_ext"

    CREATE_TABLE = ("CREATE TABLE "
        + TABLE_NAME
        + " ("
        + COLUMN_ID + " INT PRIMARY KEY NOT NULL, "
        + COLUMN_COVERART_URL + " TEXT NOT NULL, "
        + COLUMN_COVERART_EXT + " TEXT NOT NULL"
        + ");")


class ReleaseDownloadedStatusTable(DbTable):
    TABLE_NAME = "release_downloaded_status"
    COLUMN_ID = "release_id"
    COLUMN_DOWNLOADED_STATUS = "downloaded_status"

    CREATE_TABLE = ("CREATE TABLE "
        + TABLE_NAME
        + " ("
        + COLUMN_ID + " INT PRIMARY KEY NOT NULL, "
        + COLUMN_DOWNLOADED_STATUS + " INT NOT NULL"
        + ");")
