#pylint: skip-file

import os
import urllib
import urllib2
import cookielib

import binascii
from urlparse import urlparse, urlunsplit
import hashlib as hashlib

from gui import *

from bencode import encode, decode

from db.classes import Release



class Rss(object):
	def __init__(self, dbHelper):
		self.dbHelper = dbHelper
		self.runMain = True; #specifies whether the file retrival section will run
		self.count = 500; #put this number as the number of new releases to grab
		self.guirun = True;

		#Holds all the releases, a list of lists where each release is a 
		#list itself with its information as each element in the list
		self.releases = [] 
		self.newReleases = []

		#a list of all the keys.  Is first filled with keys from key.log
		#and any extra releases' keys are added later
		self.keys = [];

		self.opener = None
		

	def run(self):
		rssXml = self.readRssFeed()
		self.releases = self.dbHelper.getReleases()
		print self.releases
		# self.releases = self.getReleasesFromFile()
		self.keys = self.getIds(self.releases)

		ttlinks = self.parseRssUrls(rssXml)
		newReleases = []
		print "self.keys"
		print self.keys
		print type(self.keys[0])
		for releaseId, url in ttlinks:
			print type(releaseId)
			print "releaseid, url"
			print releaseId, url
			if releaseId in self.keys:
				print "ALREADY HAVE IT"
				# already have it
				print len(ttlinks)
				ttlinks.remove((releaseId, url))
				print len(ttlinks)

		self.authenticate()

		releasesInfolist = self.parseTTLinks(ttlinks)

		self.rssReleases = self.parseInfolist(releasesInfolist)
		newReleases = []
		for release in self.rssReleases:
			if release.id not in self.keys:
				newReleases.append(release)

		self.dbHelper.addReleases(newReleases)

		print "rss releases"
		for r in self.releases:
			try:
				print r.id
				print r.artist
				print r.album
			except:
				pass
		self.releases.extend(newReleases)
		print "rss releases"
		for r in self.releases:
			try:
				print r.id
				print r.artist
				print r.album
			except:
				pass

		# self.writeReleaseInfo()

		self.downloadTorrents()
		self.downloadImages()

		# torrentScrapes = self.scrapeTorrents()
		# print "\n\ntorrentScrapes"
		# print torrentScrapes

		#hyperlink the text
		#mark things as downloaded



	def readRssFeed(self):
		##copy the rss feed into rss.txt
		rssfile = urllib.urlopen \
		('http://www.torrentech.org/index.php?act=rssout&passkey=wy36mhhnh7loklezcg5fd9o07umque38&id=31')
		rssXml = rssfile.read()
		return rssXml



	def getReleasesFromFile(self):
		releases = []
		try:
			with open('releaseinfo.txt', 'r') as rf:
				
				for line in rf:
					sr = line.split('|+| ')
					sr.remove('\n')
					releases.append(sr) #releases[] list holds release info
				
		except IOError as e:
			# relaseinfo.txt does not exist
			pass
		
		return releases


	def getIds(self, releases):
		keys = []
		if releases is not None:
			for release in releases:
				# tup[0] is releaseId
				keys.append(release.id)

			return keys




	def parseRssUrls(self, rssXml):
		#retrieve the last part of the url, the 6 digit release ID,
		#to create a list of urls for the actual releases
		#http://www.torrentech.org/index.php?showtopic=210022
		
		ttlinks = []    #list of torrenttech release links


		for line in rssXml.split('\n'):
			checkline = line
			
			checkline = checkline.lstrip("\t")
			
			#if the first part of the checkline is <link>,
			#and the TT ID of release is not already in the key[] list,
			#add the link to the torlinks[] list
			if checkline[0:6] == '<link>':
				idLoc = checkline.rfind("id=") + len("id=")

				# Make sure the url includes id=
				if idLoc != len("id=")-1:
					idEndLoc = checkline.find(".", idLoc)
					releaseId = checkline[idLoc:idEndLoc]

					ttlinks.append((int(releaseId),
						('http://www.torrentech.org/index.php?showtopic=' + releaseId)))
		#ttlinks is full of the urls of the releases

		return ttlinks



	def authenticate(self):
		username = 'username'
		password = 'password'
		#open the Torrenttech website and pass login credentials to
		#recieve cookies for authenticated downloading of links in the future
		url = 'http://www.torrentech.org/index.php?act=Login&CODE=01'
		cj = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		login_data = urllib.urlencode( \
				 {'UserName' : username,
				  'PassWord' : password,
				  'submit' : 'Log me in',
				  'referer' : 'http://www.torrentech.org/index.php?act=Login'})
		self.opener.open(url, login_data)
		#future access of Torrenttech is now authenticated with cookies

	def parseTTLinks(self, ttlinks):

		# fw = open('info.txt', 'w').close()  #clear info.txt
		
		infolist = []


		#open, parse, and log each ttlink
		for releaseId, r in ttlinks:
			print releaseId
			print r
			if self.keys is not None and releaseId not in self.keys:
				self.newReleases.append(int(releaseId))
				self.count -= 1  #removes one from count
				#if count isn't yet -1, open the link from ttlinks
				#count variable is to limit the number of websites to download
				#during testing
				if self.count > -1:  
					resp = self.opener.open(r)
				
				the_page = resp.read()


				wait = 1    #will help indicate which line the release info begins
				found = False   #indicates when the release precursor "<!--THE POST" has been found

				# Go through each line in the release's html
				for line in the_page.split("\n"):
					wait += 1
					checkline = line
				
					#remove tabs from front of line
					# checkline = checkline.lstrip("\t")
				
					#We're now at the line where the post actually starts
					#found variable ensures we're not where the post ends,
					#since it has the same '<!--THE POST' text
					if '<!-- THE POST' in checkline and not found:
					# if checkline[0:13] == '<!-- THE POST' and not found:
						print "wait"
						print wait
						wait = -2
						found = True
						
					#after going down 2 lines from '<!--THE POST' line,
					#(this is what the wait variable is used to ensure)
					#we are now at the line with the actual release info
					if wait == 0:
						print "wait == 0"
						#replace all breaks with newlines to format
						#how I like
						checkline = checkline.replace('<br />','\n')

						#if a Discogs tag is in the line, put the html
						#on its own line with no other formatting
						#Discogs: http://blahblahblah...
						if "Discogs:" in checkline:
							starthtml = checkline.find('<')
							endhtml = checkline.find('"',starthtml + 2) + 1
							urlend = checkline.find('"',endhtml + 2)
							htmlend = checkline.find("</a>",urlend + 2) + 4
							checkline = checkline[:starthtml] + checkline[endhtml:urlend] + checkline[htmlend:]
						
						#if a Weblink tag is in the line, put the html
						#on its own line with no other formatting
						#Weblink: http://blahblahblah...
						if "Weblink:" in checkline:
							starthtml = checkline.find('<')
							endhtml = checkline.find('"',starthtml + 2) + 1
							urlend = checkline.find('"',endhtml + 2)
							htmlend = checkline.find("</a>",urlend + 2) + 4
							checkline = checkline[:starthtml] + checkline[endhtml:urlend] + checkline[htmlend:]
						
						#if a image link tag is in the line, put the html
						#on its own line with no other formatting
						#Imagelink: http://blahblahblah...
						if "<img src=" in checkline:
							starthtml = checkline.find('<')
							checkline = checkline.replace('<img src="','Imagelink: ')
							urlend = checkline.find('"',starthtml + 2)
							checkline = checkline[:urlend]
						
						#replace some html formatting with its english characters
						checkline = checkline.replace('&amp;','&')
						checkline = checkline.replace('&#33;','!')
						checkline = checkline.replace('&#39;','\'')
						
						#add the torrentech release link to the front
						#of the current checkline info
						checkline = r + '\n' + checkline
						
						infolist.append(checkline)
						# fw = open('info.txt', 'a+')
						# fw.write(checkline)     #append the checkline to info.txt
						# fw.write("\n\nENDRELEASE!\n\n") #finish release section with newlines and tag
						# fw.close()
						print "wait == 0 end"
		
		return infolist
		
		#info.txt is now filled with the unparsed html code from the 
		#release page; infolist is the same data in list form

		#example output for one element of infolist:
		# # http://www.torrentech.org/index.php?showtopic=210031
		# # Artist: Geiom
		# # Album: 2-4-6
		# # Weblink: http://www.junodownload.com/products/geiom-terrible-shock-2-4-6/2204101-02/
		# # Label: Well Rounded
		# # Catalog#: WRND 017
		# # Released: 2013-05-27
		# # Style: UK Funky

		# # Tracklist:

		# # 1 2-4-6 (5:56)
		# # 2 2-4-6 (Desto Remix) (4:31)

		# # Imagelink: http://images.junostatic.com/150/CS2204101-02A.jpg

		# # ENDRELEASE!
		



	def parseInfolist(self, infolist):
		#parse the infolist entries so each of these categories is on its own line
		#Artist, Album, weblink, Label, Catalog#, Release Date, Style
		#Tracklist, and Album Art 

		releases = []
		
		for l in infolist:
			#print l
			line = l
			print line
			
			wordtup = 'http:/', 'Artist:', 'Album:', 'Weblink:', 'Discogs:' \
			, 'Label:', 'Catalog#:', 'Released:', 'Style:', 'Imagelink:' \
			, 'ext!@#$%', 'status!@#$%'

			worddict = {
				
				'artist': 'Artist:',
				'album': 'Album:',
				'weblink_url': 'Weblink:',
				'discogs_url': 'Discogs:',
				'label': 'Label:',
				'catalog_number': 'Catalog#:',
				'release_date': 'Released:',
				'style': 'Style:',
				'coverart_url': 'Imagelink:'
			}

			
			cur = []
			imgLink = ''

			release = Release()

			for key, value in worddict.iteritems():
				if value in line:
					start = line.find(value) + len(value) + 1
					end = line.find('\n', start)

					# This is the last label
					if end == -1:
						end = len(line)

					linePiece = line[start:end]

					linePiece = linePiece.replace("'", "''")


					setattr(release, key, linePiece)

			# Get release url and id
			start = line.find('http://')
			end = line.find('\n', start)
			linePiece = line[start:end]
			release.release_url = linePiece
			release.id = int(linePiece[-6:])


			if release.coverart_url is not None:
				# Get coverart ext
				extStart = release.coverart_url.rfind('.') + len('.')
				release.coverart_ext = release.coverart_url[extStart:]

			print "New release added: {0}: {1} - {2}".format(release.id, release.artist, release.album)
			releases.append(release)

			
			# for w in wordtup:
			# 	a = ''
				
			# 	if w in line:
					
			# 		word = w
			# 		start = line.find(word) + word.__len__() + 1
			# 		end = line.find('\n', start)
					
			# 		a = line[start:end]
					
			# 		#cant get the last g of the URL for some reason..
			# 		if w == 'Imagelink:':
			# 			a = a + 'g'
			# 			imgLink = a
					
			# 		#first entry in the list will be the release ID
			# 		if w == 'http:/':
			# 			release.id = a[-6:]
			# 			# cur.append(a[-6:])
			# 			self.keys.append(a[-6:])
						
			# 	if w == 'ext!@#$%':
			# 		extStart = imgLink.rfind('.')
			# 		a = imgLink[extStart:]
					
			# 	if w == 'status!@#$%':
			# 		a = 'Not Downloaded'

			# 	setattr(release, word, a) #equivalent to: self.varname= 'something'
			# 	print getattr(release, word)
			# 	print word
			# 	# release.word = a
			# 	# cur.append(a)
				
				
			# # print "New release added: {0}: {1} - {2}".format(cur[0], cur[2], cur[3])
			# print "New release added: {0}: {1} - {2}".format(release.id, release.artist, release.album)
			# releases.append(release)
			
		print "parseInfolist"
		for r in releases:
			print r.id
			print r.artist 
			print r.album
		return releases
		#releases is now a list of lists.  Each inner list has the
		#info about each release in order defined above in wordtup




	def writeReleaseInfo(self):       
		rf = open('releaseinfo.txt', 'w')
		
		for r in self.releases:
			# print r
			for k in r:
				rf.write(k + "|+| ")
			rf.write('\n')
		rf.close()



	def downloadTorrents(self):
		os.chdir(os.getcwd() + '/torrents/')

		for releaseId in self.newReleases:
			for release in self.releases:
				if releaseId == release.id:
					torrentUrl = "http://www.torrentech.org/index.php?act=attach&type=post&passkey=wy36mhhnh7loklezcg5fd9o07umque38&id="
					torrentUrl += str(releaseId)

					urllib.urlretrieve (torrentUrl, str(releaseId) + ".torrent")



	def downloadImages(self):
		# os.chdir(os.getcwd() + '/releaseImages/')
		os.chdir('..\\releaseImages\\')
		
		image = urllib.URLopener()
		
		for releaseId in self.newReleases:
			for release in self.releases:
				if releaseId == release.id:
					url = release.coverart_url
					ext = release.coverart_ext

					folderName = '/releaseImages/'
					
					try:
						print "attempting to retrieve: "
						print url, releaseId, ext
						image.retrieve(url, str(releaseId) + '.' + ext)
					except Exception as e:
						pass
						# print "Exception"
						# print e
						# raise



	def scrapeTorrents(self):
		path = "C:\\Users\\Dillon\\Documents\\Programming\\Python\\rss\\torrents\\"
		torrentFiles = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]

		if len(torrentFiles) > 0:
			announceTracker = None

			info_hashes = []
			for torrent in torrentFiles:
				torrentData = open(path + torrent, "rb").read()
				metadata = decode(torrentData)

				if announceTracker is None:
					announceTracker = metadata["announce"]
					print "announceTracker"
					print announceTracker

				calchash = hashlib.sha1(encode(metadata['info'])).hexdigest()
				info_hashes.append(calchash)

			return scrape(announceTracker, info_hashes)
		else:
			return {}

			
