from boggle_board_randomizer import *

HEIGHT = 4
WIDTH = 4


class Board:
    """
    this class creates the board to boggle game.
    """
    def __init__(self):
        self.__board = randomize_board()
        self.__dic_board = {}
        self.set_dic()

    def set_dic(self):
        """
        modify the diction according to the board. key = tuple of
        coordination. value = letter/s.
        :return: None
        """
        for index_row, row in enumerate(self.__board):
            for index_col, col in enumerate(row):
                self.__dic_board[(index_row, index_col)] = col

    def __str__(self):
        return '\n'.join([str(i) for i in self.__board])

    def get_board(self):
        return self.__board

    def get_diction(self):
        """
        returns all diction e.g {(row, col): 'T'}
        """
        return self.__dic_board

    def get_letter(self, col, row):
        return self.__dic_board[(col, row)]

    def combine_letter_from_path(self, path):
        """
        this function run over tuples of location in path and return the
        letter/s the path create based on the the board.
        :param path: list of tuples. each tuple is a location in the board of a
        letter
        :return: word from the path and the board
        """
        letters = ""
        for loc in path:
            letters += str(self.get_letter(loc[0], loc[1]))
        return letters
