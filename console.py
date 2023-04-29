from play import Play


class Console(Play):
    """
    1. Вивід правил
    3. Игра
        3.1. Вывод игрового поля:
            1. Колоду - PlayDeck: |A-S|
            2. Мусорку - PlayBin: |None|
            3. Игровые ряды - Row 1 | 1. [10-S, 9-S] | 2. [10-S, 9-S] | 3. [10-S, 9-S] | 4. [10-S, 9-S] | 5. [10-S, 9-S] | 6. [10-S, 9-S] |
                              Row 2 | 1. [10-S, 9-S] | 2. [10-S, 9-S] | 3. [10-S, 9-S] | 4. [10-S, 9-S] | 5. [10-S, 9-S] | 6. [10-S, 9-S] |
            4. Базовые ряды - | 1. A-S | 2. A-D | 3. A-C | 4. A-H |
        3.2. Возможность перемещения карт из разных колод
    """

    def __init__(self):
        super().__init__()
        self.play()

    def get_play_field(self):
        playdeck_card = None
        playbin_card = None
        if self._playdeck:
            playdeck_card = self._playdeck.top()
        if self._playbin:
            playbin_card = self._playbin.top()

        base_cards = [stack.top() for stack in self._base] if self._base else [None for i in range(self.NBASE)]
        base_card_message = ""
        for i in range(self.NBASE):
            base_card_message += f"| {i+ 1}. {base_cards[i]} "

        play_columns_message = ""
        for i in range(self.NPLAY_ROWS):
            play_columns_message += f"    Row {i + 1} "
            for n in range(self.NPLAY):
                play_columns_message += f"| {n + 1}. {self._play[i][n]} "

            play_columns_message += "\n"

        play_field = f"---- PLAY FIELD ----\n" \
                     f"PlayDeck: |{playdeck_card}|\n" \
                     f"PlayBin: |{playbin_card}|\n" \
                     f"Base Row: {base_card_message} |\n" \
                     f"Play Rows:\n{play_columns_message}\n" \
                     f"*****************\n\n"
        return play_field

    def move_cards(self):
        """
        1. Перемещение из игрового ряда в базовый
        2. Вывод сообщения, если карту нельзя переместить
        3. Вывод сообщения, если пользователь ввел неверную цифру действия
        4. Вывод сообщения об ошибке, если пользователь пытается переместить карту в несуществующую колонку(например в колонку 100)
        5. Обработка ошибки если пользователь ввел не число
        6. Передавать два аргумента в методы перемещения с игровыми рядами(индекс игрового ряда, индекс колонки в игровом ряду)
        7. Куда-то прикрутить метод win
        """
        var = int(input("Choose number of operation for card movement from/to:\n"
                        "1: deck/play row\n"
                        "2: deck/bin\n"
                        "3: deck/base row\n"
                        "4: bin/play row\n"
                        "5: bin/base row\n"
                        "6: play row/ play row\n"
                        ))

        result = True
        if var == 1:
            pos1 = int(input("Write coordinates to which row, column you want move your card"))
            result = self.deck_play(pos1)

        if var == 2:
            result = self.deck_bin()

        if var == 3:
            pos1 = int(input("Write to which row, column you want move your card"))
            result = self.deck_base(pos1)

        if var == 4:
            row = int(input("Write to which row you want move your card"))
            col = int(input("Write to which column you want move your card"))
            result = self.bin_play(row - 1, col - 1)

        if var == 5:
            pos1 = int(input("Write to column you want move your card"))
            result = self.bin_base(pos1)

        if var == 6:
            pos1 = int(input("Write coordinates from which row, column to which row, column you want move your card"))
            result = self.play_play(pos1)

        if not result:
            print("Wrong choose")

    def play(self):
        while self._in_play:
            print(self.get_play_field())
            self.move_cards()
