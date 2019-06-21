210101010101001
000000000001101
011111101000000
001000001101010
100111111010000
110010000001000
101011111011110
000010001011100
011110101011110
000010100010001
011010100000111
010010111100011
010110000111011
010011110101333
100000000001113
b444esp44444444

"""
Maze Structure : 
Each number in this structure represents a sprite in the game.
they are 15 columns and 16 lines.
Each will be convert to a surface and replaced by an image in the Labyrinth Class 
to draw the maze level.
They are nine values :
_ 0, 2, 3 : represents the path on witch Macgyver can walk
_ 1 : walls
_ 2 : Start position which represent a Checkboard
_ 3 : forbidden sprites for the items positions, because they are too close to the keeper.
        Walls (1) and start position (2) are also denied to the items position.
        Those two values are linked to specific images. 
        So i needed to get an new value no related to an image.
_ 4 : Black sprites for the inventory bar. The three on the left are the emplacements for the items.
        The eight on the right are for the messages.
_ b : Macgyver Backpack icon.
_ e : Equal symbol icon
_ s : Syringe icon
_ p : Penny icon
"""
