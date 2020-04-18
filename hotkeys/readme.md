# HotKeys

## Purpose
If you are like me, you find yourself typing the same stuff over and over. HotKeys allows you to automate some of that typing by placing comments in a config.ini file and running main.py from the command line. If you name each one of your HotKeys logically, you cab simply type them in the command line when prompted. The output will be printed and copied to your clipboard. If there are phrases in a given comment that can be slightly different based on context, you can add brackets in your comment and you will be asked to replace each bracketed phrase before it is copied to your clipboard.  

The config.ini file is just an example. I use this process for my work at Western Governers University, but I can't share that that publicly.  

There are paid services that allow you to do this ([ShortKeys](https://www.shortkeys.com/)) but this is an example of a free application that anyone can install and use.  

## Requirements
- Python 3
- `pip install pyperclip`