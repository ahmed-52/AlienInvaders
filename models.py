"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything
that you interact with on the screen is model: the ship, the laser bolts, and
the aliens.

Just because something is a model does not mean there has to be a special
class for it. Unless you need something special for your extra gameplay
features, Ship and Aliens could just be an instance of GImage that you move
across the screen. You only need a new class when you add extra features to
an object. So technically Bolt, which has a velocity, is really the only model
that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens. That is
because there are a lot of constants in consts.py for initializing the
objects, and you might want to add a custom initializer.  With that said,
feel free to keep the pass underneath the class definitions if you do not want
to do that.

You are free to add even more models to this module.  You may wish to do this
when you add new features to your game, such as power-ups.  If you are unsure
about whether to make a new class or not, please ask on Piazza.

# Ahmed Abdulla (aaa384), Harvey Zhu (hz639)
# December 5, 2023
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other
# than consts.py.  If you need extra information from Gameplay, then it should
# be a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships
    dimensions. These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a
    ship just means changing the x attribute (which you can do directly),
    you want to prevent the player from moving the ship offscreen.  This
    is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like animation).
    """
    # ATTRIBUTES:
    # Attribute x: the x-coordinate of the Ship
    # Invariant : x is an int

    # Attribute y: the y-coordinate of the Ship
    # Invariant : y is an int

    # Attribute width: the width of the Ship
    # Invariant : width is an int

    # Attribute height: the height of the Ship
    # Invariant : height is an int

    # Attribute source: the picture of ship
    # Invariant : source is a string representing the image file


    def getXPosition(self):
        """Returns the X position of the ship object"""
        return self.x


    def __init__(self, x, y, source):
        """
        Initializes a Ship object with the specified image source at the given
        coordinates.

        This constructor ensures that the provided x and y coordinates, as well
        as the image source, are valid. It then calls the superclass
        initializer to create a GImage instance representing the ship.

        Parameters:
            x (int/float): The x-coordinate
            of the ship's initial position.
            y (int/float): The y-coordinate
            of the ship'sinitial position.
            source (str): The file path or name of
            the image file to use for the ship.

        Precondition:
            x and y must be numbers (int or float).
            source must be a string and exactly 'ship.png'.
        """
        assert isinstance(x, (int, float))
        assert isinstance(y, (int, float))
        assert isinstance(source,str)
        assert source == 'ship.png'

        super().__init__(x = x, y = y, width = SHIP_WIDTH,
                                    height = SHIP_HEIGHT, source = source)


    def MoveRight(self):
        """
        Moves the Ship to the right within the bounds of the Game

        This method adjusts the ship's x-coordinates to move it right by
        SHIP_MOVEMENT increment. It aslo ensure that the ship does not move
        beyond the right edge of the game
        """
        if self.x + SHIP_MOVEMENT + SHIP_WIDTH/2 <= GAME_WIDTH:
            self.x += SHIP_MOVEMENT


    def MoveLeft(self):
        """
        Moves the Ship to the left within the bounds of the Game

        This method adjusts the ship's x-coordinates to move it left by
        SHIP_MOVEMENT increment. It aslo ensure that the ship does not move
        beyond the left edge of the game
        """
        if self.x - SHIP_MOVEMENT - SHIP_WIDTH/2 >= 0:
            self.x -= SHIP_MOVEMENT


    def collides(self,bolt):
        """
        Returns True if the alien bolt collides with this ship

        This method returns False if bolt was not fired by the alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)

        if not bolt.isPlayerBolt():
            for xy in bolt.getFourCorners():
                if self.contains(xy):
                    return True
        else:
            return False


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien
    dimensions. These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We
    do not require this.  You could put this method in Wave if you wanted to.
    But the advantage of putting it here is that Ships and Aliens collide
    with different bolts.  Ships collide with Alien bolts, not Ship bolts.
    And Aliens collide with Ship bolts, not Alien bolts. An easy way to
    keep this straight is for this class to have its own collision method.

    However, there is no need for any more attributes other than those
    inherited by GImage. You would only add attributes if you needed them
    for extra gameplay features (like giving each alien a score value).
    """
    # ATTRIBUTES:
    # Attribute x: the x-coordinate of the Alien
    # Invariant : x is an int

    # Attribute y: the y-coordinate of the Alien
    # Invariant : y is an int

    # Attribute width: the width of the Alien
    # Invariant : width is an int

    # Attribute height: the height of the Alien
    # Invariant : height is an int

    # Attribute source: the picture of the Alien
    # Invariant : source is a string representing the image file


    def getX(self):
        """
        Returns the x-coordinate of the alien's current position.
        """
        return self.x


    def getY(self):
        """
        Returns the y-coordinate of the alien's current position.
        """
        return self.y


    def getSource(self):
        """
        Returns the file name of the image file used for the alien
        """
        return self._source

    def __init__(self, x, y, source):
        """
        Initializes an Alien object with the specified
        image source at the given coordinates.

        This constructor ensures that the provided x
        and y coordinates, as well as the image source,
        are valid. It then calls the superclass initializer
        to create a GImage instance representing an alien.

        Precondition:
            x and y must be numbers (int or float).
            source must be a string and in ALIEN_IMAGES in the file consts.py
        """
        assert isinstance(x, (int, float)), "x must be an integer or float"
        assert isinstance(y, (int, float)), "y must be an integer or float"
        assert isinstance(source,str)
        assert source in ALIEN_IMAGES
        self._x = x
        self._y = y
        self._source = source

        super().__init__(x = self._x, y = self._y, width = ALIEN_WIDTH,
                        height = ALIEN_HEIGHT, source = self._source)


    def collides(self,bolt):
        """
        Returns True if the player bolt collides with this alien

        This method returns False if bolt was not fired by the player.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert isinstance(bolt,Bolt)

        if bolt.isPlayerBolt():
            for xy in bolt.getFourCorners():
                if self.contains(xy):
                    return True
        else:
            return False


    def AlienRight(self):
        """
        Moves the x-coordinates of the alien to the right by ALIEN_H_WALK
        """
        self.x += ALIEN_H_WALK


    def AlienLeft(self):
        """
        Moves the x-coordinates of the alien to the left by ALIEN_H_WALK
        """
        self.x -= ALIEN_H_WALK


    def AlienDown(self):
        """
        Moves the y-coordinates of the alien down by ALIEN_H_WALK
        """
        self.y -= ALIEN_V_WALK


