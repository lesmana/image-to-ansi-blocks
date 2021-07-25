#! /usr/bin/env python3

# image to ansi blocks
# Copyright Lesmana Zimmer lesmana@gmx.de
# Licensed under WTFPL version 2
# http://www.wtfpl.net/about/

import sys
import itertools
import pprint

from PIL import Image

try:
  filename = sys.argv[1]
except:
  print('need argument: filename of image')
  sys.exit(1)

with Image.open(filename) as im:
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
    if ua < 128:
      ua = 0
    if ua >= 128:
      ua = 255
    if la < 128:
      la = 0
    if la >= 128:
      la = 255
    if ua == 0 and la == 0:
      sys.stdout.write(noblock)
    elif ua == 0 and la == 255:
      sys.stdout.write(f'\033[38;2;{lr};{lg};{lb}m' + lowerhalfblock + '\033[0m')
    elif ua == 255 and la == 0:
      sys.stdout.write(f'\033[38;2;{ur};{ug};{ub}m' + upperhalfblock + '\033[0m')
    elif ua == 255 and la == 255:
      sys.stdout.write(f'\033[38;2;{ur};{ug};{ub};48;2;{lr};{lg};{lb}m' + upperhalfblock + '\033[0m')
    else:
      raise Exception(f'unexpected alpha value: {ua}, {la}')
  sys.stdout.write('\n')
