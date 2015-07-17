#Kishan Rajasekhar, 57609613, Project 5, Section 12
#Game functions for othello and class

#othello game state class
class Othello:

    #attributes rows, columns, board
    def __init__(self, num_rows:int, num_columns:int, first_turn:str,
                 first_placement:str, version:int):
        self._num_rows = num_rows #even number between 4-16 (inclusive)
        self._num_columns = num_columns #even number between 4-16 (inclusive)
        self._turn = first_turn #either 'B' or 'W'
        #first_placement is either 'R' (right) or 'L' (left)
        self._board = self.make_new_board(first_placement)
        if version == 1:
            self._win_requirement = 'more'
        else:
            self._win_requirement = 'less'
        #pass_count increments if a player cannot place a piece.
        #if pass count is 2 (or greater), then the game is over
        self._pass_count = 0
        

    def make_new_board(self, placement:str) -> [[str]]:
        '''Creates a new board with the number of rows and columns specified
        and puts the four pieces in the center. The order depends on the placement
        of the first player (his top piece can either be on the right or the left,
        the bottom piece will always be diagonal to the top piece)'''
        result = []
        #the 2 center rows where the initial pieces are placed
        row_center2 = self._num_rows/2 
        row_center1 = row_center2 - 1
        #the first center column where the initial piece is placed
        col_center1 = (self._num_columns/2)-1 
        for row in range(self._num_rows):
            temp = []
            for col in range(self._num_columns):
                #if the row or columns is one of the top center spaces
                if (row == row_center1) and (col == col_center1): #top center cells
                    #if the first player is white and wants to place his top piece in the left
                    #OR the first player is black and wants to place his top piece in the right
                    if (self._turn == 'W') and (placement == 'L') or (self._turn == 'B') and (placement == 'R'):
                        temp.append('W')
                        temp.append('B')
                    else:
                        temp.append('B')
                        temp.append('W')
                #if row or column is one of the bottom center spaces
                elif(row == row_center2) and (col == col_center1): #bottom center cells
                    if self._turn == 'W' and (placement == 'L') or (self._turn == 'B') and (placement == 'R'):
                        temp.append('B') #opposite, since the order changes for the bottom center row
                        temp.append('W')
                    else:
                        temp.append('W')
                        temp.append('B')
                #if not one of the center spaces, append a . (signifying an empty space)
                else:
                    temp.append('.')
            result.append(temp)
        return result

    def get_num_rows(self) -> int:
        '''Returns the number of rows on the board.'''
        return self._num_rows

    def get_num_columns(self) -> int:
        '''Returns the number of columns on the board.'''
        return self._num_columns

    def num_pieces(self, color:str) -> int:
        '''Counts the number of pieces of the specified color ('W' or 'B')
        on the board.'''
        count = 0
        for row in self._board:
            for element in row:
                if element == color:
                    count += 1
        return count

    def change_turn(self) -> None:
        '''Changes the turn of the player (W -> B or B -> W)'''
        if self._turn == 'W':
            self._turn = 'B'
        else:
            self._turn = 'W'

    def display_board(self) -> None:
        '''Prints the board in a readable format'''
        #HEADER - column numbers
        print(end = '    ')
        for col in range(self._num_columns):
            print('{:<2}'.format(col+1), end = ' ')
        print()
        for row in range(self._num_rows):
            for col in range(self._num_columns):
                if col == 0:
                    print('{:>2}'.format(row+1), end = '  ') #display row numbers on the left
                print(self._board[row][col], end = '  ')
                if(col == self._num_columns -1):
                    print(row+1, end = '  ') #display row numbers on the right
            print()
        #FOOTER - column numbers
        print(end = '    ')
        for col in range(self._num_columns):
            print('{:<2}'.format(col+1), end = ' ')
        print()
        print('Score: Black {}         White {}'.format(self.num_pieces('B'), self.num_pieces('W')))

    def empty_locations(self) -> 'list of paired tuples(row, column)':
        '''Returns a list of empty locations (that does not have 'W' or
        'B')'''
        result = []
        for row in range(self._num_rows):
            for col in range(self._num_columns):
                if self._board[row][col] == '.':
                    tup = (row, col)
                    result.append(tup)
        return result

    def is_empty(self, row, column) -> bool:
        '''Checks whether the specified row and column is in an empty
        space on the board.'''
        return (row, column) in o.empty_locations()
        
    def locations_to_flip(self, row, col) -> [[str]]:
        '''Returns a list of locations in each direction of the specified
        location (the row and column) which can have
        its contents flipped (B->W or W->B) if the specified location is a
        valid location for a piece to be placed.'''
        if not ((row,col) in self.empty_locations()):
            return []
        result = []
        #a list of functions
        directions  = [north, south, east, west,
                       north_east, north_west,
                       south_east, south_west]
        for direction in directions:
            locs = direction(self._board,row,col)
            elements = self.location_elements(locs)
            if squish(elements, self._turn):
                result.append(locs)
        return result

    def add_piece(self,row,col)->None:
        '''Adds a piece to the board'''
        self._board[row][col] = self._turn

    def flip (self, locations_list:[[str]]) -> None:
        '''Flips the pieces in locations_list to match the same color
        as the piece placed in the specified row and column.'''
        if self._turn == 'W':
            opposite_color = 'B'
        else:
            opposite_color = 'W'
        for locations in locations_list:
            for coordinate in locations:
                row = coordinate[0]
                col = coordinate[1]
                #Must change elements using indexing
                if self._board[row][col] == opposite_color:
                    self._board[row][col] = self._turn
                else:
                    break

    def make_move_prompt(self) -> None:
        '''Prints out who's turn it is to make a move.'''
        if (self._turn == 'W'):
            print("The player with the WHITE pieces can now make a move.")
        else:
            print("The player with BLACK pieces can now make a move.")

    def no_possible_move(self)-> bool:
        '''Returns True if the player cannot make a move'''
        locs = self.empty_locations()
        if locs == []:
            return True
        for l in locs:
            if len(self.locations_to_flip(l[0],l[1])) > 0:
                return False
        return True

    def increment_pass_count(self) -> None:
        '''Increments the pass_count attribute of the game state.'''
        self._pass_count += 1

    def player_turn(self) -> str:
        '''Returns the color of the pieces depending on whose turn it is.'''
        if self._turn == 'B':
            return 'BLACK'
        return 'WHITE'

    class InvalidMoveError(Exception):
        '''Raised whenever an invalid move is made'''
        pass
    
    def make_move(self, row, column) -> None:
        '''Player adds piece at the specified location, and the pieces around
        that space gets flipped.'''
        locs = self.locations_to_flip(row,column)
        if len(locs) == 0: #if a piece cannot be placed in the specified row and column
            raise self.InvalidMoveError()
        self.add_piece(row,column)
        self.flip(locs)
        self.change_turn()
        self._pass_count = 0

    def is_winner(self) -> bool:
        '''Returns True if any more pieces cannot be placed on the board'''
        if self.num_pieces('B') == 0 or self.num_pieces('W') == 0:
            return True
        if self.empty_locations() == []: #no empty locations, all the space occupied
            return True
        if self._pass_count >= 2: #both players pass their turn
            return True
        return False
        #more conditions to check...

    def game_over_message(self) -> str:
        '''Prints out who wins the game, based on the version (one with the
        most pieces or one with the least pieces)'''
        if self.num_pieces('B') == self.num_pieces('W'):
            return("It's a draw!")
        elif self._win_requirement == 'more':
            message = "The player with the most pieces wins, so...\n"
            if self.num_pieces('B') > self.num_pieces('W'):
                message += "The player with the BLACK pieces wins!"
                return message
            else:
                message+= "The player with the WHITE pieces wins!"
                return message
        else:
            message = "The player with the least pieces wins, so...\n"
            if self.num_pieces('B') > self.num_pieces('W'):
                message += "The player with the WHITE pieces wins!"
                return message
            else:
                message += "The player with the BLACK pieces wins!"
                return message

    def location_elements(self, locs:'list of paired tuples') -> list:
        '''Returns a list of elements contained within the location
        (row, column).'''
        result = []
        for l in locs:
            result.append(self._board[l[0]][l[1]])
        return result

    def get_board(self)->[[str]]:
        '''Returns the list at its current game state'''
        return self._board

