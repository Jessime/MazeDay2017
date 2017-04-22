# MazeDay2017

A collection of arcade style audio games for MazeDay 2017.

# Usage

To play these games, you have to have Python3 on your computer. If you don't have it installed, the easiest place to get it is from the [Anaconda distribution](https://www.continuum.io/downloads).

To install dependencies navigate to the repository and run:

```
pip install -r requirements.txt
```

Each mini-game is currently run independently. Please refer to the `README` of the game you're interested in for specific instructions.

# Games

Below is a list of games currently available

1. Speedy Typer - A type racing games where you must reach a certain Words-Per-Minute to make it to the next level.
2. Minesweeper - Modeled after the classic Windows puzzle game, see if you can clear the board of mines to win the game.
3. Plants vs. Zombies - A castle defense style game!
4. Binball - A pinball arcade game where flippers have been replaced by bins. How many points can you score?!
5.

# Contributing

Feel free to submit a pull request if you have a feature you would like added!

## Adding a game
Each game should be given it's own directory. For example, if you're interested in contributing a "Call of Duty" clone, the directory structure should be:
```

└── src/
    └── call_of_duty_game/
        ├── tests/
        ├── __init__.py
        ├── README.md
        └── call_of_duty.py

```
