#pylint: skip-file

class ReleaseInfo(object):
    DEFAULT_ID = 0
    DEFAULT_ARTIST = ''
    DEFAULT_ALBUM = ''
    DEFAULT_LABEL = ''
    DEFAULT_CATALOG_NUMBER = ''
    DEFAULT_RELEASE_DATE = ''
    DEFAULT_STYLE = ''

    def __init__(self, release_id=DEFAULT_ID, artist=DEFAULT_ARTIST, 
        album=DEFAULT_ALBUM, label=DEFAULT_LABEL, 
        catalog_number=DEFAULT_CATALOG_NUMBER, 
        release_date=DEFAULT_RELEASE_DATE, style=DEFAULT_STYLE):

        self.id = release_id
        self.artist = artist
        self.album = album
        self.label = label
        self.catalog_number = catalog_number
        self.release_date = release_date
        self.style = style


class ReleaseUrl(object):
    DEFAULT_ID = 0
    DEFAULT_RELEASE_URL = ''
    DEFAULT_WEBLINK_URL = ''
    DEFAULT_DISCOGS_URL = ''

    def __init__(self, release_id=DEFAULT_ID, release_url=DEFAULT_RELEASE_URL, 
        weblink_url=DEFAULT_WEBLINK_URL, discogs_url=DEFAULT_DISCOGS_URL):

        self.id = release_id
        self.release_url = release_url
        self.weblink_url = weblink_url
        self.discogs_url = discogs_url


class ReleaseCoverart(object):
    DEFAULT_ID = 0
    DEFAULT_COVERART_URL = ''
    DEFAULT_COVERART_EXT = ''

    def __init__(self, release_id=DEFAULT_ID, coverart_url=DEFAULT_COVERART_URL,
        coverart_ext=DEFAULT_COVERART_EXT):

        self.id = release_id
        self.coverart_url = coverart_url
        self.coverart_ext = coverart_ext


class ReleaseDownloadedStatus(object):
    DEFAULT_ID = 0
    DEFAULT_DOWNLOADED_STATUS = 0

    def __init__(self, release_id=DEFAULT_ID, 
        downloaded_status=DEFAULT_DOWNLOADED_STATUS):

        self.id = release_id
        self.downloaded_status = downloaded_status

class Release(object):
    DEFAULT_ID = 0

    DEFAULT_RELEASE_DICT = {
        'release_id': DEFAULT_ID,

        'artist': ReleaseInfo.DEFAULT_ARTIST,
        'album': ReleaseInfo.DEFAULT_ALBUM,
        'label': ReleaseInfo.DEFAULT_LABEL,
        'catalog_number': ReleaseInfo.DEFAULT_CATALOG_NUMBER,
        'release_date': ReleaseInfo.DEFAULT_RELEASE_DATE,
        'style': ReleaseInfo.DEFAULT_STYLE,

        'release_url': ReleaseUrl.DEFAULT_RELEASE_URL,
        'weblink_url': ReleaseUrl.DEFAULT_WEBLINK_URL,
        'discogs_url': ReleaseUrl.DEFAULT_DISCOGS_URL,

        'coverart_url': ReleaseCoverart.DEFAULT_COVERART_URL,
        'coverart_ext': ReleaseCoverart.DEFAULT_COVERART_EXT,

        'downloaded_status': ReleaseDownloadedStatus.DEFAULT_DOWNLOADED_STATUS
    }

    def __init__(self, release_dict=DEFAULT_RELEASE_DICT):
        self.release_data = {}

        for key in Release.DEFAULT_RELEASE_DICT:
            if key in release_dict:
                self.release_data[key] = release_dict[key]
            else:
                self.release_data[key] = DEFAULT_RELEASE_DICT[key]


    @property
    def id(self):
        return self.release_data['release_id']

    @id.setter
    def id(self, value):
        self.release_data['release_id'] = value


    @property
    def artist(self):
        return self.release_data['artist']

    @artist.setter
    def artist(self, value):
        self.release_data['artist'] = value


    @property
    def album(self):
        return self.release_data['album']

    @album.setter
    def album(self, value):
        self.release_data['album'] = value


    @property
    def label(self):
        return self.release_data['label']

    @label.setter
    def label(self, value):
        self.release_data['label'] = value


    @property
    def catalog_number(self):
        return self.release_data['catalog_number']

    @catalog_number.setter
    def catalog_number(self, value):
        self.release_data['catalog_number'] = value


    @property
    def release_date(self):
        return self.release_data['release_date']

    @release_date.setter
    def release_date(self, value):
        self.release_data['release_date'] = value


    @property
    def style(self):
        return self.release_data['style']

    @style.setter
    def style(self, value):
        self.release_data['style'] = value


    @property
    def release_url(self):
        return self.release_data['release_url']

    @release_url.setter
    def release_url(self, value):
        self.release_data['release_url'] = value


    @property
    def weblink_url(self):
        return self.release_data['weblink_url']

    @weblink_url.setter
    def weblink_url(self, value):
        self.release_data['weblink_url'] = value


    @property
    def discogs_url(self):
        return self.release_data['discogs_url']

    @discogs_url.setter
    def discogs_url(self, value):
        self.release_data['discogs_url'] = value


    @property
    def coverart_url(self):
        return self.release_data['coverart_url']

    @coverart_url.setter
    def coverart_url(self, value):
        self.release_data['coverart_url'] = value


    @property
    def coverart_ext(self):
        return self.release_data['coverart_ext']

    @coverart_ext.setter
    def coverart_ext(self, value):
        self.release_data['coverart_ext'] = value


    @property
    def downloaded_status(self):
        return self.release_data['downloaded_status']

    @downloaded_status.setter
    def downloaded_status(self, value):
        self.release_data['downloaded_status'] = value


