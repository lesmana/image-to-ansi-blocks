image to ansi blocks
====================

translate image pixel by pixel to ansi blocks
so that it can be displayed in terminal.

![screenshot](examples/tux-demo.png)

for more screenshots see examples directory.

the tool takes an image and outputs a bunch of characters.
the characters are terminal code for something similar to
"pixels with color information".

it does not change the size of the image.
one pixel in the image will always be one pixel in the terminal.
the only thing changed are the color of the transparent pixels
because the terminal has a very limited transparency.
also at the request of the user a one pixel border might be added.

it only works well with tiny images. icons to be precise.
if the image is too big you will get a jumbled mess of colored pixels.

the output of the tool can be saved in a file.
if the file is to be displayed in the terminal at a later time
the image will be shown.

main use case for me is to put a server logo icon in /etc/motd.
so when i ssh into a server i get a strong visual cue which server it is.

background information
----------------------

the smallest drawing element of the terminal is a character.
a character might be a letter, a number, a symbol,
and, more recently, an emoji.

on a typical terminal every character is the same size (monospace font).
a character is about twice as high as wide.
a character has a foreground color and a background color.
for example a white letter on black background.
the foreground color is white and the background color is black.

since a character is twice as high as wide,
and a character has two colors (foreground and background color),
we can put two pixels in one character.
one pixel in the top half in foreground color
and the other pixel in the bottom half in background color.
we just need such a symbol.

the upperhalfblock is a symbol
with a block at the upper half and nothing at the lower half.
the block at the upper half will be drawn in foreground color.
the nothing at lower half will will be drawn in background color.

now we assign the color of the top pixel to foreground color
and the color of the bottom pixel to background color.
when the character gets drawn it will effectively draw the two pixels.

there is also the lowerhalfblock which is just
the opposite of the upperhalfblock.

https://en.wikipedia.org/wiki/Block_Elements

practically all modern terminals can draw all RGB colors
for foreground and background color.

here a list of terminal supporting RGB

https://gist.github.com/XVilka/8346728

the terminal has no concept of alpha values for transparency.
a "terminal pixel" is either fully transparent or fully opaque.
so either the alpha values are cut off at a certain threshold.
or the alpha pixels are "flattened" to a certain color
before translating the image to terminal pixels.

technical details
-----------------

an example output of the tool might look like this

```
\033[38;2;255;0;0;48;2;0;0;255m\u2580\033[0m\033[38;2;0;255;0m\u2580\033[0m\n
```

this code will make the terminal draw a 2x2 "image".
the pixels in the image has the following colors (left to right, top to bottom):
red, green, blue, and "transparent".
transparent meaning whatever the background color of your terminal is.

technically this draws two characters.
both times the upperhalfblock characters.
the first character in the foreground color red and background color blue.
and the second character in the foreground color green
and no defined background color.
no defined background color means
the default background color of the terminal will be drawn.

let's take that thing apart

first we separate the two characters

```
\033[38;2;255;0;0;48;2;0;0;255m\u2580\033[0m \033[38;2;0;255;0m\u2580\033[0m\n
^ first                                      ^ second
```

each block consists of color information,
character to print,
and reset of color information.

```
\033[38;2;255;0;0;48;2;0;0;255m \u2580 \033[0m
^ color                         ^ char ^ reset color
```

the character is the upperhalfblock.
the color information tells the terminal what color we want
as foreground and background color.
all the following characters will then be printed in those colors.
at the end we reset the color information
so the terminal reverts back to the default colors.

the color block begins with an escape code (`\033[`).
so the terminal knows what follows is terminal code
and not characters to be printed.

the terminal code block spans from the escape to the `m`.
the `m` is the terminal code for color.
everything else between those two symbols are the parameters for `m`.

the `38` signifies foreground color.
the `2` signifies RGB color.
the following three numbers are the actual R and G and B parts.

the `48` signifies background color.
the `2` and the following three numbers again the RGB color.

once the colors are set
every character from now on are printed in those colors.

in the reset color block we only have `0` as parameter for `m`.
that means to reset the color to the terminal default colors.

in the second code block we only have `38` for foreground color.
that means the background color stays the default color.
or to be more precise: the background color stays
at whatever it was set before this code.

limitations:
------------

only rgb color which may or may not be supported by your terminal.

terminal has no transparency.
pixels with transparency will become either total transparent or full color

this can be customized using --alphathreshold

or use --background r g b to flatten alpha values

requirements:
-------------

python3

PIL/Pillow

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
