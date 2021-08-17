#! /usr/bin/env python3

# image to ansi blocks
# Copyright Lesmana Zimmer lesmana@gmx.de
# Licensed under GNU GPL version 3 or later
# https://www.gnu.org/licenses/gpl-3.0.html

import unittest

import imagetoansiblocks as t

from PIL import Image

class TestPixelToAnsiBlock(unittest.TestCase):

  def test_bothalpha(self):
    upperpixel = (11, 22, 33, 0)
    lowerpixel = (44, 55, 66, 0)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, ' ')

  def test_upperalpha(self):
    upperpixel = (11, 22, 33, 0)
    lowerpixel = (44, 55, 66, 255)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;44;55;66m\u2584\033[0m')

  def test_loweralpha(self):
    upperpixel = (11, 22, 33, 255)
    lowerpixel = (44, 55, 66, 0)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;11;22;33m\u2580\033[0m')

  def test_bothcolor(self):
    upperpixel = (11, 22, 33, 255)
    lowerpixel = (44, 55, 66, 255)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;11;22;33;48;2;44;55;66m\u2580\033[0m')

  def test_alphathreshold0(self):
    upperpixel = (11, 22, 33, 99)
    lowerpixel = (44, 55, 66, 99)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, ' ')

  def test_alphathreshold1(self):
    upperpixel = (11, 22, 33, 99)
    lowerpixel = (44, 55, 66, 100)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;44;55;66m\u2584\033[0m')

  def test_alphathreshold2(self):
    upperpixel = (11, 22, 33, 100)
    lowerpixel = (44, 55, 66, 99)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;11;22;33m\u2580\033[0m')

class TestBackground(unittest.TestCase):

  def test_noalpha(self):
    im = Image.new('RGBA', (1,1), (22,22,22,255))
    background = (0,0,0)
    bm = t.background(im, background)
    self.assertEqual(bm.width, 1)
    self.assertEqual(bm.height, 1)
    self.assertEqual(list(bm.getdata()), [(22,22,22,255)])

  def test_withalpha(self):
    im = Image.new('RGBA', (3,1))
    im.putdata([(22,22,22,0), (22,22,22,128), (22,22,22,255)])
    background = (0,0,0)
    bm = t.background(im, background)
    self.assertEqual(bm.width, 3)
    self.assertEqual(bm.height, 1)
    self.assertEqual(list(bm.getdata()), [(0,0,0,255), (11,11,11,255), (22,22,22,255)])


class TestToEvenHeight(unittest.TestCase):

  def test_unevenheight(self):
    im = Image.new('RGBA', (1,1))
    im.putdata([(11,11,11,255)])
    paddingheightoffset = 0
    pm = t.toevenheight(im, paddingheightoffset)
    self.assertEqual(pm.width, 1)
    self.assertEqual(pm.height, 2)
    self.assertEqual(list(pm.getdata()), [(11,11,11,255), (0,0,0,0)])

  def test_evenheight(self):
    im = Image.new('RGBA', (1,2))
    im.putdata([(11,11,11,255), (11,11,11,255)])
    paddingheightoffset = 0
    pm = t.toevenheight(im, paddingheightoffset)
    self.assertEqual(pm.width, 1)
    self.assertEqual(pm.height, 2)
    self.assertEqual(list(pm.getdata()), [(11,11,11,255), (11,11,11,255)])

  def test_paddingattop(self):
    im = Image.new('RGBA', (1,1))
    im.putdata([(11,11,11,255)])
    paddingheightoffset = 1
    pm = t.toevenheight(im, paddingheightoffset)
    self.assertEqual(pm.width, 1)
    self.assertEqual(pm.height, 2)
    self.assertEqual(list(pm.getdata()), [(0,0,0,0), (11,11,11,255)])

if __name__ == '__main__':
  unittest.main()
