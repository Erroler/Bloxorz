# Bloxorz

**Bloxorz** (also known as *Roll the Block*) is a challenging puzzle game. The objective is to reach the final square with a two-story block by rolling it vertically and horizontally without having it fall off the edge of the map. See [here](https://www.youtube.com/watch?v=1LaoH4I4iNQ&feature=youtu.be) a visual demonstration of the mechanics described.


The original version of the game developed by Damien Clarke in 2007 is no longer available on the internet but there are several modern remakes: 

* [Android (1)](https://play.google.com/store/apps/details?id=com.superpow.bloxorz)
* [Android (2)](https://play.google.com/store/apps/details?id=com.albinoblacksheep.bloxorzgame)
* [iOS](https://apps.apple.com/us/app/bloxorz-roll-the-block/id1409476339)
* [Browser](https://www.miniclip.com/games/bloxorz)

**This repository contains a remake of the game in Python.**

**This project was developed as an academic project for an Artificial Intelligence college subject**. As such, several graph search algorithms have been implemented, namely: Depth-first Search, Breadth-First Search, Uniform cost Search, Best first Search and A*.

You can simply play the game or see the performance of each algorithm on a game level (Solution cost, Nodes explored, Time solved (ms)).

*Project finished on April 2019.*

## Screenshots

* [Main Menu](https://i.imgur.com/0m0eZ2J.png)
* [Playing a Level (GIF)](https://i.imgur.com/NF2r863.gif)
* [Viewing algorithm performance (GIF)](https://i.imgur.com/eIpoJuH.gif)

## Setup

Requires Python 3.

Steps:

> 1. Clone this repository and execute `pip install -r requirements.txt` to install dependencies (namely NumPy, PyGame and PyGameMenu).
> 2. Execute `python main.py` to play the game.

**Use the keyboard to play the game (Arrows and Enter). Mouse is not supported.**

## Note

> Part of the code was adapted from the [official repository of the book "*Artificial Intelligence - A Modern Approach*"](https://github.com/aimacode/aima-python).
