import play


class Console(play.Play):

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

    def make_menu_choice(self):
        pass
