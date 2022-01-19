from boggle_utils import *
import random

WORDS_DICT = "boggle_dict.txt"


class BoggleLog():
    """
    this class responsible to the logic of the game.
    """

    def __init__(self, board):
        self.__score = 0
        self.__words = open_words(WORDS_DICT)  # list of strings.
        self.__board = board
        self.__guessed_already = []
        self.__hint_given_word = []

    def is_right_word(self, path):
        """
        this function check if the word that the path create is mentioned at the words.
        func also modify score and guessed list.
        :param path: list of tuples, each tuple is location: (i: row, j: col).
        :return: False - if the word was been chosen already, word - if the word
         the path create is legal, None- otherwise
        """
        word = create_word_from_path(self.__board.get_board(), path)
        if word in self.__guessed_already:
            return False
        if word in self.__words:
            self.__guessed_already.append(word)
            self.__score += len(word) ** 2
            return word

    def is_neighbors(self, loc1, loc2):
        """
        checks if two locations are possible to move from one to another.
        not consider location out of board
        :param loc1: tuple: (i: row, j: col)
        :param loc2: tuple: (i: row, j: col)
        :return: True if they are neighbors, False otherwise.
        """
        return loc1 in legal_moves(loc2)

    def get_hint_word(self):
        """
        this function creates hint word basef on the list of words
        :return:
        """
        index = 0
        len_word = random.randint(3, 5)
        paths_list = []
        words = list(filter(lambda word: len(word) == len_word, self.__words))
        while len(paths_list) < 50 and index < len(words):
            word = words[index]
            result = paths_for_word([], [], word, self.__board.get_board(), 0)
            if result:
                result = list(filter(lambda x: len(x) == len_word, result))
                for path in result:
                    word = create_word_from_path(self.__board.get_board(),
                                                 path)
                    if word not in self.__hint_given_word and word not in\
                        self.__guessed_already:
                        paths_list.append(path)
            index += 1
        chosen_path = random.choice(paths_list)
        chosen_word = create_word_from_path(self.__board.get_board(),
                                            chosen_path)
        self.__hint_given_word.append(chosen_word)
        chosen_word = chosen_word[0:2] + '_ ' * (len_word - 2)
        return chosen_word

    def get_score(self):
        return self.__score

    def get_words_guessed(self):
        return self.__guessed_already