class BossAlien(Alien):
    """
    A class to represent a boss alien with extra health.

    This class inherits from Alien and represents a more challenging enemy with
    additional health points. The boss alien takes multiple hits to be destroyed.

    The boss alien's health is represented by the _health attribute.
    """

    def __init__(self, x, y, source, health):
        """
        Initializes a BossAlien object with specified image source, position, and health.

        The constructor initializes the boss alien's position, image, and health.

        Precondition:
            x and y must be numbers (int or float).
            source must be a string representing the image file.
            health must be an integer representing the health points of the boss alien.
        """
        super().__init__(x, y, source)
        self._health = health


    def hit(self):
        """
        Reduces the health of the boss alien by one.

        If the health reaches zero, the boss alien is considered destroyed.
        """
        self._health -= 1
        return self._health <= 0



class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles. The size of the bolt
    is determined by constants in consts.py. We MUST subclass GRectangle,
    because we need to add an extra (hidden) attribute for the velocity of
    the bolt.

    The class Wave will need to look at these attributes, so you will need
    getters for them.  However, it is possible to write this assignment with
    no setters for the velocities.  That is because the velocity is fixed and
    cannot change once the bolt is fired.

    In addition to the getters, you need to write the __init__ method to set
    the starting velocity. This __init__ method will need to call the __init__
    from GRectangle as a  helper.

    You also MIGHT want to create a method to move the bolt.  You move the
    bolt by adding the velocity to the y-position.  However, the getter
    allows Wave to do this on its own, so this method is not required.
    """
    # INSTANCE ATTRIBUTES:
    # Attribute _velocity: the velocity in y direction
    # Invariant : _velocity is an int BOLTSPEED or -BOLTSPEED

    # Attribute x: the x-coordinate of the Bolt
    # Invariant : x is an int

    # Attribute y: the y-coordinate of the Bolt
    # Invariant : y is an int

    # Attribute width: the width of the Bolt
    # Invariant : width is an int

    # Attribute height: the height of the Bolt
    # Invariant : height is an int

    # Attribute fillcolor: the color of the Bolt
    # Invariant : color is a string that represents a color


    def getVelocity(self):
        """
        Returns the velocity of the Bolt
        """
        return self._velocity


    def getY(self):
        """
        Returns the y-coordinates of the bolt
        """
        return self.y


    def getX(self):
        """
        Returns the x-coordinates of the bold"""
        return self.x


    def __init__(self, x, y, velocity):
        """
        Initializes a Bolt object with the specified coordinates and velocity.

        This constructor creates a Bolt instance positioned at the given coordinates with
        the specified velocity. It asserts the types of the coordinates to ensure they are
        numerical values. The Bolt is visualized using the GRectangle superclass with a
        specified width, height, and fill color.

        Precondition:
            x and y must be numbers (int or float), representing the bolt's starting
            position. The position corresponds to the middle front of the ship for player
            bolts, or the bottom center of the alien for alien bolts. Velocity
            must be BOLT_SPEED or -BOLTSPEED.
        """
        assert isinstance(x, (int, float)), "x must be an integer or float"
        assert isinstance(y, (int, float)), "y must be an integer or float"
        assert velocity == BOLT_SPEED or -BOLT_SPEED

        self._velocity = velocity
        super().__init__(x = x, y = y, width = BOLT_WIDTH, height = BOLT_HEIGHT, fillcolor = 'red')


    def BoltMove(self):
        """
        Moves the bolt along the y-axis based on its velocity.

        This method updates the bolt's position by incrementing its y-coordinate by its
        velocity. If the bolt is a player bolt (BOLT_SPEED), it moves up. If the
        bolt is an alien bolt (-BOLT_SPEED), it moves down.
        """
        if self.isPlayerBolt():
            self.y += BOLT_SPEED
        else:
            self.y -= BOLT_SPEED


    def isPlayerBolt(self):
        """
        Determines if the bolt was fired by the player's ship.

        This method checks the bolt's velocity against
        the BOLT_SPEED constant.
        If the velocity equals BOLT_SPEED, it was fired by the player.

        Returns:
            True if the bolt is a player bolt, False otherwise.
        """
        return self._velocity == BOLT_SPEED


    def getFourCorners(self):
        """
        Calculates and returns the coordinates of the four corners of the bolt.

        Returns:
            A list of tuples, where each tuple contains the x and y coordinates
            for one of the corners of the bolt, in the order of top right, top left,
            bottom right, and bottom left.
        """

        list = []
        w = BOLT_WIDTH
        h = BOLT_HEIGHT
        list.append((self.x + w/2, self.y + h/2)) # top right
        list.append((self.x - w/2, self.y + h/2)) # top left
        list.append((self.x + w/2, self.y - h/2)) # bottom right
        list.append((self.x - w/2, self.y - h/2)) # bottom left
        return list
