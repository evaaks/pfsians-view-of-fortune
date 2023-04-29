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
        play_field = self.get_play_field()
        print(play_field)

    def get_play_field(self):
        playdeck_card = None
        playbin_card = None
        if self._playdeck:
            playdeck_card = self._playdeck.top()
        if self._playbin:
            playbin_card = self._playbin.top()
        return (playdeck_card, playbin_card)

        base_cards = [stack.top() for stack in self._base] if self._base else [None for i in range(self.NBASE)]
        base_card_message = ""
        for i in range(self.NBASE):
            base_card_message += f"| {i+ 1}. {base_cards[i]} "

        play_columns_message = ""
        for i in range(self.NPLAY_ROWS):
            play_columns_message += f"    Row {i + 1} "
            for n in range(self.NPLAY):
                play_columns_message += f"| {n + 1}. {self._play[i][n]} "#+=???????????????????????

            play_columns_message += "\n"

        play_field = f"---- PLAY FIELD ----\n" \
                     f"PlayDeck: |{playdeck_card}|\n" \
                     f"PlayBin: |{playbin_card}|\n" \
                     f"Base Row: {base_card_message} |\n" \
                     f"Play Rows:\n{play_columns_message}\n" \
                     f"*****************\n\n"
        return play_field


    def move_cards(self, card):
        var = int(input("Choose number of operation for card movement from/to:\n"
                      "1: deck/play row\n"
                      "2: deck/bin\n"
                      "3: deck/base row\n"
                      "4: bin/play row\n"
                      "5: bin/base row\n"
                      "6: play row/ play row\n"
                        ))
        if var == 1:
            pos1 = int(input("Write coordinates to which row, column you want move your card"))
            pos2 = card.deck_play(pos1)

        if var == 2:
            pos1 = int(input("Write coordinates to which row, column you want move your card"))
            pos2 = card.deck_bin(pos1)

        if var == 3:
            pos1 = int(input("Write to which row, column you want move your card"))
            pos2 = card.deck_base(pos1)

        if var == 4:
            pos1 = int(input("Write to which row, column you want move your card"))
            pos2 = card.bin_play(pos1)

        if var == 5:
            pos1 = int(input("Write to column you want move your card"))
            pos2 = card.bin_play(pos1)

        if var == 6:
            pos1 = int(input("Write coordinates from which row, column to which row, column you want move your card"))
            pos2 = card.play_play(pos1)