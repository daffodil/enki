---
layout: default
title: Install mksv3 from sources
---

# Instal from sources

## Dependencies
1. Python 2. Tested on v2.6.6 and v2.7.2
2. PyQt4
3. QScintilla 2 and Python bindings. v2.4.1 or newer
4. pyparsing
5. pygments. (Optional, for highlighting Scheme files)
6. markdown. (Optional, for Markdown preview)
#### Install on Debian and Debian based

   `apt-get install python python-qt4 python-qscintilla2 python-pyparsing python-pygments python-markdown`
#### Install on other Unixes
   Find and install listed packages with your package manager
#### Install on other systems

* [http://python.org/download](http://python.org/download)
* [http://www.riverbankcomputing.co.uk/software/pyqt/download](http://www.riverbankcomputing.co.uk/software/pyqt/download)
* [http://www.riverbankcomputing.co.uk/software/qscintilla/download](http://www.riverbankcomputing.co.uk/software/qscintilla/download)
* [http://pyparsing.wikispaces.com/Download+and+Installation](http://pyparsing.wikispaces.com/Download+and+Installation)
* [http://pygments.org/download](http://pygments.org/download) (Optional, for highlighting Scheme files)
* [http://packages.python.org/Markdown/install.html](http://packages.python.org/Markdown/install.html) (Optional, for Markdown preview)

## Get the sources
####Git
`git clone git://github.com/hlamer/mksv3.git`
####Source archive
Download from [github tags](https://github.com/hlamer/mksv3/tags) and unpack

## Setup
    
`./setup.py instal`

## Enjoy
Don't forget to send a bug report, if you are having some problems