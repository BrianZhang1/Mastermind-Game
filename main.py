'''
PROGRAM STRUCTURE OVERVIEW
=============================
main.py is the program entrypoint. It simply creates a GameHandler instance.

The GameHandler class, located in game_handler.py, controls higher-level functions such
as starting and restarting the game. It starts the game by creating a MastermindGame instance.

The MastermindGame class, located in mastermind_game.py, handles all game functions. It includes
the game GUI, event handling, etc.
'''


import tkinter as tk

from game_handler import GameHandler


def main():
    '''Program Entrypoint.'''

    root = tk.Tk()
    game_handler = GameHandler(root)
    root.mainloop()


if __name__ == '__main__':
    # Run the main function if this python script is being run directly (not imported as module).
    main()
