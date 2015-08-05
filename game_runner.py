#Kishan Rajasekhar, 57609613, Project 5, Lab Section 12
import tkinter
import othello_game_logic2
import othello_board2
import othello_options

class start_game:
    def __init__(self):
        '''Initialized the game board.'''
        self._window = tkinter.Tk()
        self._play_button = tkinter.Button(master = self._window,
                                     text = "Play!",
                                    command = self.play_game)
        self._play_button.grid(row=0, column=1)
        self._quit_button = tkinter.Button(master=self._window,
                                           text = "Quit",
                                           command = self.quit_game)
        self._quit_button.grid(row=1, column=1)
        self.play = True

    def play_game(self):
        options = othello_options.Othello_options()
        options.start()
        choices = options.return_choices()
        options.end()
        game_state = othello_game_logic2.Othello(choices[1],choices[2],
                                                 choices[0],choices[3],
                                                 choices[4])
        othello_board2.Othello_board(game_state).start()

    def quit_game(self):
        self.play=False
         
    def start(self):
        self._window.mainloop()

    def end(self):
        self._window.destroy()
 


if __name__ =='__main__':
    options = othello_options.Othello_options()
    options.start()
    choices = options.return_choices()
    options.end()
    game_state = othello_game_logic2.Othello(choices[1],choices[2],
                                             choices[0],choices[3],
                                             choices[4])
    othello_board2.Othello_board(game_state).start()





