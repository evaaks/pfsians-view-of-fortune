import play


class Console(play.Play):
    """
    1. Вывод меню игры
    2. Создания меню
        2.1. Старт игры
        2.2 Правила игры
        2.3 Перезапустить игру (во время игры)
    3. Игра
        3.1. Вывод игрового поля:
            1. Колоду - PlayDeck: |A-S|
            2. Мусорку - PlayBin: |None|
            3. Игровые ряды - Row 1 | 1. 10-S | 2. 8-C | 3. J-D | 4. Q-H | 5. K-S | 6. A-C |
                              Row 2 | 1. 10-D | 2. 8-H | 3. Q-C | 4. J-H | 5. 6-S | 6. 2-D |
            4. Базовые ряды - | 1. A-S | 2. A-D | 3. A-C | 4. A-H |
        3.2. Возможность перемещения карт из разных колод
    """

    def __init__(self):
        super().__init__()

    def _set_menu(self):
        pass

    def _do_action(self):
        pass

    def show_play_field(self):
        playdeck_card = self._playdeck.top() if self._playdeck else None
        playbin_card = self._playbin.top() if self._playbin else None
        base_cards = [stack.top() for stack in self._base] if self._base else [None for i in range(self.NBASE)]
        play_columns = []
        pass

    def show_menu(self):
        pass
