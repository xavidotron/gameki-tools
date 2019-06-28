# Gameki Tools

## About

Command-line tools useful for writing/running LARPs based on [GameTeX](http://web.mit.edu/kenclary/Public/Guild/GameTeX/). Used for the backend of [Gameki](http://xavidotron.github.io/ep_gameki/), but can also be used directly with an ordinary GameTeX repo.

### Tools Included

* `casting`: Generate an interactive webpage for casting based on a csv of app responses (from, e.g., Google Forms).
* `mail`: Mail out casting/costuming hints or packets based on GameTeX templates.
* `prod`: Convenience script to prod sheets and such with GameTeX. Uses [latexmk](https://www.ctan.org/pkg/latexmk/) to avoid unnecessary rebuilds.
* `book`: Typeset a packet as a foldable booklet.

### Booklet Production

* Enable plugins by adding {{{\input \gamepath/Gameki/lib/plugins.sty}}}
  before {{{%% Finishing up the setup for the class.}}} and
  put {{{\def\booksheets{}}}} in your LaTeX/*.cls file. 
* Put a cover image as Images/Cover.jpg or Images/Cover.png.
* To customize the font/formatting for the character on the cover, define
  \covernameformat{} in your LaTeX/*.cls file.

### Known Issues

* Text output depends on accurate conversion between TeX characters/tokens and
  Unicode. For unusual characters and formatting, this is not yet
  implemented.
* Several tools are powered by LuaTeX, which may have some slight differences
  from pdfTeX/XeTeX. Reported issues include:
  * File names for fonts can't have spaces in them.

### Installation

* Check out the Gameki repository to a Gameki directory next to your LaTeX
  directory.
* To use plugins like stickeritems typesetting, add the following before
  ```\ProcessOptions*\relax```
   in LaTeX/gametex.sty:
   ```
   \input \gamepath/Gameki/lib/plugins.sty
   ```

   You may want to comment out individual plugins in Gameki/lib/plugins.sty.
* Run commands as Gameki/bin/prod or whatever.