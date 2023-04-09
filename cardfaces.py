from PIL import ImageTk, Image


def load_image(path):
    with Image.open(path) as image:
        image.load()
    return image


def part(image, *bbox):
    return ImageTk.PhotoImage(image=image.crop(bbox))


def card_image(tile, card, w, h):
    return part(tile, card.j * w, card.i * h, card.j * w + w, card.i * h + h)


class CardFaces:
    W = 72
    H = 96
    _TILE = None
    BACK = None
    # It's impossible to create PhotoImage while no root windows exists.
    # So we should do delayed initialization of _TILE and BACK.
    _faces = {}

    @staticmethod
    def _create_back():
        image = load_image('card_jfitz_back.png')
        CardFaces.BACK = part(image, 0, 0, CardFaces.W, CardFaces.H)

    @staticmethod
    def _create_faces():
        CardFaces._TILE = load_image('cards_jfitz.png')

    @staticmethod
    def create_global_images():
        if not CardFaces._TILE:
            CardFaces._create_faces()
        if not CardFaces.BACK:
            CardFaces._create_back()

    @staticmethod
    def get(card):
        if card not in CardFaces._faces:
            CardFaces._faces[card] = card_image(CardFaces._TILE, card, w=CardFaces.W, h=CardFaces.H)
        return CardFaces._faces[card]

    @staticmethod
    def image(card, opened):
        if opened:
            return CardFaces.get(card)
        else:
            return CardFaces.BACK
