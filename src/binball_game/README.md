# Binball

This is a pinball game that isn't modeled off of Microsoft's *Space Cadet* game.

## About

Score as many points as possible by keeping the ball in play and scoring special bonuses. In binball, the ball eventually falls into a bin. When this occurs, a note sounds, and the player has a small amount of time to hit the corresponding key to set the ball back into play. If the player fails to do so, the ball falls through the bin and a life is lost.

## Usage

Run:

```
python binball.py
```

to start a new game.

### Options

Flag | Full Flag | Default | Description
--- | --- | --- | ---
-ns | --no_sound | False | Set to turn off all audio
-nv | --no_video | False | Set to turn off all video

## Gameplay

Gameplay is fairly straightforward. After launching the ball, your objective is to score as many points as possible by keeping the ball alive.

### Keys

Here is a table of all keys, and their effects:

Flag | Full Flag |
--- | --- |
d | activates left most bin
f | activates inner left bin
j | activates inner right bin
k | activates right most bin
esc | quits game
t | tests noises for bins. Bin key will be said, then noise will sound
b | number of balls left before game is over
p | pause game

### Components

The ball can interact with a variety of components. In certain cases, interacting with combos of components will result in bonus points. The basic components are listed below.

#### Segment

These are basic straight lines. They're worth very few points, and generally don't do anything special. Their noise is __.mp3

#### Particle

Round bumpers are almost as common as segments, and also don't do anything special. Their noise is __.mp3

#### Spinner

These rectangles are hard to get to, as they're generally protected by tunnels of segments. You'll know if you hit a spinner because it'll freeze the ball for a while while it's spinning. This freeze is worth it, since it comes with a large score reward. Their noise is __.mp3

#### Tubes

Tubes are, as the name may imply, components that send your ball to a different location. Maybe you'll get lucky and score a bunch of points this way!

#### Coins

Coins have no other effect than giving you points! If you collect enough coins, you'll get extra points!

## Winning

In this game, you win by having fun. :)

Actually, you have only three lives and no way to gain extra lives. So do your best to have quick reflexes! The game is over after you spend your three ball lives.
