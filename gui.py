from tkinter import *
from tkinter.messagebox import showinfo

import play
from cardfaces import CardFaces
from locus import Locus
import enum

Locus.coords = Locus.left_bottom


def place_image(parent, image, locus: Locus):
    return parent.create_image(*locus.coords(), image=image, anchor=SW)


class GUICard(play.Deck.Card, CardFaces):
    # noinspection PyMissingConstructor
    def __init__(self, card, parent, locus):
        self._irank = card.j
        self._isuit = card.i
        self._parent = parent
        self._item = place_image(self._parent, CardFaces.get(self), locus)

    def away(self):
        if self._parent is not None:
            self._parent.delete(self._item)
        self._parent = None

    def reset(self, locus):
        if self._parent is not None:
            self._parent.coords(self._item, *locus.coords())

    def move(self, dx, dy):
        if self._parent is not None:
            self._parent.move(self._item, dx, dy)

    def raise_(self):
        self._parent.tag_raise(self._item)


class _LAP(Locus):  # LocusAndParent
    def __init__(self, *, parent, **kwargs):
        self._parent = parent
        super().__init__(**kwargs)


# noinspection PyProtectedMember
class _GUIPlayDeck(play._PlayDeck, _LAP):
    def __init__(self, deck, **kwargs):
        _LAP.__init__(self, **kwargs, width=CardFaces.W, height=CardFaces.H)
        self._iback = None
        self._iback = place_image(self._parent, CardFaces.BACK, self)
        play._PlayDeck.__init__(self, deck)

    def _away(self):
        self.card = GUICard(self.deck.deal(), parent=self._parent, locus=self)
        if not self.deck and self._iback:
            self._parent.delete(self._iback)
            self._iback = None


# noinspection PyProtectedMember
class _GUIStack(play._Stack, _LAP):
    def __init__(self, **kwargs):
        _LAP.__init__(self, **kwargs, width=CardFaces.W, height=CardFaces.H)
        play._Stack.__init__(self)
        self._parent.create_rectangle(*self.rectangle(), width=1, outline=GUI._border)

    def _put(self, card):
        if self:
            self.card.away()
        super()._put(card)
        card.reset(self)


# noinspection PyProtectedMember
class _GUIPlayColumn(play._PlayColumn, _LAP):
    def __init__(self, playdeck, h, **kwargs):
        _LAP.__init__(self, **kwargs, width=CardFaces.W, height=CardFaces.H)
        self._parent.create_rectangle(*self.rectangle(), width=1, outline=GUI._border)
        self._h = h
        play._PlayColumn.__init__(self, playdeck)
        self._parent.update()

    def _card_h(self):
        n = len(self) - 1
        if n <= 0:
            return 0
        h = CardFaces.H
        free = self._h - h
        per_card = free // n
        if per_card > h // 2:
            per_card = h // 2
        elif per_card > h // 3:
            per_card = h // 3
        elif per_card > h // 4:
            per_card = h // 4
        return per_card

    def update(self):
        n = len(self)
        if n == 0:
            return
        self.top().reset(self)
        self.top().raise_()
        per_card = self._card_h()
        tmp = self.up(per_card)
        for i in range(n - 2, -1, -1):
            self.row[i].reset(tmp)
            tmp = tmp.up(per_card)

    def _put(self, card):
        super()._put(card)
        self.update()

    def away(self):
        super().away()
        self.update()


class _XLocator:
    def __init__(self, n, x0, width, wc):
        self._n = n
        self._x0 = x0
        self._w = width
        self._wc = wc
        self._dx = 0
        self._off = 0
        self._calculate()

    def __getitem__(self, item):
        return self._x0 + self._off + item * (self._wc + self._dx)

    def _calculate(self, offset: bool = True):
        if offset:
            n = 1
        else:
            n = -1
        self._dx = (self._w - self._n * self._wc) // (self._n + n)
        self._off = self._dx


