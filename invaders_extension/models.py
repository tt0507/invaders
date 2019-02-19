"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

# Toshi Tokuyama (tt426)
# December 2nd 2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    posx : The x coordinate of the position of the ship. Value is int or a float.
            
    """    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getPosx(self):
        """
        Returns the x coordinate of the ship
        """
        return self.x

    def setPosx(self, value):
        """
        Sets the x coordinate of the ship
        """
        assert type(value) == int or type(float)
        self.x = value

    def getPosy(self):
        """
        Returns the y coordinate of the ship
        """
        return self.y
    
    # INITIALIZER TO CREATE A NEW SHIP

    def __init__(self, x, y, width, height, source):
        """
        Initializer: Creates the ship

        Parameter x: x-coordinate of the position of the alien
        Precondition: The value is [float, int] > 0 
        Parameter y: y-coordinate of the position of the alien
        Precondition: The value is [float, int] > 0 
        Parameter width: Width of the alien
        Precondition: The value is [float, int] > 0
        Parameter height: Height of the alien
        Precondition: The value is [float, int] > 0
        Parameter source: Source of the alien (image file)
        Precondition: Image from the Images file
        """
        super().__init__(x = x, y = y, width = width, height = height, source = source)
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS

    def collidesShip(self, alienBolt):
        """
        Returns: True if the bolt was fired by the alien and collides with the ship
            
        Parameter alienBolt: The laser alienbolt to check
        Precondition: bolt is of class Bolt
        """
        top_left = self.contains((
            alienBolt.x - BOLT_WIDTH/2, alienBolt.y + BOLT_HEIGHT/2))
        top_right = self.contains((
            alienBolt.x + BOLT_WIDTH/2, alienBolt.y + BOLT_HEIGHT/2))
        bottom_right = self.contains((
            alienBolt.x + BOLT_WIDTH/2, alienBolt.y - BOLT_HEIGHT/2))
        bottom_left = self.contains((
            alienBolt.x - BOLT_WIDTH/2, alienBolt.y - BOLT_HEIGHT/2))

        determine_hit_ship = top_left or top_right or bottom_left or bottom_right

        return determine_hit_ship
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

    APosx: x-coordinate of the position of the alien  [int or float >= 0]

    APosy: y-coordinate of the position of the alien  [int or float >= 0]
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    def getAPosx(self):
        """
        Returns the x coordinate of the alien
        """
        return self.x

    def setAPosx(self, value):
        """
        Sets the x coordinate of the alien
        """
        assert type(value) == int or type(float)
        self.x = value

    def getAPosy(self):
        """
        Returns the y coordinate of the alien
        """
        return self.y

    def setAPosy(self, value):
        """
        Sets the y coordinate of the alien
        """
        assert type(value) == int or type(float)
        self.y = value

    # INITIALIZER TO CREATE AN ALIEN

    def __init__(self, x, y, width, height, source):
        """
        Initializer: Creates the aliens. 

        Parameter x: x-coordinate of the position of the alien
        Precondition: The value is [float, int] > 0 
        Parameter y: y-coordinate of the position of the alien
        Precondition: The value is [float, int] > 0 
        Parameter width: Width of the alien
        Precondition: The value is [float, int] > 0
        Parameter height: Height of the alien
        Precondition: The value is [float, int] > 0
        Parameter source: Source of the alien (image file)
        Precondition: Image from the Images file
        """
        super().__init__(x = x, y = y, width = width, height = height, source = source)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def collidesAlien(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """

        top_left = self.contains((
            bolt.x - BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        top_right = self.contains((
            bolt.x + BOLT_WIDTH/2, bolt.y + BOLT_HEIGHT/2))
        bottom_right = self.contains((
            bolt.x + BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))
        bottom_left = self.contains((
            bolt.x - BOLT_WIDTH/2, bolt.y - BOLT_HEIGHT/2))

        determine_hit = top_left or top_right or bottom_left or bottom_right
        #print(determine_hit)
        return determine_hit
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        Y: The y-coordinate of the bolt [int or float]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)   
    def getX(self):
        return self.x

    def getY(self):
        """
        Returns: The y-coordinate of the bolt
        """
        return self.y

    def setY(self, value):
        """
        Sets the y-coordinate of the bolt.

        Parameter: y coordinate
        Precondition: Value is int or a float
        """
        self.y = value

    def getVelocity(self):
        """
        Returns: The y-direction velocity of the bolt
        """
        return self._velocity

    def setVeloctiy(self, value):
        """
        Sets the y-direction velocity of the bolt.

        Parameter: y-direction velocity
        Precondition: Value is int or a float
        """
        assert type(value) == int or type(value) == float
        self._velocity = value
    
    # INITIALIZER TO SET THE VELOCITY

    def __init__(self, x, y, width, height, fillcolor, velocity):
        """
        Initializer: Creates the bolts that are shot by the ship

        Parameter x: x-coordinate of the center of the bolt
        Precondition: The value is [float, int] > 0 
        Parameter y: y-coordinate of the center of the bolt
        Precondition: The value is [float, int] > 0 
        Parameter width: Width of the bolt 
        Precondition: The value is [float, int] > 0
        Parameter height: Height of the bolt
        Precondition: The value is [float, int] > 0
        Parameter fillcolor: The color of the bolt
        Precondition: Valid color object (RGB, HSV and others)
        Parameter velocity: speed of the bolt
        Precondition: The value is [float, int] > 0
        """
        super().__init__(x = x, y = y, width = width, height = height,
                        fillcolor = fillcolor)

        self._velocity = BOLT_SPEED

    def move(self):
        """
        Moves the y coordinate of the bolt by the y-direction velocity
        """
        self.y += self._velocity
        

    def isPlayerBolt(self):
        """
        Distinguish between bolts fired by player and bolts fired by alien
        """
        # inside = True
        pass

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE

class DLine(GPath):
    """
    Class representing the defense line
    """
    def __init__(self, points, linecolor, linewidth):
        super().__init__(points = points, linecolor = linecolor, 
            linewidth = linewidth)


class alienBolt(GRectangle):
    """
    A class representing a laser bolt.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
        Y: The y-coordinate of the bolt [int or float]
    """

    # Getters and Setters
    def getY(self):
        """
        Returns: The y-coordinate of the bolt
        """
        return self.y

    def setY(self, value):
        """
        Sets the y-coordinate of the bolt.

        Parameter: y coordinate
        Precondition: Value is int or a float
        """
        self.y = value

    def getVelocity(self):
        """
        Returns: The y-direction velocity of the bolt
        """
        return self._velocity

    def setVeloctiy(self, value):
        """
        Sets the y-direction velocity of the bolt.

        Parameter: y-direction velocity
        Precondition: Value is int or a float
        """
        assert type(value) == int or type(value) == float
        self._velocity = value

    # INITIALIZER TO SET THE VELOCITY

    def __init__(self, x, y, width, height, fillcolor, velocity):
        """
        Initializer: Creates the bolts that are shot by the alien

        Parameter x: x-coordinate of the center of the bolt
        Precondition: The value is [float, int] > 0 
        Parameter y: y-coordinate of the center of the bolt
        Precondition: The value is [float, int] > 0 
        Parameter width: Width of the bolt 
        Precondition: The value is [float, int] > 0
        Parameter height: Height of the bolt
        Precondition: The value is [float, int] > 0
        Parameter fillcolor: The color of the bolt
        Precondition: Valid color object (RGB, HSV and others)
        Parameter velocity: speed of the bolt
        Precondition: The value is [float, int] > 0
        """
        super().__init__(x=x, y=y, width=width, height=height,
                         fillcolor=fillcolor)

        self._velocity = -1 * BOLT_SPEED

    def moveBoltAlien(self):
        """
        Moves the y coordinate of the bolt by the y-direction velocity
        """
        self.y += self._velocity

    


