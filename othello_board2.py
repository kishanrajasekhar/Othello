#Kishan Rajasekhar, 57609613, Project 5, Lab Section 12
#othello board

import tkinter
import othello_game_logic2

test = othello_game_logic2.Othello(14, 14, 'W','L', 1)

def draw_rectangle(canvas, width:int,height:int, x:int ,y:int, color:str)->None:
    '''Draws a rectangle only using the the coordinates of the
    top left corner.'''
    canvas.create_rectangle(x,y, x+width, y+height, fill = color)

def draw_oval(canvas, width:int,height:int, x:int ,y:int, color:str)->None:
    '''Draws a oval only using the the coordinates of the
    top left corner of the bounding box.'''
    canvas.create_oval(x,y, x+width, y+height, fill = color)

class Othello_space:
    '''An othello space can have a piece or be empty'''

    def __init__(self, canvas, x_coor:int, y_coor:int, color:str):
        '''Initialized the space with data.'''
        self._master = canvas
        self._x = x=coor
        self._y = y_coor
        self._color = color

class Othello_board:

    def __init__(self, game_state) -> None:
        '''Initializes the board, canvas and labels (turn, scores, and title)'''
        #Storing game state date into variables
        self._game_state = game_state
        self._board = game_state.get_board()
        self._num_row = len(self._board)
        self._num_col = len(self._board[0])
        #setting up tkinter widgets
        self._root_window = tkinter.Tk()
        #default height and width of the window
        self._height = 500 
        self._width = 500
        self._background = 'orange'
        #LABELS AND CANVAS
        #Title
        self._title = tkinter.Label(master = self._root_window,
            text = "OTHELLO!")
        self._title.grid(row=0, column=0)
        #Who's turn it is
        self._turn = tkinter.Label(master = self._root_window,
                                   text = self._game_state.player_turn())
        self._turn.grid(row=1,column=0)
        #The game board (Canvas)
        self._canvas = tkinter.Canvas(
            master = self._root_window, width = self._width, height = self._height,
            background = self._background)
        self._canvas.grid(row=2, column=0,
                         sticky = tkinter.N + tkinter.S + tkinter.E + tkinter.W,
                          columnspan = 2) 
        #The score of the players
        self._black_score = tkinter.Label(master = self._root_window,
            text = "Black: " + str(self._game_state.num_pieces('B')))
        self._black_score.grid(row=3,column=0,
                               sticky = tkinter.W)

        self._white_score = tkinter.Label(master = self._root_window,
            text = "White: " + str(self._game_state.num_pieces('W')))
        self._white_score.grid(row=3,column=1,
                               sticky = tkinter.W)
        #EXTRA - MENU!
        self._menu = tkinter.Menubutton(master = self._root_window,
                             text = "OPTIONS")
        self._menu.grid()
        #ROW AND COLUMN CONFIGURATIONS
        self._root_window.rowconfigure(0, weight = 0)
        self._root_window.rowconfigure(1, weight = 0)
        self._root_window.rowconfigure(2,weight=1)
        self._root_window.rowconfigure(3,weight=0)
        self._root_window.columnconfigure(0, weight = 1)
        #call the update board method if the window is resized
        self._canvas.bind('<Configure>', self.update_board)
        #call the add_piece method if the mouse is clicked
        self._canvas.bind('<Button-1>', self.make_move)
        
    def update_board(self, event) -> None:
        '''Updates the board whenever it is resize or whenever a move is made
        (like who's turn it is or score)'''
        self._title['text'] = 'OTHELLO'
        #Changing the canvas
        self._canvas.delete(tkinter.ALL)
        self._height = self._canvas.winfo_height() #assigning them to shorter attrubute names for convenience
        self._width = self._canvas.winfo_width()
        self.draw_grid()
        #Checking if the game is over
        if self._game_state.is_winner():
            self._title['text'] = 'GAME OVER!'
            self._turn['text'] = self._game_state.game_over_message()
            self._black_score['text'] = "Black: " + str(self._game_state.num_pieces('B'))
            self._white_score['text'] = "White: " + str(self._game_state.num_pieces('W'))
            #disable the window..
            self._root_window.quit()
            return
        #Check if there is a possible move for the next player
        if self._game_state.no_possible_move():
            self._title['text'] = str(self._game_state.player_turn()) + " PASSES."
            self._game_state.change_turn()
            self._game_state.increment_pass_count() #if more than 2 passes, game over
        #Updating whose turn it is.
        self._turn['text'] = self._game_state.player_turn()
        #Updating the score
        self._black_score['text'] = "Black: " + str(self._game_state.num_pieces('B'))
        self._white_score['text'] = "White: " + str(self._game_state.num_pieces('W'))
    
    def draw_grid(self) -> None:
        '''Draws the grid using the draw_rectange and draw_oval methods,
        which are defined above the class.'''
        #side length determines the length of each square everytime the canvas is resized
        square_height = self._height//self._num_row
        square_width = self._width//self._num_col
        for x in range(len(self._board[0])): #traversing through columns
            x2 = x*square_width #scale depending on the size of the board
            for y in range(len(self._board)): #traversing throught rows
                y2 = y*square_height
                draw_rectangle(self._canvas,square_width,square_height, x2,y2, 'orange')
                if self._game_state.locations_to_flip(y,x) != []:
                    draw_rectangle(self._canvas,square_width,square_height, x2,y2, 'red')
                if self._board[y][x] == 'W': #have to switch y and x because 2-d lists search the rows first and then the columns
                    draw_oval(self._canvas,square_width,square_height, x2,y2, 'white')
                elif self._board[y][x] =='B':
                    draw_oval(self._canvas,square_width,square_height, x2,y2, 'black')

    def make_move(self, event) -> None:
        '''Adds piece to the game_state board which will then be
        translated onto the canvas.'''
        #convert canvas coordinates from mouse click into 2d array coordinates
        col = event.x//(self._width//self._num_col)
        row = event.y//(self._height//self._num_row)
        try:
            self._game_state.make_move(row,col) #2-d list goes through rows first...
            self._board = self._game_state.get_board() #updating self._board
        except self._game_state.InvalidMoveError:
            return #ignore the any clicks on invalid spaces
        self.update_board(event)
        
    def start(self) -> None:
        '''Calls the mainloop'''
        self._root_window.mainloop()

    def end(self) -> None:
        '''Closes the window'''
        self._root_window.destroy()


if __name__ == '__main__':
    o = Othello_board(test)
    o.start()
    
            

   
