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

class TestToEvenHeight(unittest.TestCase):

  def test_unevenheight(self):
    im = Image.new('RGBA', (1,1), (11,11,11,255))
    pm = t.toevenheight(im)
    self.assertEqual(pm.height, 2)
    self.assertEqual(pm.width, 1)
    self.assertEqual(list(pm.getdata()), [(11,11,11,255), (0,0,0,0)])

  def test_evenheight(self):
    im = Image.new('RGBA', (1,2), (11,11,11,255))
    pm = t.toevenheight(im)
    self.assertEqual(pm.height, 2)
    self.assertEqual(pm.width, 1)
    self.assertEqual(list(pm.getdata()), [(11,11,11,255), (11,11,11,255)])

if __name__ == '__main__':
  unittest.main()
