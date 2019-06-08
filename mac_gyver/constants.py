"""
Global constants

"""

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Screen dimensions
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 800

# Sprites attributes
sprites_height = 16
sprites_width = 15
sprite_size = 50
window_height = sprites_height * sprite_size
window_width = sprites_width * sprite_size

# Texts for the player
MESSAGES = {
    'Intro': [
        "Try to find the exit, but be careful, the keeper ",
        "won't let you pass."
    ],
    'first_item': [
        "You found something but that seems useless."
    ],
    'second_item': [
        "Something else ! But still nothing interesting...",
        "keep searching."
    ],
    'syringe': [
        "Well done !! you build a drowsy syringe.",
        "You may have a chance against the keeper !"
    ],
    'victory1': [
        "YOU MADE IT ! ",
        "Come find me at the Phoenix foundation handsome ;)"
    ],
    'victory2' : [
        "Looking for Penny, Macgyver lost himself in the building",
        "Let's free him in FREE MACGYVER II ! Coming soon !"
    ],
    'fail1': [
        "Oh noo... Too bad",
        "Your fists were not enough to beat the keeper."
    ],
    'fail2': [
        "MacGyver was brought in jail",
        "Let's free him in FREE MACGYVER II ! Coming soon !"
    ]}