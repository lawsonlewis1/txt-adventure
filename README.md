# txt-adventure

Version 1.00  

A shell for text adventure games that is designed to be simple and flexible  
but allow for some advanced functionality.

## Status

Stable.

Future updates:  

- GUI interface
- Ability to branch storyline
- Space for images/artwork

## Features

__Character Stats__  
Easily create, set, and modify custom player stats throughout the game.

__Saveable__  
The player can save their progress at any time and easily pick up
where they left off.

__Choices__  
Offer the player a yes/no choice with a unique outcome for each response.

__Puzzles__  
Create a riddle/puzzle for the player with consequences/rewards.
Easily set the number of attempts and optionally provide hints.

## Installation

The project is composed of the python script 'txt_game.py', which is the functional shell of the game, and the 'Dialogue.txt' file which contains the games dialogue and player rewards.

To get it to run download both of these files, put them in the same directory and then run the txt_game.py file as a python script by typing the following command at the prompt.

    python txt_game.py

The game is written in python 3.6, im not sure if previous python 3 distributions will work but they probably will, python 2 will not work.

Instructions on how to change the games dialogue is contained in the 'Dialogue.txt' file, The process is pretty straight forward but must be followed exactly.