# Speedy Typer

How fast do you think you can type?

## About

Speedy Typer is a straightforward typing game to test how quickly you can type sentences. 

## Usage

Just running:

`python typing.py`

will launch straight into a game.

### Options

Flag | Full Flag | Default | Description
--- | --- | --- | ---
-n | --num_lvls | 5 | The number of levels you want to play
-v | --verbose | N/A | Set to print information to help with debugging 
-po | --print_only | N/A | Set if you do not want to use sound-based sentences
-np | --no_printing | N/A | Set if you do not want the sentences printed to the console.

A couple of interesting notes:

1. `--verbose` will print the aligned sentences so you can see where you made mistakes.
2. The sentences used for `--print-only` are different than the spoken sentences (if you're looking for variety.)

## Gameplay

* After starting the game, you'll be prompted to start each level. 
* Time starts as soon as you accept the prompt, and stops when the level is over. Sentences will be given one at a time, but the next sentence will start as soon as you submit the current sentence.
* Submit your sentence by hitting enter.
* The number of sentences given each round is equal to the level number. 
* Your allowed minimum Adjusted Words Per Minute will increase each level.
* Your Adjusted Words Per Minute is your Raw Words Per Minute corrected for accuracy.
* Sentences are all lowercase, but do contain proper punctuation. Be careful there.  

