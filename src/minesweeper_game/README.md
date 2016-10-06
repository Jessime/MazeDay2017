# Minesweeper

Can you figure out where the mines are hidden?

## About

This is an audio-game version of the standard minesweeper game.
Most resources are image heavy, but here are a couple sources that offer text explanations as well:

1. [Minesweeper Wikipedia page](https://en.wikipedia.org/wiki/Minesweeper_(video_game))
2. [Strategy](http://www.minesweeper.info/wiki/Strategy)
3. [More Strategy](http://computronium.org/minesweeper/index.html)

## Usage

Run:

`python minesweeper.py`

to launch straight into a game.

### Options

Flag | Full Flag | Default | Description
--- | --- | --- | ---
-po | --print_only | N/A | Set if you do not want to use sound-based sentences
-np | --no_printing | N/A | Set if you do not want the sentences printed to the console.

## Gameplay

* **Arrow Keys:** Move player around on board.
* **Space:** Flips active button if it is still hidden.
* **f:** Mark button with flag (or unmark).
* **m:** States player's current row and column.
* **b:** Shows the current state of the board. *(print only)*
* **a:** States how many unused flags you have, or how many bombs are remaining.
