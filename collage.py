#!/usr/bin/env python
"""
Generate a sequence from a set of input images.

All settings can be overwritten in settings_local.py.
"""
import re
import urllib2
import StringIO
import glob
import math
import os
import sys
import time
from optparse import OptionParser
from planar import Affine
from PIL import Image, ImageFont, ImageDraw


class Collage:
    @staticmethod
    def build(infiles,cols=3,padding=2,bgcolor='#1a1a1a',max_width=500):
	    # List of input files.
        print('Found %s input files.' % len(infiles))
        bigImg = Image.new('RGBA', (812,500), '#0f0f0f')
        for f in infiles:
            img = urllib2.urlopen(f['src']).read()
            tile = Image.open(StringIO.StringIO(img)).convert('RGBA')
            print f['attrs']
            x = int(f['attrs']['x'])
            y = int(f['attrs']['y'])
            w = math.ceil(float(f['attrs']['size']['x'])) 
            h = math.ceil(float(f['attrs']['size']['y']))
            tile.thumbnail((int(w),int(h)), Image.ANTIALIAS)
            print tile.size, "---SIZE"
            #m = re.search('t(?P<translate>.+)s(?P<scale>.+)r(?P<rotate>.+)',f['transform'])
            
            if f['attrs'].has_key('rotate') and f['attrs']['rotate'] != 0:
                tile = tile.rotate(-float(f['attrs']['rotate']),Image.NEAREST,True)
               
                       #if m and m.group('scale'):
            if f['attrs'].has_key('scale') and f['attrs']['scale']['x'] != 1:
                #scale = m.group('scale').split(',')
                #ascale = Affine.scale(float(scale[0]))
                #print float(scale[0]), "----SCALE"
                #print ascale
                print f['attrs']['scale']['x'], '---SCALE'
                w = math.ceil(float(f['attrs']['size']['x']) * f['attrs']['scale']['x']) * 1.8
                h = math.ceil(float(f['attrs']['size']['y']) * f['attrs']['scale']['y']) * 1.8
            #if m and m.group('rotate'):
                #rotate = m.group('rotate').split(',')
                #print rotate, "___ROTATE"
                #arotate = Affine.rotation(float(rotate[0]), pivot=(w/2,h/2))
                #arotate = Affine.rotation(92, pivot=(w/2,h/2))
                         #if m and m.group('translate'):
            if f['attrs'].has_key('translate') and f['attrs']['translate']['x'] != 0:
                #translate = m.group('translate').split(',')
                #offset = Affine.translation((float(translate[0]), float(translate[1])))
                x = int(f['attrs']['x'] + f['attrs']['translate']['x'] - (f['attrs']['rotate'] / 2)) 
                y = int(f['attrs']['y'] + f['attrs']['translate']['y'] + (f['attrs']['rotate'] / 2)) 
                #if x < 0: x = 0
                #if y < 0: y = 0

 
            print w,h
            print tile
            tile.thumbnail((int(w),int(h)), Image.ANTIALIAS)
            #tile = tile.rotate(43, Image.NEAREST, True)
            if False and offset and arotate and ascale:
                aff =  arotate * offset 
                print aff,"1---"
                    
                aff =  ascale * aff
                print aff, "----"
                print aff[0],"0"
                print aff[1],"1"
                print aff[2],"2"
                print aff[3],"3"
                print aff[4],"4"
                print aff[5],"5"
                print aff[6],"6"
                print aff[7],"7"
                print aff[8],"8"
                print aff
                #t = tile.transform(bigImg.size,Image.AFFINE,(aff[0],aff[1],aff[2],aff[3],aff[4],aff[5]))
                #t = tile.transform((1000,1000),Image.AFFINE,(1,0,0,0,1,0))
                #print t.size
                #t.save('static/test.png',quality=95)
            #print t.mode
            #print f['matrix'].split(','), '---matrix'
            #print t.mode
            b = []
            #for a in f['matrix'].split(','):
            #    b.append(float(a))
            #c = tuple(b)
            #print c
            #t = tile.transform(bigImg.size,Image.AFFINE,c)
            #t.save('static/test.png',quality=95)
            print x,y,"_______________"
            print tile.size
            bigImg.paste(tile, (x,y), mask=tile)
        """
        Gtiles = []
	    tile_count = len(infiles) 
	    COLS = cols
	    x        = 0;
	    imgsizeX = []
	    imgsizeY = 0
	    imgno    = 0
	    maxY     = 0
	    for k,tile_file in infiles.items():
		print('Processing %s...' % tile_file)

		# Tile position.
		pos = imgno 
		if pos % cols == 0 and x: 
			imgsizeX.append(x)
			imgsizeY += maxY

			x    = 0
			maxY = 0
		y = pos // COLS

		# Offsets.
	        img = urllib2.urlopen(tile_file[0]).read()
	        tile = Image.open(StringIO.StringIO(img))
		height_to = tile.size[1]
		if tile.size[0] > max_width:
			height_to =int((float(max_width) / tile.size[0]) * tile.size[1])
			tile.thumbnail((max_width, height_to), Image.ANTIALIAS)
		maxY = max((maxY, height_to))

		xoff = padding + x 
		yoff = padding + y +imgsizeY
		tiles.append((tile, (xoff,yoff)))

		#setup for new image
		x+= tile.size[0]
		if len(infiles)-1 == imgno:
			imgsizeX.append(x)	
			imgsizeY += maxY
		imgno += 1

	    # Create canvas.
	    ROWS = imgno // COLS + (1 if tile_count % COLS else 0)
	    imgsize = (2* padding + max(imgsizeX),	
		       2 * padding + imgsizeY) 
	    img = Image.new('RGB', imgsize, bgcolor)
	    for tile in tiles:
		# Place tile on canvas.
		img.paste(tile[0], (tile[1][0], tile[1][1]))
	    print('Creating a grid with %s columns and %s rows.' % (COLS, ROWS))
        """
        path = 'static/collage/'+str(time.time())+'.jpg'
        print('Writing output file: %s' % path)
        bigImg.save(path, quality=95)

        return path




