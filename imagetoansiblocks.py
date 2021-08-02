#! /usr/bin/env python3

# image to ansi blocks
# Copyright Lesmana Zimmer lesmana@gmx.de
# Licensed under GNU GPL version 3 or later
# https://www.gnu.org/licenses/gpl-3.0.html

import sys
import itertools
import pprint
import argparse

from PIL import Image

def filenamefromargv():
  parser = argparse.ArgumentParser()
  parser.add_argument('filename')
  args = parser.parse_args()
  return args.filename

def imagefiletopixels(filename):
  with Image.open(filename) as im:
    pixels = im.getdata()
    width = im.width
    height = im.height
    #print(im.getbands())
  return pixels, height, width

def toevenheight(pixels, height, width, unevenheightpadding):
  if height % 2 != 0:
    fillvalue = [unevenheightpadding] * width
    pixels.extend(fillvalue)
    return pixels, height+1, width
  else:
    return pixels, height, width

def pixelstorows(pixels, height, width):
  iterpixels = iter(pixels)
  rows = []
  for y in range(height):
    row = []
    for x in range(width):
      pixel = next(iterpixels)
      row.append(pixel)
    rows.append(row)
  return rows

def rowstodoublerows(rows):
  iterrows = iter(rows)
  doublerows = itertools.zip_longest(iterrows, iterrows)
  return doublerows

def pixelstodoublerows(pixels, height, width):
  rows = pixelstorows(pixels, height, width)
  doublerows = rowstodoublerows(rows)
  return doublerows

upperhalfblock = '\u2580'
lowerhalfblock = '\u2584'
fullblock = '\u2588'
noblock = ' '

def pixeltoansiblock(upperpixel, lowerpixel, alphathreshold):
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

def doublerowstoansiblocks(doublerows, alphathreshold):
  for upperrow, lowerrow in doublerows:
    for upperpixel, lowerpixel in zip(upperrow, lowerrow):
      yield pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    yield '\n'

def main():
  filename = filenamefromargv()
  alphathreshold = 128
  unevenheightpadding = (0, 0, 0, 0)
  pixels, height, width = imagefiletopixels(filename)
  pixels, height, width = toevenheight(pixels, height, width, unevenheightpadding)
  doublerows = pixelstodoublerows(pixels, height, width)
  for ansiblock in doublerowstoansiblocks(doublerows, alphathreshold):
    sys.stdout.write(ansiblock)

if __name__ == '__main__':
  main()
