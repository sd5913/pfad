"""Two independent tiles: choosing one changes only its own selected state."""


class Tile:
    def __init__(self, colour):
        self.colour = colour
        self.selected = False

    def choose(self):
        self.selected = True


def main():
    blue = Tile("blue")
    red = Tile("red")
    print(f"Before: blue={blue.selected}, red={red.selected}")
    blue.choose()
    print(f"After:  blue={blue.selected}, red={red.selected}")


if __name__ == "__main__":
    main()
