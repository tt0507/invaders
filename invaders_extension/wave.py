"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Toshi Tokuyama (tt426)
# December 2nd 2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the player laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY

        _direction: the direction in which the aliens are moving
        _alienbolts: the alien laser bolts currently on screen [list of Bolt, possibly empty]
        _tofire: the number of steps between alien shots
        _soundEffect: sound effect when the alien or the ship is destroyed
        _score: Score of the game
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getShip(self):
        """
        Returns the ship which the player controls
        """
        return self._ship

    def setShip(self, value):
        """
        Add specification
        """
        self._ship = value

    def getAliens(self):
        """
        Returns the 2d list of aliens in the wave
        """
        return self._aliens

    def getBolts(self):
        """
        Returns the player laser bolts currently on the screen
        """
        return self._bolts

    def getDlines(self):
        """
        Returns the defensive line being protected
        """
        return self._dline

    def getLives(self):
        """
        Returns the number of lives left
        """
        return self._lives

    def setLives(self, value):
        """
        Sets the number of lives left

        Precondition: value is int greater than 0 (int>0)
        """
        assert type(value) == int
        self._lives = value

    def getTime(self):
        """
        Returns the the amount of time since the last Alien "step"
        """
        return self._time

    def getAlienBolts(self):
        """
        Returns the alien bolts currently on the screen
        """
        return self._alienbolts

    # Extensions

    def getsoundEffect(self):
        """
        Add specification
        """
        return self._soundEffect

    def setsoundEffect(self, value):
        """
        Add specification
        """
        self._soundEffect = value

    def getScore(self):
        """
        Add specification
        """
        return self._score

    def setScore(self, value):
        """
        Add specification
        """
        self._score = value


    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS

    def __init__(self):
        """
        Initializer: Creates aliens and ship necessary for the game
        """
        self._time = 0

        self._direction = 1

        self.alien_create()

        self._ship = Ship(x=GAME_WIDTH / 2, y=SHIP_BOTTOM, width=SHIP_WIDTH,
                            height=SHIP_HEIGHT, source='ship.png')

        self._dline = DLine(points = [0,DEFENSE_LINE,GAME_WIDTH,DEFENSE_LINE],
                            linecolor = COLOR, linewidth = 2)

        self._bolts = []

        self._alienbolts = []

        self._tofire = random.randrange(1, BOLT_RATE, 1)

        self._lives = 3

        #Extension
        self._soundEffect = True 

        self._score = 0


    def alien_create(self):
        """
        Creates the alien used in the game.
        """
        self._aliens = []

        for row in range(ALIEN_ROWS):
            accum = []
            for alien in range(ALIENS_IN_ROW):
                if (row % ALIEN_ROWS) == 0:
                    accum.append(Alien((LEFT_TO_FIRST) + (ADDING_ROW) * alien,
                                       y=(TOP_TO_FIRST) - (ADDING_COLUMN) * row, width=ALIEN_WIDTH,
                                       height=ALIEN_HEIGHT, source='alien3.png'))
                if row in range(1, 3):
                    accum.append(Alien((LEFT_TO_FIRST) + (ADDING_ROW) * alien,
                                       y=(TOP_TO_FIRST) - (ADDING_COLUMN) * row, width=ALIEN_WIDTH,
                                       height=ALIEN_HEIGHT, source='alien2.png'))
                if row in range(3, 5):
                    accum.append(Alien((LEFT_TO_FIRST) + (ADDING_ROW) * alien,
                                       y=(TOP_TO_FIRST) - (ADDING_COLUMN) * row, width=ALIEN_WIDTH,
                                       height=ALIEN_HEIGHT, source='alien1.png'))
                if row in range(5, 7):
                    accum.append(Alien((LEFT_TO_FIRST) + (ADDING_ROW) * alien,
                                       y=(TOP_TO_FIRST) - (ADDING_COLUMN) * row, width=ALIEN_WIDTH,
                                       height=ALIEN_HEIGHT, source='alien2.png'))
                if row in range(7, 10):
                    accum.append(Alien((LEFT_TO_FIRST) + (ADDING_ROW) * alien,
                                       y=(TOP_TO_FIRST) - (ADDING_COLUMN) * row, width=ALIEN_WIDTH,
                                       height=ALIEN_HEIGHT, source='alien1.png'))
            self._aliens.append(accum)
        
    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS

    ######################################## Ship ########################################

    def updateShip(self,input):
        """
        Updates the x-coordinate of the ship to move the ship horizontally.
        Ship can not go beyond the borders of the game.

        Parameter input: The user input used to control the position of the ship
        Precondition: Immutable instance of GInput
        """
        assert isinstance(input, GInput)

        if self._ship is not None:
            if input.is_key_down('left'):
                if min(0, self._ship.getPosx() - SHIP_WIDTH/2) == 0:
                    self._ship.setPosx(self._ship.getPosx() - SHIP_MOVEMENT)
            if input.is_key_down('right'):
                if max(self._ship.getPosx() + SHIP_WIDTH/2, GAME_WIDTH) == GAME_WIDTH:
                    self._ship.setPosx(self._ship.getPosx() + SHIP_MOVEMENT)

    ######################################## Alien ########################################

    def updateAlien(self, dt):
        """
        Updates the x-coordinate and y-coordinate of the alien to move
        the alien horizontally by ALIEN_H_WALK and vertically
        by ALIEN_V_WALK for the game. 

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        if self._direction == 1:
            if self._time > ALIEN_SPEED:
                for x in self.getAliens():
                    for y in x:
                        if y != None: # Added
                            y.setAPosx(y.getAPosx() + ALIEN_H_WALK)
                            self._time = 0
                self._tofire -= 1
        if self._direction == -1:
            if self._time > ALIEN_SPEED:
                for x in self.getAliens():
                    for y in x:
                        if y != None: # Added
                            y.setAPosx(y.getAPosx() - ALIEN_H_WALK)
                            self._time = 0
                self._tofire -= 1
        
        self.moveLeftRight()


    def moveLeftRight(self):
        """
        If the alien reaches the right end of the screen, the alien will move
        down by ALIEN_V_WALK and march to the left by ALIEN_H_WALK. Similarily,
        if the alien reaches the left end of the screen, the alien will move
        down by ALIEN_V_WALK and march to the right by ALIEN_H_WALK.
        """
        if self.countAlienAlive() > 1:
            if self.mostright() >= GAME_WIDTH - ALIEN_WIDTH/2 - ALIEN_H_SEP:
                for x in self.getAliens():
                    for y in x:
                        if y is not None:
                            y.setAPosy(y.getAPosy() - ALIEN_V_WALK)
                            y.setAPosx(y.getAPosx() - ALIEN_H_WALK)
                    self._direction = -1
            elif self.mostleft() <= ALIEN_WIDTH/2 + ALIEN_H_SEP:
                for x in self.getAliens():
                    for y in x:
                        if y is not None:
                            y.setAPosy(y.getAPosy() - ALIEN_V_WALK)
                            y.setAPosx(y.getAPosx() + ALIEN_H_WALK)
                    self._direction = 1
        else:
            if self.alienOneLeft().getAPosx() >= BORDER_RIGHT:
                self.alienOneLeft().setAPosy(self.alienOneLeft().getAPosy()
                                            - ALIEN_V_WALK)
                self.alienOneLeft().setAPosx(self.alienOneLeft().getAPosx()
                                            - ALIEN_H_WALK)
                self._direction = -1
            elif self.alienOneLeft().getAPosx() <= ALIEN_WIDTH/2 + ALIEN_H_SEP:
                self.alienOneLeft().setAPosy(self.alienOneLeft().getAPosy()
                                            - ALIEN_V_WALK)
                self.alienOneLeft().setAPosx(self.alienOneLeft().getAPosx()
                                            + ALIEN_H_WALK)
                self._direction = 1
                

    def mostright(self):
        """
        Finds the rightmost alien that is on the screen.
        """
        new_alien = self.transpose(self._aliens)
        new_list = [] # new_list is 2D list
        new_list_2 = [] # new_list_2 is 1D list

        # Get x-position of alien for each element in list
        for row in range(ALIENS_IN_ROW):
            accum = []
            for col in range(ALIEN_ROWS):
                if new_alien[row][col] is not None:
                    accum.append(new_alien[row][col].getAPosx())
            new_list.append(accum)

        # Get maximum alien(x-position) from new_list and append to new_list_2
        for index in range(len(new_list)):
            if new_list[index] != []:
                new_list_2.append(max(new_list[index]))
       
        # Remove all None(s) from new_list_2
        for x in new_list_2:
            if len(new_list_2) > 1:
                if x == None:
                    new_list_2.remove(x)
                getmax = max(new_list_2)
            else:
                getmax = new_list_2[0]

        return getmax
        
    def mostleft(self):
        """
        Finds the leftmost alien that is on the screen.
        """
        alien_list = self._aliens
        new_alien = self.transpose(alien_list)
        new_list = []  # new_list is 2D list
        new_list_2 = []  # new_list_2 is 1D list

        # Get x-position of alien for each element in list
        for row in range(ALIENS_IN_ROW):
            accum = []
            for col in range(ALIEN_ROWS):
                if new_alien[row][col] is not None:
                    accum.append(new_alien[row][col].getAPosx())
            new_list.append(accum)

        # Get minimum alien(x-position) from new_list and append to new_list_2
        for index in range(len(new_list)):
            if new_list[index] != []:
                new_list_2.append(min(new_list[index]))
    
        # Remove all None(s) from new_list_2
        for x in new_list_2:
            if len(new_list_2) > 1:
                if x == None:
                    new_list_2.remove(x)
                getmin = min(new_list_2)
            else:
                getmin = new_list_2[0]

        return getmin

    def transpose(self, table):
        """
        Returns: copy of table with rows and columns swapped

        Parameter table: 2d list
        Precondition: table is a (non-ragged) 2d List
        """
        numrows = len(table)  # Need number of rows
        numcols = len(table[0])  # All rows have same no. cols
        result = []  # Result (new table) accumulator
        for m in range(numcols):
            row = []  # Single row accumulator
            for n in range(numrows):
                row.append(table[n][m])  # Create a new row list
            result.append(row)  # Add result to table
        return result

        #Code copied from Lecture 16

    def countAlienAlive(self):
        """
        Counts the number of alien in self._aliens that are not None
        """
        count = 0

        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] != None:
                    count += 1
        return count

    def alienOneLeft(self):
        """
        Returns the last alien on the screen.
        """
        lastalien = []

        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self._aliens[row][col] != None:
                    lastalien.append(self._aliens[row][col])
        return lastalien[0]

    ######################################## Bolt ########################################

    def makeBolts(self):
        """
        Creates the bolt shot by the ship.
        """
        self._bolts.append(Bolt(x=self._ship.getPosx(), y=self._ship.getPosy() + SHIP_HEIGHT/2,
                           width=BOLT_WIDTH, height=BOLT_HEIGHT,
                           fillcolor=introcs.HSV(0.2, 0.3, 0.4), velocity=BOLT_SPEED))

    def updateBolts(self, input):
        """
        Moves the y-coordinate of the bolts to shoot the alien

        Parameter input: The user input used to shoot the bolt
        Precondition: Immutable instance of GInput
        """
        assert isinstance(input, GInput)

        if input.is_key_down('up'):
            if self._bolts == []:
                self.makeBolts()
            
        for x in self._bolts:
            x.move()
        
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].y - BOLT_HEIGHT/2 > GAME_HEIGHT:
                del self._bolts[i]
            else:
                i += 1

    def makeAlienBolts(self):
        """
        Creates the bolts shot by the alien. The bottom-most alien
        shoots the bolt.
        """
        t_list = self.transpose(self._aliens)
        t_list_2 = [] # Transpose matrix
        t_list_3 = []
        
        #Create a transpose matrix and find y-coordinate
        for row in range(ALIENS_IN_ROW):
            accum = []
            for col in range(ALIEN_ROWS):
                if t_list[row][col] is not None:
                    accum.append(t_list[row][col])
            t_list_2.append(accum)
        
        #Find the minimum alien of each row and append to new list
        for index in range(len(t_list_2)):
            if t_list_2[index] != []:
                t_list_3.append(t_list_2[index][-1])
                column = random.randint(0, len(t_list_3)-1)
        
        if len(t_list_3) > 1:
            for x in t_list_3:
                if x == None:
                    t_list_3.remove(x)

        self._alienbolts.append(alienBolt(x=t_list_3[column].getAPosx(),
                                y=t_list_3[column].getAPosy() - ALIEN_WIDTH/2,
                                width=BOLT_WIDTH, height=BOLT_HEIGHT,
                                fillcolor=COLOR, velocity=BOLT_SPEED))

    def updateAlienBolts(self):
        """
        Makes the alien fire the bolts
        """
        #print(self._tofire)

        if self._tofire == 0:
            self.makeAlienBolts()

        for x in self._alienbolts:
            x.moveBoltAlien()

            self._tofire = random.randrange(1, BOLT_RATE, 1)

        i = 0
        while i < len(self._alienbolts):
            if self._alienbolts[i].y + BOLT_HEIGHT/2 < 0:
                del self._alienbolts[i]
            else:
                i += 1

        
    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the ship, aliens, defensive line, and bolts

        
        Parameter view: the game view, used in drawing
        Precondition: Immutable instance of GView; it is inherited from GameApp
        """
        assert isinstance(view, GView)

        for x in self.getAliens():
            for y in x:
                if y != None: # Added
                    y.draw(view)

        if self._ship != None:
            self.getShip().draw(view)

        self.getDlines().draw(view)

        for x in self.getBolts():
            x.draw(view)

        for x in self.getAlienBolts():
            x.draw(view)


    # HELPER METHODS FOR COLLISION DETECTION

    def collision(self):
        """
        Removes the bolt from _bolt if the bolt hits the alien
        and sets the _alien which was hit to None
        """
       
        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                for z in self.getBolts():
                    if self._aliens[row][col] != None: # Added
                        if self._aliens[row][col].collidesAlien(z):
                            self._aliens[row][col] = None
                            if self._aliens[row][col] == None:
                                self._bolts.remove(z)

                            #Extension
                            if row % 6 == 0:
                                self.setScore(self.getScore() + 30)
                            elif (row-1) % 6 == 0 or (row-2) % 6 == 0:
                                self.setScore(self.getScore() + 20)
                            else:
                                self.setScore(self.getScore() + 10)
                            if self._soundEffect == True:
                                sound = Sound('pew1.wav')
                                sound.play()

    def collisionShip(self):
        """
        Removes the bolt from _alienbolt if the bolt hits the ship
        and sets _ship to None
        """
        sound_2 = Sound('blast3.wav')
        
        for alienbolts in self.getAlienBolts():
            if self._ship != None:
                if self._ship.collidesShip(alienbolts):
                    self._ship = None
                    self._alienbolts.remove(alienbolts)
                    if self._soundEffect == True:
                        sound_2 = Sound('blast3.wav')
                        sound_2.play()

    def loseRound(self):
        """
        Returns True if the _ship is equal to None
        """
        
        return self._ship is None
    
    def overDefenseLine(self):
        """
        Returns True is alien pass over the defense line.
        """
        aliveAlien = []

        for row in range(ALIEN_ROWS):
            for col in range(ALIENS_IN_ROW):
                if self.getAliens()[row][col] != None:
                    aliveAlien.append(self.getAliens()[row][col])

        for x in aliveAlien:
            if x.getAPosy()-ALIEN_HEIGHT/2 <= DEFENSE_LINE:
                return True

    def restoreShip(self):
        """
        Restores the ship after it was set to None
        """
        if self._ship == None:
            self._ship = Ship(x=GAME_WIDTH/2, y=SHIP_BOTTOM, width=SHIP_WIDTH,
                            height=SHIP_HEIGHT, source='ship.png')

        

        
