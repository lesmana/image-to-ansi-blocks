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
from PIL import ImageColor

def parseargv():
  parser = argparse.ArgumentParser()
  parser.add_argument('filename')
  parser.add_argument('--alphathreshold', type=int, default=128)
  parser.add_argument('--paddingattop', action='store_true')
  parser.add_argument('--background', dest='backgroundcolor')
  parser.add_argument('--border', dest='bordercolor')
  parser.add_argument('--debug', action='store_true')
  args = parser.parse_args()
  return args

def openimage(filename):
  with Image.open(filename) as im:
    im.load()
    im = im.convert('RGBA')
    return im

def background(im, colorstr):
  if colorstr is not None:
    color = ImageColor.getrgb(colorstr)
    bm = Image.new('RGBA', im.size, color)
    bm.alpha_composite(im)
    return bm
  else:
    return im

def border(im, colorstr):
  if colorstr is not None:
    color = ImageColor.getrgb(colorstr)
    bm = Image.new('RGBA', (im.width+2, im.height+2), color)
    bm.paste(im, (1, 1))
    return bm
  else:
    return im

def padding(im, paddingattop):
  if im.height % 2 != 0:
    offset = 1 if paddingattop else 0
    pm = Image.new('RGBA', (im.width, im.height+1), (0,0,0,0))
    pm.paste(im, (0, offset))
    return pm
  else:
    return im

def alpha(im, alphathreshold):
  alphachannel = im.getchannel('A')
  alphachannel = alphachannel.point(lambda a: 255 if a >= alphathreshold else 0)
  im.putalpha(alphachannel)
  return im

def pixelstorows(im):
  pixels = list(im.getdata())
  width = im.width
  height = im.height
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
  # zip over the same iterator
  # for list [1,2,3,4,5]
  # will get [(1,2), (3,4), (5,None)]
  iterrows = iter(rows)
  doublerows = itertools.zip_longest(iterrows, iterrows)
  return doublerows

def pixelstodoublerows(im):
  rows = pixelstorows(im)
  doublerows = rowstodoublerows(rows)
  return doublerows

def debugprint(im):
  doublerows = pixelstodoublerows(im)
  linecount = 1
  for upperrow, lowerrow in doublerows:
    print('lines', linecount, linecount+1)
    if lowerrow is not None:
      for upperpixel, lowerpixel in zip(upperrow, lowerrow):
        print(upperpixel, lowerpixel)
    else:
      for upperpixel in upperrow:
        print(upperpixel, None)
    linecount += 2

upperhalfblock = '\u2580'
lowerhalfblock = '\u2584'
fullblock = '\u2588'
noblock = ' '

def pixeltoansiblock(upperpixel, lowerpixel):
  #print(upperpixel, lowerpixel)
  ur, ug, ub, ua = upperpixel
  lr, lg, lb, la = lowerpixel
  if ua < 255 and la < 255:
    return noblock
  elif ua < 255 and la == 255:
    return f'\033[38;2;{lr};{lg};{lb}m{lowerhalfblock}\033[0m'
  elif ua == 255 and la < 255:
    return f'\033[38;2;{ur};{ug};{ub}m{upperhalfblock}\033[0m'
  elif ua == 255 and la == 255:
    return f'\033[38;2;{ur};{ug};{ub};48;2;{lr};{lg};{lb}m{upperhalfblock}\033[0m'
  else:
    raise Exception(f'unexpected alpha value: {ua}, {la}')

def doublerowstoansiblocks(doublerows):
  for upperrow, lowerrow in doublerows:
    for upperpixel, lowerpixel in zip(upperrow, lowerrow):
      yield pixeltoansiblock(upperpixel, lowerpixel)
    yield '\n'

def main():
  args = parseargv()
  im = openimage(args.filename)
  if args.debug:
    debugprint(im)
  im = background(im, args.backgroundcolor)
  im = border(im, args.bordercolor)
  im = padding(im, args.paddingattop)
  im = alpha(im, args.alphathreshold)
  doublerows = pixelstodoublerows(im)
  for ansiblock in doublerowstoansiblocks(doublerows):
    sys.stdout.write(ansiblock)

if __name__ == '__main__':
  main()
