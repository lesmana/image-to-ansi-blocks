image to ansi blocks
====================

translate image pixel by pixel to ansi blocks
so that it can be displayed in terminal.

using upper half block and lower half block

https://en.wikipedia.org/wiki/Block_Elements

using foreground and background color

effectively two pixels in one ascii char

limitations:
------------

only rgb color which may or may not be supported by your terminal.
see here for list of terminal supporting rgb:
https://gist.github.com/XVilka/8346728

terminal has no transparency.
alpha value below 128 is translated to terminal background color.
alpha values above 128 is translated to color of pixel.

this can be customized using --alphathreshold

or use --background r g b to flatten alpha values

requirements:
-------------

python3

PIL/Pillow

examples:
---------

cat image from https://www.favicon.cc/?action=icon&file_id=851700

mario https://www.favicon.cc/?action=icon&file_id=962351

heart https://www.favicon.cc/?action=icon&file_id=951526

license:
--------

Copyright Lesmana Zimmer lesmana@gmx.de

This program is free software.
It is licensed under the GNU GPL version 3 or later.
That means you are free to use this program for any purpose;
free to study and modify this program to suit your needs;
and free to share this program or your modifications with anyone.
If you share this program or your modifications
you must grant the recipients the same freedoms.
To be more specific: you must share the source code under the same license.
For details see https://www.gnu.org/licenses/gpl-3.0.html
