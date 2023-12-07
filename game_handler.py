from mastermind_game import MastermindGame


class GameHandler:
    '''Controls higher-level functions such as starting and restarting the game.'''

    def __init__(self, root):
        self.root = root
        root.title('Mastermind')
        self.game = MastermindGame(self.root, self.play_again)


    def play_again(self):
        '''Restarts the game by deleting the old game instance and instantiating a new one.'''

        self.game.frame.pack_forget()
        del self.game
        self.game = MastermindGame(self.root, self.play_again)