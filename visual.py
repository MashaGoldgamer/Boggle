from tkinter import *
from boggle_logic import BoggleLog
import Timer
from PIL import Image, ImageTk
from Board import Board
from Timer import Timer

# game sizes:
WIDTH_FRAME = 500
HEIGHT_FRAME = 650
WIDTH_BOARD = 400
HEIGHT_BOARD = 400
NUM_OF_COLUMN = 4  # depend on number of board
# other variables:
TRY_WORD_TAG = 'word_try'
FONT_TRY = ("Consolas", 30, "bold italic")
FONT_TRY_SMALL = ("Consolas", 20, "bold italic")
GAME_TIME = 180
REGULAR_COLOR = "SteelBlue2"
ACTIVE_COLOR = "DeepSkyBlue2"
BUTTON_STYLE = {"font": ("Courier", 15),
                "relief": RAISED,
                "bg": REGULAR_COLOR,
                "activebackground": ACTIVE_COLOR}
BG_COLOR = "DarkSeaGreen3"
BG_COLOR_CHOSE_CELL = "DarkSeaGreen3"
NUM_HINT = 3
FLATTER_TAG = "flatter"


class BoggleShow:
    """
    responsible to the GUI part of the game.
    """

    def __init__(self):
        # fields that are there always.
        self.outer = Tk()
        self.outer.title("Boggle game")  # todo change moto
        self.outer.iconbitmap("boggle_icon.ico")
        self.canvas = Canvas(self.outer, width=WIDTH_FRAME,
                             height=HEIGHT_FRAME)
        self.canvas.configure(background=BG_COLOR)
        self.start_or_end = "start"
        self.__start_view = self.start_end_game()
        self.canvas.pack()
        self.__board = None
        self.__logic = None
        # fields that changing in the course of the game
        self.__score = None
        self.__timer = Timer(self)
        self.__reset_button = None
        self.__rectangle_dict = {}  # eg: {(col, row): int(represents the name of the rectangle)
        self.__letter_coord_dic = {}  # eg: {(col, row): x_0, y_0, x_1, y_1}.
        self.new_game_timer = None
        self.path = []
        self.__hint_button_lst = []
        self.__hint_left = NUM_HINT - 1  # -1 so hint function can delete icons
        self.__escape = self.outer.bind("<Escape>",
                                        lambda x: self.outer.destroy())

    """""""""""""""""""""""""""""""""""""""""""""""""""""
                      START AND OVER:
    """""""""""""""""""""""""""""""""""""""""""""""""""""

    def start_end_game(self):
        """
        creates the screen before or after the game.
        :return: None
        """
        if self.start_or_end == "start":
            screen_view = PhotoImage(file="start_image.png")
            screen_view_button = Button(self.canvas, image=screen_view,
                                        comman=self.play)
            screen_view_button.photo = screen_view
            screen_view_button.place(x=0, y=0)
        else:
            self.canvas.delete("all")
            screen_view = PhotoImage(file="game_over.png")
            screen_view_button = Button(self.canvas, image=screen_view,
                                        comman=self.play)
            screen_view_button.photo = screen_view
            screen_view_button.place(x=0, y=0)
            score_text = Label(self.canvas, text="SCORE:" + str(
                self.__logic.get_score()),
                               font=("Comic Sans MS", 30), fg="white",
                               bg="red3")
            score_text.place(x=20, y=200)
        return screen_view

    def play(self):
        """
        this part starts when the player start new game, restarting all
        parameters and creates the display of the game.
        :return: None
        """
        self.canvas.destroy()
        self.canvas = Canvas(self.outer, width=WIDTH_FRAME,
                             height=HEIGHT_FRAME)
        self.canvas.configure(background=BG_COLOR)
        self.canvas.pack()
        self.__board = Board()
        self.__logic = BoggleLog(self.__board)
        self.__score = 0
        self.__hint_button_lst = []
        self.__hint_left = NUM_HINT - 1
        self.create_score()
        self.__rectangle_dict = {}
        self.__letter_coord_dic = {}
        self.create_letters_board()
        self.create_reset_button()
        self.new_game_timer = True
        self.__timer.clock()
        self.new_game_timer = False  # this double is for the timer to restart.
        self.__timer.clock()
        self.create_hint_button()
        self.create_hint_emoji()
        self.outer.bind('<B1-Motion>', lambda event: self.guess_try(event))
        self.outer.bind('<B1-ButtonRelease>', lambda event: self.end_of_try())

    def run_game(self):
        """
        this part run the game
        :return:
        """
        self.outer.mainloop()

    """""""""""""""""""""""""""""""""""""""""""""""""""""
                       GAME DISPLAY:
    """""""""""""""""""""""""""""""""""""""""""""""""""""

    def create_letters_board(self):
        """
        creates the main board of the game - rectangle with letter/s in.
        :return: None
        """
        for row in range(NUM_OF_COLUMN):
            for col in range(NUM_OF_COLUMN):
                new_cell = self.create_letter(row, col)
                self.__letter_coord_dic[(row, col)] = self.canvas.coords(
                    new_cell)

    def create_letter(self, row, col):
        """
        creates new cell on the screen.
        """
        m = 10  # (margin)
        letter = self.__board.get_letter(row, col)
        x_0, y_0, x_1, y_1 = self.get_coord(row, col)
        letter_cell = self.canvas.create_rectangle(x_0 + m, y_0 + m,
                                                   x_1 - m, y_1 - m,
                                                   fill="SkyBlue2",
                                                   outline="DeepSkyBlue2",
                                                   width=5)
        self.__rectangle_dict[(row, col)] = letter_cell
        self.canvas.create_text((x_0 + x_1) / 2, (y_0 + y_1) / 2, text=letter,
                                font=("Courier", 25))
        return letter_cell

    def get_coord(self, row, col):
        """
        finds 4 elements of each cell, depend on the GAME_SIZE and BOARD_SIZE.
        :param row: row of the cell
        :param col: column of the cell
        :return: x_0, y_0, x_1, y_1
        """
        len_x = WIDTH_BOARD / NUM_OF_COLUMN
        len_y = HEIGHT_BOARD / NUM_OF_COLUMN
        x_0 = 50 + len_x * col
        y_0 = 225 + len_y * row
        x_1 = x_0 + len_x
        y_1 = y_0 + len_y
        return x_0, y_0, x_1, y_1

    def create_score(self):
        """
        create text of score on the canvas.
        """
        self.canvas.delete("score")
        text_score = self.__logic.get_score()
        self.__score = self.canvas.create_text(WIDTH_FRAME / 2, 120,
                                               text=text_score,
                                               font=("CourierBold", 35),
                                               tag="score")

    def create_reset_button(self):
        """
        this function creates the reset button on the screen
        :return: None
        """
        reset_button = Button(self.canvas, BUTTON_STYLE, text="restart",
                              command=self.play)
        reset_button.place(x=25, y=12)

    def create_hint_button(self):
        """
        this function creates the hint button on the screen
        :return: None
        """
        hint_button = Button(self.canvas, BUTTON_STYLE, text="hint",
                             command=self.hint)
        hint_button.place(x=25, y=57)

    def create_hint_emoji(self):
        """
        this function creates the emoji of the hint on the screen
        :return: the hint image
        """
        hint_image = PhotoImage(file="hint.png")
        for i in range(NUM_HINT):
            hint_image_label1 = Label(self.canvas, image=hint_image)
            hint_image_label1.photo = hint_image
            hint_image_label1.place(x=25, y=100 + i * 40)
            self.__hint_button_lst.append(hint_image_label1)
        return hint_image

    def create_flatter(self, word):
        """
        this function creates text on board. the text is shown after the gamer
        guessed a word
        :param word: the word the player guessed
        :return: None
        """
        if len(word) <= 3:
            self.canvas.create_text(WIDTH_FRAME / 2, 175, text="nice",
                                    tag=FLATTER_TAG, font=FONT_TRY)
        if len(word) == 4:
            self.canvas.create_text(WIDTH_FRAME / 2, 175,
                                    text="you are great!",
                                    tag=FLATTER_TAG, font=FONT_TRY_SMALL)
        if len(word) >= 5:
            self.canvas.create_text(WIDTH_FRAME / 2, 175, text="amazing!!!",
                                    tag=FLATTER_TAG, font=FONT_TRY)

    """""""""""""""""""""""""""""""""""""""""""""""""""""
                     GAME COMMANDS:
    """""""""""""""""""""""""""""""""""""""""""""""""""""

    def guess_try(self, event):
        """
        this function checks if the gamer chose a valid path
        :param event: the gamer clicked on the board
        :return:None
        """
        self.canvas.delete("chosen")
        self.canvas.delete("hint_word")
        self.canvas.delete(FLATTER_TAG)
        x, y = event.x, event.y
        if 50 < x < 450 and 225 < y < 625:  # if the mouse is on the board
            for row_and_col, cell in self.__letter_coord_dic.items():  # found cell
                if cell[0] < x < cell[2] and cell[1] < y < cell[3]:
                    if self.path and not self.__logic.is_neighbors(
                            self.path[-1],
                            row_and_col) or row_and_col in self.path:
                        return  # means that player jumped into invalid cell or
                        # returned to a cell he was alredy.
                    self.path.append(row_and_col)
                    self.canvas.itemconfig(self.__rectangle_dict[row_and_col],
                                           fill=BG_COLOR_CHOSE_CELL)
                    self.show_try()

    def show_try(self):
        """
        this function creates the text inside the guessing try
        :return: None
        """
        self.canvas.delete(TRY_WORD_TAG)
        letters = self.__board.combine_letter_from_path(self.path)
        self.canvas.create_text(WIDTH_FRAME / 2, 175, text=letters,
                                font=FONT_TRY if len(
                                    letters) < 10 else FONT_TRY_SMALL,
                                tag=TRY_WORD_TAG)

    def end_of_try(self):
        """
        this function checks if the word the player chose is legal, and if so
        the game modify the score, adding the word to the list of right words
        and gives the player a flatter.
        :return: None
        """
        self.color_cell_back()
        self.canvas.delete(TRY_WORD_TAG)
        word = self.__logic.is_right_word(self.path)
        if word is False:
            self.canvas.create_text(WIDTH_FRAME / 2, 175,
                                    text="CHOSEN ALREADY!", tag="chosen",
                                    font=FONT_TRY_SMALL, fill="red")
            self.path = []
            return
        len_right_words = len(self.__logic.get_words_guessed()) - 1
        x, y = len_right_words % 7, len_right_words // 7
        if word:
            labelword = Label(self.canvas,
                              text=str(len_right_words + 1) + "." + word,
                              font=("Consolas", 11), bg=BG_COLOR)
            labelword.place(relx=0.615 + (3 * (50 * y)) / 1000, rely=0.007 + (
                    3 * (10 * x)) / 1000)
            self.create_flatter(word)
            self.create_score()
        self.path = []

    def color_cell_back(self):
        """
        this function colors the cell back to the original color.
        :return:
        """
        for cell in self.path:
            self.canvas.itemconfig(self.__rectangle_dict[cell],
                                   fill="SkyBlue2")

    def hint(self):
        """
        this function gives a hint to the player if he not used all of them
        already
        """
        self.canvas.delete("chosen")
        self.canvas.delete("hint_word")
        self.canvas.delete(FLATTER_TAG)
        if self.__hint_left < 0:
            return
        self.__hint_button_lst[self.__hint_left].destroy()
        hint_word = self.__logic.get_hint_word()
        self.canvas.create_text(WIDTH_FRAME / 2, 175,
                                text=hint_word, tag="hint_word",
                                font=FONT_TRY, fill="red")
        self.__hint_left -= 1
