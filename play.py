from deck import Decks, Deck


class _AbstractStack(list):
    # Абстрактна стопка карт. Можна покласти, скинути та подивитись верхню.
    def __len__(self):
        raise NotImplementedError

    def top(self):
        raise NotImplementedError

    def can_put(self, card):
        raise NotImplementedError

    def put(self, card):
        if self.can_put(card):
            self._put(card)
            return True
        else:
            return False

    def _put(self, card):
        raise NotImplementedError

    def away(self):
        pass


class _Stack(_AbstractStack):
    # Стопка базового ряду ідентифікується верхньою картою.
    def __init__(self, playaces):
        self.card = next(playaces)

    def top(self):
        return self.card

    def __len__(self):
        if self.card is None:
            return 0
        return self.card.value

    def full(self):
        return len(self) == len(Deck.RANKS)

    def can_put(self, card):
        return (not self and card.ace()) or \
            ((self and self.top().value + 1 == card.value) and (self.top().suit == card.suit))

    def _put(self, card):
        self.card = card


class _PlayColumn(_AbstractStack):
    # Вертикальний ігровий ряд.
    def __init__(self, playdeck):
        self.row = []
        self._put(playdeck.top())
        playdeck.away()

    def can_put(self, card):
        return not self or self.top() > card

    def _put(self, card):
        self.row.append(card)

    def __len__(self):
        return len(self.row)

    def top(self):
        return self.row[-1]

    def away(self):
        self.row.pop()


class _PlayDeck:
    def __init__(self, deck):
        self.deck = deck
        self.card = None
        self.away()

    def top(self):
        return self.card

    def __len__(self):
        return len(self.deck) + (self.card is not None)

    def away(self):
        if self.deck:
            self._away()
        else:
            self.card = None

    def _away(self):
        self.card = self.deck.deal()

    def put(self, card):
        return False


class _PlayBin(_AbstractStack):
    # смітник.
    def __init__(self):
        self.row = []

    def _put(self, card):
        self.row.append(card)

    def __len__(self):
       return len(self.row)

    def top(self):
        return self.row[-1]

    def away(self):
        self.row.pop()


class Play:
    NBASE = 4
    NPLAY = 6
    NPLAY_ROWS= 2

    def __init__(self):
        self._deck = Decks()
        self._playdeck = None  # колода на столі
        self._playaces = None  # колода виз тузис
        self._base = None  # базовий ряд
        self._play = list()  # гральні вертикальні ряди
        self._in_play = False
        self._playbin = None
        self.new_play()

    def new_play(self):
        self._deck.shuffle()
        self._playdeck = _PlayDeck(self._deck)
        self._play = self.fill_play_rows()
        aces = Deck.all_aces()
        self._base = [_Stack(aces) for i in range(self.NBASE)]
        self._playbin = _PlayBin()
        self._in_play = True

    def fill_play_rows(self):
        for row in range(self.NPLAY_ROWS):
            row_columns = []
            for col in range(self.NPLAY):
                row_columns.append(_PlayColumn(self._playdeck))
            self._play.append(row_columns)

    def win(self):
        res = all(stack.full() for stack in self._base.row)
        self._in_play = not res
        return res

    @staticmethod
    def move(stack_from, stack_to):
        card = stack_from.top()
        if card is None:
            return False
        res = stack_to.put(card)
        if not res:
            return False
        stack_from.away()
        return True

    def play_play(self, i_from_row, i_from_col, i_to_row, i_to_col):
        if i_from_row != i_to_row and i_from_col != i_to_col:
            return self.move(self._play[i_from_row][i_from_col], self._play[i_to_row][i_to_col])
        return True

    def play_base(self, i_from_row, i_from_col, i_to):
        return self.move(self._play[i_from_row][i_from_col], self._base.row[i_to])

    def deck_play(self, i_to_row, i_to_col):
        return self.move(self._playdeck, self._play[i_to_row][i_to_col])

    def deck_base(self, i_to):
        return self.move(self._playdeck, self._base.row[i_to])

    def bin_play(self, i_to_row, i_to_col):
        return self.move(self._playbin, self._play[i_to_row][i_to_col])

    def bin_base(self, i_to):
        return self.move(self._playbin, self._base.row[i_to])

    def deck_bin(self):
        return self.move(self._playdeck, self._playbin)
