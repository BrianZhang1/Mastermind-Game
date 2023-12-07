import tkinter as tk    # create gui.
from tkinter import messagebox
import random           # generate secret code.
import time             # to track game lengths.


class MastermindGame:
    '''
    Handles all game functions, including the GUI, event handling, code generation,
    submission evaluation, etc.
    '''


    def __init__(self, root, play_again):

        # Constant attributes.
        self.ROWS = 15       # total rows in the Mastermind game.
        self.COLUMNS = 4     # total columns in the Mastermind game.
        self.COLORS = ['red', 'blue', 'pink', 'yellow', 'green', 'cyan']     # Available colors.

        # Core attributes.
        self.root = root
        self.play_again = play_again    # a callback function to restart the game.
        self.current_row = None      # the row of buttons that is currently available to the user.
        self.secret_code = None     # secret code to be guessed will be generated on game start.
        self.current_color = None   # the color selected by the user from the color palette.
        self.start_time = None      # tracks when the game started (time).

        # a pixel image allows dimensions of certain widgets to be scaled by pixels.
        self.PIXEL_IMG = tk.PhotoImage(width=1, height=1)    

        self.initialize_gui()


    def initialize_gui(self):
        '''
        Initially creates and displays tkinter widgets.

        Widget Hierarchy
        ====================================
        self.frame
        |   self.logo_label
        |   self.palette_frame
            |   self.palette_label
        |   |   [self.palette_buttons]
        |   |   self.current_color_label
        |   self.play_area_frame
        |   |   [self.button_list]
        |   |   [self.feedback_label_list]
        |   self.control_panel_frame
        |   |   self.start_button
        |   |   self.submit_button
        |   |   self.quit_button
        |   self.instructional_label
        '''

        # Frame that encapsulates this GUI
        self.frame = tk.Frame(self.root)
        self.frame.pack()

        # LOGO
        try:
            logo_image = tk.PhotoImage(file='logo.png')
            self.logo_label = tk.Label(self.frame, image=logo_image)
            self.logo_label.image = logo_image
            self.logo_label.pack(padx=20)
        except tk.TclError:
            print('ERROR: Logo image file could not be found. Continuing game without logo.')

        # COLOR PALETTE
        self.palette_frame = tk.Frame(self.frame)
        self.palette_frame.pack(pady=5)
        self.palette_label = tk.Label(self.palette_frame, text='Color Palette', font=('Helvetica', 10, 'bold'))
        self.palette_label.grid(row=0, column=0, columnspan=len(self.COLORS))
        self.palette_buttons = []
        self.current_color = self.COLORS[0]
        for i, color in enumerate(self.COLORS):
            color = self.COLORS[i]
            button = tk.Button(self.palette_frame, background=color, width=2, command=lambda color=color: self.set_color(color))
            button.grid(row=1, column=i, padx=3)
            self.palette_buttons.append(button)
        self.current_color_label = tk.Label(self.palette_frame, text=f'Selected color: {self.current_color}')
        self.current_color_label.grid(row=2, column=0, columnspan=len(self.COLORS))

        # PLAY AREA BUTTON/LABEL GRID
        self.play_area_frame = tk.Frame(self.frame)
        self.play_area_frame.pack(pady=5)
        self.button_list = []   # contains all the buttons in the play area.
        self.feedback_label_list = []   # contains tuples of 4 labels whose color can be changed
                                        #   to give feedback on submissions.
        for row in range(self.ROWS):
            for col in range(self.COLUMNS):
                button = tk.Button(self.play_area_frame, 
                                   command= lambda row=row, col=col: self.update_button_color(row, col),
                                   background='gray',
                                   image=self.PIXEL_IMG,
                                   width=20,
                                   height=20,
                                   state=tk.DISABLED)
                button.grid(row=row, column=col, padx=1, pady=1)
                self.button_list.append(button)
            # Create a feedback area for each row, which is four labels wrapped by a frame..
            feedback_frame = tk.Frame(self.play_area_frame)
            feedback_frame.grid(row=row, column=self.COLUMNS, padx=5)
            feedback_labels = []
            for i in range(4):
                feedback_label = tk.Label(feedback_frame, image=self.PIXEL_IMG, background='black', height=6, width=6)
                feedback_label.grid(row=i//2, column=i%2, padx=1, pady=1)
                feedback_labels.append(feedback_label)
            self.feedback_label_list.append(tuple(feedback_labels))


        # CONTROL PANEL
        self.control_panel_frame = tk.Frame(self.frame)
        self.control_panel_frame.pack(pady=5)
        self.start_button = tk.Button(self.control_panel_frame, text='START', font=('Helvetica', 12, 'bold'), command=self.start_game)
        self.start_button.pack(side='left', padx=8)
        self.submit_button = tk.Button(self.control_panel_frame, text='SUBMIT', font=('Helvetica', 12, 'bold'), state=tk.DISABLED, command=self.handle_submit)
        self.submit_button.pack(side='left', padx=8)
        self.quit_button = tk.Button(self.control_panel_frame, text='QUIT', font=('Helvetica', 12, 'bold'), command=self.root.destroy)
        self.quit_button.pack(side='left', padx=8)

        # INSTRUCTIONAL LABEL
        self.instructional_label = tk.Label(self.frame, text='Click START to begin.', font=('Helvetica', 10, 'bold'))
        self.instructional_label.pack(pady=5)

    

    def start_game(self):
        '''Starts the game.'''

        # Deactivate start button and activate submit button.
        self.start_button.configure(state=tk.DISABLED)
        self.submit_button.configure(state=tk.ACTIVE)

        # Generate secret code.
        self.secret_code = []
        for i in range(self.COLUMNS):
            color = random.choice(self.COLORS)
            self.secret_code.append(color)
            
        # Activate the first row of buttons.
        self.increment_current_row()

        # Update instructional text.
        self.instructional_label.configure(text='Select four (4) colors.')

        # Set game start time.
        self.start_time = time.time()


    def handle_submit(self):
        '''Handles a click on the submit button.'''

        # Isolate the buttons in the submitted row.
        actual_row = self.ROWS - 1 - self.current_row   # the actual row in the list (top to bottom)
        start_index = actual_row*self.COLUMNS
        end_index = (actual_row+1)*self.COLUMNS
        submitted_button_row = self.button_list[start_index:end_index]
        
        # Get the submitted colors.
        submitted_colors = [button['background'] for button in submitted_button_row]

        # Validate submission by ensuring four colors have been selected.
        for color in submitted_colors:
            if color not in self.COLORS:
                messagebox.showerror('Invalid submission.', 'You must select four (4) colors before selecting SUBMIT!')
                return

        # Evaluate the submission.
        correct_color_count = 0
        correct_location_color_count = 0
        correct_color_tracker = [False for i in range(self.COLUMNS)]   # a parallel list that tracks which colors
                                                            #   correct to avoid double counting.
        remaining_colors = self.secret_code[:]  # a copy of the submitted_colors to track which have been counted
                                                # to avoid double counting.
        for i in range(len(submitted_colors)):
            if submitted_colors[i] == self.secret_code[i]:
                correct_color_count += 1
                try:
                    # attempt to find the color in the remaining colors and remove it.
                    correct_color_index = remaining_colors.index(submitted_colors[i])
                    remaining_colors.pop(correct_color_index)
                    # update tracker to indicate correct color at this index
                    correct_color_tracker[i] = True
                except ValueError:
                    # Error: a color that should still be remaining isn't remaining.
                    print('Something has gone wrong in evaluating the submission.')
        # second for loop pass to check for correct colors in incorrect places.
        for i in range(len(submitted_colors)):
            if correct_color_tracker[i]:
                continue
            elif submitted_colors[i] in remaining_colors:
                correct_location_color_count += 1
                try:
                    # attempt to find the color in the remaining colors and remove it.
                    correct_color_index = remaining_colors.index(submitted_colors[i])
                    remaining_colors.pop(correct_color_index)
                except ValueError:
                    # Error: a color that should still be remaining isn't remaining.
                    print('Something has gone wrong in evaluating the submission.')

        # Update instructional label to give feedback.
        self.instructional_label.configure(text=f'{correct_location_color_count} color(s) correct.\n{correct_color_count} color(s) in the correct location.')

        # Check if user has won (handled after the feedback labels/pegs are updated)
        has_won = True if correct_color_count == 4 else False

        # Get tuple of feedback labels (pegs).
        feedback_labels = self.feedback_label_list[actual_row]

        # Update feedback grid to give feedback on submission
        current_label = 0   # iterate through labels (pegs) and update colors.
        while correct_color_count > 0:
            feedback_labels[current_label].configure(background='red')
            correct_color_count -= 1
            current_label += 1

        while correct_location_color_count > 0:
            feedback_labels[current_label].configure(background='white')
            correct_location_color_count -= 1
            current_label += 1

        # Handle user win if applicable.
        if has_won:
            self.deactivate_current_row()
            self.submit_button.configure(state=tk.DISABLED)
            play_time = int(time.time() - self.start_time)
            messagebox.showinfo('You win!', f'Congratulations... you cracked the code!\nIt took you {self.current_row+1} attempt(s).\nYou finished in {play_time} seconds.')
            play_again = messagebox.askyesno('Play again?', 'Would you like to play again?')
            if play_again:
                self.play_again()
        # Handle user loss if applicable.
        elif self.current_row == self.ROWS-1:
            self.deactivate_current_row()
            self.submit_button.configure(state=tk.DISABLED)
            messagebox.showwarning('You lose!', f'GAME OVER!\nYou failed to crack the code!\n\nThe code was {self.secret_code[0]}, {self.secret_code[1]}, {self.secret_code[2]}, {self.secret_code[3]}.')
            play_again = messagebox.askyesno('Play again?', 'Would you like to play again?')
            if play_again:
                self.play_again()
        else:
            # Continue game as normal by incrementing current row.
            self.increment_current_row()


    def increment_current_row(self):
        '''Deactivate the previous row and activate the next row.'''

        # if this is the first guess (active_row == None), we do not need to deactivate old row.
        if self.current_row != None:
            self.deactivate_current_row()

        # increment the active row, and initialize the active row to 0 if no value yet.
        if self.current_row == None:
            self.current_row = 0
        else:
            self.current_row += 1

        # activate the new row.
        self.activate_current_row()

    
    def activate_current_row(self):
        '''Activates the current row.'''

        # isolate the row of buttons to be activated. Use formula to calculate indices.
        actual_row = self.ROWS - 1 - self.current_row   # the actual row in the list (top to bottom)
        start_index = actual_row*self.COLUMNS
        end_index = (actual_row+1)*self.COLUMNS
        button_row = self.button_list[start_index:end_index]

        # activate the buttons and reset color
        for button in button_row:
            button.configure(state=tk.ACTIVE, background='SystemButtonFace')

    
    def deactivate_current_row(self):
        '''Deactivates the current row.'''

        # isolate the row of buttons to be deactivated. Use formula to calculate indices.
        actual_row = self.ROWS - 1 - self.current_row   # the actual row in the list (top to bottom)
        start_index = actual_row*self.COLUMNS
        end_index = (actual_row+1)*self.COLUMNS
        button_row = self.button_list[start_index:end_index]

        # deactivate the buttons
        for button in button_row:
            button.configure(state=tk.DISABLED)


    def set_color(self, color):
        '''
        Updates the currently selected color.

        Passed to the command argument for buttons in the color palette.
        '''

        self.current_color = color
        # Update label to reflect change.
        self.current_color_label.configure(text=f'Selected color: {self.current_color}')


    def update_button_color(self, row, column):
        '''
        Updates the color of a button to the selected color on click.

        Passed to the command argument for buttons in the 2D button list.
        '''

        index = row*self.COLUMNS + column   # Use formula to calculate index of target button.
        button = self.button_list[index]
        button.configure(background=self.current_color)


