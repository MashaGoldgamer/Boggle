import itertools as it
import copy

HEIGHT = 4
WIDTH = 4

def loc_in_board(location):
    """
    checks if a given location is in board or outside the board.
    :param location: tuple: (i: row, j: col)
    :return: True- if it is in board, False- otherwise
    """
    if not location:
        return False
    i, j = location[0], location[1]
    return not i < 0 and not j < 0 and not i > HEIGHT - 1 and not j > WIDTH - 1


def legal_moves(location):
    """
    creates a list of tuples, each one is a legal location to move from the
    current location. this function doesn't refers to the limits of the board.
    :param location: tuple: (i: row, j: col)
    :return: list of tuples each one is a legal location to move from the
    current location.
    """
    i, j = location[0], location[1]
    lst_moves = []
    for r in range(i - 1, i + 2):
        for c in range(j - 1, j + 2):
            lst_moves.append((r, c))
    lst_moves.remove((i, j))
    return lst_moves


def is_path_legal(path):
    """
    checks if a given path is leggal
    :param path: list of tuples, each tuple is location: (i: row, j: col)
    :return: True if it's legal path, False otherwise.
    """
    index = 0
    if path:
        location = path[index]
    else:
        location = []
    while index + 1 < len(path):
        if not loc_in_board(location) or path[index + 1] not in legal_moves(
                location):
            return False
        index += 1
        location = path[index]
    return loc_in_board(location)  # checks if the last loc is in board and if
    # so it's means the all path is legal.


def open_words(file_name):
    """
   this function creates a list from text file
   :param file_name: the file we want to convert to a list
   :return: a list of strings
   """
    with open(file_name) as data_file:
        words = []
        for line in data_file:
            words.append(line.strip())
    return words


def create_word_from_path(board, path):
    """
    this function run over tuples of location in path and return the word the
    path create based on the the board
    :param board: the board we use it's value to create the word
    :param path: list of tuples. each tuple is a location in the board of a
    letter
    :return: word from the path and the board
    """
    word = ""
    for loc in path:
        word += board[loc[0]][loc[1]]
    return word


def is_valid_path(board, path, words):
    """
    this function check if a path is valid based on the location of it's tuples
    and if the word that the path create is mentioned at words ist
    :param board: the board we check if a path is legal at
    :param path: the path we check
    :param words: the list we check if a word belongs to
    :return: the word the path create if it's legal, None otherwise
    """
    if not is_path_legal(path):
        return
    word = create_word_from_path(board, path)
    if word in words:
        return word


def paths_for_word(all_path, path, word, board, index):
    """
    this function create a path for a word based on the location of the letters
    on the board. if there are more than one path, the function returns every
    each path. in case the board doesn't contain the word, the function returns
    an empty list.
    :param word: the word we look for it's path on the board
    :param board: the board we try look for the word's letters at.
    :param all path:
    :return: list of lists, each list contains tuples- if there is at least
    one legal path. empty list- if there aren't any legal path for the word
    """
    if len(word) == index:
        all_path.append(copy.deepcopy(path))
        return
    for index_row, row in enumerate(board):
        for index_col, col in enumerate(row):
            if path:
                if len(col) == 2 and index <= len(word) - 2 and col == word[
                    index] \
                        + word[index + 1] and (
                        index_row, index_col) not in path and \
                        path[-1] in legal_moves((index_row, index_col)):
                    paths_for_word(all_path, path + [(index_row, index_col)],
                                   word, board, index + 2)
            else:
                if len(col) == 2 and index <= len(word) - 2 and col == word[
                    index] + word[index + 1]:
                    paths_for_word(all_path, path + [(index_row, index_col)],
                                   word, board, index + 2)
            if path:
                if col == word[index] and (
                        index_row, index_col) not in path and path[
                    -1] in legal_moves(
                    (index_row, index_col)):
                    paths_for_word(all_path, path + [(index_row, index_col)],
                                   word, board, index + 1)
            else:
                if col == word[index]:
                    paths_for_word(all_path, path + [(index_row, index_col)],
                                   word, board, index + 1)
    if path:
        path.pop()
    return all_path


def find_length_n_paths(n, board, words):
    """
    this function find all the words on the board that their path length is n
    :param n: the length
    :param board: the board we look for it's letters
    :param words: list of words
    :return:list of lists of tuple. each inner list is a path of a word in
    length n that is on the board
    """
    paths_list = []
    words = set(words)
    for word in words:
        result = paths_for_word([], [], word, board, 0)
        if result:
            result = list(filter(lambda x: len(x) == n, result))
            for path in result:
                paths_list.append(path)
    return paths_list


def find_length_n_words(n, board, words):
    """
   this function find all the words in length n on the board and their path
   :param n: the length
   :param board: the board we look for it's letters
   :param words: list of words
   :return:list of lists of tuples. each inner list is a path length n
    of a word in the board
   """
    relevant_words = set(filter(lambda x: len(x) == n, words))
    paths_list = []
    for word in relevant_words:
        result = paths_for_word([], [], word, board, 0)
        for path in result:
            paths_list.append(path)
    return paths_list


def max_score_paths(board, words):
    """
    this function find the longest path for words in the board
    :param board: the board we look at it's letters
    :param words: list of words
    :return: list of lists of tuples. each inner list is the longest path for a
    word that is on the board
    """
    paths_list = []
    for word in words:
        result = paths_for_word([], [], word, board, 0)
        if result:
            max_score_path = max(result, key=lambda x: len(x))
            paths_list.append(max_score_path)
    return paths_list
