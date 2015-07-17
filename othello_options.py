#Kishan Rajasekhar, 57609613, Project 5, Lab Section 12
#othello gui

import tkinter

class Othello_options:

    def __init__(self):
        self._window = tkinter.Tk()
        #This disables the exit button. The user has to pick the options.
        self._window.protocol("WM_DELETE_WINDOW", self.do_nothing)
        self._black_or_white = tkinter.StringVar()
        self._row_number = tkinter.IntVar()
        self._col_number = tkinter.IntVar()
        self._right_or_left = tkinter.StringVar()
        self._more_or_less = tkinter.IntVar()
        self._setup()

    def do_nothing(event):
        pass

    def _setup(self):
        tkinter.Label(master = self._window,
                      text = "Select the color which moves first.").grid(row = 1, column = 0)
        #black or white?
        tkinter.Radiobutton(master = self._window,
                            text = "White", variable = self._black_or_white,
                            value = 'W').grid(row = 1,column = 1)
        tkinter.Radiobutton(master = self._window,
            text = "Black", variable = self._black_or_white,
            value = 'B').grid(row = 1,column = 2)

        #number of rows
        label2 = tkinter.Label(master = self._window,
                               text = 'How many rows?')
        label2.grid(row = 3, column = 0)
        iteration_count = 0
        for i in range (4,17,2): #4-16
            iteration_count += 1
            tkinter.Radiobutton(master = self._window, text = str(i),
                                variable = self._row_number,
                                value = i).grid(row = 3,
                                                column = iteration_count)
        #number of columns
        column_label = tkinter.Label(master = self._window,
                               text = 'How many columns?')
        column_label.grid(row = 4, column = 0)
        iteration_count = 0
        button_group_column = tkinter.IntVar()
        for i in range (4,17,2): #4-16
            iteration_count += 1
            tkinter.Radiobutton(master = self._window, text = str(i),
                                variable = self._col_number,
                                value = i).grid(row = 4,
                                                column = iteration_count)

        #left or right?
        left_right_label = tkinter.Label(master = self._window, text = "Left or Right?")
        left_right_label.grid(row = 5, column = 0)
        left = tkinter.Radiobutton(master = self._window,
                            text = "Left", variable = self._right_or_left,
                            value = 'L').grid(row = 5,column = 1)
        tkinter.Radiobutton(master = self._window,
            text = "Right", variable = self._right_or_left,
            value = 'R').grid(row = 5,column = 2)

        #winner has more pieces or less pieces?
        tkinter.Label(master = self._window,
                      text = "More Pieces or Less Pieces?").grid(row = 6, column = 0)
        left = tkinter.Radiobutton(master = self._window, text = "More pieces",
                            variable = self._more_or_less,
                            value = 1).grid(row=6,column=1)
        tkinter.Radiobutton(master = self._window, text = "Less pieces",
                            variable = self._more_or_less,
                            value = 2).grid(row=6,column=2)
        #The button to press after the player picked all the options
        self._submit = tkinter.Button(master=self._window,
                                      text = "Pick all your options first. Then click me.",
                                      command = self.return_choices)
        self._submit.grid(row = 7, column=0)
        self._window.bind('<Button-1>', self.enable_button)
        

    def choices_selected(self):
        '''Enables the button after all the choices have been selected'''
        if (self._black_or_white.get() != '' and
            self._row_number.get() !=0 and
            self._col_number.get() !=0 and
            self._right_or_left.get() != '' and
            self._more_or_less.get() != 0):
            return True
        else:
            return False

    def enable_button(self, event):
        if self.choices_selected():
            #activate button
            self._submit["text"] = "Let's Play!"
##            self._submit["command"] == self.print_choices
            #unbind event
            self._window.unbind(self.enable_button)
            
    def return_choices(self):
        if self.choices_selected():
            #stops the mainloop and returns choices
            self._window.quit()
            return(self._black_or_white.get(),
                    self._row_number.get(),
                    self._col_number.get(),
                    self._right_or_left.get(),
                    self._more_or_less.get())
                    

    def print_choices(self):
        if self.choices_selected():
            self._window.quit()
            print(self._black_or_white.get())
            print(self._row_number.get())
            print(self._col_number.get())
            print(self._right_or_left.get())
            print(self._more_or_less.get())
            print()

    def start(self):
        self._window.mainloop()

    def end(self):
        self._window.destroy()


if __name__=='__main__':
    o = Othello_options()
    #o.setup()
    o.start()
    #after window closes
    choices = o.return_choices()
    o.end()
    print(choices)

   
