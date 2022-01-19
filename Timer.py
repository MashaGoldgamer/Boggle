TIME_OVER = 180  # in seconds
WIDTH_FRAME = 500
HEIGHT_FRAME = 630
X_SPACE = WIDTH_FRAME / 10  # (50)
Y_SPACE = HEIGHT_FRAME / 4  # (210)
BOARD_SIZE = WIDTH_FRAME - (2 * X_SPACE)  # (400)
# display:
BG = 'SkyBlue2'
BG_30 = 'gold'
BG_10 = 'red'
FONT = 'Consolas 20'


class Timer:
    """
    creates a timer to BoggleGame.
    """

    def __init__(self, house):
        self.__house = house
        self.__time_to_over = TIME_OVER
        self.__time_started = False
        self.keep_move = None

    def clock(self):
        """
        this function update the timer.
        :return: None
        """
        if self.__time_to_over == -1:
            self.__time_to_over = TIME_OVER
            self.__house.start_or_end = "end"
            self.__house.start_end_game()
            return
        bg = BG
        if self.__time_to_over <= 30:
            bg = BG_30
        if self.__time_to_over <= 10:
            bg = BG_10
        x_0, y_0, x_1, y_1 = WIDTH_FRAME / 2 - 50, Y_SPACE - 125, WIDTH_FRAME / 2 + 50, Y_SPACE - 75
        self.__house.canvas.create_rectangle(x_0, y_0, x_1, y_1, fill=bg,
                                             width=5, outline='SteelBlue2')
        min, sec = self.__time_to_over // 60, self.__time_to_over % 60
        time_text = str(min) + ':' + str(sec).zfill(2)
        self.__house.canvas.create_text((x_0 + x_1) / 2 - 29,
                                        (y_0 + y_1) / 2 - 16,
                                        text=time_text, font=FONT, anchor='nw',
                                        tag='timer')
        if not self.__house.new_game_timer:
            self.__time_to_over -= 1
            self.keep_move = self.__house.outer.after(1000, self.clock)
            self.__time_started = True
        else:  # restarting the timer
            self.__time_to_over = TIME_OVER
            if self.__time_started:
                self.__house.outer.after_cancel(self.keep_move)
            return
