# Simple Tool for Building JPEG/JS Polyglot Images

A polyglot file is one that looks and behaves like two different file types.  This tool builds one that is simultaneously a JPEG image and a JavaScript script.

Such files can introduce vulnerabilities in web services as many browsers, by default, examine the contents of a downloaded resource and override the `Content-Type` if it disagrees with what the browser believes the file to be.  This is the so-called MIME Confusion Attack.

A file created with this tool will display as a regular image with

```html
<img src="hackedimage.jpg">
```

Many browsers, without `nosniff` set in the response headers, will execute it as JavaScript with

```html
<script charset="ISO-8859-1" src="hackedimage.jpg"></script> 
```

Despite the fact that it is an image, and the server returns it with a `Content-Type` of `image/jpeg`, the browser inspects the file, determines it is JavaScript code, which matches what the `<script>` tag expects, and executes it as JavaScript.

Note that some browsers need the charset set (as above), otherwise they expect UTF-8, which will cause it to break.

## How it works

This script is inspired by the article ["Bypassing CSP using polyglot JPEGs"](https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs) by Gareth Heyes at Portswigger.

The first observation is that JavaScript variable names do not have to be ASCII but can be a binary value.  The first two characters of a JPEG/JFIF image are `FF D8` and the next two characters are the JFIF header marker `FF E0`.  We use these four bytes as a variable name.  

We want to follow the variable name by an equals sign `=`.  In a JPEG file, the header marker should be followed by the length of the header as two bytes.  We make the length of this header 12074 bytes, which is `2F2A`, which in ASCII is `/*`, ie the start of a JavaScript comment.  Thus when interpreted as JavaScript, everything after this and before the first `*/` will be skipped as a comment.

We follow this with the regular things JPEG expects in a JFIF header and pad it out to 12074 bytes with zeroes.  

We now create a JPEG comment header, which begins with the marker `FF FE` and the length in bytes.  We insert, as the JPEG comment, `*/` to close the JavaScript comment, followed by `=` for the variable assignment, followed by the JavaScript we want the browser to execute, followed by another `/*` to start a new JavaScript comment.  

Then we insert our actual image data, which is inside the JavaScript comment therefore ignored by the JavaScript interpreter.  A restriction is that the image may not contain the bytes `2A 2F` which would close the JavaScript comment (unless it is also followed by a `2F 2A`immediately after).

Finally we add an additional JPEG comment to close the JavaScriot comment with a `2A 2F` and open an inline comment `//` with `2F 2F`, then finish with the end-of-JPEG marker `FF D9`.

## Requirements

This tool only requires Python 3 with no additional dependencies.  It has been tested with Python 3.8.3.  It should work with 3.6 onwards but only 3.8.3 has been tested.
 
## How to Use the Script

The command line usage is

```
python3 --image input-image.jpg --output output-image.jpg --js javascript-file.js
```

`--image` can be replaced with `-i`, `--output` with `-o` and `--js` with `-j`.

### Example

```
python3 --image plainimage.jpg --output hackedimage.jpg --js code.js
```

The images and JavaScript code are included in the distribution.  To view it, open the `index.html` file in your web browser.  You should see the image, and the alert opened by the JavaScript code should also pop up.

### Caveats

As noted above, if the image data contains the bytes `2A 2F` then it will fail as JavaScript code as the bytes that follow would be outside the JavaScript comment.  If you find this happens, try re-encoding your JPEG.  The chance of it happening is less if your image is smaller.

It will not work for large images because the browser sniffing will stop scanning and determine that it is not JavaScript code.  I have had success with 256x256 images.

This is proof-of-concept code and has not been tested in anger.  It has worked on a variety of (small) images I have given it, but it has not been exhaustively tested.

