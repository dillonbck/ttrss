#pylint: skip-file

from Tkinter import *
from PIL import Image, ImageTk
import webbrowser
import functools

import os


class Gui(object):
	def __init__(self, releases):
		self.releases = releases
		print "gui releases"
		try:
			for r in self.releases:
				print r.id
				print r.artist
				print r.album
		except:
			pass

	def run(self):
		#gui run
		#Uses autoscrollbar:
		#http://effbot.org/zone/tkinter-autoscrollbar.htm
		
		root = Tk()

		vscrollbar = AutoScrollbar(root)
		vscrollbar.grid(row=0, column=1, sticky=N+S)
		hscrollbar = AutoScrollbar(root, orient=HORIZONTAL)
		hscrollbar.grid(row=1, column=0, sticky=E+W)

		canvas = Canvas(root,
						yscrollcommand=vscrollbar.set,
						xscrollcommand=hscrollbar.set)
		canvas.grid(row=0, column=0, sticky=N+S+E+W)

		vscrollbar.config(command=canvas.yview)
		hscrollbar.config(command=canvas.xview)

		# make the canvas expandable
		root.grid_rowconfigure(0, weight=1)
		root.grid_columnconfigure(0, weight=1)
		
		#Create a frame to hold all the smaller blocks on the canvas
		frame = Frame(canvas)
		frame.rowconfigure(1, weight=1)
		frame.columnconfigure(1, weight=1)
		
		#add the blocks to the frame
		if self.releases is not None:
			for i in range(len(self.releases)):
				if not(self.releases[i].coverart_ext == '') and self.releases[i].coverart_ext is not None:
					block = Block(frame, self.releases[i].artist, self.releases[i].album, \
						self.releases[i].label, self.releases[i].downloaded_status, self.releases[i].id, \
						self.releases[i].release_url, str(self.releases[i].id) + '.' + self.releases[i].coverart_ext)
				else:
					block = Block(frame, self.releases[i].artist, self.releases[i].album, \
						self.releases[i].label, self.releases[i].downloaded_status)
		
		#Force the frame's contents to be visible
		frame.pack()
		
		canvas.create_window(0, 0, anchor=NW, window=frame)
		frame.update_idletasks()
		canvas.config(scrollregion=canvas.bbox("all"))
		
		root.mainloop()

class Block:

	def click_link_tt(self, event, link):
		print "you clicked a link"
		webbrowser.open(link)
		# http://www.torrentech.org/index.php?act=attach&amp;type=post&amp;passkey=wy36mhhnh7loklezcg5fd9o07umque38&amp;id=210224

	def click_link_torrent(self, event, ID):
		print "you clicked a link"
		link = 'http://www.torrentech.org/index.php?act=attach&type=post&passkey=wy36mhhnh7loklezcg5fd9o07umque38&id='
		link += ID
		webbrowser.open(link)

	def click_link_status(self, event, status):
		print "you clicked a link"
		webbrowser.open("url")
		# http://www.torrentech.org/index.php?act=attach&amp;type=post&amp;passkey=wy36mhhnh7loklezcg5fd9o07umque38&amp;id=210224

		
			
	def __init__(self, root, artist = 'artist', album = 'album', \
		label  = 'label', \
		downloaded = 'Not Downloaded', id = '', ttlink = '', \
		cover = 'defaultimg.jpg', img = '..\\resources\dlk.gif'):

		# os.chdir('..\\')
		# os.chdir('resources')
		# print os.getcwd()
		
		sizeimg = 25, 25
		sizecover = 100, 100
		
		framep = Frame(root)
		framel = Frame(framep)
		framer = Frame(framep, width = 300)

		image = Image.open(img)
		image = image.resize(sizeimg, Image.ANTIALIAS)
		photoimg = ImageTk.PhotoImage(image)
		
		try:
			image = Image.open(cover)
		except:
			image = Image.open('..\\resources\defaultimg.jpg')
		image = image.resize(sizecover, Image.ANTIALIAS)
		photocover = ImageTk.PhotoImage(image)
		
		link1 = Label(framer, anchor=W, wraplength=250, padx=15, text=artist + ' - ' + album)
		link1.grid(row=0, column=0, sticky=W)
		link2 = Label(framer, anchor=W, wraplength=250, padx=15, text=label)
		link2.grid(row=1, column=0, sticky=W)
		link3 = Label(framer, anchor=W, wraplength=250, padx=15, text=downloaded)
		link3.grid(row=2, column=0, sticky=W)
		
		link1.bind("<1>", functools.partial(self.click_link_tt, link = ttlink))
		#link2.bind("<1>", self.click_link)
		link3.bind("<1>", functools.partial(self.click_link_status, status = downloaded))
						  
						  
		
		labelimg = Label(framer, image=photoimg)
		labelimg.grid(row=0, column=1)
		labelimg.image = photoimg	#save a reference to the image
									#in order to display properly
		
		labelcover = Label(framel, image=photocover)
		labelcover.grid()
		labelcover.image = photocover #save a reference to the image
									  #in order to display properly
		
		labelimg.bind("<1>", functools.partial(self.click_link_torrent, ID = id))
		labelcover.bind("<1>", self.click_link_tt)

		framer.pack(side=RIGHT)
		framel.pack(side=LEFT)
		framep.pack(anchor=W)
		



class AutoScrollbar(Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)
    def pack(self, **kw):
        raise TclError, "cannot use pack with this widget"
    def place(self, **kw):
        raise TclError, "cannot use place with this widget"