#'DIRECTION' functions for checking adjacent locations..........................

def direction(board:[list], row, col, row_increment, col_increment) -> 'list of pari tuples (row, column)':
    '''Returns a list of locations (row and col tuples) of the spaces in the
    board of the direction of row_increment, col_increment. This function will
    be used in the functions below.'''
    result = []
    # these limits (0 and len(board)) make sure that the index does not
    # go out of bounds
    row += row_increment
    col += col_increment
    while (0 <= row < len(board)) and (0<=col<len(board[0])):
        result.append((row,col))
        row += row_increment
        col += col_increment
    return result

def west(board:[list], row, column)-> 'list of pair tuples (row, column)':
    '''Returns all the locations left (or west of) the specified location
    and returns them in a list. The specified location should not be in the
    list.'''
    #Only need to decrement the column. The row is the same
    return direction(board, row, column, 0, -1)

def east(board:[list], row, column) -> 'list of pair tuples (row, column)':
    '''Returns all the locations right (or east of) the specified location
    and returns them in a list. The specified location should not be in the
    list.'''
    #Only need to increment the column. The row is the same
    return direction(board, row, column, 0, 1)

def north(board:[list],row,column)-> 'list of pair tuples (row, column)':
    '''Returns all the locations above (or north of) the specified location
    and returns them in a list. The specified location should not be in the
    list.'''
    #Only need to decrement the row. The column is the same
    return direction(board, row, column, -1, 0)