# noinspection PyProtectedMember,PyProtectedMember
class GUI(play.Play):
    _background = '#80ff80'
    _border = '#cd0532'

    class _DragFrom(enum.Enum):
        DECK = 1
        PLAY = 2
        BASE = 3
        NONE = 4

    def __init__(self, root):
        CardFaces.create_global_images()
        self._blocked = False
        self._root = root
        self._config_root()
        self._create_canvas()
        self._create_places()
        self._create_menu()
        super().__init__()
        self._set_bindings()

    def _create_places(self):
        self._y_base = CardFaces.H + 50
        self._y_play = self._ch - 50
        self._y_play_height = self._y_play - self._y_base - 40
        # self._x = 0
        self._ch = CardFaces.H
        self._columns = _XLocator(10, 0, self._cw, CardFaces.W)

    def new_play(self):
        if self._blocked:
            return
        self._blocked = True
        self.clear()
        self._deck.shuffle()
        self._playdeck = _GUIPlayDeck(self._deck, parent=self._c, left=self._columns[9], bottom=self._y_base)
        self._root.update()
        it = iter(self._columns)
        self._base = play.Row(self.NBASE,
                              iter(lambda: _GUIStack(parent=self._c, left=next(it), bottom=self._y_base), None))
        self._root.update()
        it = iter(self._columns)
        self._play = play.Row(self.NPLAY, iter(lambda: _GUIPlayColumn(self._playdeck, parent=self._c, left=next(it),
                                                                      bottom=self._y_play, h=self._y_play_height),
                                               None))
        self._in_play = True
        self._blocked = False

    def clear(self):
        tmp = self._c.find_all()
        for i in tmp:
            if i not in self._sysitems:
                self._c.delete(i)
        self._dragging = None

    def _set_bindings(self):
        self._c.bind('<Button-1>', self.on_press)
        self._c.bind('<B1-Motion>', self.on_move)
        self._c.bind('<ButtonRelease-1>', self.on_release)
        self._root.bind('<F5>', lambda x: self.new_play())
        self._dragging = None
        self._drag_from = None
        self._posx = None
        self._posy = None

    def _config_root(self):
        self._root.title('Жозефіна')
        self._root.resizable(width=False, height=False)
        self._root.config(bg=GUI._background)
        self._w = w = 900
        self._h = h = 600
        sw = self._root.winfo_screenwidth()
        sh = self._root.winfo_screenheight()
        self._root.geometry(f'{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}')

    def _create_canvas(self):
        dx = 25
        dy = 25
        self._cw = self._w - 2 * dx
        self._ch = self._h - 2 * dy
        self._c = Canvas(self._root, background='#004200', width=self._cw, height=self._ch, bd=-2)
        self._sysitems = []
        self._sysitems.append(self._c.create_line(0, 0, self._cw, 0, fill='red', width=2))
        self._sysitems.append(self._c.create_line(self._cw, 0, self._cw, self._ch, fill='red', width=2))
        self._sysitems.append(self._c.create_line(self._cw, self._ch, 0, self._ch, fill='red', width=2))
        self._sysitems.append(self._c.create_line(0, 0, 0, self._ch, fill='red', width=2))
        self._c.place(x=dx, y=dy)

    def _rollback(self):
        self._dragging.reset(self._drag_from)

    # noinspection PyUnusedLocal
    def on_release(self, event):
        if self._dragging:
            to = self._locate(event.x, event.y)
            if to is not None:
                to = to[0]
                self._dragging.reset(to)
            if to is None or not self.move(self._drag_from, to):
                self._rollback()
            self._dragging = None
            self._drag_from = None

    def on_move(self, event):
        if self._dragging:
            x, y = self._posx, self._posy
            self._posx, self._posy = event.x, event.y
            self._dragging.move(self._posx - x, self._posy - y)

    def _locate(self, x, y):
        res = None
        if y < self._y_base:
            if self._playdeck.inside(x, y):
                return self._playdeck, self._DragFrom.DECK
            for el in self._base:
                if el.inside(x, y):
                    res = el, self._DragFrom.BASE
                    break
            return res

        for el in self._play:
            if el.inside(x, y):
                res = el, self._DragFrom.PLAY
                break
        return res

    def _which_is_dragged(self, event):
        tmp = self._locate(event.x, event.y)
        if tmp and tmp[1] != self._DragFrom.BASE:
            self._drag_from = tmp[0]
        if self._drag_from:
            self._dragging = self._drag_from.top()
            self._dragging.raise_()
        else:
            self._drag_from = None

    def on_press(self, event):
        if self._blocked:
            return
        self._which_is_dragged(event)
        if self._dragging:
            self._posx, self._posy = event.x, event.y

    def _create_menu(self):
        self._menu = Menu(self._root)
        self._root.config(menu=self._menu)
        self._create_file_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        file = Menu(self._menu, tearoff=0)
        file.add_command(label='New game F5', command=self.new_play)
        file.add_command(label='Close', command=self._root.destroy)
        self._menu.add_cascade(label='File', menu=file)

    def _create_help_menu(self):
        help = Menu(self._menu, tearoff=0)
        help.add_command(label='Help', command=self._help)
        help.add_command(label='About', command=lambda: showinfo('About', 'Only a sample'))
        self._menu.add_cascade(label='Help', menu=help)

    def _help(self):
        win = Toplevel(self._root)
        win.title('Жозефіна')
        win.resizable(width=False, height=False)
        s = self._root.geometry()
        rest = s.split('+', maxsplit=1)[1]
        win.geometry('650x450+' + rest)
        text = """\
    Кількість колод: 2
    Кількість карт у колоді: 52
    Мета пасьянсу: зібрати всі карти на базові стопки у висхідних послідовностях у масть.
    
    Правила пасьянсу. Вважається, що даний пасьянс розкладала як гадання Жозефіна Богарне й \
результат даного пасьянсу давав відповідь на поставлене питання. Правила пасьянсу наступні. \
Перед розкладанням пасьянсу ставиться питання, потім дві колоди змішуються в одну, після чого \
отримана колода ретельно тасується й викладаються 10 вертикальних рядів карт по 4 карти в кожному ряді. \
Колода, що залишилась, кладеться поруч. Зверху розташовуються 8 місць для базових стопок. \
Стартовими картами в базових стопках є тузи, які кладуть туди в процесі гри. \
Дозволяється переміщати нижні повністю відкриті карти вертикальних рядів і верхню карту колоди, \
що залишилася, в ігрових рядах у спадній послідовності в масть. Якщо ряд залишається без карт, \
то дозволяється на порожнє місце покласти будь-яку карту.
    
    Пасьянс зійшовся, якщо всі карти зібрані на базових стопках у висхідних послідовностях у масть, \
у цьому випадку відповіддю на поставлене питання є "так", в іншому випадку "ні".

    Локалізація позиції налаштована так, що за перенесення карти стопка призначення визначається \
за позицією курсора, а не за перетином карти з її майбутнім місцем розташування.
"""
        Message(win, text=text, justify=LEFT, font=('Times',)).pack(padx=5, pady=5, ipadx=5, ipady=5, anchor=CENTER,
                                                                    expand=YES)
        win.bind('<Escape>', lambda event: win.destroy())
        win.focus_set()
        win.grab_set()
        win.wait_window()