def scrape(tracker, hashes):
	"""
	Returns the list of seeds, peers and downloads a torrent info_hash has, according to the specified tracker
	Args:
		tracker (str): The announce url for a tracker, usually taken directly from the torrent metadata
		hashes (list): A list of torrent info_hash's to query the tracker for
	Returns:
		A dict of dicts. The key is the torrent info_hash's from the 'hashes' parameter,
		and the value is a dict containing "seeds", "peers" and "complete".
		Eg:
		{
			"2d88e693eda7edf3c1fd0c48e8b99b8fd5a820b2" : { "seeds" : "34", "peers" : "189", "complete" : "10" },
			"8929b29b83736ae650ee8152789559355275bd5c" : { "seeds" : "12", "peers" : "0", "complete" : "290" }
		}
	"""
	tracker = tracker.lower()
	parsed = urlparse(tracker)	
	if parsed.scheme == "udp":
		return scrape_udp(parsed, hashes)

	if parsed.scheme in ["http", "https"]:
		if "announce" not in tracker:
			raise RuntimeError("%s doesnt support scrape" % tracker)
		parsed = urlparse(tracker.replace("announce", "scrape"))		 
		return scrape_http(parsed, hashes)

	raise RuntimeError("Unknown tracker scheme: %s" % parsed.scheme)


