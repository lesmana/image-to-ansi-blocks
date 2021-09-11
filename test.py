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
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel)
    self.assertEqual(ansiblock, ' ')

  def test_upperalpha(self):
    upperpixel = (11, 22, 33, 0)
    lowerpixel = (44, 55, 66, 255)
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel)
    self.assertEqual(ansiblock, '\033[38;2;44;55;66m\u2584\033[0m')

  def test_loweralpha(self):
    upperpixel = (11, 22, 33, 255)
    lowerpixel = (44, 55, 66, 0)
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel)
    self.assertEqual(ansiblock, '\033[38;2;11;22;33m\u2580\033[0m')

  def test_bothcolor(self):
    upperpixel = (11, 22, 33, 255)
    lowerpixel = (44, 55, 66, 255)
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel)
    self.assertEqual(ansiblock, '\033[38;2;11;22;33;48;2;44;55;66m\u2580\033[0m')

class TestBackground(unittest.TestCase):

  def test_noalpha(self):
    im = Image.new('RGBA', (1,1))
    im.putdata([(22,22,22,255)])
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

class TestBorder(unittest.TestCase):

  def test_border(self):
    im = Image.new('RGBA', (1,1))
    im.putdata([(22,22,22,255)])
    border = (99,99,99)
    bm = t.border(im, border)
    self.assertEqual(bm.width, 3)
    self.assertEqual(bm.height, 3)
    self.assertEqual(list(bm.getdata()), [
          (99,99,99,255), (99,99,99,255), (99,99,99,255),
          (99,99,99,255), (22,22,22,255), (99,99,99,255),
          (99,99,99,255), (99,99,99,255), (99,99,99,255)])

class TestAlpha(unittest.TestCase):

  def test_middle(self):
    im = Image.new('RGBA', (1,3))
    im.putdata([(22,22,22,30), (22,22,22,130), (22,22,22,230)])
    alphathreshold = 128
    am = t.alpha(im, alphathreshold)
    self.assertEqual(am.width, 1)
    self.assertEqual(am.height, 3)
    self.assertEqual(list(am.getdata()), [
          (22,22,22,0), (22,22,22,255), (22,22,22,255)])

  def test_low(self):
    im = Image.new('RGBA', (1,3))
    im.putdata([(22,22,22,30), (22,22,22,130), (22,22,22,230)])
    alphathreshold = 10
    am = t.alpha(im, alphathreshold)
    self.assertEqual(am.width, 1)
    self.assertEqual(am.height, 3)
    self.assertEqual(list(am.getdata()), [
          (22,22,22,255), (22,22,22,255), (22,22,22,255)])

  def test_high(self):
    im = Image.new('RGBA', (1,3))
    im.putdata([(22,22,22,30), (22,22,22,130), (22,22,22,230)])
    alphathreshold = 250
    am = t.alpha(im, alphathreshold)
    self.assertEqual(am.width, 1)
    self.assertEqual(am.height, 3)
    self.assertEqual(list(am.getdata()), [
          (22,22,22,0), (22,22,22,0), (22,22,22,0)])

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
