#! /usr/bin/env python3

# image to ansi blocks
# Copyright Lesmana Zimmer lesmana@gmx.de
# Licensed under WTFPL version 2
# http://www.wtfpl.net/about/

import sys
import itertools
import pprint

from PIL import Image

def filenamefromargv():
  try:
    filename = sys.argv[1]
  except:
    print('need argument: filename of image')
    sys.exit(1)
  return filename

def imagefiletopixels(filename):
  with Image.open(filename) as im:
    pixels = im.getdata()
    width = im.width
    height = im.height
    #print(im.getbands())
  return pixels, height, width

def pixelstodoublerows(pixels, height, width):

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

  return doublerows

upperhalfblock = '\u2580'
lowerhalfblock = '\u2584'
fullblock = '\u2588'
noblock = ' '

alphathreshold = 128

def pixeltoansiblock(upperpixel, lowerpixel):
  #print(upperpixel, lowerpixel)
  ur, ug, ub, ua = upperpixel
  lr, lg, lb, la = lowerpixel
  if ua < alphathreshold and la < alphathreshold:
    return noblock
  elif ua < alphathreshold and la >= alphathreshold:
    return f'\033[38;2;{lr};{lg};{lb}m' + lowerhalfblock + '\033[0m'
  elif ua >= alphathreshold and la < alphathreshold:
    return f'\033[38;2;{ur};{ug};{ub}m' + upperhalfblock + '\033[0m'
  elif ua >= alphathreshold and la >= alphathreshold:
    return f'\033[38;2;{ur};{ug};{ub};48;2;{lr};{lg};{lb}m' + upperhalfblock + '\033[0m'
  else:
    raise Exception(f'unexpected alpha value: {ua}, {la}')

def doublerowstoansiblocks(doublerows):
  for upperrow, lowerrow in doublerows:
    for upperpixel, lowerpixel in zip(upperrow, lowerrow):
      yield pixeltoansiblock(upperpixel, lowerpixel)
    yield '\n'

def main():
  filename = filenamefromargv()
  pixels, height, width = imagefiletopixels(filename)
  doublerows = pixelstodoublerows(pixels, height, width)
  for ansiblock in doublerowstoansiblocks(doublerows):
    sys.stdout.write(ansiblock)

if __name__ == '__main__':
  main()
