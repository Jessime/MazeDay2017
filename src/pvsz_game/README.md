# Definitely Not Plants vs. Zombies

This is an audio clone of the popular castle defense game Plants vs. Zombies&trade;

## About

Waves of hungry zombies are coming to attack your house. Can you build your line of defense well enough to fend them off? Different plants will have different abilities, and it's up to you to figure out which to grow to protect yourself from almost certain doom. 

## Usage

Just running:

`python plants_vs_zombies.py`

will launch straight into a game.

### Options

There are currently no options

## Gameplay

This is a fairly complicated game, so there are several key aspects to understand about the gameplay.

### Environment

The game is played on a board with 5x10 board. You're attempting to defend the left side of the board, while zombies flood in from the right. 

### User Actions

* Move around the board using the arrow keys. 
  * If you move to an occupied position, the appropriate sounds will play based on the occupants of the position.
  * Changing rows while a zombie is anywhere it that row, causes their sound will play. The louder the sound, the nearer the zombie. 
* To plant a plant is an empty square, press a number key while positioned at the square. (See below for Plant types)
  * You must also have enough gold to perform this action.
* The space bar can be used to collect suns.
* 'b' (i.e. board) will give general information about the board.
* 'm' (i.e. me) will give general information about you.
* 'esc' will quit the game.

### Plants

Here's a list of plants you can use, their price, and a little bit about what they do. Their numerical order corresponds to the keys used to place the plant in game.

1. Sunflowers [50g] are key to maintaining a steady income of gold. They steadily produces Suns which can be collected and converted into gold. 
2. Peashooters [100g] are the most basic form of defense plants. They slowly shoot peas at the zombies.
3. Doubleshooters [200g] are just like Peashooters, but fire twice as fast.
4. Icepeas [175g] have the ability to drastically slow a Zombies progress.
 
### Zombies

While zombies come in all shapes and sizes, they all conform to a few rules:

* Zombies are guaranteed not to switch rows/lanes.
* They start at the right of the board, and attempt to cross through the plants to the left side of the board.
* They must pause to destroy any plants in their way.

### Winning (or maybe losing)

This is a survival game. If you can defeat the last zombie, you win. On the other hand, if a Zombie makes it through all of your plant defenses and into your house, you lose the game.

