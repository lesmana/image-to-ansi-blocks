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
  args = parser.parse_args()
  if args.background is not None:
    args.background = tuple(args.background)
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

def toevenheight(im, paddingheightoffset):
  if im.height % 2 != 0:
    pm = Image.new('RGBA', (im.width, im.height+1), (0,0,0,0))
    pm.paste(im, (0, paddingheightoffset))
    return pm
  else:
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
  args = parseargv()
  im = openimage(args.filename)
  im = background(im, args.background)
  im = toevenheight(im, args.paddingheightoffset)
  pixels = list(im.getdata())
  width = im.width
  height = im.height
  doublerows = pixelstodoublerows(pixels, width, height)
  for ansiblock in doublerowstoansiblocks(doublerows, args.alphathreshold):
    sys.stdout.write(ansiblock)

if __name__ == '__main__':
  main()
