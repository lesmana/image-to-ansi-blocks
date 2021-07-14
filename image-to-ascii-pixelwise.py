#! /usr/bin/env python

import sys
import itertools
import pprint

from PIL import Image

with Image.open('mario.ico') as im:
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
    # ignore alpha for now
    sys.stdout.write(f'\033[38;2;{ur:03};{ug:03};{ub:03};48;2;{lr:03};{lg:03};{lb:03}m\u2580')
  sys.stdout.write('\033[0m\n')