def scrape_http(parsed_tracker, hashes):
	print "Scraping HTTP: %s for %s hashes" % (parsed_tracker.geturl(), len(hashes))
	ret = {}
	maxSize = 65
	for x in range((len(hashes)/maxSize) + 1):
		qs = []
		#url_param = binascii.a2b_hex(hashes[x])
		#qs.append(("info_hash", url_param))
		for hash in hashes[0:min(maxSize,len(hashes))]:
			print hash
			url_param = binascii.a2b_hex(hash)
			qs.append(("info_hash", url_param))

		hashes[0:min(maxSize,len(hashes))] = []
		print len(hashes)

		print qs
		qs = urllib.urlencode(qs)
		pt = parsed_tracker	
		url = urlunsplit((pt.scheme, pt.netloc, pt.path, qs, pt.fragment))
		print url
		handle = urllib.urlopen(url)
		if handle.getcode() is not 200:
			raise RuntimeError("%s status code returned" % handle.getcode())	
		decoded = decode(handle.read())
		# print decoded
		for hash, stats in decoded['files'].iteritems():		
			nice_hash = binascii.b2a_hex(hash)		
			s = stats["complete"]
			p = stats["incomplete"]
			c = stats["downloaded"]
			ret[nice_hash] = { "seeds" : s, "peers" : p, "complete" : c}		
	return ret

