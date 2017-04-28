# Binball

This is a pinball game that isn't modeled off of Microsoft's *Space Cadet* game.

## About

Score as many points as possible by keeping the ball in play and collecting as many coins as you can. In binball, the ball eventually falls into a bin. When this occurs, a note sounds, and the player has a small amount of time to hit the corresponding key to set the ball back into play. If the player fails to do so, the ball falls through the bin and a life is lost.

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

Keys | Description |
--- | --- |
space | launches the ball (hold for power)
d | activates left most bin
f | activates inner left bin
j | activates inner right bin
k | activates right most bin
esc | quits game
t | tests noises for bins. Bin key will be said, then noise will sound
b | number of balls left before game is over
p | pause game

### Components

The ball can interact with a variety of components. The basic components are listed below.

#### Bins

The ball will fall into bins and a corresponding note will play to indicate to the player which key to hit. These bins are located similarly to where flippers would be located if you were playing normal pinball. If you hit the wrong key, you will not be able to correct yourself! The longer you wait after the note plays, the further left the ball will be angled. Wait too long though, and you will lose a life! The bin's noises are (from left to right) note1.mp3, note2.mp3, note3.mp3, and note4.mp3.

#### Segment

These are basic straight lines. They're worth very few points, and generally don't do anything special. Their noise is seg2.mp3

#### Platforms

These are the horizontally moving segments. The ball can only interact with the top platform, and when it does, the ball will teleport to the bottom platform's position and drop down below.

#### Particle

Round bumpers are almost as common as segments, and also don't do anything special. Their noise is jump.mp3

#### Spinner

These rectangles are hard to get to, as they're generally protected by tunnels of segments. You'll know if you hit a spinner because it'll freeze the ball for awhile while it's spinning. This freeze is worth it, since it comes with a large score reward. Their noise is spin.mp3

#### CurveBall

These circles are subclasses of Particle, but they have centripetal force associated with it that curves the ball's trajectory. For each frame the ball is in a CurveBall, you will get a small point reward. Their noise is chimes.mp3

#### Tubes

Tubes are, as the name may imply, components that send your ball to a different location. Maybe you'll get lucky and score a bunch of points this way! Their noise is suck.mp3

#### Coins

Coins have no other effect than giving you points! Some hard to reach coins are worth more than normal coins. If you collect all of the coins, they reset and be double the amount! Their noise is coins.mp3

### Winning

In this game, you win by having fun. :)

Actually, you have only three lives and no way to gain extra lives. So do your best to have quick reflexes! The game is over after you spend your three ball lives.
