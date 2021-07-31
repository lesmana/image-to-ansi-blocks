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

if __name__ == '__main__':
  unittest.main()
