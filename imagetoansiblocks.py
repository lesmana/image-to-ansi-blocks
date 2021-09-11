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

def parseargv():
  parser = argparse.ArgumentParser()
  parser.add_argument('filename')
  parser.add_argument('--alphathreshold', type=int, default=128)
  parser.add_argument('--paddingattop', action='store_const', dest='paddingheightoffset', const=1, default=0)
  parser.add_argument('--background', type=int, nargs=3)
  parser.add_argument('--border', type=int, nargs=3)
  parser.add_argument('--debug', action='store_true')
  args = parser.parse_args()
  if args.background is not None:
    args.background = tuple(args.background)
  if args.border is not None:
    args.border = tuple(args.border)
  return args

def openimage(filename):
  with Image.open(filename) as im:
    im.load()
    im = im.convert('RGBA')
    return im

def background(im, background):
  if background is not None:
    bm = Image.new('RGBA', im.size, background)
    bm.alpha_composite(im)
    return bm
  else:
    return im

def border(im, border):
  if border is not None:
    bm = Image.new('RGBA', (im.width+2, im.height+2), border)
    bm.paste(im, (1, 1))
    return bm
  else:
    return im

def toevenheight(im, paddingheightoffset):
  if im.height % 2 != 0:
    pm = Image.new('RGBA', (im.width, im.height+1), (0,0,0,0))
    pm.paste(im, (0, paddingheightoffset))
    return pm
  else:
    return im

def alpha(im, alphathreshold):
  alphachannel = im.getchannel('A')
  alphachannel = alphachannel.point(lambda a: 255 if a >= alphathreshold else 0)
  im.putalpha(alphachannel)
  return im

def pixelstorows(pixels, width, height):
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

def pixelstodoublerows(pixels, width, height):
  rows = pixelstorows(pixels, width, height)
  doublerows = rowstodoublerows(rows)
  return doublerows

def debugprint(im):
  pixels = list(im.getdata())
  width = im.width
  height = im.height
  doublerows = pixelstodoublerows(pixels, width, height)
  linecount = 1
  for upperrow, lowerrow in doublerows:
    print('lines', linecount, linecount+1)
    for upperpixel, lowerpixel in zip(upperrow, lowerrow):
      print(upperpixel, lowerpixel)
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
  im = background(im, args.background)
  im = border(im, args.border)
  im = toevenheight(im, args.paddingheightoffset)
  im = alpha(im, args.alphathreshold)
  pixels = list(im.getdata())
  width = im.width
  height = im.height
  doublerows = pixelstodoublerows(pixels, width, height)
  for ansiblock in doublerowstoansiblocks(doublerows):
    sys.stdout.write(ansiblock)

if __name__ == '__main__':
  main()
