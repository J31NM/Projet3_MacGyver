"""
Global constants

"""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Sprites attributes
sprites_height = 16
sprites_width = 15
sprite_size = 50
window_height = sprites_height * sprite_size
window_width = sprites_width * sprite_size

# Messages for the player
MESSAGES = {
    'Intro': [
        "Try to find the exit, but be careful, the keeper ",
        "won't let you pass."
    ],
    'first_item': [
        "You found something but that seems useless.",
        "keep searching."
    ],
    'second_item': [
        "Something else ! But still nothing interesting...",
        "Maybe if you assemble them... no"

    ],
    'syringe': [
        "Well done !! you build a drowsy syringe.",
        "You may have a chance against the keeper !"
    ],
    'victory': [
        "YOU MADE IT ! ",
        "Let's celebrate at the Phoenix Foundation !"
    ],
    'fail': [
        "Oh noo... Too bad.... YOU LOOSE",
        "Your fists were not enough to beat the keeper."
    ],
}
