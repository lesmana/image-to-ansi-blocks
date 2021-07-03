#! /usr/bin/env python

import sys
import itertools
import pprint

from PIL import Image

with Image.open('cat.ico') as im:
  pixels = im.getdata()
  width = im.width
  height = im.height
  #print(im.getbands())

iterpixels = iter(pixels)

rows = []
for y in range(height):
  row = []
  for x in range(width):
    pixel = next(iterpixels)
    row.append(pixel)
  rows.append(row)

pairs = [iter(rows)] * 2
doublerows = itertools.zip_longest(*pairs)

upperhalfblock = '\u2580'
lowerhalfblock = '\u2584'
fullblock = '\u2588'
noblock = ' '

for upperrow, lowerrow in doublerows:
  for upperpixel, lowerpixel in zip(upperrow, lowerrow):
    #print(upperpixel, lowerpixel)
    ur, ug, ub, ua = upperpixel
    lr, lg, lb, la = lowerpixel
    # for now this just looking at alpha ignoring color completely
    if ua == 0 and la == 0:
      sys.stdout.write(noblock)
    elif ua == 0 and la == 255:
      sys.stdout.write(lowerhalfblock)
    elif ua == 255 and la == 0:
      sys.stdout.write(upperhalfblock)
    elif ua == 255 and la == 255:
      sys.stdout.write(fullblock)
  sys.stdout.write('\n')