def south(board:[list],row,column)-> 'list of pair tuples (row, column)':
    '''Returns all the locations below (or south of) the specified location
    and returns them in a list. The specified location should not be in the
    list.'''
    #Only need to increment the row. The column is the same
    return direction(board, row, column, 1, 0)

def north_west(board:[list],row,column) -> 'list of pair tuples (row,column)':
    '''Returns all the locations on the upper left diagonal (north west)
    of the specified location.'''
    #Need to decrement both the row and the column
    return direction(board, row, column, -1, -1)

def north_east(board:[list],row,column) -> 'list of pair tuples (row,column)':
    '''Returns all the locations on the upper right diagonal (north east)
    of the specified location.'''
    #Need to decrement the row and increment the column
    return direction(board, row, column, -1, 1)

def south_west(board:[list],row,column) -> 'list of pair tuples (row,column)':
    '''Returns all the locations on the lower left diagonal (south west)
    of the specified location.'''
    #Need to increment the row and decrement the column
    return direction(board, row, column, 1, -1)

def south_east(board:[],row,column) -> 'list of pair tuples (row,column)':
    '''Returns all the locations on the lower right diagonal (south east)
    of the specified location.'''
    #Need to increment the row and the column
    return direction(board, row, column, 1, 1)


#game functions.................................................................
def ask_number(lower_limit:int, upper_limit:int, even_only:bool) -> int:
    '''Asks user for an integer (only even if specified) between the lower
    and and upper limit and returns it. This function could be used to
    set number of rows or number of columns.'''
    while True:
        try:
            number = int(input())
            if (number < lower_limit) or (number > upper_limit): #if the number is out of the range (4-16)
                print("Invalid. The number must be between {} and {} (inclusive).".format(lower_limit, upper_limit))
            elif (even_only and number%2 ==1): #if the number is odd
                    print("Invalid. The number must be an even number.")
            else:
                return number
        except ValueError: #occurs when user attempts to input a string, decimal, or fraction
            print("Invalid. Only input an integer.")

def choose_first_player() -> str:
    '''Asks user for which piece the  first player uses. Returns 'W' (White)
    or 'B' (black).'''
    while True:
        choice = input('''First Player: Input 'W' for white pieces
or 'B' for Black pieces.\n ''')
        if choice.upper().strip() == 'W' or choice.upper().strip() == 'B':
            return choice.upper().strip()
        else:
            print("Invalid Input\n")

def choose_placement() -> str:
    '''Asks the first player if he wants his top piece to be placed on the
    right or left. He inputs 'R' (right) or 'L' (Left)'''
    while True:
        choice = input('''Input 'R' to place your top center piece in the
right or input 'L' to place your top center piece to the left.\n''')
        if choice.upper().strip() == 'R' or choice.upper().strip() == 'L':
            return choice.upper().strip()
        else:
            print("Invalid Input\n")


def squish(l:list, element) -> bool:
    '''Returns True if the specified element ('B' or 'W') is in the list,
    such that there are other elements between the two identical elements (if
    the specified element were to be placed at the front of the list)
    hence, being 'squished' by those two elements. In Othello, two pieces have
    to be on both sides of the opposite piece in order for that move to be
    valid.'''
    l = [element] + l
    if len(l) >= 3:
        if l[0] == l[1] or l[1] == '.': #if the piece next to the element is the same or is empty
            return False
        for i in range(2,len(l)):
            if l[0] == l[i]: #now return True if the piece is the same as the element.
                return True
            if l[i] == '.': #if there is an empty space and the function did not return True yet
                return False
        return False
    else:
        return False

            


        
    
