#! /usr/bin/env python3

# image to ansi blocks
# Copyright Lesmana Zimmer lesmana@gmx.de
# Licensed under WTFPL version 2
# http://www.wtfpl.net/about/

import unittest

import imagetoansiblocks as t

class TestPixelToAnsiBlock(unittest.TestCase):

  def test_bothalpha(self):
    upperpixel = (101, 102, 103, 0)
    lowerpixel = (201, 202, 203, 0)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, ' ')

  def test_upperalpha(self):
    upperpixel = (101, 102, 103, 0)
    lowerpixel = (201, 202, 203, 255)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;201;202;203m\u2584\033[0m')

  def test_loweralpha(self):
    upperpixel = (101, 102, 103, 255)
    lowerpixel = (201, 202, 203, 0)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;101;102;103m\u2580\033[0m')

  def test_bothcolor(self):
    upperpixel = (101, 102, 103, 255)
    lowerpixel = (201, 202, 203, 255)
    alphathreshold = 128
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;101;102;103;48;2;201;202;203m\u2580\033[0m')

  def test_alphathreshold0(self):
    upperpixel = (101, 102, 103, 99)
    lowerpixel = (201, 202, 203, 99)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, ' ')

  def test_alphathreshold1(self):
    upperpixel = (101, 102, 103, 99)
    lowerpixel = (201, 202, 203, 100)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;201;202;203m\u2584\033[0m')

  def test_alphathreshold2(self):
    upperpixel = (101, 102, 103, 100)
    lowerpixel = (201, 202, 203, 99)
    alphathreshold = 100
    ansiblock = t.pixeltoansiblock(upperpixel, lowerpixel, alphathreshold)
    self.assertEqual(ansiblock, '\033[38;2;101;102;103m\u2580\033[0m')

class TestPixelsToDoubleRows(unittest.TestCase):

  def test_4x3(self):
    pixels = [1,2,3,4,5,6,7,8,9,10,11,12]
    height = 4
    width = 3
    doublerows = t.pixelstodoublerows(pixels, height, width)
    self.assertEqual(list(doublerows), [([1,2,3],[4,5,6]),([7,8,9],[10,11,12])])

if __name__ == '__main__':
  unittest.main()
