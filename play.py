from deck import Decks, Deck


class _AbstractStack:
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
    def __init__(self):
        self.card = None

    def top(self):
        return self.card

    def __len__(self):
        if self.card is None:
            return 0
        return self.card.value

    def full(self):
        return len(self) == len(Deck.RANKS)

    def can_put(self, card):
        return (self.top().value + 1 == card.value) and (self.top().suit == card.suit)

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


class Row(tuple):
    """
    Кортеж фіксованого розміру.
    Конструктор отримує кількість елементів та iterable.
    """

    def __new__(cls, n, it):
        it = iter(it)
        obj = super().__new__(cls, (next(it) for _ in range(n)))
        return obj


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

   # def __len__(self):
   #     return len(self.row)

    def top(self):
        return self.row[-1]

    def away(self):
        self.row.pop()


class Play:
    NBASE = 8
    NPLAY = 10

    def __init__(self):
        self._deck = Decks()
        self._playdeck = None  # колода на столі
        self._base = None  # базовий ряд
        self._play = None  # гральні вертикальні ряди
        self._in_play = False
        self._bin = None
        self.new_play()

    def new_play(self):
        self._deck.shuffle()
        self._playdeck = _PlayDeck(self._deck)
        self._base = Row(self.NBASE, iter(_Stack, None))
        self._play = Row(self.NPLAY, iter(lambda: _PlayColumn(self._playdeck), None))
        self._playbin = _PlayBin()
        self._in_play = True

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

    def play_play(self, i_from, i_to):
        assert (0 <= i_from < len(self._play))
        assert (0 <= i_to < len(self._play))
        if i_from != i_to:
            return self.move(self._play.row[i_from], self._play.row[i_to])
        return True

    def play_base(self, i_from, i_to):
        assert (0 <= i_from < len(self._play))
        assert (0 <= i_to < len(self._base))
        return self.move(self._play.row[i_from], self._base.row[i_to])

    def deck_play(self, i_to):
        assert (0 <= i_to < len(self._play))
        return self.move(self._playdeck, self._play.row[i_to])

    def deck_base(self, i_to):
        assert (0 <= i_to < len(self._base))
        return self.move(self._playdeck, self._base.row[i_to])

    def bin_play(self, i_to):
        assert (0 <= i_to < len(self._play))
        return self.move(self._playbin, self._play.row[i_to])

    def bin_base(self, i_to):
        assert (0 <= i_to < len(self._base))
        return self.move(self._playbin, self._base.row[i_to])

    def deck_bin(self):
        return self.move(self._playdeck, self._playbin)
